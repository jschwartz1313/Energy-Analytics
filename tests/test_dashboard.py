import unittest

from energy_analytics.dashboard import _scenario_index


class DashboardTests(unittest.TestCase):
    def test_scenario_index_keying(self) -> None:
        rows = [
            {
                "price_case": "base",
                "capex_case": "base",
                "npv_musd": "1.2",
                "irr": "0.1",
                "min_dscr": "1.1",
                "avg_dscr": "1.2",
                "lcoe_usd_mwh": "50.0",
                "year1_revenue_musd": "5.0",
            }
        ]
        idx = _scenario_index(rows)
        self.assertIn("contracted|base|base", idx)
        self.assertAlmostEqual(idx["contracted|base|base"]["npv_musd"], 1.2)


if __name__ == "__main__":
    unittest.main()
