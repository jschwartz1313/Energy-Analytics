from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def csv_profile(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        rows = sum(1 for _ in reader)
    return {"row_count": rows, "columns": cols}


def build_manifest_record(
    dataset: str,
    target_path: Path,
    source_type: str,
    source_ref: str,
    contract_errors: list[str],
) -> dict[str, Any]:
    profile = csv_profile(target_path)
    return {
        "dataset": dataset,
        "target_path": str(target_path),
        "source_type": source_type,
        "source_ref": source_ref,
        "retrieved_at_utc": now_utc_iso(),
        "file_bytes": target_path.stat().st_size,
        "sha256": sha256_file(target_path),
        "row_count": profile["row_count"],
        "columns": profile["columns"],
        "contract_valid": len(contract_errors) == 0,
        "contract_errors": contract_errors,
    }


def write_manifest(records: list[dict[str, Any]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "manifest_generated_at_utc": now_utc_iso(),
        "record_count": len(records),
        "records": records,
    }
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
