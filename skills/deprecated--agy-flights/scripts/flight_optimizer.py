#!/usr/bin/env python3
"""
Flight Optimizer CLI & Agent Tool.
Programmatically discovers optimal flight date windows, calculates fare estimates,
evaluates free airline stopovers (e.g., Copa Panama Stopover), constructs split-ticket
alternatives, and generates pre-populated direct booking deep links.
"""

import argparse
import json
import sys
import os
from datetime import date, timedelta
from typing import List, Dict, Any, Optional

try:
    from fare_estimator import estimate_fare, DAY_MULTIPLIERS
except ImportError:
    from scripts.fare_estimator import estimate_fare, DAY_MULTIPLIERS


def build_google_flights_url(origin: str, dest: str, dep: date, ret: date) -> str:
    """Generate pre-populated Google Flights search query URL."""
    return f"https://www.google.com/travel/flights?q=Flights%20to%20{dest}%20from%20{origin}%20on%20{dep.isoformat()}%20through%20{ret.isoformat()}"


def build_google_multicity_url(origin: str, hub: str, dest: str, dep: date, stopover_end: date, ret: date) -> str:
    """Generate multi-city Google Flights URL with stopover."""
    return f"https://www.google.com/travel/flights?q=Flights%20from%20{origin}%20to%20{hub}%20on%20{dep.isoformat()}%20and%20from%20{hub}%20to%20{dest}%20on%20{stopover_end.isoformat()}%20and%20from%20{dest}%20to%20{origin}%20on%20{ret.isoformat()}"


def build_kayak_url(origin: str, dest: str, dep: date, ret: date) -> str:
    """Generate pre-populated Kayak search URL."""
    return f"https://www.kayak.com/flights/{origin}-{dest}/{dep.isoformat()}/{ret.isoformat()}"


def build_skyscanner_url(origin: str, dest: str) -> str:
    """Generate Skyscanner route page URL."""
    return f"https://www.skyscanner.com/transport/flights/{origin.lower()}/{dest.lower()}/"


def build_copa_stopover_url() -> str:
    """Link to Copa Airlines official Panama Stopover booking portal."""
    return "https://www.copaair.com/en-us/panama-stopover/"


def compute_drive_economics(
    one_way_miles: float,
    one_way_hours: float,
    mpg: float = 28.0,
    gas_price: float = 3.75,
    extra_costs: float = 0.0
) -> Dict[str, Any]:
    """Cost/time math for driving to a cheaper positioning-hub airport instead of flying direct.

    This is real, verifiable arithmetic (not a fare guess) — the caller supplies actual
    distance/time (e.g. from Google/Apple Maps) rather than the tool inventing them.
    """
    round_trip_miles = round(one_way_miles * 2, 1)
    round_trip_hours = round(one_way_hours * 2, 2)
    gallons = round_trip_miles / mpg
    fuel_cost = round(gallons * gas_price, 2)
    total_cost = round(fuel_cost + extra_costs, 2)
    return {
        "one_way_miles": one_way_miles,
        "one_way_hours": one_way_hours,
        "round_trip_miles": round_trip_miles,
        "round_trip_hours": round_trip_hours,
        "mpg": mpg,
        "gas_price_per_gallon": gas_price,
        "round_trip_fuel_cost": fuel_cost,
        "extra_costs": extra_costs,
        "total_positioning_cost": total_cost,
        "note": (
            "This is real drive-cost math, not a fare estimate. Compare "
            f"total_positioning_cost (${total_cost}) plus the LIVE fare from the positioning "
            "hub against the LIVE fare flying direct from home — whichever sum is lower wins. "
            f"Also weigh the added {round_trip_hours}h round-trip drive time against any "
            "domestic layover time saved."
        )
    }


