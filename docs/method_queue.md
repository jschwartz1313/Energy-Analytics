# Queue Method Notes

## Objective
Normalize interconnection queue records and estimate expected online MW by COD year.

## Inputs
- `data/raw/ercot_queue.csv`

## Logic
1. Normalize technology and status labels to canonical values.
2. Apply status-based completion probabilities.
3. Blend with empirical technology completion rate when enough historical terminal statuses exist.
4. Produce annual expected online MW for P50 and P90 views.

## Outputs
- `data/staged/ercot_queue_normalized.csv`
- `data/curated/ercot_queue_expected_online_mw.csv`
