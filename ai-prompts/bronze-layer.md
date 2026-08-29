# AI Prompts — Bronze Layer (Phase 3)

**Prompts in this file:** 05, 06, 25
**Implementation order:** Bronze ingest → Databricks Spark session fix

Significant prompts include full **PROMPT SENT** text.

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

## Prompt 05 — Bronze layer implementation

**TYPE:** Implementation

**PROMPT SENT:**

```text
We are now starting PHASE 3 — BRONZE LAYER IMPLEMENTATION.

Do NOT re-inspect or re-scaffold the repository. Phase 1 foundation and Phase 2 data generation are already complete.

Use the existing project documentation as the source of truth, especially:

- requirements-analysis.md
- design-notes.md
- data-model.md
- data-quality-strategy.md
- tool-workflow.md
- README.md
- src/data_generation/DATA_GENERATION_NOTES.md
- tool-specific/cursor-workflow/project-context.md
- tool-specific/cursor-workflow/spec.md
- tool-specific/cursor-workflow/cursor-rules-or-instructions.md
- tool-specific/cursor-workflow/task-breakdown.md
- data/customers.csv
- data/products.csv
- data/orders.csv

==================================================
PHASE 3 OBJECTIVE
==================================================

Implement ONLY the Bronze layer of the Databricks medallion pipeline.

The Bronze layer must ingest the three generated CSV datasets:

- data/customers.csv
- data/products.csv
- data/orders.csv

into corresponding Bronze Delta tables/objects in Databricks.

Planned implementation files:

src/bronze/
├── 01_ingest_customers.py
├── 02_ingest_orders.py
├── 03_ingest_products.py
└── ingest_all.py

==================================================
ARCHITECTURAL REQUIREMENTS
==================================================

Follow the established architecture:

Raw/sample CSV
      ↓
Bronze
      ↓
Silver
      ↓
Gold
      ↓
Dashboard

Bronze responsibilities:

- ingest source data
- preserve source values as much as practical
- perform only minimal structural handling
- add useful ingestion metadata where appropriate
- avoid business cleansing
- avoid Silver-level data-quality remediation
- avoid Gold aggregations

IMPORTANT:

The intentionally defective records created during Phase 2 MUST NOT be removed or "fixed" in Bronze.

The Bronze layer should preserve those records so that the Silver data-quality implementation can detect them.

Do not move quality rules into Bronze merely because the input contains bad records.

==================================================
DATA MODEL
==================================================

Use the finalized Phase 2 schemas documented in data-model.md.

customers.csv:

customer_id
customer_name
email
country
signup_date
customer_segment
lifetime_value

products.csv:

product_id
product_name
category
unit_price

orders.csv:

order_line_id
order_id
customer_id
product_id
order_date
quantity
unit_price

Orders represent LINE ITEMS.

Revenue is:

quantity × unit_price

Do not change this model.

==================================================
IMPLEMENTATION EXPECTATIONS
==================================================

For each entity:

1. Read the corresponding CSV.
2. Create/write the corresponding Bronze Delta table/object.
3. Preserve the source schema and values as much as practical.
4. Add appropriate ingestion metadata if consistent with the architecture, such as:
   - ingestion timestamp
   - source file/path
5. Make the implementation reusable and reasonably parameterized.
6. Avoid hardcoded credentials or secrets.
7. Use Databricks/PySpark patterns appropriate for this project.
8. Keep the three ingestion scripts independently understandable.
9. Provide ingest_all.py as the orchestration entry point.

Do NOT implement:

- Silver transformations
- data-quality checks
- quarantine logic
- Gold SQL
- dashboard logic
- streaming
- unnecessary production infrastructure
- Databricks Asset Bundles unless already required by the existing project specification

==================================================
PATH / ENVIRONMENT HANDLING
==================================================

Before choosing paths or table names, inspect the existing documentation for any established convention.

If a Databricks-specific path/catalog/schema/table naming decision is still genuinely unresolved, choose the simplest assessment-appropriate approach and DOCUMENT the decision rather than inventing a complex architecture.

Do not introduce Unity Catalog configuration, external locations, volumes, jobs, or infrastructure unless required by the existing project requirements.

==================================================
VALIDATION
==================================================

After implementation, validate the code as far as the current environment allows.

At minimum:

- Python syntax/compile validation
- verify imports where possible
- inspect schemas
- verify expected Bronze entities exist
- verify row counts against the generated CSVs
- verify intentionally defective records have NOT been silently removed
- verify Bronze preserves the Phase 2 source data
- test ingest_all.py appropriately if the Databricks environment is available

If Databricks execution is NOT available from the current Cursor environment, do NOT fabricate execution results.

Clearly distinguish:

- validated locally
- validated in Databricks
- unable to validate because environment access is unavailable

==================================================
ITERATION / REVIEW
==================================================

Do not blindly accept your first implementation.

After generating the Bronze implementation:

1. Review it against data-model.md and design-notes.md.
2. Check that Bronze is not accidentally performing Silver responsibilities.
3. Check that all three entities are handled consistently.
4. Check error handling and path/table configuration.
5. Fix any issues found.
6. Perform validation again after fixes.

Document meaningful iteration/fixes because this project is specifically demonstrating responsible Cursor-assisted development.

==================================================
DOCUMENTATION — REQUIRED IN THIS SAME PHASE
==================================================

This is critical.

Implementation + validation + documentation + AI prompt artifact are ONE unit of work.

Do not finish the code and leave documentation for later.

Update/create the appropriate documentation as part of this phase:

1. ai-prompts/bronze-layer.md

Record this implementation prompt and meaningful follow-up/refinement prompts using the established structure:

PROMPT SENT
AI RESPONSE SUMMARY
YOUR EVALUATION
FINAL DECISION

Do not fabricate the developer evaluation. Where a human decision is still required, explicitly mark it as pending.

2. Update README.md

Mark Bronze implementation status appropriately and describe what is actually implemented.

3. Update tool-workflow.md

Mark the Bronze phase status and record that implementation, review, validation, and prompt documentation were completed.

4. Update design-notes.md

Replace only the Bronze portions that were previously marked as TBD where the implementation has now made an actual decision.

5. Create/update any Bronze-specific documentation only if justified by the existing project structure.

Do NOT prematurely update Silver, Gold, or Dashboard implementation status.

==================================================
GIT
==================================================

Do NOT push anything.

Do NOT commit yet unless explicitly instructed.

At the end, report:

- files created
- files modified
- implementation decisions made
- validation performed
- validation limitations
- issues found and fixes
- documentation/prompt artifacts updated
- remaining human decisions, if any
- git status

STOP after Phase 3 Bronze is complete.

Do NOT start Silver.
```

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

