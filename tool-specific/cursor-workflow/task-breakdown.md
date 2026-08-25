# Task Breakdown

## Project Phase Overview

| Phase | Status |
|-------|--------|
| Phase 1: Foundation | Complete |
| Phase 2: Data generation | Complete |
| Phase 3: Bronze ingestion | Complete (Databricks validated) |
| **Phase 4: Silver** | **Iteration 5 implemented — Databricks validation pending** |
| Phase 5: Gold | Not started |
| Phase 6: Dashboard | Not started |

---

## Phase 4 — Silver (iterative plan)

### Iteration 1: Design & task planning — **COMPLETE**

| # | Task | Status |
|---|------|--------|
| 4.1.1 | Review `data-quality-strategy.md`, `data-model.md`, `DATA_GENERATION_NOTES.md` | Done |
| 4.1.2 | Review validated Bronze context (row counts, preserved defects) | Done |
| 4.1.3 | Define Silver catalog/schema/table naming (`de_c1_coding_evaluation.silver`) | Done |
| 4.1.4 | Propose Silver execution flow and check ordering | Done |
| 4.1.5 | Define quarantine table structure (`silver_quarantine_records`) | Done |
| 4.1.6 | Define DQ summary structure (`silver_dq_summary`) | Done |
| 4.1.7 | Define idempotency strategy (overwrite per run) | Done |
| 4.1.8 | Create design draft `src/silver/SILVER_LAYER_NOTES.md` | Done |
| 4.1.9 | Document Iteration 1 in `ai-prompts/silver-layer.md` | Done |

### Iteration 1b: Resolve open design decisions — **COMPLETE**

| # | Task | Status |
|---|------|--------|
| 4.1b.1 | Finalize completeness — full `data-quality-strategy.md` field lists | Done |
| 4.1b.2 | Finalize single centralized quarantine table | Done |
| 4.1b.3 | Finalize STRING identifiers + numeric-parse validation | Done |
| 4.1b.4 | Finalize D17 quarantine-only (no auto-correction) | Done |
| 4.1b.5 | Finalize date rules (`current_date()`) + `run_timestamp` traceability | Done |
| 4.1b.6 | Confirm execution order unchanged | Done |
| 4.1b.7 | Update `SILVER_LAYER_NOTES.md`, `data-quality-strategy.md`, `spec.md`, `silver-layer.md` | Done |
| 4.1b.8 | **Developer approval before Iteration 2** | **Pending** |

---

### Iteration 2: Type standardization, completeness, uniqueness — **COMPLETE (local validation)**

| # | Task | Status |
|---|------|--------|
| 4.2.1 | Create `silver_common.py` (config, Bronze read, cast helpers, Spark session) | Done |
| 4.2.2 | Implement safe STRING trim / normalization | Done |
| 4.2.3 | Implement typed column parsing (DATE, DECIMAL, INT) with failure flags | Done |
| 4.2.4 | Implement `01_quality_completeness.py` | Done |
| 4.2.5 | Implement `02_quality_uniqueness.py` (deterministic duplicate handling) | Done |
| 4.2.6 | Implement `03_quality_type_validation.py` | Done |
| 4.2.7 | Local `py_compile` validation | Done |
| 4.2.8 | Local helper unit tests (`test_silver_helpers.py`) | Done |
| 4.2.9 | Document Iteration 2 in `ai-prompts/silver-layer.md` | Done |
| 4.2.10 | Databricks module validation | Done |
| 4.2.11 | **Developer approval before Iteration 3** | Done |

---

### Iteration 3: Referential integrity, business logic — **ACCEPTED**

| # | Task | Status |
|---|------|--------|
| 4.3.1 | Establish canonical valid parent records (customers, products) | Done |
| 4.3.2 | Implement `04_quality_referential_integrity.py` (anti-join orphans) | Done |
| 4.3.3 | Implement `05_quality_business_logic.py` (dates, qty, prices, segment, catalog match) | Done |
| 4.3.4 | Local `py_compile` + helper tests | Done |
| 4.3.5 | Validate logic against Phase 2 defect matrix (Databricks Serverless) | Done |
| 4.3.6 | Document Iteration 3 in `ai-prompts/silver-layer.md` | Done |
| 4.3.7 | **Developer approval before Iteration 4** | **Pending** |

---

### Iteration 4: Quarantine + DQ summary — **ACCEPTED**

| # | Task | Status |
|---|------|--------|
| 4.4.1 | Implement quarantine writer (`silver_quarantine_records`) | Done |
| 4.4.2 | Support multiple failure reasons per record where practical | Done |
| 4.4.3 | Implement DQ summary writer (`silver_dq_summary`) | Done |
| 4.4.4 | Ensure all five DQ categories appear in summary | Done |
| 4.4.5 | Local validation of summary/quarantine schema logic | Done |
| 4.4.6 | Refine based on inspection | Done |
| 4.4.7 | Document Iteration 4 in `ai-prompts/silver-layer.md` | Done |
| 4.4.8 | Databricks Serverless validation (tables, counts, idempotency) | Done |
| 4.4.9 | **Developer approval before Iteration 5** | **Pending** |

---

### Iteration 5: Orchestration + Databricks validation — **IMPLEMENTED (Databricks validation pending)**

| # | Task | Status |
|---|------|--------|
| 4.5.1 | Implement `create_silver_tables.py` orchestration | Done |
| 4.5.2 | `CREATE SCHEMA IF NOT EXISTS de_c1_coding_evaluation.silver` | Done |
| 4.5.3 | Write `silver_customers`, `silver_products`, `silver_orders` | Done |
| 4.5.4 | Run full pipeline in Databricks | **Pending** |
| 4.5.5 | Verify Silver schema/types | **Pending** |
| 4.5.6 | Verify row counts explainable vs Bronze | **Pending** |
| 4.5.7 | Verify DQ summary exists and covers all 5 categories | **Pending** |
| 4.5.8 | Verify quarantine counts align with known defects | **Pending** |
| 4.5.9 | Verify rerun does not accumulate duplicates | **Pending** |
| 4.5.10 | Update `data-quality-strategy.md`, `design-notes.md`, `README.md`, `requirements-analysis.md`, `tool-workflow.md` | **Deferred** (post-Databricks acceptance) |
| 4.5.11 | Finalize `SILVER_LAYER_NOTES.md` with actual validation results | Done (pending Databricks evidence) |
| 4.5.12 | Document Iteration 5 + acceptance in `ai-prompts/silver-layer.md` | Done |
| 4.5.13 | **Developer approval / ACCEPTED** | **Pending** |

---

## Phase 3 — Bronze (complete)

| # | Task | Status |
|---|------|--------|
| 3.1–3.11 | Bronze implementation + Databricks validation | Done |

---

## Phase 2 — Data Generation (complete)

See git history for Phase 2 subtasks.
