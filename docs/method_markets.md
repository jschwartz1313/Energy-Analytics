# Markets Method Notes

## Objective
Estimate market-facing project signals from hub price data.

## Metrics
- Capture prices: profile-weighted average prices for solar and wind.
- Capture ratios: capture price divided by average hub price.
- Congestion proxy: absolute deviation from 24-hour rolling average price.
- Negative price metrics: count/share of hours with price < 0.

## Inputs
- `data/curated/ercot_hourly_panel.csv`

## Outputs
- `data/marts/ercot_market_hourly_enriched.csv`
- `data/marts/ercot_market_metrics.csv`
- `reports/market_findings.md`
