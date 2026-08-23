# AI Prompts — Bronze Layer

Evidence artifact for Phase 3 Bronze implementation (Cursor-assisted development).

---

## Phase 3 Implementation Context

**Scope:** Ingest Phase 2 CSVs into Bronze Delta tables only. No Silver, Gold, or Dashboard.

**Files implemented:**

| File | Role |
|------|------|
| `src/bronze/bronze_common.py` | Shared config, STRING-schema CSV read, metadata, Delta write, dry-run validation |
| `src/bronze/01_ingest_customers.py` | Ingest `customers.csv` |
| `src/bronze/02_ingest_orders.py` | Ingest `orders.csv` (line items) |
| `src/bronze/03_ingest_products.py` | Ingest `products.csv` |
| `src/bronze/ingest_all.py` | Orchestration entry point (`customers` → `products` → `orders`) |
| `src/bronze/BRONZE_LAYER_NOTES.md` | Bronze execution and design notes |

**Key design decisions (documented in `design-notes.md`, `BRONZE_LAYER_NOTES.md`):**

| Decision | Value |
|----------|-------|
| Bronze tables | `bronze.bronze_customers`, `bronze.bronze_products`, `bronze.bronze_orders` |
| Databricks catalog (validation) | `de_c1_coding_evaluation` |
| Bronze schema | `bronze` |
| Fully qualified targets | `de_c1_coding_evaluation.bronze.bronze_*` |
| Source column types | **STRING** — preserves intentionally injected Phase 2 defects |
| Metadata columns | `_ingestion_timestamp`, `_source_file` |
| Write mode | `overwrite` (full reload) |
| Data quality in Bronze | **None** — no filtering, casting, deduplication, FK enforcement, or business-rule validation |
| Local validation without PySpark | `--dry-run` |
| Shared logic | `bronze_common.py` to avoid duplicated ingest code across entity scripts |

---

## Prompt 1: Phase 3 — Bronze Layer Implementation (Primary)

**PROMPT SENT:**

> Phase 3 BRONZE LAYER for `DE_C1_Coding_Evaluation`. Implement only:
> - `src/bronze/01_ingest_customers.py`, `02_ingest_orders.py`, `03_ingest_products.py`, `ingest_all.py`
>
> Ingest `data/customers.csv`, `products.csv`, `orders.csv` into Bronze Delta tables.
> Preserve Phase 2 defects — no cleansing/DQ in Bronze. Minimal transform + ingestion metadata.
> Parameterized paths/catalog/schema. No secrets. No Silver/Gold/Dashboard.
>
> Validate locally where possible; do not fabricate Databricks results.
> Update README, tool-workflow, design-notes, ai-prompts/bronze-layer.md.
> Do not commit.

**AI RESPONSE SUMMARY:**

- Added `bronze_common.py` (shared ingest logic) plus four planned scripts and `BRONZE_LAYER_NOTES.md`
- All source columns read as **STRING**; metadata `_ingestion_timestamp`, `_source_file`
- Tables: `bronze.bronze_customers`, `bronze.bronze_products`, `bronze.bronze_orders` (optional `--catalog`)
- Write mode `overwrite` default; `CREATE SCHEMA IF NOT EXISTS <schema>`
- `--dry-run` for local CSV validation without PySpark
- Updated README, design-notes, tool-workflow, requirements-analysis, data-model, task-breakdown

**YOUR EVALUATION (initial implementation):**

- ✓ STRING schema preserves intentional defects for Silver
- ✓ Consistent entity handling via `bronze_common.py`
- ✓ Dry-run validates row counts and spot-checks known defects
- ✓ Clear separation from Silver responsibilities
- △ Databricks execution deferred — PySpark not available in local Cursor environment

**FINAL DECISION (initial):** Implementation accepted for local validation; Databricks run required before closing Phase 3.

---

## Prompt 2: Databricks Execution Refinement

**PROMPT SENT:**

> User ran Bronze ingest on Databricks using `!python .../ingest_all.py` with catalog `de_c1_coding_evaluation`, schema `bronze`, write mode `overwrite`.
>
> Error: `PySparkValueError: [INVALID_CONNECT_URL] Invalid URL for Spark Connect ... must start with 'sc://'`
>
> Fix Bronze scripts to work in Databricks notebooks without using `!python` subprocess.

**AI RESPONSE SUMMARY:**

- Root cause: `!python` runs a **separate process** without the notebook `spark` session; `SparkSession.builder.getOrCreate()` fails with Spark Connect URL error on recent Databricks runtimes
- Added `resolve_spark()` and `notebook_spark_if_defined()` in `bronze_common.py` to reuse notebook/active Spark session
- Added `run_ingestion(config, spark=spark)` in `ingest_all.py` for notebook-cell execution
- Updated `BRONZE_LAYER_NOTES.md` with recommended Databricks patterns (`run_ingestion(..., spark=spark)` or `%run`, not `!python`)
- Changes committed and pushed (`d1f10fe`)

**YOUR EVALUATION:**

- ✓ Correct diagnosis — subprocess vs notebook Spark session
- ✓ Fix aligns with Databricks best practice
- ✓ Documentation updated to prevent repeat error

**FINAL DECISION:** Refinement accepted; proceed with notebook-based Databricks validation.

---

## Iteration / Refinement Evidence

These fixes demonstrate review and refinement rather than blind acceptance of the first generated implementation:

