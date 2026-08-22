# Requirement Analysis

## Problem Statement

Build an **e-commerce-style sales analytics data pipeline** on Databricks using the **medallion architecture**. The pipeline will ingest generated sample data for **customers**, **orders**, and **products**, land it in Bronze, cleanse and validate it in Silver (with explicit data quality checks), aggregate it into analytical Gold datasets, and expose results for dashboard-style analytics.

The problem is not only to move data between layers, but to demonstrate **coherent data engineering practice**: consistent modeling, traceable quality rules, incremental delivery, and documented AI-assisted development.

**Current status:** Phase 2 (data generation) and Phase 3 (Bronze ingestion) are **complete**. Silver and later layers are **not started**.

---

## Functional Requirements

### Confirmed (project scope)

- Implement medallion flow: Raw/Sample → Bronze → Silver → Gold → Analytics/Dashboard
- Organize code under `src/data_generation`, `src/bronze`, `src/silver`, `src/gold`, `src/dashboard`
- Generate sample CSVs in `data/` for customers, orders, and products
- Bronze: per-entity ingestion scripts plus orchestration entry point; minimal transformation
- Silver: cleansing, conformed tables, and five quality check categories:
  - Completeness
  - Uniqueness
  - Type validation
  - Referential integrity
  - Business logic
- Gold: analytical SQL datasets (sales by product, revenue by customer, daily/weekly trends, customer segmentation)
- Dashboard: queries and usage guide under `src/dashboard/`
- Database artifacts under `database/` (schema, setup notes)
- Documentation and `ai-prompts/` updated with each implementation phase
- Work proceeds **incrementally**; do not implement all layers at once

### To be delivered per phase

| Phase | Deliverables | Status |
|-------|--------------|--------|
| Data generation | `generate_sample_data.py`, `DATA_GENERATION_NOTES.md`, `ai-prompts/data-generation.md`, `data/*.csv` | **Complete** |
| Bronze | Ingest scripts, `ingest_all.py`, `BRONZE_LAYER_NOTES.md`, `ai-prompts/bronze-layer.md` | **Complete** |
| Silver | Quality modules, `create_silver_tables.py`, updated `data-quality-strategy.md` | Not started |
| Gold | SQL files, `create_gold_tables.py`, `ai-prompts/gold-layer.md` | Not started |
| Dashboard | `dashboard_queries.sql`, `DASHBOARD_GUIDE.md` | Not started |
| Closure | `debugging-notes.md`, `reflection.md`, `final-ai-usage-summary.md` | Not started |

---

## Non-Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| NFR-01 | **Consistency** — Same entities and relationships across data, Bronze, Silver, Gold, and dashboard | Required |
| NFR-02 | **Maintainability** — Readable, modular Python/SQL; layer separation | Required |
| NFR-03 | **Security** — No hardcoded credentials, tokens, or secrets in repo | Required |
| NFR-04 | **Traceability** — AI prompts and design decisions preserved in `ai-prompts/` and docs | Required |
| NFR-05 | **Documentation** — Docs updated alongside implementation, not deferred to project end | Required |
| NFR-06 | **Databricks alignment** — Lakehouse/medallion patterns (Delta, PySpark where applicable) | Planned |
| NFR-07 | **Reproducibility** — Pipeline runnable from documented steps in target environment | Data generation reproducible via `--seed` (verified) |
| NFR-08 | **Performance / scale** — Appropriate for assessment/demo dataset sizes | Default: 1,006 customers, 206 products, 5,163 order lines |

---

## Assumptions

- Sample data is **generated locally or in Databricks**, not sourced from production systems
- Domain is simplified retail/e-commerce: customers place orders that reference products
- **Delta Lake** is the expected table format on Databricks (to be confirmed during implementation)
- Single-currency, batch processing unless scope is explicitly expanded later
- Developer reviews all AI-generated code and documentation before acceptance
- Repository root (`DE_C1_Coding_Evaluation`) is the project root (no nested project folder)

---

## Edge Cases

_Validated during Phase 2 data generation; Silver handling TBD._

| Edge case | Sample data evidence | Expected Silver handling |
|-----------|---------------------|--------------------------|
| NULL or empty required fields | D01, D02, D07 | Completeness → quarantine |
| Duplicate business keys | D03, D08, D16 | Uniqueness → quarantine |
| Invalid data types / formats | D04, D05, D09, D13 | Type validation → reject/quarantine |
| Orphan FK on orders | D11, D12 | Referential integrity → quarantine |
| Invalid business values | D06, D10, D14, D15, D17 | Business logic → quarantine |
| Re-running ingestion idempotently | Bronze design TBD | — |
| Partial pipeline failure mid-layer | Bronze design TBD | — |

See defect matrix in `src/data_generation/DATA_GENERATION_NOTES.md`.

---

## Clarifications Needed

| # | Topic | Status |
|---|-------|--------|
| 1 | Databricks environment | Open — workspace; Bronze uses `bronze` schema by default |
| 2 | Entity schema | **Resolved (Phase 2)** — see `data-model.md` |
| 3 | Order granularity | **Resolved (Phase 2)** — line-item model in `orders.csv` |
| 4 | Sample data volume | **Resolved (Phase 2)** — defaults in `DATA_GENERATION_NOTES.md` |
| 5 | Intentional quality defects | **Resolved (Phase 2)** — 17 defect types, 328 injections |
| 6 | DQ thresholds | Open — target % documented; Silver implementation TBD |
| 7 | Failed record handling | Open — quarantine design at Silver phase |
| 8 | Gold metric definitions | Open — formulas/grains at Gold phase |
| 9 | Dashboard target | Open |
| 10 | Orchestration | Open — notebooks, jobs, bundles |

---

## Traceability

| Document | Role |
|----------|------|
| `design-notes.md` | Architecture and layer design |
| `data-model.md` | Logical entities and relationships |
| `data-quality-strategy.md` | Quality check definitions and thresholds |
| `tool-workflow.md` | AI-assisted development process |

## Out of Scope (Unless Added Later)

- Production SLA, monitoring, and alerting
- Real-time streaming ingestion
- Advanced PII governance beyond basic secure-coding practices
