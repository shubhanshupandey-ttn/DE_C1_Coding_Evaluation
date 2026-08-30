# Candidate Information

**Name:** Shubhanshu Pandey  
**Role:** SSE  
**Primary Technology Stack:** Python / PySpark, SQL, Databricks  
**Primary AI Tool Used:** Cursor  
**Project Option Selected:** Data Pipeline (Medallion Architecture)  
**Assessment Start Date:** 20/08/2026  
**Submission Date:** 31/08/2026

> **Note:** Do not include secrets, API tokens, or connection credentials in this file.

---

## Tools & Environment

| Item | Value |
|------|-------|
| Databricks (development / workspace) | Community Edition (initial workspace reference) |
| Databricks (final validation) | **Serverless** — pipeline validation **26/26 PASS** (`VALIDATION_REPORT.md`, 2026-08-30) |
| Languages | Python, PySpark, SQL |
| Libraries used | PySpark, Delta Lake |
| AI Tool | Cursor |
| Repository | `DE_C1_Coding_Evaluation` |
| Architecture | Medallion (Bronze → Silver → Gold → Dashboard) |

## Setup Summary

Quick reference — full run instructions in `README.md`.

| Step | Status |
|------|--------|
| Clone repository | Available |
| Configure Databricks workspace | Unity Catalog `de_c1_coding_evaluation` (validated) |
| Generate sample data | **Complete** — `data/*.csv` (seed 42) |
| Run Bronze ingestion | **Complete** (Databricks validated) |
| Run Silver + quality checks | **Complete** (Databricks validated) |
| Build Gold tables | **Complete** (Databricks validated) |
| Run dashboard queries | **Complete** — 3-page Databricks SQL dashboard |
| Pipeline validation | **Complete** — 26/26 PASS |

See `README.md` and `final-ai-usage-summary.md` for run instructions and provenance.

## Optional Context for Reviewer

- Incremental delivery (Phases 2–6) with AI-assisted development; prompt history in `ai-prompts/`.
- Generated datasets (`data/*.csv`, seed 42) are committed and traced through Bronze → validation.
- `database/` schema/setup artifacts **implemented** (`schema.sql`, seed and setup notes); external RDBMS deployment **not claimed**.
- Dashboard: 3 Databricks SQL pages (Executive Overview, Product Performance, Customer Insights); Gold-only consumption.