def get_candidate_dates(
    window: str,
    base_year: int,
    after_day: int = 1,
    min_days: int = 28,
    max_days: int = 42,
    max_stay_days: int = 90
) -> List[Dict[str, Any]]:
    """Generate and rank date pairs by day-of-week and seasonal efficiency."""
    window = window.lower().strip()
    
    if window == "may":
        start_date = date(base_year, 5, max(1, after_day))
        end_date = date(base_year, 5, 31)
    elif window in ("december", "dec"):
        start_date = date(base_year, 12, max(1, after_day))
        end_date = date(base_year, 12, 31)
    elif ":" in window:
        parts = window.split(":")
        start_date = date.fromisoformat(parts[0])
        end_date = date.fromisoformat(parts[1])
    else:
        raise ValueError(f"Unknown window: '{window}'. Use 'may', 'december', or 'YYYY-MM-DD:YYYY-MM-DD'")

    candidates = []
    curr = start_date
    while curr <= end_date:
        # Check departures: prefer Tuesday (1), Wednesday (2)
        dow = curr.weekday()
        
        # In December, penalize departures on Dec 18-24
        if curr.month == 12 and 18 <= curr.day <= 24:
            curr += timedelta(days=1)
            continue
            
        # Try trip durations between min_days and max_days
        for days in range(min_days, min(max_days, max_stay_days) + 1):
            ret = curr + timedelta(days=days)
            
            # Penalize returns during peak New Year week (Jan 1 - Jan 8)
            if ret.month == 1 and 1 <= ret.day <= 8:
                continue
                
            # Score this date pair (lower score = cheaper / better)
            dep_dow_penalty = 0 if dow in (1, 2) else (1 if dow in (0, 3) else 3)
            ret_dow_penalty = 0 if ret.weekday() in (1, 2) else (1 if ret.weekday() in (0, 3) else 3)
            
            # December specific scoring: earlier departure after Dec 12 is better
            holiday_penalty = 0
            if curr.month == 12:
                holiday_penalty = (curr.day - 12) * 2
                
            total_penalty = dep_dow_penalty + ret_dow_penalty + holiday_penalty
            
            candidates.append({
                "dep_date": curr,
                "ret_date": ret,
                "duration_days": days,
                "penalty": total_penalty
            })
            
        curr += timedelta(days=1)
        
    candidates.sort(key=lambda x: (x["penalty"], abs(x["duration_days"] - 35)))
    return candidates


