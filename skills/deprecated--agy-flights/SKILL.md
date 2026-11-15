---
name: agy-flights
description: >-
  Finds candidate cheap-vs-expensive travel windows, computes layovers and free airline stopovers (e.g., Copa Panama Stopover), evaluates split-ticketing hubs and drive-to-a-cheaper-airport positioning tradeoffs, and generates deep links for Google Flights, Kayak, and Skyscanner — then requires fetching REAL prices for those links (via browser automation or web search) before quoting any number to the user. Use when asked to find optimal flight dates, compare travel seasons or departure airports, or plan international flight itineraries. Do NOT use its bundled fare numbers as real pricing — they are a relative-ranking heuristic only.
---

# Flight Optimizer Skill (`agy-flights`)

A programmatic skill for discovering candidate flight dates, comparing departure airports (including "drive to a farther, cheaper airport" positioning plays), analyzing multi-leg connections, leveraging free airline stopover programs, and generating 1-click live booking deep links.

> ⚠️ **This skill does not know real prices.** `fare_estimator.py` is a static heuristic (hardcoded per-route baselines × day-of-week × season multipliers) used only to rank dates/origins relative to each other. It has baselines for exactly three routes (`LAS-ASU`, `MIA-ASU`, `LAS-MIA`); every other origin silently falls back to a generic placeholder that can be off by hundreds of dollars or more. **Never present its dollar figures to the user as quotes.** Real prices must come from actually fetching the generated deep links.

---

## Capabilities & Architecture

