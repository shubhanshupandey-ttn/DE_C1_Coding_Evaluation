# Silver Layer Notes — Design (Iteration 1 — Finalized)

**Status:** Silver Iterations 1–5 **ACCEPTED** (`SERVERLESS_COMPAT_VERSION = 9`). **RI alignment fix ACCEPTED** (`SERVERLESS_COMPAT_VERSION = 10`). Phase 4 Silver **complete**.

Phase 4 Silver design defines how Bronze transforms into curated, typed Delta tables with explicit data-quality enforcement. Open design decisions were resolved in the Iteration 1 design-refinement pass (see `ai-prompts/silver-layer.md`).

---

## Environment

| Item | Value |
|------|-------|
| Catalog | `de_c1_coding_evaluation` |
| Bronze schema | `bronze` |
| Silver schema | `silver` |
| Bronze inputs | `bronze_customers` (1,006), `bronze_products` (206), `bronze_orders` (5,163) |
| Silver outputs | `silver_customers`, `silver_products`, `silver_orders` |

Fully qualified examples:

- `de_c1_coding_evaluation.bronze.bronze_customers`
- `de_c1_coding_evaluation.silver.silver_orders`

---

## Objective

Silver is the **trusted/curated layer**. It must:

1. Read Bronze Delta tables (STRING source columns)
2. Apply safe typing and light cleansing (trim whitespace)
3. Run five DQ categories (completeness, uniqueness, type validation, referential integrity, business logic)
4. Write **valid** rows to Silver entity tables
5. Route **invalid** rows to quarantine (not silently dropped)
6. Write a **DQ summary** per run
7. Remain modular, idempotent, and aligned with the line-item order model

**Bronze is not modified.** Silver consumes Bronze as-is.

---

## Proposed File Responsibilities

| File | Responsibility |
|------|----------------|
| `silver_common.py` | Catalog/schema config, Bronze reads, safe cast helpers, quarantine/DQ writers, Spark session resolution (Bronze pattern) |
| `01_quality_completeness.py` | Required-field checks per entity |
| `02_quality_uniqueness.py` | PK uniqueness: `customer_id`, `product_id`, `order_line_id` |
| `03_quality_type_validation.py` | Parse dates, numerics, email format; flag unparseable values |
| `04_quality_referential_integrity.py` | `orders.customer_id` → customers; `orders.product_id` → products |
| `05_quality_business_logic.py` | Dates, quantities, prices, segment, catalog-price consistency |
| `06_write_dq_results.py` | Quarantine + DQ summary persistence (Iteration 4) |
| `create_silver_tables.py` | Orchestration entry point; runs full pipeline in documented order |

---

## Execution Flow (Finalized)

```
Bronze tables (STRING)
        │
        ▼
┌───────────────────────────────────────┐
│ 1. Read Bronze + trim string fields   │
│ 2. Safe parse → typed Silver columns  │
└───────────────────────────────────────┘
        │
        ├──► 01 Completeness (per entity)
        ├──► 02 Uniqueness (per entity)
        └──► 03 Type validation (per entity)
        │
        ▼
┌───────────────────────────────────────┐
│ 4. Canonical valid customers/products │  ← parents that passed 01–03
└───────────────────────────────────────┘
        │
        ├──► 04 Referential integrity (orders)
        └──► 05 Business logic (all entities)
        │
        ▼
┌──────────────┐   ┌─────────────────────┐   ┌──────────────────┐
│ Silver tables│   │ silver_quarantine_  │   │ silver_dq_       │
│ (valid only) │   │ records             │   │ summary          │
└──────────────┘   └─────────────────────┘   └──────────────────┘
```

**No additional DQ categories.** Execution order is fixed for implementation.

### Execution order rationale

| Step | Why this order |
|------|----------------|
| Completeness before uniqueness | Empty keys are not meaningful uniqueness candidates |
| Uniqueness before FK | Canonical parent keys must be deduplicated before FK checks |
| Type validation before business logic | Business rules operate on typed values |
| FK after canonical parents | Orphan detection must use **valid** parent key sets |
| Business logic last | Rules like catalog-price match need typed prices and valid parents |
| Write Silver last | Curated tables contain only rows passing all checks |

---

