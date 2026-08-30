# AI Prompts — Debugging (Consolidated)

Cross-reference artifact for debugging iterations across the project. **Not every item below originated as a standalone debugging prompt** — some were documented inside phase-specific `ai-prompts/<layer>.md` files during implementation.

**Numbered prompt reference:** Prompts **01–36** in phase `ai-prompts/*.md` files (index at top of `documentation.md`).

---

## Debug 1 — Bronze local dry-run without PySpark

**TYPE:** Correction (discovered during local validation)

**RELATED PROMPT:** Prompt 05 (`bronze-layer.md`)

**SOURCE:** `ai-prompts/bronze-layer.md` § Iteration / Refinement Evidence (no standalone PROMPT SENT)

**SYMPTOM:** `ingest_all.py --dry-run` failed when PySpark was not installed locally.

**INVESTIGATION:** Top-level PySpark imports in `bronze_common.py` executed at import time.

**RESOLUTION:** Moved PySpark imports inside Spark-dependent functions (lazy import).

**ARTIFACTS MODIFIED:** `src/bronze/bronze_common.py`

**VALIDATION:** `py_compile` + `--dry-run` PASS (`bronze-layer.md`)

**FINAL DECISION:** ACCEPTED

---

## Debug 2 — Bronze dry-run indentation error

**TYPE:** Correction (draft fix before validation)

**RELATED PROMPT:** Prompt 05 (`bronze-layer.md`)

**SOURCE:** `ai-prompts/bronze-layer.md` § Iteration / Refinement Evidence

**SYMPTOM:** Indentation error in dry-run print logic.

**RESOLUTION:** Fixed before local validation completed.

**FINAL DECISION:** ACCEPTED

---

## Debug 3 — Databricks `!python` / Spark Connect (`INVALID_CONNECT_URL`)

**TYPE:** Debugging

**RELATED PROMPT:** **Prompt 06** (`bronze-layer.md`)

**PROMPT SENT (excerpt — full text in Prompt 06):**

> User ran Bronze ingest on Databricks using `!python .../ingest_all.py` with catalog `de_c1_coding_evaluation`, schema `bronze`, write mode `overwrite`.
>
> Error: `PySparkValueError: [INVALID_CONNECT_URL] Invalid URL for Spark Connect ... must start with 'sc://'`
>
> Fix Bronze scripts to work in Databricks notebooks without using `!python` subprocess.

**SYMPTOM:** Subprocess Python could not attach to notebook Spark session on Databricks Serverless / Spark Connect.

**RESOLUTION:** Added `resolve_spark()`, `notebook_spark_if_defined()`, `run_ingestion(config, spark=spark)`; documented notebook execution in `BRONZE_LAYER_NOTES.md`.

**ARTIFACTS MODIFIED:** `src/bronze/bronze_common.py`, `src/bronze/ingest_all.py`, `BRONZE_LAYER_NOTES.md`

**VALIDATION:** Databricks ingest 1,006 / 206 / 5,163 rows; defect preservation PASS (`bronze-layer.md`)

**FINAL DECISION:** ACCEPTED

---

## Debug 4 — Silver Serverless: `df.rdd.isEmpty()`

**TYPE:** Debugging / compatibility

**RELATED PROMPT:** Prompt 09 (`silver-layer.md`)

**SOURCE:** `ai-prompts/silver-layer.md` — Prompt 09 § Serverless compatibility

**SYMPTOM:** RDD API blocked on Databricks Serverless.

**RESOLUTION:** Removed `rdd.isEmpty()`; use DataFrame `filter().select()` + `unionByName()`.

**ARTIFACTS MODIFIED:** Silver DQ modules (`silver-layer.md`)

**VALIDATION:** Completeness / uniqueness / type validation PASS on Serverless

**FINAL DECISION:** ACCEPTED

---

## Debug 5 — Silver Serverless: array+explode false completeness inflation

**TYPE:** Debugging

**RELATED PROMPT:** Prompt 09 (`silver-layer.md`)

**SOURCE:** `ai-prompts/silver-layer.md` — Prompt 09

**SYMPTOM:** Failure builder v3 produced false 100% completeness failures (~7× row inflation) on Spark Connect.

**RESOLUTION:** Reverted array+explode failure builder.

**FINAL DECISION:** ACCEPTED

---

## Debug 6 — Silver Serverless: ANSI `to_date` throws on invalid strings

**TYPE:** Debugging

**RELATED PROMPT:** Prompt 09 (`silver-layer.md`)

**SOURCE:** `ai-prompts/silver-layer.md` — Prompt 09

**SYMPTOM:** `to_date('NOT-A-DATE')` throws under ANSI SQL.

**RESOLUTION:** Use SQL `try_to_date` via `F.expr` (NULL on invalid).

**FINAL DECISION:** ACCEPTED

---

## Debug 7 — Silver Serverless: `F.try_cast` unavailable

**TYPE:** Debugging

**RELATED PROMPT:** Prompt 09 (`silver-layer.md`)

**SOURCE:** `ai-prompts/silver-layer.md` — Prompt 09

**SYMPTOM:** `F.try_cast` not available in notebook PySpark bindings.

**RESOLUTION:** Int/decimal parsing uses `when` + `rlike` + `.cast()` on matched patterns only.

**FINAL DECISION:** ACCEPTED

