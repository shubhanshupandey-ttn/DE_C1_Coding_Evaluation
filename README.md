# Databricks Medallion Pipeline

A practical data engineering project demonstrating the **medallion architecture** on Databricks, built incrementally with AI-assisted development and accompanying documentation.

## Project Purpose

This repository implements an end-to-end analytics data pipeline for a small retail-style domain centered on **customers**, **orders**, and **products**. The goal is to show realistic data engineering practices—not placeholder scaffolding—including:

- Sample/raw data generation
- Bronze-layer ingestion
- Silver-layer cleansing, transformation, and data quality
- Gold-layer analytical datasets
- Dashboard-oriented queries and guidance
- End-to-end pipeline validation on Databricks

The project is intended as a coherent, reviewable artifact suitable for demonstrating data engineering design, implementation discipline, and responsible AI-assisted development.

## High-Level Architecture

```
Raw / sample data  (data/)
        ↓
Bronze             (src/bronze/)       — raw ingestion, minimal transformation
        ↓
Silver             (src/silver/)       — cleansed, conformed data + quality checks
        ↓
Gold               (src/gold/)         — analytical / business-ready datasets
        ↓
Analytics          (src/dashboard/)    — dashboard queries and usage guidance
        ↓
Validation         (src/validation/)   — Databricks SQL checks across all layers
```

**Unity Catalog (validated):** `de_c1_coding_evaluation` with schemas `bronze`, `silver`, and `gold`.

Supporting assets:

- **`ai-prompts/`** — preserved prompts from AI-assisted implementation phases
- **`VALIDATION_REPORT.md`** — final validation evidence (26/26 PASS on Databricks Serverless)
- **Root documentation** — requirements, design, data model, and quality strategy
- **`database/`** — listed in original scope; **not yet implemented** in this repository

Data quality is a first-class concern in the Silver layer, with explicit checks for completeness, uniqueness, type validation, referential integrity, and business logic. Invalid records are written to `silver_quarantine_records`; category results are persisted in `silver_dq_summary`.

## Repository Structure

```
.
├── README.md
├── VALIDATION_REPORT.md
├── candidate-info.md
├── tool-workflow.md
├── requirements-analysis.md
├── design-notes.md
├── data-model.md
├── data-quality-strategy.md
├── reflection.md
├── final-ai-usage-summary.md
├── debugging-notes.md
│
├── src/
│   ├── data_generation/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── dashboard/
│   └── validation/
│
├── data/
└── ai-prompts/
```

Layer-specific notes: `DATA_GENERATION_NOTES.md`, `BRONZE_LAYER_NOTES.md`, `SILVER_LAYER_NOTES.md`, `GOLD_LAYER_NOTES.md`, `DASHBOARD_GUIDE.md`.

## Technology & Tooling Context

| Area | Approach |
|------|----------|
| Platform | Databricks Serverless (lakehouse / medallion pattern) |
| Catalog | `de_c1_coding_evaluation` (Unity Catalog) |
| Languages | Python (ingestion, Silver DQ, orchestration), SQL (Gold, dashboard, validation) |
| Table format | Delta Lake |
| Source data | Generated sample CSV files in `data/` |
| Development | Incremental phases with documentation and `ai-prompts/` artifacts |

Bronze defaults to schema `bronze` and tables `bronze_customers`, `bronze_products`, `bronze_orders`. Use `--catalog de_c1_coding_evaluation` for Unity Catalog. See layer notes for notebook execution patterns.

## Development Approach

Work proceeds in **incremental phases**. Each phase delivers:

1. **Implementation** (code and/or data as applicable)
2. **Documentation** (updated or new project docs)
3. **Prompt artifact** (recorded in the relevant `ai-prompts/` file)

Foundation documentation (requirements, design, data model, quality strategy) was created before pipeline code so later phases remain internally consistent. AI tools assisted with drafting and implementation; all output was subject to developer review and Databricks validation.

## Current Project Status

