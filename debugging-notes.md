# Debugging Notes

Concise chronological log of non-trivial debugging during `DE_C1_Coding_Evaluation`. **Detailed prompt history:** `ai-prompts/debugging.md` and phase-specific `ai-prompts/<layer>.md` files.

---

## 1. Bronze — local PySpark import (Phase 3)

| Field | Detail |
|-------|--------|
| **Issue** | `--dry-run` failed without PySpark installed |
| **Symptom** | Import error on `bronze_common.py` top-level PySpark imports |
| **Investigation** | Dry-run path should not require Spark |
| **Resolution** | Lazy PySpark imports inside Spark-dependent functions |
| **Files** | `src/bronze/bronze_common.py` |
| **Validation** | `py_compile`, `--dry-run` PASS |

---

## 2. Bronze — Databricks `!python` / Spark Connect (Phase 3)

| Field | Detail |
|-------|--------|
| **Issue** | Bronze ingest via `!python ingest_all.py` in notebook |
| **Symptom** | `PySparkValueError: [INVALID_CONNECT_URL]` |
| **Investigation** | Subprocess lacks notebook `spark` session |
| **Resolution** | `resolve_spark()`, `run_ingestion(..., spark=spark)`; notebook guidance |
| **Files** | `bronze_common.py`, `ingest_all.py`, `BRONZE_LAYER_NOTES.md` |
| **Validation** | Databricks row counts 1,006 / 206 / 5,163; defects preserved |
| **Prompt** | `ai-prompts/bronze-layer.md` Prompt 2 |

---

## 3. Silver — Databricks Serverless compatibility (Phase 4, Iteration 2)

| Field | Detail |
|-------|--------|
| **Issue** | Multiple Serverless API incompatibilities |
| **Symptoms** | `rdd.isEmpty()` blocked; array+explode false completeness; ANSI `to_date` throws; `F.try_cast` missing |
| **Resolution** | DataFrame-only patterns; `try_to_date`; `when`+`rlike` casts; partitioned windows |
| **Files** | `src/silver/*.py` |
| **Validation** | Completeness/uniqueness/type checks PASS with exact defect counts |
| **Prompt** | `ai-prompts/silver-layer.md` Iteration 2 |

---

## 4. Silver — RI parent key alignment (post–Gold validation)

| Field | Detail |
|-------|--------|
| **Issue** | Curated `silver_orders` FKs not aligned with curated dimension tables |
| **Symptom** | Gold validation exposed orphan FK diagnostics |
| **Investigation** | RI used `canonical_valid_filter()` parents; curated tables used broader `filter_valid_rows()` |
| **Resolution** | `curated_eligible_parent_keys_df()`; DQ order 05 before 04; `SERVERLESS_COMPAT_VERSION = 10` |
| **Files** | `silver_common.py`, `04_quality_referential_integrity.py`, `06_write_dq_results.py`, `create_silver_tables.py` |
| **Validation** | 0 orphan FKs; orders 3,646; Gold revenue 2,708,411.08 reconciles |
| **Prompt** | `verbatim-recoveries.md` key `silver-ri-alignment` |

---

## 5. Gold — notebook module loading (Iteration 6)

| Field | Detail |
|-------|--------|
| **Issue** | `importlib` load of `create_gold_tables.py` in notebook |
| **Symptom** | `AttributeError` without `sys.modules` registration |
| **Resolution** | Register module before `exec_module` (documented cells) |
| **Validation** | `run_gold_pipeline`, `validate_gold_pipeline`, idempotency PASS |

---

## 6. Dashboard — `order_count` column confusion (Phase 6)

| Field | Detail |
|-------|--------|
| **Issue** | Databricks error `order_count` on `gold_sales_by_product` |
| **Investigation** | Repo SQL had no such reference; `order_count` valid only on trends table |
| **Resolution** | Schema contract comments in SQL + guide (no logic change) |
| **Prompt** | `ai-prompts/dashboard.md` Iteration 2 |

---

## 7. Validation SQL — first Databricks run (2026-08-30)

| Field | Detail |
|-------|--------|
| **Issue** | 3 of 26 checks failed (SQL syntax/schema) |
| **Symptoms** | `DESCRIBE` in subquery; `entity_name` vs `table_name` |
| **Resolution** | `information_schema.columns`; `table_name` filter |
| **Files** | `src/validation/pipeline_validation.sql`, `VALIDATION_REPORT.md` |
| **Validation** | **26/26 PASS** on re-run |
| **Prompt** | `ai-prompts/validation.md` Prompt 2 (operator re-run — prompt text not preserved) |

---

## 8. Data generation — defect count correction (Phase 2)

| Field | Detail |
|-------|--------|
| **Issue** | Duplicate defect count mismatch (3 vs 6) |
| **Resolution** | Fixed generator + argparse typo |
| **Validation** | MD5 reproducibility seed 42; defect spot checks |
| **Prompt** | `ai-prompts/data-generation.md` |
