#!/usr/bin/env python3
"""
Fare Estimator Engine for International Flight Routing.
Models ATPCO/IATA base fares, international departure/arrival taxes,
transit fees, and seasonal/day-of-week multipliers.
"""

from datetime import date
from typing import Dict, Any, Tuple

# Base round-trip baseline fare reference by route (Economy Basic)
ROUTE_BASELINES = {
    ("LAS", "ASU"): {
        "base_fare_low": 460.0,
        "base_fare_high": 540.0,
        "us_taxes": 85.0,
        "foreign_taxes": 78.0,
        "transit_fee": 20.0,
        "baggage_fee_each_way": 45.0,
        "primary_airline": "Copa Airlines",
        "primary_hub": "PTY"
    },
    ("MIA", "ASU"): {
        "base_fare_low": 280.0,
        "base_fare_high": 360.0,
        "us_taxes": 65.0,
        "foreign_taxes": 78.0,
        "transit_fee": 20.0,
        "baggage_fee_each_way": 45.0,
        "primary_airline": "Copa / Avianca / LATAM",
        "primary_hub": "PTY/BOG"
    },
    ("LAS", "MIA"): {
        "base_fare_low": 120.0,
        "base_fare_high": 180.0,
        "us_taxes": 35.0,
        "foreign_taxes": 0.0,
        "transit_fee": 0.0,
        "baggage_fee_each_way": 35.0,
        "primary_airline": "Southwest / Frontier / Spirit / American",
        "primary_hub": None
    }
}

DEFAULT_BASELINE = {
    "base_fare_low": 500.0,
    "base_fare_high": 650.0,
    "us_taxes": 85.0,
    "foreign_taxes": 75.0,
    "transit_fee": 25.0,
    "baggage_fee_each_way": 45.0,
    "primary_airline": "Major Carrier",
    "primary_hub": None
}

DAY_MULTIPLIERS = {
    0: 1.00,  # Monday
    1: 0.90,  # Tuesday (cheapest)
    2: 0.90,  # Wednesday (cheapest)
    3: 0.98,  # Thursday
    4: 1.18,  # Friday (weekend surcharge)
    5: 1.05,  # Saturday
    6: 1.22   # Sunday (highest)
}


def get_date_multiplier(d: date) -> Tuple[float, str]:
    """Calculate seasonal multiplier for a given flight date."""
    month, day = d.month, d.day
    
    # Christmas & New Year Surge (Dec 18 - Jan 8)
    if (month == 12 and day >= 18) or (month == 1 and day <= 8):
        return 1.60, "Christmas/New Year Peak Surcharge"
    
    # Pre-holiday sweet spot (Dec 12 - Dec 16)
    if month == 12 and 12 <= day <= 16:
        return 1.05, "Pre-Holiday Shoulder Window"
        
    # May Shoulder Season
    if month == 5:
        return 0.85, "May Low/Shoulder Season"
        
    # Post-Holiday January Rebound (Jan 15 - Jan 31)
    if month == 1 and day >= 15:
        return 0.92, "January Post-Holiday Rebound"
        
    # US Summer Peak (late June - mid August)
    if (month == 6 and day >= 20) or month == 7 or (month == 8 and day <= 18):
        return 1.35, "Summer Vacation Peak"
        
    return 1.00, "Standard Season"


def estimate_fare(
    origin: str,
    dest: str,
    dep_date: date,
    ret_date: date,
    has_stopover: bool = False,
    stopover_tax: float = 45.0,
    include_checked_bag: bool = False
) -> Dict[str, Any]:
    """Calculate estimated fare breakdown for round-trip travel."""
    key = (origin.upper(), dest.upper())
    meta = ROUTE_BASELINES.get(key, DEFAULT_BASELINE)
    has_route_baseline = key in ROUTE_BASELINES
    
    dep_dow_mult = DAY_MULTIPLIERS[dep_date.weekday()]
    ret_dow_mult = DAY_MULTIPLIERS[ret_date.weekday()]
    dow_avg = (dep_dow_mult + ret_dow_mult) / 2.0
    
    dep_seas_mult, dep_reason = get_date_multiplier(dep_date)
    ret_seas_mult, ret_reason = get_date_multiplier(ret_date)
    seas_avg = (dep_seas_mult + ret_seas_mult) / 2.0
    
    combined_mult = dow_avg * seas_avg
    
    est_base_low = round(meta["base_fare_low"] * combined_mult, 2)
    est_base_high = round(meta["base_fare_high"] * combined_mult, 2)
    
    taxes = round(meta["us_taxes"] + meta["foreign_taxes"] + meta["transit_fee"], 2)
    stopover_fee = stopover_tax if has_stopover else 0.0
    baggage = (meta["baggage_fee_each_way"] * 2) if include_checked_bag else 0.0
    
    total_low = round(est_base_low + taxes + stopover_fee + baggage, 2)
    total_high = round(est_base_high + taxes + stopover_fee + baggage, 2)
    
    return {
        "route": f"{origin.upper()} ⇄ {dest.upper()}",
        "dep_date": dep_date.isoformat(),
        "ret_date": ret_date.isoformat(),
        "days_of_week": f"{dep_date.strftime('%A')} -> {ret_date.strftime('%A')}",
        "dep_multiplier": round(dep_dow_mult * dep_seas_mult, 2),
        "ret_multiplier": round(ret_dow_mult * ret_seas_mult, 2),
        "dep_season_note": dep_reason,
        "ret_season_note": ret_reason,
        "base_airfare_range": [est_base_low, est_base_high],
        "mandatory_taxes_and_fees": taxes,
        "stopover_tax": stopover_fee,
        "checked_bag_cost": baggage,
        "total_estimated_range": [total_low, total_high],
        "midpoint_estimate": round((total_low + total_high) / 2, 2),
        "is_live_data": False,
        "has_route_baseline": has_route_baseline,
        "disclaimer": (
            "STATIC HEURISTIC ONLY — not a real fare quote."
            + ("" if has_route_baseline else f" NO baseline exists for {origin.upper()}-{dest.upper()}; "
               "this used the generic DEFAULT_BASELINE placeholder, which is even less trustworthy.")
            + " Use this only to rank dates/origins relative to each other; fetch the deep_links "
              "live before quoting any dollar amount to a human."
        )
    }


if __name__ == "__main__":
    import sys
    print("Testing Fare Estimator:")
    sample = estimate_fare("LAS", "ASU", date(2027, 5, 5), date(2027, 6, 9), has_stopover=True)
    print(sample)
