# Requirement Analysis

## Problem Statement

Build an **e-commerce-style sales analytics data pipeline** on Databricks using the **medallion architecture**. The pipeline will ingest generated sample data for **customers**, **orders**, and **products**, land it in Bronze, cleanse and validate it in Silver (with explicit data quality checks), aggregate it into analytical Gold datasets, and expose results for dashboard-style analytics.

The problem is not only to move data between layers, but to demonstrate **coherent data engineering practice**: consistent modeling, traceable quality rules, incremental delivery, and documented AI-assisted development.

**Current status:** Phases 2–6 (data generation through dashboard) are **complete and Databricks-validated**. End-to-end pipeline validation (`src/validation/pipeline_validation.sql`) is **complete — 26/26 PASS** on Databricks Serverless. Submission provenance artifacts (`ai-prompts/`, `data/`, `final-ai-usage-summary.md`, `reflection.md`, `debugging-notes.md`) are **complete**. Database schema/setup artifacts (`database/`) are **implemented**; external relational-database deployment is **not claimed**.

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
| Bronze | Ingest scripts, `ingest_all.py`, `BRONZE_LAYER_NOTES.md`, `ai-prompts/bronze-layer.md` | **Complete** (Databricks validated) |
| Silver | Quality modules (`01`–`05`), quarantine/DQ summary (`06`), `create_silver_tables.py`, `SILVER_LAYER_NOTES.md`, `ai-prompts/silver-layer.md` | **Complete** (Databricks validated) |
| Gold | SQL files (`01`–`04`), `create_gold_tables.py`, `GOLD_LAYER_NOTES.md`, `ai-prompts/gold-layer.md` | **Complete** (Databricks validated) |
| Dashboard | `dashboard_queries.sql`, `DASHBOARD_GUIDE.md`, `ai-prompts/dashboard.md`; Databricks SQL dashboard (3 pages) | **Complete** (Databricks validated) |
| Pipeline validation | `src/validation/pipeline_validation.sql`, `VALIDATION_REPORT.md`, `ai-prompts/validation.md` | **Complete** (26/26 PASS on Databricks Serverless) |
| Submission provenance | `ai-prompts/` (numbered prompts 01–36 in phase files), `data/*.csv`, `final-ai-usage-summary.md` | **Complete** |
| Database | `database/` schema and setup notes | **Complete** (schema/setup artifacts; no external RDBMS deployment) |
| Closure | `debugging-notes.md`, `reflection.md`, `final-ai-usage-summary.md` | **Complete** |

---

## Non-Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| NFR-01 | **Consistency** — Same entities and relationships across data, Bronze, Silver, Gold, and dashboard | **Met** — validated via `pipeline_validation.sql` reconciliation checks |
| NFR-02 | **Maintainability** — Readable, modular Python/SQL; layer separation | **Met** |
| NFR-03 | **Security** — No hardcoded credentials, tokens, or secrets in repo | **Met** |
| NFR-04 | **Traceability** — AI prompts and design decisions preserved in `ai-prompts/` and docs | **Met** (per-phase prompt artifacts) |
| NFR-05 | **Documentation** — Docs updated alongside implementation, not deferred to project end | **Mostly met** — layer notes and validation report complete; some root docs updated at project close |
| NFR-06 | **Databricks alignment** — Lakehouse/medallion patterns (Delta, PySpark where applicable) | **Met** — Unity Catalog `de_c1_coding_evaluation`; Delta tables; Serverless validated |
| NFR-07 | **Reproducibility** — Pipeline runnable from documented steps in target environment | **Met** — data generation via `--seed`; layer orchestration documented in `*_LAYER_NOTES.md` |
| NFR-08 | **Performance / scale** — Appropriate for assessment/demo dataset sizes | **Met** — default: 1,006 customers, 206 products, 5,163 order lines |

---

## Assumptions

- Sample data is **generated locally or in Databricks**, not sourced from production systems
- Domain is simplified retail/e-commerce: customers place orders that reference products
- **Delta Lake** is the table format on Databricks (implemented)
- Single-currency, batch processing unless scope is explicitly expanded later
- Developer reviews all AI-generated code and documentation before acceptance
- Repository root (`DE_C1_Coding_Evaluation`) is the project root (no nested project folder)

---

## Edge Cases

_Validated during Phase 2 data generation; Silver handling implemented and Databricks-validated._

| Edge case | Sample data evidence | Silver handling |
|-----------|---------------------|-----------------|
| NULL or empty required fields | D01, D02, D07 | Completeness → quarantine |
| Duplicate business keys | D03, D08, D16 | Uniqueness → quarantine |
| Invalid data types / formats | D04, D05, D09, D13 | Type validation → quarantine |
| Orphan FK on orders | D11, D12 | Referential integrity → quarantine (detected; curated orders exclude orphans post–RI alignment) |
| Invalid business values | D06, D10, D14, D15, D17 | Business logic → quarantine |
| Re-running ingestion idempotently | Bronze/Silver/Gold | Overwrite per run (documented in layer notes) |
| Partial pipeline failure mid-layer | — | Not formally orchestrated as a workflow engine; per-layer scripts are idempotent on re-run |

See defect matrix in `src/data_generation/DATA_GENERATION_NOTES.md` and DQ evidence in `src/silver/SILVER_LAYER_NOTES.md`.

---

## Clarifications Needed

| # | Topic | Status |
|---|-------|--------|
| 1 | Databricks environment | **Resolved** — Unity Catalog `de_c1_coding_evaluation`; Serverless validated |
| 2 | Entity schema | **Resolved (Phase 2)** — see `data-model.md` |
| 3 | Order granularity | **Resolved (Phase 2)** — line-item model in `orders.csv` |
| 4 | Sample data volume | **Resolved (Phase 2)** — defaults in `DATA_GENERATION_NOTES.md` |
| 5 | Intentional quality defects | **Resolved (Phase 2)** — 17 defect types, 328 injections |
| 6 | DQ thresholds | **Resolved (Phase 4)** — implemented in Silver; summary in `silver_dq_summary` |
| 7 | Failed record handling | **Resolved (Phase 4)** — `silver_quarantine_records` + `silver_dq_summary` |
| 8 | Gold metric definitions | **Resolved (Phase 5)** — frozen in `GOLD_LAYER_NOTES.md` |
| 9 | Dashboard target | **Resolved (Phase 6)** — Databricks SQL dashboard; Gold-only `dashboard_queries.sql` |
| 10 | Orchestration | **Partially resolved** — per-layer Python orchestrators (`ingest_all.py`, `create_silver_tables.py`, `create_gold_tables.py`); no Databricks Jobs/bundles artifact |

---

## Traceability

| Document | Role |
|----------|------|
| `design-notes.md` | Architecture and layer design |
| `data-model.md` | Logical entities and relationships |
| `data-quality-strategy.md` | Quality check definitions and thresholds |
| `tool-workflow.md` | AI-assisted development process |
| `VALIDATION_REPORT.md` | End-to-end Databricks validation evidence (26/26 PASS) |

## Out of Scope (Unless Added Later)

- Production SLA, monitoring, and alerting
- Real-time streaming ingestion
- Advanced PII governance beyond basic secure-coding practices
