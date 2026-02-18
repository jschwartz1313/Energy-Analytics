from __future__ import annotations

import argparse

from energy_analytics.charts import run_charts
from energy_analytics.dashboard import run_dashboard
from energy_analytics.finance import run_finance
from energy_analytics.forecast import run_forecast
from energy_analytics.ingest import run_ingest
from energy_analytics.markets import run_markets
from energy_analytics.qa import run_qa
from energy_analytics.queue import run_queue_transform
from energy_analytics.transform import run_transform


def main() -> None:
    parser = argparse.ArgumentParser(description="Energy analytics Milestone 1-5 pipeline")
    parser.add_argument(
        "command",
        choices=[
            "ingest",
            "ingest-real",
            "ingest-hybrid",
            "transform",
            "forecast",
            "queue",
            "markets",
            "finance",
            "charts",
            "dashboard",
            "qa",
            "run-all",
        ],
        help="Pipeline command",
    )
    args = parser.parse_args()

    if args.command == "ingest":
        run_ingest()
    elif args.command == "ingest-real":
        run_ingest(mode_override="real")
    elif args.command == "ingest-hybrid":
        run_ingest(mode_override="hybrid")
    elif args.command == "transform":
        run_transform()
    elif args.command == "forecast":
        run_forecast()
    elif args.command == "queue":
        run_queue_transform()
    elif args.command == "markets":
        run_markets()
    elif args.command == "finance":
        run_finance()
    elif args.command == "charts":
        run_charts()
    elif args.command == "dashboard":
        run_dashboard()
    elif args.command == "qa":
        run_qa()
    else:
        run_ingest()
        run_transform()
        run_forecast()
        run_queue_transform()
        run_markets()
        run_finance()
        run_charts()
        run_dashboard()
        run_qa()


if __name__ == "__main__":
    main()
