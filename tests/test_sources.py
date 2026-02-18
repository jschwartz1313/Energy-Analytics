import unittest

from energy_analytics.sources import build_open_meteo_weather_rows


class SourceAdapterTests(unittest.TestCase):
    def test_open_meteo_weather_mapping(self) -> None:
        payload = {
            "hourly": {
                "time": ["2025-01-01T00:00", "2025-01-01T01:00"],
                "temperature_2m": [50.0, 49.5],
            }
        }
        rows = build_open_meteo_weather_rows(payload, region="ERCOT")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["region"], "ERCOT")
        self.assertTrue(rows[0]["timestamp_utc"].endswith("Z"))


if __name__ == "__main__":
    unittest.main()