## Prompt 06 — Databricks Spark session refinement

**TYPE:** Debugging / refinement

**PROMPT SENT:**

```text
@DE_C1_Coding_Evaluation/src/bronze/ingest_all.py 
when run in databricks 
!python /Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/src/bronze/ingest_all.py \
  --data-dir /Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/data \
  --catalog de_c1_coding_evaluation \
  --schema bronze \
  --write-mode overwrite

gave 
Traceback (most recent call last):
  File "/Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/src/bronze/ingest_all.py", line 61, in <module>
    main()
  File "/Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/src/bronze/ingest_all.py", line 44, in main
    spark = get_spark()
            ^^^^^^^^^^^
  File "/Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/src/bronze/bronze_common.py", line 154, in get_spark
    return SparkSession.builder.getOrCreate()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/databricks/python/lib/python3.12/site-packages/pyspark/sql/session.py", line 548, in getOrCreate
    RemoteSparkSession.builder.config(map=opts).getOrCreate(),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/databricks/python/lib/python3.12/site-packages/pyspark/sql/connect/session.py", line 286, in getOrCreate
    session = self.create()
              ^^^^^^^^^^^^^
  File "/databricks/python/lib/python3.12/site-packages/pyspark/sql/connect/session.py", line 270, in create
    session = SparkSession(
              ^^^^^^^^^^^^^
  File "/databricks/python/lib/python3.12/site-packages/pyspark/sql/connect/session.py", line 334, in __init__
    self._init_client = SparkConnectClient(
                        ^^^^^^^^^^^^^^^^^^^
  File "/databricks/python/lib/python3.12/site-packages/pyspark/sql/connect/client/core.py", line 891, in __init__
    else DefaultChannelBuilder(connection, channel_options)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/databricks/python/lib/python3.12/site-packages/pyspark/sql/connect/client/core.py", line 401, in __init__
    raise PySparkValueError(
pyspark.errors.exceptions.base.PySparkValueError: [INVALID_CONNECT_URL] Invalid URL for Spark Connect: The URL must start with 'sc://'. Please update the URL to follow the correct format, e.g., 'sc://hostname:port'.
```

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