def optimize_flight(
    origin: str = "LAS",
    dest: str = "ASU",
    window: str = "may",
    after_day: int = 1,
    min_days: int = 28,
    max_days: int = 42,
    max_stay_days: int = 90,
    budget_max: float = 1000.0,
    budget_target: float = 700.0,
    stopover_hub: Optional[str] = "PTY",
    stopover_days: int = 1,
    split_hub: Optional[str] = "MIA",
    year: Optional[int] = None
) -> Dict[str, Any]:
    """Main optimization procedure producing structured itineraries and links."""
    today = date.today()
    if year is None:
        if window.lower() in ("december", "dec"):
            # If currently past December, use next year
            year = today.year if today.month <= 12 else today.year + 1
        else:
            # May
            year = today.year if today.month <= 5 else today.year + 1

    candidates = get_candidate_dates(
        window=window,
        base_year=year,
        after_day=after_day,
        min_days=min_days,
        max_days=max_days,
        max_stay_days=max_stay_days
    )

    if not candidates:
        return {"error": f"No valid date candidates found for window '{window}'."}

    # Pick top 3 diverse duration candidates (approx 4 weeks, 5 weeks, 6 weeks)
    selected_pairs = []
    durations_covered = set()
    for c in candidates:
        dur_cat = "4_weeks" if c["duration_days"] <= 30 else ("5_weeks" if c["duration_days"] <= 37 else "6_weeks")
        if dur_cat not in durations_covered:
            selected_pairs.append(c)
            durations_covered.add(dur_cat)
        if len(selected_pairs) == 3:
            break

    # If we don't have 3, just fill from best candidates
    for c in candidates:
        if len(selected_pairs) >= 3:
            break
        if c not in selected_pairs:
            selected_pairs.append(c)

    results = []
    for idx, pair in enumerate(selected_pairs, start=1):
        dep = pair["dep_date"]
        ret = pair["ret_date"]
        dur = pair["duration_days"]
        
        # Standard Fare Estimate
        fare = estimate_fare(origin, dest, dep, ret, has_stopover=False)
        
        # Stopover Option (e.g. Copa PTY)
        stopover_info = None
        if stopover_hub:
            stopover_end = dep + timedelta(days=stopover_days)
            stopover_fare = estimate_fare(origin, dest, dep, ret, has_stopover=True, stopover_tax=45.0)
            stopover_info = {
                "hub": stopover_hub,
                "stopover_days": stopover_days,
                "stopover_end_date": stopover_end.isoformat(),
                "estimated_fare_range": stopover_fare["total_estimated_range"],
                "midpoint_estimate": stopover_fare["midpoint_estimate"],
                "google_multicity_url": build_google_multicity_url(origin, stopover_hub, dest, dep, stopover_end, ret),
                "copa_stopover_url": build_copa_stopover_url()
            }
            
        # Split Ticket Option (via MIA)
        split_ticket_info = None
        if split_hub:
            domestic_fare = estimate_fare(origin, split_hub, dep, ret)
            intl_fare = estimate_fare(split_hub, dest, dep, ret)
            total_split_low = round(domestic_fare["total_estimated_range"][0] + intl_fare["total_estimated_range"][0], 2)
            total_split_high = round(domestic_fare["total_estimated_range"][1] + intl_fare["total_estimated_range"][1], 2)
            split_ticket_info = {
                "connection_hub": split_hub,
                "domestic_airline": "Southwest / Frontier / Spirit / American",
                "intl_airline": "Copa / Avianca / LATAM",
                "domestic_estimated_range": domestic_fare["total_estimated_range"],
                "intl_estimated_range": intl_fare["total_estimated_range"],
                "combined_total_range": [total_split_low, total_split_high],
                "combined_midpoint": round((total_split_low + total_split_high) / 2, 2),
                "google_domestic_url": build_google_flights_url(origin, split_hub, dep, ret),
                "google_intl_url": build_google_flights_url(split_hub, dest, dep, ret)
            }

        label = f"Option {chr(64+idx)} ({dur} days / {round(dur/7, 1)} weeks)"
        results.append({
            "option_label": label,
            "departure_date": dep.isoformat(),
            "return_date": ret.isoformat(),
            "departure_day_of_week": dep.strftime("%A"),
            "return_day_of_week": ret.strftime("%A"),
            "duration_days": dur,
            "fare_estimate": fare,
            "fits_target_budget": fare["total_estimated_range"][0] <= budget_target,
            "fits_max_budget": fare["total_estimated_range"][0] <= budget_max,
            "deep_links": {
                "google_flights": build_google_flights_url(origin, dest, dep, ret),
                "kayak": build_kayak_url(origin, dest, dep, ret),
                "skyscanner": build_skyscanner_url(origin, dest)
            },
            "stopover_itinerary": stopover_info,
            "split_ticket_itinerary": split_ticket_info
        })

    return {
        "query": {
            "origin": origin,
            "destination": dest,
            "window": window,
            "year": year,
            "min_days": min_days,
            "max_days": max_days,
            "budget_max": budget_max,
            "budget_target": budget_target
        },
        "visa_and_passport_guidance": "US citizens can enter Paraguay visa-free for up to 90 days. Passport must have 6 months validity.",
        "live_price_verification_required": True,
        "disclaimer": (
            "Every fare_estimate below is a STATIC HEURISTIC for ranking dates/origins relatively "
            "cheap-vs-expensive — it is NOT a real price quote. Before telling a human any dollar "
            "figure, open the deep_links (Google Flights / Kayak / Skyscanner) live — via browser "
            "automation or a fresh web search — and report what those pages actually show."
        ),
        "recommended_itineraries": results
    }


