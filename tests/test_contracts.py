import tempfile
import unittest
from pathlib import Path

from energy_analytics.contracts import validate_csv_contract


class ContractTests(unittest.TestCase):
    def test_validate_csv_contract_pass(self) -> None:
        contract = {
            "required_columns": ["timestamp_utc", "value"],
            "column_types": {"timestamp_utc": "datetime", "value": "float"},
        }
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.csv"
            p.write_text("timestamp_utc,value\n2025-01-01T00:00:00Z,1.5\n", encoding="utf-8")
            errors = validate_csv_contract(p, contract)
            self.assertEqual(errors, [])

    def test_validate_csv_contract_fail(self) -> None:
        contract = {
            "required_columns": ["timestamp_utc", "value"],
            "column_types": {"timestamp_utc": "datetime", "value": "float"},
        }
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.csv"
            p.write_text("timestamp_utc,value\nnot-a-date,abc\n", encoding="utf-8")
            errors = validate_csv_contract(p, contract)
            self.assertGreater(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
