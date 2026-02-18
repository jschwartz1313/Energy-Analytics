import unittest

from energy_analytics.finance import _annuity_payment, _npv
from energy_analytics.markets import _moving_average


class MarketsFinanceTests(unittest.TestCase):
    def test_moving_average(self) -> None:
        self.assertEqual(_moving_average([10, 20, 30], 2), [10.0, 15.0, 25.0])

    def test_annuity_payment_positive(self) -> None:
        payment = _annuity_payment(1000, 0.05, 10)
        self.assertGreater(payment, 0)

    def test_npv_discounting(self) -> None:
        val = _npv(0.1, [-100, 60, 60])
        self.assertGreater(val, 0)


if __name__ == "__main__":
    unittest.main()
