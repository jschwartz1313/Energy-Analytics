from __future__ import annotations

import shutil
from pathlib import Path

from energy_analytics.config import load_config
from energy_analytics.metadata import log_metadata


def run_ingest() -> None:
    cfg = load_config()
    src = cfg["sample_data"]
    dst = cfg["raw_output"]
    log_path = cfg["reports"]["metadata_log"]

    for key in ("load", "price", "weather", "queue"):
        in_path = Path(src[key])
        out_path = Path(dst[key])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(in_path, out_path)
        size = out_path.stat().st_size
        log_metadata(log_path, f"ingest:{key} source={in_path} target={out_path} bytes={size}")

    log_metadata(log_path, f"ingest complete region={cfg['region']}")


if __name__ == "__main__":
    run_ingest()
