# Databricks Medallion Pipeline

A practical data engineering project demonstrating the **medallion architecture** on Databricks, built incrementally with AI-assisted development and accompanying documentation.

## Project Purpose

This repository implements an end-to-end analytics data pipeline for a small retail-style domain centered on **customers**, **orders**, and **products**. The goal is to show realistic data engineering practices—not placeholder scaffolding—including:

- Sample/raw data generation
- Bronze-layer ingestion
- Silver-layer cleansing, transformation, and data quality
- Gold-layer analytical datasets
- Dashboard-oriented queries and guidance

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
```

Supporting assets:

- **`database/`** — schema and setup notes for the underlying data store context
- **`ai-prompts/`** — preserved prompts from AI-assisted implementation phases
- **Root documentation** — requirements, design, data model, and quality strategy

Data quality is a first-class concern in the Silver layer, with explicit checks for completeness, uniqueness, type validation, referential integrity, and business logic.

## Planned Repository Structure

```
.
├── README.md
├── candidate-info.md
├── tool-workflow.md
├── requirements-analysis.md
├── design-notes.md
├── data-model.md
├── data-quality-strategy.md
├── debugging-notes.md
├── reflection.md
├── final-ai-usage-summary.md
│
├── src/
│   ├── data_generation/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── dashboard/
│
├── data/
├── database/
└── ai-prompts/
```

Detailed file names for each layer are defined in the project plan and will be created during their respective implementation phases.

## Technology & Tooling Context

| Area | Planned approach |
|------|------------------|
| Platform | Databricks (lakehouse / medallion pattern) |
| Languages | Python (ingestion, transformations, orchestration helpers), SQL (Gold analytics) |
| Source data | Generated sample CSV files in `data/` |
| Version control | Git (GitHub) |
| Development | Incremental phases with documentation and prompt artifacts alongside code |

Specific Databricks configuration: Bronze defaults to schema `bronze` and tables `bronze_customers`, `bronze_products`, `bronze_orders`. Optional `--catalog` for Unity Catalog. Cluster/job setup remains environment-specific.

## Development Approach

Work proceeds in **incremental phases**. Each phase delivers:

1. **Implementation** (code and/or data as applicable)
2. **Documentation** (updated or new project docs)
3. **Prompt artifact** (recorded in the relevant `ai-prompts/` file)

Foundation documentation (requirements, design, data model, quality strategy) is created before pipeline code so later phases remain internally consistent. Doc layouts follow the **submission templates** (candidate info, requirement analysis, design notes, DQ strategy, AI prompt history, reflection) as a minimum structure.

AI tools may assist with drafting and implementation, but all output is subject to developer review, validation, and revision. The `ai-prompts/` directory preserves the development trail.

## Current Project Status

| Phase | Status |
|-------|--------|
| Repository inspection | Complete |
| Phase 1: Project foundation | Complete |
| **Phase 2: Data generation** | **Complete** |
| **Phase 3: Bronze ingestion** | **Complete** (local validation; Databricks run pending) |
| Silver + data quality | Not started |
| Gold analytics | Not started |
| Dashboard | Not started |
| Database setup artifacts | Not started |

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

**Databricks cluster** (requires PySpark + Delta):

```bash
python src/bronze/ingest_all.py --data-dir /path/to/data
```

See `src/bronze/BRONZE_LAYER_NOTES.md` for table names, design decisions, and per-entity scripts.

Silver and later layers are **not implemented yet**.

- `src/data_generation/DATA_GENERATION_NOTES.md` — sample data schemas and defects
- `requirements-analysis.md` — scope and requirements
- `design-notes.md` — architecture and design direction
- `data-model.md` — logical entities and relationships
- `data-quality-strategy.md` — planned quality framework
- `tool-workflow.md` — AI-assisted development workflow

## License & Attribution

To be finalized during implementation.
