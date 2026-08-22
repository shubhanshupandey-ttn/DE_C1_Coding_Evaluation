# AI Prompts — Bronze Layer

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

- Added `bronze_common.py` (shared ingest logic) plus four planned scripts
- **Design:** all source columns read as STRING; metadata `_ingestion_timestamp`, `_source_file`
- **Tables:** `bronze.bronze_customers`, `bronze.bronze_products`, `bronze.bronze_orders` (optional `--catalog`)
- **Write mode:** `overwrite` default; `CREATE SCHEMA IF NOT EXISTS bronze`
- `--dry-run` for local CSV validation without PySpark
- Created `BRONZE_LAYER_NOTES.md`; updated README, design-notes, tool-workflow, requirements-analysis, data-model, task-breakdown

**YOUR EVALUATION:**

_To be completed by developer._

- ✓ **What was good:**
  - STRING schema preserves intentional defects for Silver
  - Consistent entity handling via `bronze_common.py`
  - Dry-run validates row counts and spot-checks known defects
  - Clear separation from Silver responsibilities

- △ **Review:**
  - Confirm Databricks table names/catalog for your workspace
  - Run `ingest_all.py` on cluster and verify Delta row counts match CSVs

- ✗ **Databricks execution:** Not validated in Cursor environment (PySpark not installed locally)

**FINAL DECISION:** _Pending developer review and Databricks run._

---

## Validation Log (actual)

| Step | Environment | Result |
|------|-------------|--------|
| `py_compile` all Bronze `.py` files | Local | Pass |
| `ingest_all.py --dry-run` | Local | Pass |
| customers row count | Local dry-run | 1,006 |
| products row count | Local dry-run | 206 |
| orders row count | Local dry-run | 5,163 |
| null_email_rows spot-check | Local dry-run | 50 |
| orphan_customer_rows | Local dry-run | 25 |
| Delta write to Databricks | Databricks | **Not run** |

---

## Prompt 2: (Reserved for follow-up)

_Add prompts here after Databricks execution or parameter changes._
