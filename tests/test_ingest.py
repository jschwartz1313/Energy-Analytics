import json
import unittest
from pathlib import Path

from energy_analytics.ingest import run_ingest


class IngestTests(unittest.TestCase):
    def test_ingest_writes_manifest(self) -> None:
        run_ingest(mode_override="sample")
        manifest_path = Path("reports/ingestion_manifest.json")
        self.assertTrue(manifest_path.exists())
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(payload.get("record_count"), 4)
        for rec in payload.get("records", []):
            self.assertTrue(rec.get("contract_valid"))


if __name__ == "__main__":
    unittest.main()
