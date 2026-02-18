from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def log_metadata(log_path: str, message: str) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    with path.open("a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\n")
