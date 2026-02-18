import unittest

from energy_analytics.transform import PANEL_COLUMNS


class TransformTests(unittest.TestCase):
    def test_panel_columns_stable(self) -> None:
        self.assertEqual(
            PANEL_COLUMNS,
            [
                "timestamp_utc",
                "region",
                "hub",
                "load_mw",
                "price_usd_mwh",
                "temperature_f",
            ],
        )


if __name__ == "__main__":
    unittest.main()