def compare_origins(
    origins: List[str],
    dest: str = "ASU",
    window: str = "may",
    after_day: int = 1,
    min_days: int = 28,
    max_days: int = 42,
    max_stay_days: int = 90,
    budget_max: float = 1000.0,
    budget_target: float = 700.0,
    stopover_hub: Optional[str] = "PTY",
    stopover_days: int = 1,
    split_hub: Optional[str] = "MIA",
    year: Optional[int] = None,
    drive_to: Optional[str] = None,
    drive_miles: Optional[float] = None,
    drive_hours: Optional[float] = None,
    mpg: float = 28.0,
    gas_price: float = 3.75,
    drive_extra_cost: float = 0.0
) -> Dict[str, Any]:
    """Run optimize_flight() once per candidate origin airport and assemble a side-by-side
    comparison, attaching driving-positioning economics to whichever origin is reached by
    car (e.g. flying out of a farther, cheaper airport instead of the local one)."""
    origin_blocks = []
    for origin_code in origins:
        origin_code = origin_code.strip().upper()
        single = optimize_flight(
            origin=origin_code, dest=dest, window=window, after_day=after_day,
            min_days=min_days, max_days=max_days, max_stay_days=max_stay_days,
            budget_max=budget_max, budget_target=budget_target,
            stopover_hub=stopover_hub, stopover_days=stopover_days,
            split_hub=split_hub, year=year
        )
        drive_econ = None
        is_drive_positioning = bool(drive_to) and origin_code == drive_to.strip().upper()
        if is_drive_positioning:
            if drive_miles is None or drive_hours is None:
                drive_econ = {
                    "error": (
                        f"--drive-to {drive_to} was set but --drive-miles/--drive-hours were not. "
                        "Look up real one-way distance/time (e.g. Google Maps) and re-run to get "
                        "drive-cost math for this origin."
                    )
                }
            else:
                drive_econ = compute_drive_economics(
                    one_way_miles=drive_miles, one_way_hours=drive_hours,
                    mpg=mpg, gas_price=gas_price, extra_costs=drive_extra_cost
                )
        origin_blocks.append({
            "origin": origin_code,
            "is_drive_positioning": is_drive_positioning,
            "drive_economics": drive_econ,
            "recommended_itineraries": single.get("recommended_itineraries", []),
            "error": single.get("error")
        })

    return {
        "query": {
            "origins": [o.strip().upper() for o in origins],
            "destination": dest.upper(),
            "window": window,
            "year": year,
            "min_days": min_days,
            "max_days": max_days,
            "budget_max": budget_max,
            "budget_target": budget_target
        },
        "visa_and_passport_guidance": "US citizens can enter Paraguay visa-free for up to 90 days. Passport must have 6 months validity.",
        "live_price_verification_required": True,
        "disclaimer": (
            "Every fare_estimate below is a STATIC HEURISTIC for ranking dates/origins relatively "
            "cheap-vs-expensive — it is NOT a real price quote. Before telling a human any dollar "
            "figure or declaring a winner between origins, open the deep_links live (browser "
            "automation or a fresh web search) for each origin's candidate dates and compare what "
            "those pages actually show, netting out any drive_economics cost."
        ),
        "origins": origin_blocks
    }


def _format_window_label(window: str, year: Optional[int]) -> str:
    if ":" in window:
        return window
    return f"{window.capitalize()} {year}" if year is not None else window.capitalize()


