# Architecture

```mermaid
flowchart LR
  A[data/samples or real URLs] --> B[data/raw]
  B --> C[data/staged]
  C --> D[data/curated]
  D --> E[data/marts]
  E --> F[reports/charts]
  E --> G[reports/dashboard]
  E --> H[reports/market_findings.md]

  I[config/schema_contracts.yml] --> J[contracts validation]
  J --> B
  K[reports/ingestion_manifest.json] --> L[provenance + reproducibility]
```

## Orchestration
- `make all` runs the full pipeline in deterministic order.
- `make ingest-real` and `make ingest-hybrid` support live-source workflows.

## Data Quality and Provenance
- Schema contracts are enforced at ingestion.
- Ingestion manifest records source refs, checksums, and row counts.
- QA validates artifacts across all milestones.