| # | Issue | Fix |
|---|-------|-----|
| 1 | `bronze_common.py` had top-level PySpark imports — `--dry-run` failed without PySpark installed locally | Moved PySpark imports inside Spark-dependent functions (lazy import) |
| 2 | Indentation error in dry-run print logic (draft) | Fixed before local validation completed |
| 3 | `!python ingest_all.py` on Databricks failed with `[INVALID_CONNECT_URL]` | Added `resolve_spark()`, `run_ingestion()`, notebook execution guidance |

No additional implementation iterations are documented beyond the above.

---

## Local Validation

Performed in the Cursor/local environment. **Could not prove Delta table creation** — PySpark was not installed locally.

| Check | Result |
|-------|--------|
| Python `py_compile` (all Bronze `.py` files) | **PASS** |
| `ingest_all.py --dry-run` | **PASS** |
| CSV row counts — customers | **1,006** |
| CSV row counts — products | **206** |
| CSV row counts — orders | **5,163** |
| Defect spot-check — NULL/empty emails | **50** |
| Defect spot-check — orphan customer IDs | **25** |
| Defect spot-check — orphan product IDs | **25** |
| Defect spot-check — non-positive quantities | **40** |
| Delta write / Bronze table read | **Not performed locally** (no PySpark) |

---

## Databricks Validation

The Cursor-generated Bronze implementation was subsequently executed in the **actual Databricks environment** using the orchestration entry point:

`src/bronze/ingest_all.py`

**Configuration:**

| Parameter | Value |
|-----------|-------|
| Catalog | `de_c1_coding_evaluation` |
| Schema | `bronze` |
| Write mode | `overwrite` |

**Tables created/written successfully:**

- `de_c1_coding_evaluation.bronze.bronze_customers`
- `de_c1_coding_evaluation.bronze.bronze_products`
- `de_c1_coding_evaluation.bronze.bronze_orders`

**Row-count reconciliation (SQL vs Phase 2 CSV source):**

| Table | Expected / Source Rows | Actual Databricks Rows | Result |
|-------|----------------------:|----------------------:|--------|
| `bronze_customers` | 1,006 | 1,006 | **PASS** |
| `bronze_products` | 206 | 206 | **PASS** |
| `bronze_orders` | 5,163 | 5,163 | **PASS** |

---

## Defect-Preservation Validation (Databricks SQL)

Phase 2 intentionally injects data-quality defects. Bronze must **preserve** them for Silver to detect — not clean, filter, cast away, deduplicate, or enforce FK/business rules.

**Observed defect counts in Bronze tables (Databricks SQL):**

| Defect check | Count in Bronze | Result |
|--------------|----------------:|--------|
| NULL / empty customer emails | 50 | **PASS** (preserved) |
| Non-positive order quantities | 40 | **PASS** (preserved) |
| Orphan customer IDs | 25 | **PASS** (preserved) |
| Orphan product IDs | 25 | **PASS** (preserved) |

**Interpretation:**

- Bronze is responsible for **faithful ingestion and traceability** (source values + metadata).
- Silver is responsible for **data-quality validation, cleansing, standardization, and handling of invalid records**.

Successful presence of these defects confirms Bronze did **not** accidentally filter invalid records, deduplicate keys, cast invalid values away, enforce referential integrity, or apply business rules.

---

## YOUR EVALUATION

The Bronze implementation was evaluated using **both** local and target-environment validation. It was **not** accepted merely because Python code compiled.

**Acceptance was based on:**

- Successful local compilation (`py_compile`)
- Successful local dry-run (`ingest_all.py --dry-run`)
- Successful execution in Databricks (after notebook-session refinement)
- Successful Delta table creation in catalog `de_c1_coding_evaluation`
- Exact row-count reconciliation with Phase 2 generated CSVs (1,006 / 206 / 5,163)
- Verification that representative intentionally injected defects were preserved in Bronze
- Confirmation that Bronze did not perform inappropriate cleansing or Silver-level logic

---

## FINAL DECISION

**Decision: ACCEPTED**

**Reason:**

The Phase 3 Bronze implementation satisfies the documented Bronze design and has been successfully validated in the target Databricks environment. It correctly ingests all three CSV datasets into Delta tables while preserving intentionally injected data-quality defects and ingestion metadata.

**No additional Bronze implementation changes are required before proceeding to Phase 4 — Silver.**

---

## Cursor Evaluation Evidence

| Requirement | Evidence in this project |
|-------------|--------------------------|
| **Persistent project context** | `tool-specific/cursor-workflow/project-context.md`, `spec.md`, `cursor-rules-or-instructions.md`, `task-breakdown.md`; Phase 1 foundation docs referenced before implementation |
| **Iteration** | PySpark lazy-import fix; dry-run indentation fix; Databricks `!python` → `resolve_spark()` / `run_ingestion()` refinement |
| **Validation** | Local `py_compile` + `--dry-run`; actual Databricks execution; SQL row-count reconciliation; defect-preservation SQL checks |
| **Human acceptance** | Implementation validated in Databricks before final acceptance; Bronze considered complete |

**Related artifacts:** `src/bronze/BRONZE_LAYER_NOTES.md` (execution details), `design-notes.md` (Bronze architecture), `ai-prompts/documentation.md` (prompt artifact convention).

---

## Prompt 3: (Reserved)

_Add future Bronze-related prompts here only if Bronze scope changes._
