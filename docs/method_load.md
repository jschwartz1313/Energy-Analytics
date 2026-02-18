# Load Method Notes

## Objective
Create an hourly panel for one ISO region with load, hub price, and weather features.

## Inputs
- `data/raw/ercot_load.csv`
- `data/raw/ercot_price.csv`
- `data/raw/ercot_weather.csv`

## Logic
1. Parse each source and key by `timestamp_utc`.
2. Inner-join on shared hourly timestamps.
3. Write staged and curated panel outputs as CSV.

## QA focus
- Required columns present
- No duplicate timestamps
- Numeric ranges for load, price, and temperature
