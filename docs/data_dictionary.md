# Data Dictionary

## `data/curated/ercot_hourly_panel.csv`
- `timestamp_utc`: Hour timestamp in UTC.
- `region`: Region code (ERCOT).
- `hub`: Hub identifier (HB_NORTH).
- `load_mw`: Regional load in MW.
- `price_usd_mwh`: Hub price in USD/MWh.
- `temperature_f`: Temperature in Fahrenheit.

## `data/staged/ercot_queue_normalized.csv`
- `queue_id`: Queue project identifier.
- `project_name`: Project label.
- `technology`: Canonical technology (`solar`, `wind`, `storage`, `other`).
- `mw`: Nameplate MW.
- `status`: Canonical queue status.
- `queue_date`: Queue entry date.
- `target_cod`: Target COD date.
- `target_cod_year`: Target COD year.
- `completion_probability_p50`: P50 completion probability.
- `completion_probability_p90`: P90 completion probability.

## `data/curated/ercot_queue_expected_online_mw.csv`
- `year`: COD year.
- `technology`: Technology bucket.
- `project_count`: Number of projects.
- `nameplate_mw`: Sum of nameplate MW.
- `expected_online_mw_p50`: P50 expected online MW.
- `expected_online_mw_p90`: P90 expected online MW.

## `data/marts/ercot_market_metrics.csv`
- `metric`: Metric name.
- `value`: Metric numeric value.

## `data/marts/ercot_finance_scenarios.csv`
- `scenario_id`: Scenario sequence id.
- `price_case`: `low`, `base`, or `high`.
- `capex_case`: `low`, `base`, or `high`.
- `npv_musd`: Equity NPV in million USD.
- `irr`: Internal rate of return.
- `min_dscr`: Minimum DSCR over debt tenor.
- `avg_dscr`: Average DSCR over debt tenor.
- `lcoe_usd_mwh`: Levelized cost of energy.