1. **Date & Seasonality Ranking:** Scans potential travel months, detects holiday peak penalties (e.g., Christmas/New Year surges, summer peaks), enforces day-of-week fare rules (prioritizing Tuesdays and Wednesdays), and respects stay duration limits (e.g., 4–6 weeks, 90-day visa constraints). This ranking is a reasonable industry-standard heuristic even though the dollar amounts attached to it are not.
2. **Multi-Origin / Positioning-Hub Comparison:** Runs the same date search across several candidate departure airports side-by-side (e.g., the user's local airport vs. a farther major hub), and computes real drive-cost/time math (`compute_drive_economics`) for any origin reached by car instead of a local flight — e.g. "is driving 6.5 hours from Provo to fly out of Las Vegas actually worth the fare difference?"
3. **Airline Stopover Program Engine:** Discovers and calculates itineraries utilizing official \$0 airfare stopover programs (such as Copa Airlines' Panama Stopover in PTY, TAP Air Portugal in LIS, etc.).
4. **Split-Ticket Hub Optimization:** Identifies dual-ticket routes through major positioning gateways (e.g., Las Vegas → Miami + Miami → Asunción) as a shape to check live, not a guaranteed saving.
5. **Deep-Link Generator:** Programmatically constructs exact, pre-populated direct search URLs for Google Flights (round-trip and multi-city), Kayak, Skyscanner, and airline stopover engines — the only outputs of this skill that are ground truth.
6. **Live Price Verification (mandatory, agent-side):** The agent must open the generated deep links via browser automation (or a fresh web search) and report what those pages actually show before giving the user a number. See **Live Price Verification Protocol** below.

---

## Directory Structure

```text
.
├── SKILL.md                          # Main skill specification & agent runbook
├── scripts/
│   ├── flight_optimizer.py           # Date/route candidate generator, drive economics, deep-link generator
│   ├── fare_estimator.py             # Heuristic-only fare model (NOT live pricing — see disclaimer)
│   └── test_flight_optimizer.py      # Automated unit tests
├── references/
│   ├── stopover_programs.json        # Database of airlines with free/low-cost stopovers
│   ├── seasonal_rules.json           # Holiday surcharges & day-of-week multipliers
│   └── airport_hubs.json             # Key airport hubs, visa rules, and transit metadata
└── examples/
    ├── las_to_asu_input.json         # Sample agent input query payload
    ├── las_to_asu_output.json        # Sample structured JSON response payload
    └── output-example.md             # Benchmark example of final synthesized user advisory report (predates the live-pricing requirement — treat its dollar figures as illustrative formatting only, not a template to reuse verbatim)
```

---

## Output Architecture: Scripts vs. Live Lookup vs. Advisory Report

Three stages, in order — do not skip stage 2:

1. **`scripts/flight_optimizer.py` generates candidates (deterministic, no network calls):**
   - Evaluates calendar windows and calculates date candidate pairs.
   - Enforces low-fare day-of-week rules (Tuesdays and Wednesdays) and holiday penalties.
   - Computes drive-cost/time economics for any positioning-hub origin.
   - Generates exact, pre-populated booking deep links for Google Flights, Kayak, and Skyscanner.
   - Attaches a heuristic fare range to each option **purely for relative ranking** (which dates/origins look cheaper than others) — flagged `is_live_data: false` with an explicit disclaimer in every record.

2. **Live Price Verification (agent does this, not the script):**
   - For each origin being compared, and at minimum the top-ranked candidate date pair, actually fetch the real price. Prefer browser automation (`claude-in-chrome`: navigate to the `google_flights` deep link, then `get_page_text` / `read_page` to read the displayed fares) so you see live, current inventory. If browser tools aren't available, use `WebSearch`/`WebFetch` against the same links or a general query instead of guessing.
   - Do this for every origin in a comparison (e.g. both the local airport and the drive-to positioning hub) — the whole point of a multi-origin run is to compare *real* numbers, not two equally-fake heuristics.
   - If a live fetch fails or is ambiguous, say so explicitly to the user rather than silently falling back to the heuristic number.

3. **Advisory Report (agent synthesizes for the user):**
   - Present the **live-fetched** prices as the headline numbers. The heuristic range may still be mentioned as context ("model predicted X, live search shows Y") but must never stand alone as if it were a quote.
   - For multi-origin/drive comparisons: net out `drive_economics.total_positioning_cost` against the live fare difference and state a clear winner with the real math shown (e.g. "$X live fare from LAS + $113 in gas = $Y, vs. $Z live fare from SLC direct").
   - Follow the general structure in [`examples/output-example.md`](./examples/output-example.md) for tone/layout (comparison table, "why this works," itemized costs, stopover steps, curated links) — but substitute every price in it with what you actually found live.

---

## Live Price Verification Protocol

When the user wants real numbers (which is the default expectation — assume it unless they explicitly ask for a rough/offline pass):

1. Run `flight_optimizer.py` to get candidate dates, drive economics, and deep links (fast, free, no network use).
2. For each origin × top 1–3 candidate date pairs, load the `google_flights` deep link with browser automation and extract the actual lowest displayed fare. Note the airline and any stops shown — a "cheap" fare with 2 stops and a 10-hour layover is a different tradeoff than a heuristic number implies.
3. Cross-check with the `kayak` link if the Google Flights result looks stale, blocked, or inconsistent.
4. For a drive-to-a-hub comparison, repeat step 2 for the positioning-hub origin, then add `drive_economics.total_positioning_cost` to that fare before comparing it to the local-airport fare.
5. Only then write the user-facing advisory, citing what was actually observed (with rough date/time of the check, since fares move) rather than the script's placeholder math.

---

## Agent Invocation Guide

### 1. Single Origin (Markdown Output)

```bash
python3 scripts/flight_optimizer.py \
  --origin LAS \
  --dest ASU \
  --window may \
  --min-days 28 \
  --max-days 42 \
  --stopover PTY \
  --format markdown
```

### 2. Multi-Origin Comparison with Drive-to-Airport Positioning

Compare flying direct from a local airport against driving to a farther, historically-cheaper hub (e.g. Provo, UT → fly SLC direct, vs. drive to Las Vegas and fly LAS):

```bash
python3 scripts/flight_optimizer.py \
  --origins SLC,LAS \
  --dest ASU \
  --window 2027-01-15:2027-02-28 \
  --min-days 28 \
  --max-days 42 \
  --drive-to LAS \
  --drive-miles 420 \
  --drive-hours 6.5 \
  --format markdown
```

`--drive-miles`/`--drive-hours` must be a real one-way distance/time (look it up — e.g. via a maps query — don't guess). Omitting them while `--drive-to` is set produces an explicit error in the output rather than an invented number.

### 3. Programmatic JSON Run (For Agent Processing)

```bash
python3 scripts/flight_optimizer.py \
  --origins SLC,LAS \
  --dest ASU \
  --window december \
  --after-day 12 \
  --min-days 28 \
  --max-days 42 \
  --drive-to LAS --drive-miles 420 --drive-hours 6.5 \
  --format json
```

### 4. Custom Date Range

```bash
python3 scripts/flight_optimizer.py \
  --origin LAS \
  --dest ASU \
  --window 2027-05-01:2027-06-30 \
  --min-days 30 \
  --max-days 45
```

---

## CLI Options Reference

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--origin` | string | `LAS` | 3-letter IATA origin airport code. Ignored if `--origins` is set. |
| `--origins` | string | `None` | Comma-separated origin airport codes to compare side-by-side, e.g. `SLC,LAS` |
| `--dest` | string | `ASU` | 3-letter IATA destination airport code |
| `--window` | string | `may` | Target window: `may`, `december`, or `YYYY-MM-DD:YYYY-MM-DD` |
| `--after-day` | int | `1` | Earliest departure day within the month (e.g. `12` for post-Dec 12) |
| `--min-days` | int | `28` | Minimum trip length in days (4 weeks = 28) |
| `--max-days` | int | `42` | Maximum trip length in days (6 weeks = 42) |
| `--max-stay-days`| int | `90` | Hard cap on stay duration (e.g. 90 days for visa-free entry) |
| `--budget-target`| float | `700.0` | Target preferred total round-trip price in USD (compared against the heuristic, not a live price) |
| `--budget-max` | float | `1000.0`| Hard ceiling budget in USD (same caveat) |
| `--stopover` | string | `PTY` | Airport code for free airline stopover evaluation |
| `--stopover-days`| int | `1` | Duration in days for stopover in hub |
| `--split-hub` | string | `MIA` | Positioning hub for split-ticket hack evaluation |
| `--year` | int | `None` | Departure year (defaults dynamically to current/upcoming year) |
| `--drive-to` | string | `None` | Airport code reached by car instead of flying locally (positioning-hub economics) |
| `--drive-miles` | float | `None` | Real one-way driving distance in miles to `--drive-to` |
| `--drive-hours` | float | `None` | Real one-way driving time in hours to `--drive-to` |
| `--mpg` | float | `28.0` | Vehicle fuel economy in mpg |
| `--gas-price` | float | `3.75` | Gas price per gallon in USD |
| `--drive-extra-cost` | float | `0.0` | One-time extra cost for the drive option (e.g. a hotel night) |
| `--format` | choice | `markdown`| `markdown` or `json` |

---

## Verification & Testing

```bash
python3 scripts/test_flight_optimizer.py
```

Covers seasonal multipliers, date candidate generation, deep link URLs, drive-economics math, multi-origin comparison structure, and the fare heuristic's self-disclosure fields (`is_live_data`, `has_route_baseline`, `disclaimer`).
