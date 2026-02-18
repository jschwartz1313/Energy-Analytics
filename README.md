# Energy Analytics Portfolio (Milestones 1-5)

End-to-end ERCOT analytics workflow covering:
- Data foundation (load, price, weather)
- Queue normalization and expected online MW
- Market metrics and findings
- Solar project finance scenario modeling
- Dashboard and report artifacts

## Architecture

```text
sample/raw data -> staged tables -> curated tables -> marts -> dashboard/report

Ingest:     energy_analytics/ingest.py
Transform:  energy_analytics/transform.py
Queue:      energy_analytics/queue.py
Markets:    energy_analytics/markets.py
Finance:    energy_analytics/finance.py
Charts:     energy_analytics/charts.py
Dashboard:  energy_analytics/dashboard.py
QA:         energy_analytics/qa.py
```

## Milestone Status

- Milestone 1: Complete
- Milestone 2: Complete
- Milestone 3: Complete
- Milestone 4: Complete
- Milestone 5: Complete

## One-command build

Run all pipeline steps and dashboard artifacts:

```bash
make all
```

Run tests:

```bash
make test
```

Run modules individually:

```bash
make ingest
make transform
make queue
make markets
make finance
make charts
make dashboard
make qa
```

## Dashboard

Generated artifact:
- `reports/dashboard/index.html`

Features implemented per spec:
- Required pages: Overview, Load, Supply, Markets, Finance, Downloads
- Scenario controls:
  - Load: Low/Base/High
  - Queue completion: P50/P90
  - Market tightness: low/base/high congestion
- Finance knobs:
  - capex, opex, WACC, debt rate, PPA proxy, degradation
- Region selector
- Download links for CSV outputs
- Auto-generated summary report page: `reports/dashboard/summary_report.html`

Open locally with any browser.

## Key outputs

- Curated panel: `data/curated/ercot_hourly_panel.csv`
- Queue normalized: `data/staged/ercot_queue_normalized.csv`
- Queue outlook: `data/curated/ercot_queue_expected_online_mw.csv`
- Market metrics: `data/marts/ercot_market_metrics.csv`
- Market findings: `reports/market_findings.md`
- Finance scenarios: `data/marts/ercot_finance_scenarios.csv`
- Finance sensitivity: `data/marts/ercot_finance_sensitivity.csv`
- QA report: `reports/qa_report.md`
- Dashboard: `reports/dashboard/index.html`

## Documentation

- Data dictionary: `docs/data_dictionary.md`
- Load method notes: `docs/method_load.md`
- Queue method notes: `docs/method_queue.md`
- Finance method notes: `docs/method_finance.md`
- Assumptions table: `docs/assumptions.md`