## (Reserved — future Bronze scope changes only)

_Add future Bronze-related prompts here only if Bronze scope changes._
---

## Prompt 25 — Bronze layer documentation update

**TYPE:** Documentation

**PROMPT SENT:**

```text
Update `ai-prompts/bronze-layer.md` to document the complete Phase 3 Bronze implementation, iteration history, and actual Databricks validation that was performed.

IMPORTANT:
- Do NOT modify any Bronze implementation code.
- Do NOT start Phase 4 / Silver.
- Do NOT recreate or revalidate the repository.
- Do NOT change the architecture or implementation decisions.
- Only update `ai-prompts/bronze-layer.md`.
- Preserve the existing structure and content of the file where possible.
- Do not invent prompts, validation results, iterations, or decisions that are not supported by the project history/files.

The purpose of this update is to make `ai-prompts/bronze-layer.md` a clear evidence artifact for the Cursor evaluation, showing:
1. The prompt/specification given to Cursor.
2. The implementation/refinement decisions.
3. The validation performed locally.
4. The validation performed in the actual Databricks environment.
5. The final human evaluation and acceptance decision.

## 1. Document the Bronze implementation context

Ensure the artifact clearly records that Phase 3 implemented:

- `src/bronze/bronze_common.py`
- `src/bronze/01_ingest_customers.py`
- `src/bronze/02_ingest_orders.py`
- `src/bronze/03_ingest_products.py`
- `src/bronze/ingest_all.py`
- `src/bronze/BRONZE_LAYER_NOTES.md`

Document the key design decisions:

- Bronze tables:
  - `bronze.bronze_customers`
  - `bronze.bronze_products`
  - `bronze.bronze_orders`
- Catalog used for Databricks validation:
  - `de_c1_coding_evaluation`
- Bronze schema:
  - `bronze`
- Source columns are preserved as STRING values to retain intentionally injected defects.
- Metadata columns:
  - `_ingestion_timestamp`
  - `_source_file`
- Bronze uses overwrite mode for the full reload.
- Bronze performs NO data-quality cleansing.
- No filtering, casting, deduplication, FK enforcement, or business-rule validation occurs in Bronze.
- `--dry-run` allows local validation without PySpark.
- Shared Bronze functionality is implemented in `bronze_common.py` to avoid duplicated logic.

## 2. Document iteration/refinement evidence

If the existing artifact already documents implementation iterations, preserve them.

Specifically retain/document the actual issues that were encountered and fixed:

1. Initial `bronze_common.py` had top-level PySpark imports, which prevented `--dry-run` from working without PySpark.
   - This was fixed by moving PySpark imports inside Spark-dependent functions.

2. An indentation issue existed in the dry-run print logic.
   - It was fixed before validation.

Do not invent additional iterations.

Where appropriate, explain that these changes demonstrate refinement rather than blindly accepting the first generated implementation.

## 3. Document local validation

Record the actual local validation that was performed:

- Python `py_compile` for Bronze Python files: PASS
- `ingest_all.py --dry-run`: PASS
- CSV row counts:
  - customers: 1,006
  - products: 206
  - orders: 5,163
- Defect spot checks:
  - NULL emails: 50
  - orphan customers: 25
  - orphan products: 25
  - non-positive quantities: 40

Make clear that local validation could not prove Delta table creation because PySpark was not installed in the local Cursor environment.

## 4. Add actual Databricks validation

Add a clearly labelled section:

## Databricks Validation

Document that the Cursor-generated Bronze implementation was subsequently executed in the actual Databricks environment.

Execution used the Bronze orchestration implementation:

`src/bronze/ingest_all.py`

Configuration:

- Catalog: `de_c1_coding_evaluation`
- Schema: `bronze`
- Write mode: `overwrite`

The Databricks execution successfully created/wrote:

- `de_c1_coding_evaluation.bronze.bronze_customers`
- `de_c1_coding_evaluation.bronze.bronze_products`
- `de_c1_coding_evaluation.bronze.bronze_orders`

Record these exact observed row counts:

| Table | Expected/Source Rows | Actual Databricks Rows | Result |
|---|---:|---:|---|
| bronze_customers | 1,006 | 1,006 | PASS |
| bronze_products | 206 | 206 | PASS |
| bronze_orders | 5,163 | 5,163 | PASS |

## 5. Document defect-preservation validation

Record these exact Databricks SQL validation results:

- NULL/empty customer emails: 50
- Non-positive order quantities: 40
- Orphan customer IDs: 25
- Orphan product IDs: 25

Explain why these checks are important:

The Phase 2 dataset intentionally contains data-quality defects. Bronze is expected to preserve those defects rather than clean them.

Therefore the successful presence of these defects confirms that Bronze did not accidentally:
- filter invalid records,
- deduplicate records,
- cast invalid values away,
- enforce referential integrity,
- or apply business rules.

Make the distinction clear:

Bronze is responsible for faithful ingestion and traceability.

Silver is responsible for data-quality validation, cleansing, standardization, and handling of invalid records.

## 6. Add final evaluation / acceptance

Add or update a section:

## YOUR EVALUATION

State that the Bronze implementation was evaluated using both local and target-environment validation.

The implementation was not accepted merely because the Python code compiled.

Acceptance was based on:

- successful local compilation,
- successful local dry-run,
- successful execution in Databricks,
- successful Delta table creation,
- exact row-count reconciliation with Phase 2 generated CSVs,
- verification that representative intentionally injected defects were preserved,
- confirmation that Bronze did not perform inappropriate cleansing.

## 7. Add final decision

Add or update:

## FINAL DECISION

Decision: ACCEPTED

Reason:

The Phase 3 Bronze implementation satisfies the documented Bronze design and has been successfully validated in the target Databricks environment.

The implementation correctly ingests all three CSV datasets into Delta tables while preserving the intentionally injected data-quality defects and ingestion metadata.

No additional Bronze implementation changes are required before proceeding to Phase 4 — Silver.

## 8. Cursor evaluation evidence

Make the artifact explicitly useful as evidence for the Cursor evaluation requirements.

Where supported by the existing project history, identify evidence for:

- Persistent project context:
  - `tool-specific/cursor-workflow/project-context.md`
  - `tool-specific/cursor-workflow/spec.md`
  - `tool-specific/cursor-workflow/cursor-rules-or-instructions.md`
  - `tool-specific/cursor-workflow/task-breakdown.md`

- Iteration:
  - documented fixes to the PySpark import behavior and dry-run indentation issue.

- Validation:
  - local compilation/dry-run;
  - actual Databricks execution;
  - SQL row-count validation;
  - intentional defect-preservation validation.

- Human acceptance:
  - implementation was validated before being accepted;
  - Bronze is now considered complete.

Do not claim that every Cursor suggestion was accepted/rejected unless that evidence already exists in the project artifacts.

## 9. Keep the artifact concise and factual

Do not duplicate the entire contents of `BRONZE_LAYER_NOTES.md`.

This file should primarily serve as the AI/Cursor prompt-and-evaluation evidence artifact.

After updating the file, report:
1. What sections were added or updated.
2. Whether any information was unavailable from the existing project history.
3. Confirm that no implementation code was changed.
4. Confirm that Phase 4 / Silver was NOT started.
```

**AI RESPONSE SUMMARY:**

Updated `ai-prompts/bronze-layer.md` with full Phase 3 evidence, Databricks validation, defect preservation.

**FINAL DECISION:** ACCEPTED (documented)

