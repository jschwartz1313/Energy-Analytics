import unittest

from energy_analytics.queue import _blend_probability, _normalize_status, _normalize_technology


class QueueNormalizationTests(unittest.TestCase):
    def test_technology_mapping(self) -> None:
        self.assertEqual(_normalize_technology("Solar PV"), "solar")
        self.assertEqual(_normalize_technology("BESS"), "storage")

    def test_status_mapping(self) -> None:
        self.assertEqual(_normalize_status("Under Construction"), "under_construction")
        self.assertEqual(_normalize_status("Cancelled"), "cancelled")

    def test_blend_probability(self) -> None:
        blended = _blend_probability(0.4, 0.2)
        self.assertAlmostEqual(blended, 0.31, places=2)
        self.assertEqual(_blend_probability(0.4, None), 0.4)


if __name__ == "__main__":
    unittest.main()
