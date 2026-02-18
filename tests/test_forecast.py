import unittest

from energy_analytics.forecast import _linear_fit, _mape, _rmse


class ForecastTests(unittest.TestCase):
    def test_linear_fit(self) -> None:
        a, b = _linear_fit([1, 2, 3], [3, 5, 7])
        self.assertAlmostEqual(a, 1.0, places=6)
        self.assertAlmostEqual(b, 2.0, places=6)

    def test_rmse(self) -> None:
        self.assertAlmostEqual(_rmse([1, 2], [1, 4]), (2.0**0.5), places=6)

    def test_mape(self) -> None:
        self.assertAlmostEqual(_mape([10, 20], [9, 18]), 0.1, places=6)


if __name__ == "__main__":
    unittest.main()
