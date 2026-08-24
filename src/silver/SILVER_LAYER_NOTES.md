# Silver Layer Notes — Design (Iteration 1 — Finalized)

**Status:** Iteration 2 implementation complete (completeness, uniqueness, type validation). Orchestration and Databricks validation pending Iteration 5.

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

## Databricks Execution (planned — Iteration 5)

```python
# Notebook cell pattern (same as Bronze)
from pathlib import Path
import sys
REPO = Path("/Workspace/Users/.../DE_C1_Coding_Evaluation")
sys.path.insert(0, str(REPO / "src/silver"))
from create_silver_tables import run_silver_pipeline  # TBD Iteration 5
run_silver_pipeline(spark=spark)
```

**Not validated yet** — design only.

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

## Iteration 2 Implementation (Complete)

| Module | Status | Defect IDs targeted |
|--------|--------|---------------------|
| `silver_common.py` | Implemented | Type trim/parse helpers, failure schema |
| `01_quality_completeness.py` | Implemented | D01, D02, D07 |
| `02_quality_uniqueness.py` | Implemented | D03, D08, D16 |
| `03_quality_type_validation.py` | Implemented | D04, D05, D09, D13 |

**Not yet implemented:** `04_referential_integrity`, `05_business_logic`, `create_silver_tables.py`, quarantine write, DQ summary write.

**Deterministic duplicate ranking:** partition by business key; order by tiebreaker columns (asc, nulls last) then row-content hash (no global window).

**Local validation:** `py_compile` + `test_silver_helpers.py` (pure-Python helpers). Databricks execution not performed in Cursor environment.

---

- `data-quality-strategy.md` — rule definitions
- `data-model.md` — schemas and keys
- `src/data_generation/DATA_GENERATION_NOTES.md` — defect matrix
- `ai-prompts/silver-layer.md` — Cursor prompt history
- `tool-specific/cursor-workflow/task-breakdown.md` — granular Silver tasks