def _format_itinerary_block(lines: List[str], opt: Dict[str, Any], q: Dict[str, Any], origin: str) -> None:
    lines.append(f"### {opt['option_label']}")
    lines.append(f"* **Dates:** {opt['departure_date']} ({opt['departure_day_of_week']}) → {opt['return_date']} ({opt['return_day_of_week']})")
    lines.append(f"* **Duration:** {opt['duration_days']} days")
    f_est = opt['fare_estimate']
    lines.append(f"* **Heuristic Placeholder (NOT a real quote):** ${f_est['total_estimated_range'][0]} – ${f_est['total_estimated_range'][1]} — use only to compare relative cheapness; fetch the live links below for an actual number.")

    status = "✅ Within Target ($" + str(q['budget_target']) + ")" if opt['fits_target_budget'] else ("⚠️ Under Max Ceiling ($" + str(q['budget_max']) + ")" if opt['fits_max_budget'] else "❌ Over Budget")
    lines.append(f"* **Budget Status (vs. heuristic placeholder only):** {status}")

    links = opt["deep_links"]
    lines.append(f"* **Live Search Links (fetch these for real prices):**")
    lines.append(f"  * [Google Flights]({links['google_flights']})")
    lines.append(f"  * [Kayak]({links['kayak']})")
    lines.append(f"  * [Skyscanner]({links['skyscanner']})")

    if opt.get("stopover_itinerary"):
        st = opt["stopover_itinerary"]
        lines.append(f"\n  **Free Panama Stopover Option (Copa Airlines):**")
        lines.append(f"  * Stay {st['stopover_days']} day(s) in Panama City ({st['hub']}) departing to destination on {st['stopover_end_date']}.")
        lines.append(f"  * Heuristic placeholder with Panama tax (NOT a real quote): ${st['estimated_fare_range'][0]} – ${st['estimated_fare_range'][1]}")
        lines.append(f"  * [Multi-City Search on Google Flights]({st['google_multicity_url']}) | [Official Copa Stopover Portal]({st['copa_stopover_url']})")

    if opt.get("split_ticket_itinerary"):
        sp = opt["split_ticket_itinerary"]
        lines.append(f"\n  **Split-Ticket Hack via {sp['connection_hub']} (Lowest Cash Outlay):**")
        lines.append(f"  * Leg 1: {origin} ⇄ {sp['connection_hub']} (heuristic placeholder: ${sp['domestic_estimated_range'][0]}–${sp['domestic_estimated_range'][1]})")
        lines.append(f"  * Leg 2: {sp['connection_hub']} ⇄ {q['destination']} (heuristic placeholder: ${sp['intl_estimated_range'][0]}–${sp['intl_estimated_range'][1]})")
        lines.append(f"  * Combined heuristic placeholder: ${sp['combined_total_range'][0]} – ${sp['combined_total_range'][1]}")
        lines.append(f"  * [Leg 1 on Google Flights]({sp['google_domestic_url']}) | [Leg 2 on Google Flights]({sp['google_intl_url']})")

    lines.append("\n---\n")