## Type Standardization (Silver output)

Bronze stores STRING. Silver converts to analytical types per Phase 4 spec:

### customers → `silver_customers`

| Column | Silver type |
|--------|-------------|
| `customer_id` | STRING |
| `customer_name` | STRING |
| `email` | STRING |
| `country` | STRING |
| `signup_date` | DATE |
| `customer_segment` | STRING |
| `lifetime_value` | DECIMAL(12,2) |

### products → `silver_products`

| Column | Silver type |
|--------|-------------|
| `product_id` | STRING |
| `product_name` | STRING |
| `category` | STRING |
| `unit_price` | DECIMAL(10,2) |

### orders → `silver_orders` (line items)

| Column | Silver type |
|--------|-------------|
| `order_line_id` | STRING |
| `order_id` | STRING |
| `customer_id` | STRING |
| `product_id` | STRING |
| `order_date` | DATE |
| `quantity` | INT |
| `unit_price` | DECIMAL(10,2) |

**Identifier columns** (`customer_id`, `product_id`, `order_line_id`, `order_id`) are stored as **STRING** in Silver.

Type validation must confirm identifiers are **numerically parseable** before they are accepted:

| Bronze value | Result |
|--------------|--------|
| `"12345"` | Valid — stored as STRING `"12345"` in Silver |
| `"INVALID"` | Type validation failure — quarantined |

Do not silently coerce malformed identifiers.

Malformed non-identifier values: safe cast returns NULL + failure flag; row quarantined — **not silently coerced**.

---

## Data Quality Rules (from existing strategy — no new categories)

### Completeness

**Authoritative required fields** (from `data-quality-strategy.md` — full list, not a reduced minimum set):

| Entity | Required columns |
|--------|------------------|
| customers | `customer_id`, `customer_name`, `email`, `country`, `signup_date`, `customer_segment`, `lifetime_value` |
| products | `product_id`, `product_name`, `category`, `unit_price` |
| orders | `order_line_id`, `order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `unit_price` |

Rows failing completeness are **quarantined** — not silently dropped. See defect matrix D01, D02, D07.

### Uniqueness

| Entity | Key | Notes |
|--------|-----|-------|
| customers | `customer_id` | Duplicate defect D03 (6 rows) |
| products | `product_id` | Duplicate defect D08 (6 rows) |
| orders | `order_line_id` | **Not** `order_id`; D16 (8 rows) |

**Duplicate handling (proposed):** keep first occurrence in Silver; quarantine subsequent duplicates.

### Type validation

Detect: invalid dates (D04, D13), malformed email (D05), non-numeric prices (D09), invalid quantity strings, non-numeric identifiers.

Identifier columns remain STRING in Silver after numeric-parse validation passes.

### Referential integrity

| FK | Parent | Expected orphans |
|----|--------|------------------|
| `orders.customer_id` | `silver_customers` (canonical) | 25 (D11) |
| `orders.product_id` | `silver_products` (canonical) | 25 (D12) |

### Business logic

| Rule | Defect examples | Handling |
|------|-----------------|----------|
| `quantity > 0` | D15 (40 rows) | Quarantine |
| `signup_date <= current_date()` | D06 | Quarantine; use runtime `current_date()`, not a fixed evaluation date |
| `order_date <= current_date()` | D14 | Quarantine; use runtime `current_date()` |
| `products.unit_price >= 0` | D10 | Quarantine |
| `orders.unit_price = products.unit_price` (catalog match) | D17 | **Quarantine only** — do not auto-correct order `unit_price` |
| `customer_segment IN ('Premium','Standard','Basic')` | — | Quarantine |

**D17 catalog-price mismatch:** detect mismatch, quarantine the order line, preserve original Bronze value in `bronze_source_values`. Do **not** replace order `unit_price` with product catalog price.

**Traceability:** `run_timestamp` on quarantine and DQ summary records captures the pipeline run time for date-based rule evaluation.

---

## Invalid Record Handling

### Centralized quarantine table: `de_c1_coding_evaluation.silver.silver_quarantine_records`

**Single table** for all entities (`customers`, `products`, `orders`) and all five DQ categories:

- `completeness`
- `uniqueness`
- `type_validation`
- `referential_integrity`
- `business_logic`

| Column | Purpose |
|--------|---------|
| `entity_name` | `customers`, `products`, or `orders` |
| `business_key` | `customer_id`, `product_id`, or `order_line_id` |
| `check_category` | One of the five categories above |
| `failure_reason` | Human-readable rule description |
| `failed_column` | Column involved (nullable for multi-column rules) |
| `bronze_source_values` | STRING map or JSON of original Bronze row (traceability) |
| `quarantine_timestamp` | When quarantined |
| `run_timestamp` | Pipeline run identifier |

**Multiple failures:** one quarantine row per `(business_key, check_category, failure_reason)` where practical; same source row may appear multiple times.

**Invalid rows do not appear in Silver curated tables.**

---

## DQ Summary

### Table: `de_c1_coding_evaluation.silver.silver_dq_summary`

| Column | Purpose |
|--------|---------|
| `check_category` | One of five DQ categories |
| `table_name` | Entity table checked |
| `rows_tested` | Rows evaluated |
| `rows_passed` | Rows passing |
| `rows_failed` | Rows failing |
| `pass_percentage` | `rows_passed / rows_tested * 100` |
| `failure_reason` | Optional aggregate or representative reason |
| `run_timestamp` | Pipeline run time |

Overwrite each run (idempotent).

---

## Idempotency

| Object | Write mode |
|--------|------------|
| `silver_customers`, `silver_products`, `silver_orders` | `overwrite` |
| `silver_quarantine_records` | `overwrite` (full snapshot per run) |
| `silver_dq_summary` | `overwrite` |

Re-running Silver on the same Bronze input replaces outputs — no duplicate accumulation.

---

## Databricks Execution

```python
# Notebook cell pattern (Serverless)
import importlib.util, sys
from pathlib import Path