| Phase | Status |
|-------|--------|
| Phase 1: Project foundation | Complete |
| Phase 2: Data generation | Complete |
| Phase 3: Bronze ingestion | Complete (Databricks validated) |
| Phase 4: Silver + data quality | Complete (Databricks validated) |
| Phase 5: Gold analytics | Complete (Databricks validated) |
| Phase 6: Dashboard | Complete (Databricks SQL dashboard validated) |
| Pipeline validation (`pipeline_validation.sql`) | **Complete — 26/26 PASS** on Databricks Serverless |
| Submission provenance (`ai-prompts/`, `data/`, `final-ai-usage-summary.md`) | **Complete** |
| Database setup artifacts (`database/`) | Not started |
| Closure (`reflection.md`, `final-ai-usage-summary.md`, `debugging-notes.md`) | **Complete** |

## Run Data Generation

From the repository root (Python 3, stdlib only):

```bash
python3 src/data_generation/generate_sample_data.py
```

This writes `data/customers.csv`, `data/products.csv`, and `data/orders.csv`. See `src/data_generation/DATA_GENERATION_NOTES.md` for schemas, defect matrix, and CLI options.

## Run Bronze Ingestion

**Local validation** (no PySpark required):

```bash
python3 src/bronze/ingest_all.py --dry-run
```

**Databricks** (requires PySpark + Delta):

```bash
python src/bronze/ingest_all.py --data-dir /path/to/data --catalog de_c1_coding_evaluation
```

See `src/bronze/BRONZE_LAYER_NOTES.md` for table names, design decisions, and notebook execution.

## Run Silver Pipeline

Silver is orchestrated by `src/silver/create_silver_tables.py` (`run_silver_pipeline`). On Databricks, run from a notebook with an active `spark` session after Bronze ingest. The pipeline executes five DQ categories, writes quarantine and DQ summary tables, then overwrites curated `silver_*` tables.

See `src/silver/SILVER_LAYER_NOTES.md` for execution order, quarantine semantics, and validated row counts (878 customers / 164 products / 3,646 orders post–RI alignment).

**Local helper tests** (no Spark):

```bash
python3 src/silver/test_silver_helpers.py
```

## Run Gold Pipeline

Gold is built from four SQL files executed in order by `src/gold/create_gold_tables.py` (`run_gold_pipeline`). Targets:

- `gold.gold_sales_by_product`
- `gold.gold_revenue_by_customer`
- `gold.gold_daily_weekly_trends`
- `gold.gold_customer_segmentation`

See `src/gold/GOLD_LAYER_NOTES.md` for grains, metrics, reconciliation baselines, and notebook execution.

## Run Dashboard & Validation

**Dashboard SQL** (Gold-only consumption): `src/dashboard/dashboard_queries.sql` with usage guide `src/dashboard/DASHBOARD_GUIDE.md`. A Databricks SQL dashboard with three pages (Executive Overview, Product Performance, Customer Insights) has been validated against Gold tables.

**Pipeline validation** (Databricks SQL):

```text
src/validation/pipeline_validation.sql
```

Execute on Databricks Serverless after Bronze → Silver → Gold pipelines. **Result: 26/26 PASS** (documented in `VALIDATION_REPORT.md`).

## Submission Provenance (AI prompts & datasets)

Evaluators can trace AI-assisted development and source data via:

- **`ai-prompts/`** — detailed per-phase prompt history (primary provenance artifact)
- **`data/`** — committed generated datasets (seed **42**; see `DATA_GENERATION_NOTES.md`)
- **`final-ai-usage-summary.md`** — index linking prompts, artifacts, validation, and datasets
- **`VALIDATION_REPORT.md`** — end-to-end validation evidence (**26/26 PASS**)

## Further Reading

- `VALIDATION_REPORT.md` — end-to-end validation evidence
- `src/data_generation/DATA_GENERATION_NOTES.md` — sample data schemas and defects
- `requirements-analysis.md` — scope and requirements
- `design-notes.md` — architecture and design direction
- `data-model.md` — logical entities and relationships
- `data-quality-strategy.md` — quality check definitions
- `tool-workflow.md` — AI-assisted development workflow

## License & Attribution

To be finalized during implementation.
