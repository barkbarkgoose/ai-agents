#!/usr/bin/env python3
"""
Unit tests for the Flight Optimizer script.
"""

import unittest
from datetime import date
from fare_estimator import estimate_fare, get_date_multiplier
from flight_optimizer import (
    get_candidate_dates,
    optimize_flight,
    compare_origins,
    compute_drive_economics,
    build_google_flights_url,
    build_google_multicity_url
)


class TestFlightOptimizer(unittest.TestCase):

    def test_seasonal_multiplier(self):
        # Peak Christmas date
        mult_peak, reason_peak = get_date_multiplier(date(2026, 12, 22))
        self.assertGreaterEqual(mult_peak, 1.5)
        self.assertIn("Peak", reason_peak)

        # May shoulder date
        mult_may, reason_may = get_date_multiplier(date(2027, 5, 5))
        self.assertLessEqual(mult_may, 0.9)
        self.assertIn("May", reason_may)

    def test_fare_estimate_structure(self):
        fare = estimate_fare("LAS", "ASU", date(2027, 5, 5), date(2027, 6, 9))
        self.assertIn("base_airfare_range", fare)
        self.assertIn("mandatory_taxes_and_fees", fare)
        self.assertIn("total_estimated_range", fare)
        self.assertLess(fare["total_estimated_range"][0], 850.0)

    def test_candidate_dates_filtering(self):
        candidates = get_candidate_dates("may", 2027, min_days=28, max_days=42)
        self.assertTrue(len(candidates) > 0)
        for c in candidates:
            self.assertGreaterEqual(c["duration_days"], 28)
            self.assertLessEqual(c["duration_days"], 42)

    def test_december_candidates_avoid_peak(self):
        candidates = get_candidate_dates("december", 2026, after_day=12, min_days=28, max_days=42)
        self.assertTrue(len(candidates) > 0)
        for c in candidates:
            # Outbound shouldn't be right on Dec 19-24
            if c["dep_date"].month == 12:
                self.assertFalse(18 <= c["dep_date"].day <= 24)
            # Return shouldn't be Jan 1-8
            if c["ret_date"].month == 1:
                self.assertFalse(1 <= c["ret_date"].day <= 8)

    def test_url_generation(self):
        url = build_google_flights_url("LAS", "ASU", date(2027, 5, 5), date(2027, 6, 9))
        self.assertIn("LAS", url)
        self.assertIn("ASU", url)
        self.assertIn("2027-05-05", url)
        self.assertIn("2027-06-09", url)

        mc_url = build_google_multicity_url("LAS", "PTY", "ASU", date(2027, 5, 5), date(2027, 5, 6), date(2027, 6, 9))
        self.assertIn("PTY", mc_url)

    def test_optimize_flight_may(self):
        res = optimize_flight(origin="LAS", dest="ASU", window="may", year=2027)
        self.assertIn("recommended_itineraries", res)
        self.assertGreaterEqual(len(res["recommended_itineraries"]), 1)
        opt = res["recommended_itineraries"][0]
        self.assertIn("deep_links", opt)
        self.assertIn("stopover_itinerary", opt)
        self.assertIn("split_ticket_itinerary", opt)
        # Fare estimates must self-disclose they are not real prices.
        self.assertFalse(opt["fare_estimate"]["is_live_data"])
        self.assertIn("HEURISTIC", opt["fare_estimate"]["disclaimer"])
        self.assertTrue(res["live_price_verification_required"])

    def test_fare_estimate_flags_missing_baseline(self):
        # SLC has no hardcoded ROUTE_BASELINES entry, so it must fall back to the
        # generic placeholder and say so explicitly.
        fare = estimate_fare("SLC", "ASU", date(2027, 1, 19), date(2027, 2, 23))
        self.assertFalse(fare["has_route_baseline"])
        self.assertIn("NO baseline exists", fare["disclaimer"])

    def test_compute_drive_economics(self):
        econ = compute_drive_economics(one_way_miles=420, one_way_hours=6.5, mpg=28.0, gas_price=3.75)
        self.assertEqual(econ["round_trip_miles"], 840.0)
        self.assertEqual(econ["round_trip_hours"], 13.0)
        self.assertAlmostEqual(econ["round_trip_fuel_cost"], 840.0 / 28.0 * 3.75, places=2)
        self.assertEqual(econ["total_positioning_cost"], econ["round_trip_fuel_cost"])

    def test_compare_origins_multi(self):
        res = compare_origins(
            origins=["SLC", "LAS"], dest="ASU", window="may", year=2027,
            drive_to="LAS", drive_miles=420, drive_hours=6.5
        )
        self.assertEqual(len(res["origins"]), 2)
        slc_block, las_block = res["origins"]
        self.assertEqual(slc_block["origin"], "SLC")
        self.assertFalse(slc_block["is_drive_positioning"])
        self.assertIsNone(slc_block["drive_economics"])
        self.assertEqual(las_block["origin"], "LAS")
        self.assertTrue(las_block["is_drive_positioning"])
        self.assertIsNotNone(las_block["drive_economics"])
        self.assertGreaterEqual(len(las_block["recommended_itineraries"]), 1)

    def test_compare_origins_missing_drive_distance(self):
        # drive_to set without drive_miles/drive_hours should surface an actionable error,
        # not silently invent a distance.
        res = compare_origins(origins=["LAS"], dest="ASU", window="may", year=2027, drive_to="LAS")
        self.assertIn("error", res["origins"][0]["drive_economics"])


if __name__ == "__main__":
    unittest.main()