silver_dir = Path("/Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/src/silver")
for name in list(sys.modules):
    if name.startswith(("silver_common", "quality_", "referential", "business", "write_dq", "create_silver", "_load")):
        del sys.modules[name]
sys.path.insert(0, str(silver_dir))

spec = importlib.util.spec_from_file_location("silver_common", silver_dir / "silver_common.py")
silver_common = importlib.util.module_from_spec(spec)
sys.modules["silver_common"] = silver_common
spec.loader.exec_module(silver_common)

spec = importlib.util.spec_from_file_location("create_silver_tables", silver_dir / "create_silver_tables.py")
create_silver_tables = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create_silver_tables)

result = create_silver_tables.run_silver_pipeline(spark=spark)
```

**Databricks validation:** **PASS** (Iteration 5 — full `run_silver_pipeline` on Serverless).

---

## Resolved Design Decisions (Iteration 1 — finalized)

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Completeness required fields | **Full list** from `data-quality-strategy.md` (not a reduced minimum set) |
| 2 | Quarantine structure | **Single centralized table** `silver_quarantine_records` |
| 3 | Identifier types | **STRING** in Silver; type validation verifies numeric parseability |
| 4 | D17 catalog-price mismatch | **Quarantine only** — no auto-correction of order `unit_price` |
| 5 | Date-based business rules | `current_date()` at runtime; `run_timestamp` on quarantine/DQ summary for traceability |
| 6 | Execution order | Fixed flow documented above; no new DQ categories |

**No remaining open design decisions** before Iteration 2 implementation.

---

## Iteration 2 Implementation (ACCEPTED)

| Module | Status | Defect IDs targeted |
|--------|--------|---------------------|
| `silver_common.py` | Implemented + Serverless validated | Type trim/parse helpers, failure schema |
| `01_quality_completeness.py` | Implemented + Serverless validated | D01, D02, D07 |
| `02_quality_uniqueness.py` | Implemented + Serverless validated | D03, D08, D16 |
| `03_quality_type_validation.py` | Implemented + Serverless validated | D04, D05, D09, D13 |
| `_load_silver_common.py` | Implemented | Databricks fresh module loader |

**Iteration 3+ not implemented at Iteration 2 acceptance:** `04_referential_integrity`, `05_business_logic`, `create_silver_tables.py`, quarantine write, DQ summary write.

**Deterministic duplicate ranking:** partition by business key; order by tiebreaker columns (asc, nulls last) then row-content hash (no global window).

**Local validation:** `py_compile` + `test_silver_helpers.py` — **PASS**

**Databricks Serverless validation** (`SERVERLESS_COMPAT_VERSION = 7`, catalog `de_c1_coding_evaluation`, Bronze schema `bronze`):

| Check | customers | products | orders |
|-------|-----------|----------|--------|
| Completeness failures | 60 | 9 | 0 |
| Uniqueness failures | 6 | 6 | 8 |
| Type validation failures | 50 | 15 | 30 |

**Completeness notes:** customers = 50 (D01 email) + 10 (D02 name) exact; products = 9 observed vs 8 documented D07 injections (one additional blank/edge case in Bronze); orders = 0.

**Uniqueness keys:** `customer_id`, `product_id`, `order_line_id` (not `order_id`). Order duplicate `business_key` examples: 47, 47, 48, 48, 52, 52, 72, 72.

**Type validation notes:** customers 50 = 30 email + 20 signup_date; products 15 = unit_price; orders 30 = order_date; total 95 matches Phase 2 type/format defect count.

**Failure-record semantics:** counts are per validation rule / failed field; defects may overlap across DQ categories; uniqueness reports non-canonical duplicate occurrences.

**Serverless:** no RDD error during validated runs; DataFrame APIs only. Global window warning observed during earlier uniqueness debugging — not treated as validation failure; final uniqueness counts exact.

---

## Iteration 3 Implementation (ACCEPTED)

| Module | Status | Defect IDs / rules |
|--------|--------|-------------------|
| `04_quality_referential_integrity.py` | Implemented + Serverless validated | D11, D12 + canonical-parent FK semantics |
| `05_quality_business_logic.py` | Implemented + Serverless validated | D06, D10, D14, D15, D17 + valid `customer_segment` |
| `silver_common.py` (minimal additions) | Updated | Canonical parent helpers, `CHECK_REFERENTIAL_INTEGRITY`, `CHECK_BUSINESS_LOGIC`, segment validation |

**Canonical parent logic:** Bronze → trim/typed columns → completeness + type-validation pass + canonical duplicate rank (`_dup_rank = 1`) → valid parent key set. FK and catalog-price checks use this set, not raw Bronze parents.

**Referential integrity rules:**

- `orders.customer_id` → canonical `customers.customer_id` (left join anti-pattern via null parent marker)
- `orders.product_id` → canonical `products.product_id`
- Non-blank FK values only; failures use `check_category = referential_integrity`
- Order failure `business_key` = `order_line_id`; use `bronze_source_values` JSON to trace `customer_id` / `product_id`

**Business logic rules:**

| Entity | Rule | Typed column | D17 note |
|--------|------|--------------|----------|
| customers | `signup_date <= current_date()` | `signup_date_typed` | |
| customers | `customer_segment IN (Premium, Standard, Basic)` | string | |
| products | `unit_price >= 0` | `unit_price_typed` | |
| orders | `quantity > 0` | `quantity_typed` | |
| orders | `order_date <= current_date()` | `order_date_typed` | |
| orders | `unit_price = catalog unit_price` | join canonical products | **Quarantine only** — no auto-correction |

**Not implemented (Iteration 4+):** quarantine Delta writes, DQ summary writes, `create_silver_tables.py`, Silver curated table writes.

**Local validation:** `py_compile` + `test_silver_helpers.py` — **PASS**

**Databricks Serverless validation** (`SERVERLESS_COMPAT_VERSION = 7`):

| Module | Metric | Observed | Defect / notes |
|--------|--------|----------|----------------|
| RI (orders) | Total failure records | **1087** | 512 `customer_id` + 575 `product_id` |
| RI | D11 (`customer_id = 9999991` in source JSON) | **25** | Exact match |
| RI | D12 (`product_id = 9999992` in source JSON) | **25** | Exact match |
| RI | Non D11/D12 (existing but non-canonical parent) | **1037** | Expected with canonical FK semantics |
| BL customers | Future signup | **10** | D06 exact |
| BL products | Negative `unit_price` | **11** | D10 (~10) |
| BL orders | Non-positive `quantity` | **40** | D15 exact |
| BL orders | Future `order_date` | **15** | D14 exact |
| BL orders | Catalog `unit_price` total | **222** | D17 proxy (`order_date = 2024-06-01`): **18**; other mismatches: **204** |

**Interpretation:** Total RI and catalog-price counts exceed raw D11/D12/D17 injection totals because (1) canonical FK flags orders referencing **existing but Iteration-2-invalid** parents, and (2) catalog-price equality compares order snapshot prices to **current** canonical catalog prices after Phase 2 product mutations. Intentional defects D11/D12/D17 are detected at expected volumes when traced via `bronze_source_values`.

---

## Iteration 4 Implementation (ACCEPTED)

| Module | Status | Purpose |
|--------|--------|---------|
| `06_write_dq_results.py` | Implemented + Serverless validated | Persist quarantine + DQ summary Delta tables |
| `silver_common.py` (minimal additions) | Updated | Table names, summary columns, `write_delta_table`, `calculate_pass_percentage` |

**Tables written (Delta, overwrite per run):**

| Table | FQN |
|-------|-----|
| Quarantine | `de_c1_coding_evaluation.silver.silver_quarantine_records` |
| DQ summary | `de_c1_coding_evaluation.silver.silver_dq_summary` |

**Quarantine semantics:** One row per failure event (rule / failed column). A single source row may produce multiple quarantine records across categories and within a category.

**Summary semantics (row-oriented):**

| Metric | Definition |
|--------|------------|
| `rows_tested` | Entity DataFrame row count evaluated by the DQ category |
| `rows_failed` | **Distinct `business_key`** count failing that category (not failure-record count) |
| `rows_passed` | `rows_tested - rows_failed` |
| `pass_percentage` | `rows_passed / rows_tested * 100`; NULL when `rows_tested = 0` |

**Summary coverage:** 13 rows per run — completeness (3), uniqueness (3), type validation (3), referential integrity (orders only, 1), business logic (3).

**Idempotency:** Both tables use Delta `overwrite` mode. Re-running against the same Bronze input replaces the full snapshot — no append accumulation.

**Timestamps:** `run_timestamp` from shared `SilverConfig`; `quarantine_timestamp` from existing failure builders (`current_timestamp()` at failure materialization).

**Not implemented (Iteration 5):** `create_silver_tables.py`, Silver curated table writes, full pipeline orchestration.

**Local validation:** `py_compile` all Silver `.py` files + `test_silver_helpers.py` — **PASS**

**Databricks Serverless validation** (`SERVERLESS_COMPAT_VERSION = 8`):

| Check | Observed |
|-------|----------|
| Quarantine failure records (total) | **1569** |
| Summary rows | **13** |
| Idempotency (2nd run) | 1569 → 1569 (no growth) |
| `pass_percentage` validation | all `pct_ok = true` |
| D11 / D12 / D17 proxy in quarantine | 25 / 25 / 18 |

**Quarantine failure-record counts (match Iterations 2–3):**

| Category | customers | products | orders |
|----------|-----------|----------|--------|
| completeness | 60 | 9 | 0 |
| uniqueness | 6 | 6 | 8 |
| type_validation | 50 | 15 | 30 |
| referential_integrity | — | — | 1087 |
| business_logic | 10 | 11 | 277 |

**Summary `rows_failed` (distinct business_key — row-oriented):**

| Category | customers | products | orders |
|----------|-----------|----------|--------|
| completeness | 60 | 8 | 0 |
| uniqueness | 6 | 6 | 4 |
| type_validation | 50 | 15 | 30 |
| referential_integrity | — | — | 1029 |
| business_logic | 10 | 10 | 277 |

Summary `rows_failed` is intentionally lower than quarantine failure-record counts where one source row fails multiple rules within the same category (e.g. products completeness 9 records / 8 rows; orders RI 1087 records / 1029 rows).

---

## Iteration 5 Implementation (ACCEPTED)

| Module | Status | Purpose |
|--------|--------|---------|
| `create_silver_tables.py` | Implemented + Serverless validated | Full pipeline orchestration + curated Silver writes |
| `silver_common.py` (minimal additions) | Updated | Curated table names, `entity_dq_categories()` |

**Orchestration flow (`run_silver_pipeline`):**

1. `CREATE SCHEMA IF NOT EXISTS de_c1_coding_evaluation.silver`
2. Run all five DQ modules via `06_write_dq_results.run_all_dq_checks`
3. Persist quarantine + DQ summary via `06_write_dq_results.run_dq_persistence`
4. Build curated DataFrames by anti-joining category failure keys from existing `failures_df` outputs
5. Write `silver_customers`, `silver_products`, `silver_orders` (Delta overwrite)

**Curated eligibility:** A row is written only if its `business_key` does not appear in **any** applicable category's failure set (completeness, uniqueness, type validation, referential integrity for orders, business logic).

**Curated output schemas (validated — no helper columns):**

| Table | Columns |
|-------|---------|
| `silver_customers` | `customer_id` STRING, `customer_name` STRING, `email` STRING, `country` STRING, `signup_date` DATE, `customer_segment` STRING, `lifetime_value` DECIMAL(12,2) |
| `silver_products` | `product_id` STRING, `product_name` STRING, `category` STRING, `unit_price` DECIMAL(10,2) |
| `silver_orders` | `order_line_id` STRING, `order_id` STRING, `customer_id` STRING, `product_id` STRING, `order_date` DATE, `quantity` INT, `unit_price` DECIMAL(10,2) |

No `*_typed`, `_dup_rank`, `_row_num`, or `line_revenue` in curated output. D17 remains quarantine-only — no catalog price auto-correction.

**Idempotency:** All five Silver outputs use Delta `overwrite` per run.

**Local validation:** `py_compile` all Silver `.py` files + `test_silver_helpers.py` — **PASS**

**Databricks Serverless validation** (`SERVERLESS_COMPAT_VERSION = 9`):

| Check | Observed | Assessment |
|-------|----------|------------|
| `create_silver_tables` load | Success | **PASS** |
| `run_silver_pipeline` completion | Success | **PASS** |
| Quarantine failure records | **1569** | Matches Iteration 4 baseline |
| DQ summary rows | **13** | **PASS** |
| Idempotency (re-run) | 1569 → 1569 | **PASS** |
| `pass_percentage` calculations | Validated | **PASS** |
| D11 / D12 / D17 proxy in quarantine | 25 / 25 / 18 | **PASS** |

**Curated Silver row counts (validated):**

| Table | Bronze rows | Silver rows |
|-------|-------------|-------------|
| customers | 1,006 | **878** |
| products | 206 | **164** |
| orders | 5,163 | **3,832** |

Silver row counts are lower than Bronze because invalid rows are quarantined, not silently dropped.

**Validated DQ summary (`silver_dq_summary`):**

| Category | Entity | rows_tested | rows_passed | rows_failed |
|----------|--------|-------------|-------------|-------------|
| completeness | customers | 1006 | 946 | 60 |
| completeness | products | 206 | 198 | 8 |
| completeness | orders | 5163 | 5163 | 0 |
| uniqueness | customers | 1006 | 1000 | 6 |
| uniqueness | products | 206 | 200 | 6 |
| uniqueness | orders | 5163 | 5159 | 4 |
| type_validation | customers | 1006 | 956 | 50 |
| type_validation | products | 206 | 191 | 15 |
| type_validation | orders | 5163 | 5133 | 30 |
| referential_integrity | orders | 5163 | 4134 | **1029** |
| business_logic | customers | 1006 | 996 | 10 |
| business_logic | products | 206 | 196 | 10 |
| business_logic | orders | 5163 | 4886 | 277 |

**Referential integrity — intentional non-zero failures (NOT a bug):**

The Bronze dataset contains intentional D11/D12 orphan defects. Non-zero RI results are **expected and correct**:

| RI metric | Value | Meaning |
|-----------|-------|---------|
| D11 orphan `customer_id` failure records | **25** | Exact match to defect injection |
| D12 orphan `product_id` failure records | **25** | Exact match to defect injection |
| Total RI failure records (quarantine) | **1087** | Includes D11/D12 + existing-but-non-canonical parent effects (1,037) |
| Distinct failed order `business_key` rows (summary) | **1029** | Row-oriented RI metric |
| Orders failing both FK checks | Some | Explains 1087 failure records > 1029 distinct failed rows |

**Quarantine vs summary semantics (preserved):**

- **Quarantine:** failure-record oriented (one row per rule violation; 1,569 total across all categories).
- **Summary:** row-oriented — `rows_failed` = distinct `business_key` per category where applicable (e.g. orders uniqueness: 8 failure records / 4 distinct failed rows; orders RI: 1087 failure records / 1029 distinct failed rows).

**Phase 4 Silver — cumulative validated DQ baselines (Iterations 2–4, unchanged in Iteration 5):**

| Iteration | Key results |
|-----------|-------------|
| Iteration 2 completeness | customers 60; products 9 records / 8 rows; orders 0 |
| Iteration 2 uniqueness | customers 6; products 6; orders 8 records / 4 rows |
| Iteration 2 type validation | customers 50; products 15; orders 30 |
| Iteration 3 RI | D11 25 + D12 25; 1,087 total RI failure records; 1,029 distinct failed order rows |
| Iteration 3 business logic | D17 proxy 18; catalog-price mismatches 222 total (18 D17 + 204 other) |
| Iteration 4 persistence | quarantine 1,569; summary 13; idempotent overwrite |

**FINAL DECISION:** **ACCEPTED** — Silver Iteration 5 complete. Phase 4 Silver layer **complete**. Gold not started.

---

## RI Alignment Fix — Curated Parent Keys (`SERVERLESS_COMPAT_VERSION = 10`)

**Problem (discovered during Gold Iteration 6 validation):** RI previously validated order FKs against `canonical_valid_filter()` parents (`_dup_rank = 1` + completeness + type only). Curated `silver_customers` / `silver_products` use `filter_valid_rows()` which also applies uniqueness and business_logic. Order lines could pass RI while referencing parent keys absent from curated dimensions (e.g. `product_id = 184`, `customer_id = 177`), causing Gold entity-table reconciliation gaps.

**Fix (implemented — Databricks validated):**

| Change | Detail |
|--------|--------|
| DQ execution order | `01` → `02` → `03` → **`05`** → **`04`** → persistence → curated writes |
| RI parent population | `curated_eligible_parent_keys_df()` in `silver_common.py` — same `filter_valid_rows()` semantics as curated dimension writes |
| Shared helpers | `failures_for_category()`, `filter_valid_rows()`, `curated_eligible_parent_keys_df()` moved to `silver_common.py`; `create_silver_tables.py` imports shared implementation |
| `04_quality_referential_integrity.py` | Accepts `dq_results`; uses curated-eligible parent keys instead of `prepare_canonical_entity_df()` |
| `06_write_dq_results.py` | Runs business_logic before referential_integrity; passes partial `dq_results` into module 04 |

**Invariant after fix:**

```text
∀ nonblank customer_id in silver_orders → EXISTS IN silver_customers
∀ nonblank product_id  in silver_orders → EXISTS IN silver_products
```

**Expected post-fix (confirm on Databricks):**

| Check | Expected | Observed |
|-------|----------|----------|
| `SERVERLESS_COMPAT_VERSION` | 10 | **10** |
| `silver_customers` | 878 (unchanged) | **878** |
| `silver_products` | 164 (unchanged) | **164** |
| `silver_orders` | < 3,832 | **3,646** |
| Reverse RI product FK diagnostic | 0 | **0** |
| Reverse RI customer FK diagnostic | 0 | **0** |
| Silver revenue | (from Databricks) | **2,708,411.08** |
| Silver quantity | (from Databricks) | **10,899** |
| Silver distinct orders | (from Databricks) | **2,052** |

**Databricks validation (Silver RI alignment):** **PASS** (`SERVERLESS_COMPAT_VERSION = 10`).

**Gold revalidation after fix:** **PASS** — entity Gold reconciles to new `silver_orders` (revenue 2,708,411.08; Phase 5 Gold **ACCEPTED**).

**FINAL DECISION (RI alignment):** **ACCEPTED**.

---

## Related Artifacts

- `data-quality-strategy.md` — rule definitions
- `data-model.md` — schemas and keys
- `src/data_generation/DATA_GENERATION_NOTES.md` — defect matrix
- `ai-prompts/silver-layer.md` — Cursor prompt history
- `tool-specific/cursor-workflow/task-breakdown.md` — granular Silver tasks