def format_markdown(data: Dict[str, Any]) -> str:
    """Format optimization results as clean markdown. Handles both the single-origin
    shape (optimize_flight) and the multi-origin comparison shape (compare_origins)."""
    q = data["query"]
    lines = []

    if data.get("disclaimer"):
        lines.append("> ⚠️ **" + data["disclaimer"] + "**\n")

    if "origins" in data:
        # Multi-origin comparison shape
        lines.append(f"# Flight Route Comparison: {', '.join(q['origins'])} ⇄ {q['destination']}")
        lines.append(f"**Travel Window:** {_format_window_label(q['window'], q['year'])} | **Stay Duration:** {q['min_days']}–{q['max_days']} days")
        lines.append(f"**Budget Ceiling:** ${q['budget_max']} | **Target Budget:** ${q['budget_target']}")
        lines.append(f"\n> **Visa Notice:** {data['visa_and_passport_guidance']}\n")

        for block in data["origins"]:
            origin = block["origin"]
            heading = f"## Origin: {origin}"
            if block["is_drive_positioning"]:
                heading += " (drive-to-fly positioning hub)"
            lines.append(heading + "\n")

            if block.get("drive_economics"):
                de = block["drive_economics"]
                if de.get("error"):
                    lines.append(f"> ⚠️ {de['error']}\n")
                else:
                    lines.append("**Positioning Drive Economics (real math, verify inputs):**")
                    lines.append(f"* Round trip: {de['round_trip_miles']} mi / {de['round_trip_hours']}h at {de['mpg']} mpg, gas @ ${de['gas_price_per_gallon']}/gal")
                    lines.append(f"* Round-trip fuel cost: **${de['round_trip_fuel_cost']}**" + (f" + ${de['extra_costs']} extra = **${de['total_positioning_cost']}** total" if de['extra_costs'] else ""))
                    lines.append(f"* {de['note']}\n")

            if block.get("error"):
                lines.append(f"> ❌ {block['error']}\n")

            for opt in block.get("recommended_itineraries", []):
                _format_itinerary_block(lines, opt, q, origin)

        lines.append(
            "## Next Step (required)\n"
            "This report only ranks dates/origins relatively — no number above is a real fare. "
            "Fetch the live links for each origin's top candidate dates (browser automation or a "
            "fresh web search), then compare actual prices net of any drive_economics cost before "
            "recommending a winner.\n"
        )
        return "\n".join(lines)

    # Single-origin shape (legacy / --origin)
    lines.append(f"# Flight Optimization Report: {q['origin']} ⇄ {q['destination']}")
    lines.append(f"**Travel Window:** {_format_window_label(q['window'], q['year'])} | **Stay Duration:** {q['min_days']}–{q['max_days']} days")
    lines.append(f"**Budget Ceiling:** ${q['budget_max']} | **Target Budget:** ${q['budget_target']}")
    lines.append(f"\n> **Visa Notice:** {data['visa_and_passport_guidance']}\n")
    lines.append("## Candidate Itineraries (heuristic ranking — verify prices live)\n")

    for opt in data["recommended_itineraries"]:
        _format_itinerary_block(lines, opt, q, q['origin'])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Flight Optimizer CLI & Agent Tool")
    parser.add_argument("--origin", default="LAS", help="Origin airport code (default: LAS). Ignored if --origins is set.")
    parser.add_argument("--origins", default=None, help="Comma-separated origin airport codes to compare side-by-side, e.g. 'SLC,LAS'")
    parser.add_argument("--dest", default="ASU", help="Destination airport code (default: ASU)")
    parser.add_argument("--window", default="may", help="Search window: 'may', 'december', or 'YYYY-MM-DD:YYYY-MM-DD'")
    parser.add_argument("--after-day", type=int, default=1, help="Only depart after this day of the month")
    parser.add_argument("--min-days", type=int, default=28, help="Minimum stay duration in days (default: 28)")
    parser.add_argument("--max-days", type=int, default=42, help="Maximum stay duration in days (default: 42)")
    parser.add_argument("--max-stay-days", type=int, default=90, help="Absolute max stay limit in days (e.g. 90)")
    parser.add_argument("--budget-max", type=float, default=1000.0, help="Budget ceiling (default: 1000.0)")
    parser.add_argument("--budget-target", type=float, default=700.0, help="Ideal budget target (default: 700.0)")
    parser.add_argument("--stopover", default="PTY", help="Stopover hub airport code (default: PTY)")
    parser.add_argument("--stopover-days", type=int, default=1, help="Number of days for stopover (default: 1)")
    parser.add_argument("--split-hub", default="MIA", help="Positioning hub for split-ticket calculation (default: MIA)")
    parser.add_argument("--year", type=int, default=None, help="Target departure year (e.g. 2026 or 2027)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Output format")
    parser.add_argument("--drive-to", default=None, help="Airport code reached by driving instead of flying local (e.g. LAS), for positioning-hub economics")
    parser.add_argument("--drive-miles", type=float, default=None, help="One-way driving distance in miles to --drive-to (look up real value, e.g. via Google Maps)")
    parser.add_argument("--drive-hours", type=float, default=None, help="One-way driving time in hours to --drive-to")
    parser.add_argument("--mpg", type=float, default=28.0, help="Vehicle fuel economy in mpg (default: 28.0)")
    parser.add_argument("--gas-price", type=float, default=3.75, help="Gas price per gallon in USD (default: 3.75)")
    parser.add_argument("--drive-extra-cost", type=float, default=0.0, help="Extra one-time cost for the drive option (e.g. a hotel night), default 0")

    args = parser.parse_args()

    if args.origins:
        result = compare_origins(
            origins=args.origins.split(","),
            dest=args.dest,
            window=args.window,
            after_day=args.after_day,
            min_days=args.min_days,
            max_days=args.max_days,
            max_stay_days=args.max_stay_days,
            budget_max=args.budget_max,
            budget_target=args.budget_target,
            stopover_hub=args.stopover,
            stopover_days=args.stopover_days,
            split_hub=args.split_hub,
            year=args.year,
            drive_to=args.drive_to,
            drive_miles=args.drive_miles,
            drive_hours=args.drive_hours,
            mpg=args.mpg,
            gas_price=args.gas_price,
            drive_extra_cost=args.drive_extra_cost
        )
    else:
        result = optimize_flight(
            origin=args.origin,
            dest=args.dest,
            window=args.window,
            after_day=args.after_day,
            min_days=args.min_days,
            max_days=args.max_days,
            max_stay_days=args.max_stay_days,
            budget_max=args.budget_max,
            budget_target=args.budget_target,
            stopover_hub=args.stopover,
            stopover_days=args.stopover_days,
            split_hub=args.split_hub,
            year=args.year
        )

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_markdown(result))


if __name__ == "__main__":
    main()
