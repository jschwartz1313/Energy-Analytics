import unittest

from energy_analytics.queue import _calibration_rows


class QueueCalibrationTests(unittest.TestCase):
    def test_calibration_rows(self) -> None:
        rows = [
            {
                "technology": "solar",
                "target_cod_year": "2020",
                "status": "operational",
                "completion_probability_p50": "0.8",
            },
            {
                "technology": "solar",
                "target_cod_year": "2020",
                "status": "withdrawn",
                "completion_probability_p50": "0.2",
            },
        ]
        out = _calibration_rows(rows)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["technology"], "solar")


if __name__ == "__main__":
    unittest.main()
