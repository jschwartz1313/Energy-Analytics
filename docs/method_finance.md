# Finance Method Notes

## Objective
Run a solar project pro-forma and export scenario/sensitivity outputs.

## Inputs
- Market capture-price metrics from `data/marts/ercot_market_metrics.csv`
- Finance assumptions in `config/data_sources.yml`

## Logic
1. Compute annual generation from capacity and capacity factor.
2. Build revenue and opex cash flows with degradation.
3. Model debt service with annuity payment.
4. Calculate NPV, IRR, DSCR, and LCOE.
5. Run 3x3 scenario matrix over price and capex multipliers.
6. Run directional sensitivity cases and generate chart.

## Outputs
- `data/marts/ercot_finance_scenarios.csv`
- `data/marts/ercot_finance_summary.csv`
- `data/marts/ercot_finance_sensitivity.csv`
- `reports/charts/ercot_finance_sensitivity.svg`