---

## Debug 8 — Silver `datetime.utcnow()` deprecation

**TYPE:** Correction

**RELATED PROMPT:** Prompt 11 (`silver-layer.md`)

**SOURCE:** `ai-prompts/silver-layer.md` — Prompt 11

**SYMPTOM:** Deprecation warning in Databricks notebook.

**RESOLUTION:** `datetime.now(timezone.utc)` in `silver_common.py`.

**FINAL DECISION:** ACCEPTED

---

## Debug 9 — Silver RI alignment (curated parent keys)

**TYPE:** Correction (architectural)

**RELATED PROMPT:** **Prompt 13** (`silver-layer.md` — full **PROMPT SENT**)

**SYMPTOM:** Gold validation exposed order FKs in `silver_orders` referencing customers/products not present in curated dimension tables (RI parents used `canonical_valid_filter()` without uniqueness/business-logic gates).

**RESOLUTION:** `curated_eligible_parent_keys_df()`, shared `filter_valid_rows()`, DQ order 01→02→03→**05**→**04**; `SERVERLESS_COMPAT_VERSION = 10`.

**ARTIFACTS MODIFIED:** `silver_common.py`, `04_quality_referential_integrity.py`, `06_write_dq_results.py`, `create_silver_tables.py`

**VALIDATION:** 0 orphan FK diagnostics; `silver_orders` = 3,646; Gold revenue reconciles 2,708,411.08 (`silver-layer.md`, `GOLD_LAYER_NOTES.md`)

**FINAL DECISION:** ACCEPTED

---

## Debug 10 — Gold notebook `importlib` module registration

**TYPE:** Debugging (Databricks notebook pattern)

**RELATED PROMPT:** Prompt 20 (`gold-layer.md`); notebook cells in `silver-layer.md` Prompt 13

**SOURCE:** `ai-prompts/gold-layer.md` Prompt 20; notebook cells in `silver-layer.md` / `GOLD_LAYER_NOTES.md`

**SYMPTOM:** `AttributeError` when loading `create_gold_tables.py` via `importlib` without pre-registering in `sys.modules`.

**RESOLUTION:** Register module in `sys.modules` before `exec_module` (documented notebook cells).

**VALIDATION:** Gold pipeline + `validate_gold_pipeline()` + idempotency PASS

**FINAL DECISION:** ACCEPTED

---

## Debug 11 — Dashboard `order_count` on `gold_sales_by_product`

**TYPE:** Validation / schema clarification

**RELATED PROMPT:** **Prompt 22** (`dashboard.md`)

**SYMPTOM:** Databricks reported `UNRESOLVED_COLUMN: order_count` against `gold_sales_by_product`.

**INVESTIGATION:** Repository product queries did **not** reference `order_count` on `gold_sales_by_product`; valid `order_count` only on `gold_daily_weekly_trends`.

**RESOLUTION:** Defensive schema-contract comments in `dashboard_queries.sql` and `DASHBOARD_GUIDE.md` (no Gold/Silver changes).

**FINAL DECISION:** ACCEPTED (documentation hardening)

---

## Debug 12 — Validation SQL: `DESCRIBE TABLE` in subquery

**TYPE:** Validation correction

**RELATED PROMPT:** Prompt 24 follow-up (`documentation.md`; details in `validation.md` index)

**SYMPTOM:** `bronze_customers_columns` — `PARSE_SYNTAX_ERROR` on Databricks SQL.

**RESOLUTION:** Replaced with `system.information_schema.columns`.

**ARTIFACTS MODIFIED:** `src/validation/pipeline_validation.sql`

**VALIDATION:** Re-run PASS (check 2 / query 27)

**FINAL DECISION:** ACCEPTED

---

## Debug 13 — Validation SQL: `entity_name` vs `table_name` in `silver_dq_summary`

**TYPE:** Validation correction

**RELATED PROMPT:** Prompt 24 follow-up (`documentation.md`; details in `validation.md` index)

**SYMPTOM:** `silver_ri_orders_rows_failed` and `silver_completeness_customers_rows_failed` — column `entity_name` not found.

**INVESTIGATION:** Actual schema in `06_write_dq_results.py` uses **`table_name`**.

**RESOLUTION:** Updated validation queries to filter on `table_name`.

**VALIDATION:** Re-run PASS (queries 28–29)

**FINAL DECISION:** ACCEPTED

---

## Debug 14 — Data generation duplicate defect count

**TYPE:** Correction (Phase 2 validation)

**RELATED PROMPT:** Prompt 04 (`data-generation.md`)

**SOURCE:** `ai-prompts/data-generation.md`

**SYMPTOM:** Initial duplicate defect count reported 3 instead of 6.

**RESOLUTION:** Fixed `DEFECT_COUNTS` / generator logic; argparse indentation typo fixed.

**VALIDATION:** Row counts and defect spot checks PASS

**FINAL DECISION:** ACCEPTED

---

## Items without standalone debugging prompts

| Issue | Documented in |
|-------|----------------|
| Silver global window warning (uniqueness) | `silver-layer.md` Prompt 09 |
| Silver `parse_int_string` accidental removal (Prompt 10) | `silver-layer.md` Prompt 10 |
| Quarantine vs summary metric semantics | `silver-layer.md` Prompts 11–12 |
