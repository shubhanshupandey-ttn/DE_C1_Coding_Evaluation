# Gold Layer Notes — Design (Iteration 1b — Finalized)

**Status:** Iteration 1b design **ACCEPTED**. Iterations 2–6 **implemented and Databricks validated** (`GOLD_SERVERLESS_COMPAT_VERSION = 1`). **Phase 5 Gold — COMPLETE / ACCEPTED** (post Silver RI alignment `SERVERLESS_COMPAT_VERSION = 10`).

Phase 5 Gold design defines analytical Delta tables built exclusively from validated Silver curated entities. Open ambiguities from Gold Iteration 1 are resolved in this document.

---

## Environment

| Item | Value |
|------|-------|
| Catalog | `de_c1_coding_evaluation` |
| Gold schema | `gold` |
| Silver schema (inputs) | `silver` |

Fully qualified examples:

- `de_c1_coding_evaluation.gold.gold_sales_by_product`
- `de_c1_coding_evaluation.silver.silver_orders`

---

## Objective

Produce **four pre-computed analytical Delta tables** from trusted Silver data to support dashboard-style analytics:

1. Sales by product
2. Revenue by customer
3. Daily / weekly trends
4. Customer segmentation

Gold does **not** perform data quality enforcement. Silver is the trusted input layer.

---

## Source Tables (Silver only)

Gold reads **only** from validated Silver curated tables:

| Table | FQN | Reference row count (validation only — do not hard-code) |
|-------|-----|----------------------------------------------------------|
| Customers | `de_c1_coding_evaluation.silver.silver_customers` | 878 |
| Products | `de_c1_coding_evaluation.silver.silver_products` | 164 |
| Orders (line items) | `de_c1_coding_evaluation.silver.silver_orders` | 3,832 |

**Gold must NOT read:**

- Bronze tables
- `silver_quarantine_records`
- `silver_dq_summary`
- Raw CSV files
- Silver DQ intermediate DataFrames

---

## Shared Metric Definitions

### Revenue

```
line_revenue = quantity * unit_price   (per order line)
```

- Derived in Gold only — **not** a Silver column.
- All Gold `total_revenue` / `total_spend` metrics use `sum(quantity * unit_price)` unless noted otherwise.

### Order count

```
order_count = count(distinct order_id)
```

- Represents **business orders**, not order lines.
- `silver_orders` is line-item grain; one `order_id` may span multiple lines.
- Do **not** use `count(*)` or `count(order_line_id)` for order counts.

### Frequency (customer segmentation)

```
frequency = count(distinct order_id)
```

- Distinct business orders per customer — not order-line count.

---

## Gold Output Tables

All four outputs are **Delta tables** in schema `gold`, rebuilt with **overwrite** semantics each run.

| # | Table | SQL file (planned) | Grain |
|---|-------|-------------------|-------|
| 1 | `gold_sales_by_product` | `01_sales_by_product.sql` | One row per product with ≥1 Silver order line |
| 2 | `gold_revenue_by_customer` | `02_revenue_by_customer.sql` | One row per customer with ≥1 Silver order |
| 3 | `gold_daily_weekly_trends` | `03_daily_weekly_trends.sql` | One row per (`time_grain`, `period_start`) |
| 4 | `gold_customer_segmentation` | `04_customer_segmentation.sql` | One row per customer with ≥1 Silver order |

No additional Gold analytical tables unless future repository specification requires them.

---

## Table 1 — `gold_sales_by_product`

**Sources:** `silver_orders`, `silver_products`

**Join:** `silver_orders.product_id = silver_products.product_id` (**inner**)

**Grain:** One row per product with at least one valid Silver order line.

| Column | Type (Gold) | Definition |
|--------|-------------|------------|
| `product_id` | STRING | `silver_products.product_id` |
| `product_name` | STRING | `silver_products.product_name` |
| `category` | STRING | `silver_products.category` |
| `total_quantity` | BIGINT | `sum(quantity)` |
| `total_revenue` | DECIMAL | `sum(quantity * unit_price)` |

Products with zero Silver order lines are **excluded**.

---

## Table 2 — `gold_revenue_by_customer`

**Sources:** `silver_orders`, `silver_customers`

**Join:** `silver_orders.customer_id = silver_customers.customer_id` (**inner**)

**Grain:** One row per customer with at least one valid Silver order.

| Column | Type (Gold) | Definition |
|--------|-------------|------------|
| `customer_id` | STRING | `silver_orders.customer_id` |
| `total_revenue` | DECIMAL | `sum(quantity * unit_price)` |

Customer dimension attributes (`customer_name`, `country`, etc.) are **not** required in this output.

Customers with zero Silver orders are **excluded**.

---

## Table 3 — `gold_daily_weekly_trends`

**Source:** `silver_orders` only (no dimension join)

**Grain:** One row per (`time_grain`, `period_start`) — daily and weekly rows in a **single** table.

| Column | Type (Gold) | Definition |
|--------|-------------|------------|
| `time_grain` | STRING | `'day'` or `'week'` (exactly these two values) |
| `period_start` | DATE | Start of the analytical period (see below) |
| `total_revenue` | DECIMAL | `sum(quantity * unit_price)` |
| `order_count` | BIGINT | `count(distinct order_id)` |

### Daily rows

| Field | Value |
|-------|-------|
| `time_grain` | `'day'` |
| `period_start` | `order_date` |

### Weekly rows

| Field | Value |
|-------|-------|
| `time_grain` | `'week'` |
| `period_start` | **Monday** of the calendar week containing `order_date` |

- Monday-start calendar weeks only — **not** Sunday-start.
- Do **not** split into separate daily and weekly Gold tables.

---

## Table 4 — `gold_customer_segmentation`

**Sources:** `silver_customers`, `silver_orders`

**Join:** `silver_customers.customer_id = silver_orders.customer_id` (**inner**)

**Grain:** One row per customer with at least one valid Silver order.

| Column | Type (Gold) | Definition |
|--------|-------------|------------|
| `customer_id` | STRING | `silver_customers.customer_id` |
| `customer_segment` | STRING | `silver_customers.customer_segment` |
| `lifetime_value` | DECIMAL(12,2) | `silver_customers.lifetime_value` |
| `frequency` | BIGINT | `count(distinct order_id)` |
| `total_spend` | DECIMAL | `sum(quantity * unit_price)` |

Customers with zero Silver orders are **excluded**.

---

## Zero-Order Entity Rule

| Gold table | Include entities without orders? |
|------------|----------------------------------|
| `gold_sales_by_product` | **No** — products with ≥1 order line only |
| `gold_revenue_by_customer` | **No** — customers with ≥1 order only |
| `gold_customer_segmentation` | **No** — customers with ≥1 order only |
| `gold_daily_weekly_trends` | N/A — order-driven time periods only |

Do not fabricate zero-revenue rows for inactive products or customers.

---

## Join Semantics Summary

| Gold table | Join pattern | Type |
|------------|--------------|------|
| Sales by product | `silver_orders` → `silver_products` on `product_id` | Inner |
| Revenue by customer | `silver_orders` → `silver_customers` on `customer_id` | Inner |
| Daily / weekly trends | `silver_orders` only | — |
| Customer segmentation | `silver_customers` → `silver_orders` on `customer_id` | Inner |

Silver has already enforced referential integrity on the curated order set. Gold does **not** add RI checks.

---

## Write / Idempotency Semantics

| Behavior | Value |
|----------|-------|
| Write mode | Delta **overwrite** per Gold table |
| Accumulation | None — repeated runs on same Silver produce identical Gold |
| MERGE / upsert | **Not used** unless a future requirement explicitly adds it |

Orchestration entry point (planned): `create_gold_tables.py` — implementation deferred to later iteration.

---

## Output Restrictions

Final Gold tables must **not** contain:

- `*_typed`, `_dup_rank`, `_row_num`
- `_customer_parent_ok`, `_product_parent_ok`, `_catalog_unit_price_typed`
- `_ingestion_timestamp`, `_source_file`
- DQ / quarantine fields (`failure_reason`, `check_category`, `bronze_source_values`, etc.)

---

## Aggregate Sanity Validation Rule

The following reconciliation must hold (subject to normal decimal rounding):

```
sum(gold_sales_by_product.total_revenue)
  = sum(gold_revenue_by_customer.total_revenue)
  = sum(silver_orders.quantity * silver_orders.unit_price)
```

Use this as a primary Gold validation check in Databricks.

---

## Silver / Gold Boundary

| Responsibility | Layer |
|----------------|-------|
| DQ, quarantine, typing, FK validation | Silver |
| Curated entity tables | Silver |
| Analytical aggregation, revenue/order metrics | Gold |
| Dashboard queries | Dashboard (Phase 6 — not started) |

---

## Acceptance Criteria (for implementation validation)

| # | Criterion |
|---|-----------|
| G-1 | Four Gold Delta tables exist at documented FQNs |
| G-2 | Gold reads Silver curated tables only |
| G-3 | Column sets match finalized contract per table |
| G-4 | No forbidden helper/DQ columns in Gold outputs |
| G-5 | `order_count` and `frequency` use `count(distinct order_id)` |
| G-6 | Weekly `period_start` uses Monday-start calendar weeks |
| G-7 | `time_grain` values are exactly `'day'` and `'week'` |
| G-8 | Zero-order products/customers excluded from entity-grain tables |
| G-9 | Aggregate sanity reconciliation passes |
| G-10 | Re-run overwrite produces identical row counts (idempotent) |

---

## Remaining Implementation Steps

| Step | Deliverable | Status |
|------|-------------|--------|
| Gold Iteration 2 | `01_sales_by_product.sql` | **Done** (Databricks pending) |
| Gold Iteration 3 | `02_revenue_by_customer.sql` | **Done** (Databricks pending) |
| Gold Iteration 4 | `03_daily_weekly_trends.sql` | **Done** (Databricks pending) |
| Gold Iteration 5 | `04_customer_segmentation.sql` | **Done** (Databricks pending) |
| Gold Iteration 6 | `create_gold_tables.py` + Databricks validation | **Orchestration done** — Databricks validation **pending** |

---

## Iteration 2 Implementation — Sales by Product

| Item | Value |
|------|-------|
| File | `src/gold/01_sales_by_product.sql` |
| Target table | `de_c1_coding_evaluation.gold.gold_sales_by_product` |
| Sources | `silver_orders`, `silver_products` |
| Join | Inner on `product_id` |
| Write mode | `CREATE OR REPLACE TABLE` (Delta overwrite) |
| Local validation | Static SQL review — **PASS** |
| Databricks validation | **Pending** |

**SQL approach:** `CREATE SCHEMA IF NOT EXISTS` → `CREATE OR REPLACE TABLE ... USING DELTA AS` with explicit `SELECT` of five analytical columns, inner join, `GROUP BY` product attributes, `SUM(quantity)` and `SUM(quantity * unit_price)`.

---

## Iteration 3 Implementation — Revenue by Customer

| Item | Value |
|------|-------|
| File | `src/gold/02_revenue_by_customer.sql` |
| Target table | `de_c1_coding_evaluation.gold.gold_revenue_by_customer` |
| Sources | `silver_orders`, `silver_customers` |
| Join | Inner on `customer_id` |
| Write mode | `CREATE OR REPLACE TABLE` (Delta overwrite) |
| Local validation | Static SQL review — **PASS** |
| Databricks validation | **Pending** |

**SQL approach:** Silver orders inner join Silver customers on `customer_id`, `GROUP BY customer_id`, `SUM(quantity * unit_price)` as `total_revenue`. Two output columns only. Independent of `gold_sales_by_product`.

---

## Iteration 4 Implementation — Daily / Weekly Trends

| Item | Value |
|------|-------|
| File | `src/gold/03_daily_weekly_trends.sql` |
| Target table | `de_c1_coding_evaluation.gold.gold_daily_weekly_trends` |
| Source | `silver_orders` only |
| Write mode | `CREATE OR REPLACE TABLE` (Delta overwrite) |
| Local validation | Static SQL review — **PASS** |
| Databricks validation | **Pending** |

**SQL approach:** Two aggregations on `silver_orders` — daily (`time_grain = 'day'`, `period_start = order_date`) and weekly (`time_grain = 'week'`, `period_start = CAST(date_trunc('week', order_date) AS DATE)` for Monday-start weeks). Combined via `UNION ALL`. Metrics: `SUM(quantity * unit_price)`, `COUNT(DISTINCT order_id)`.

---

## Iteration 5 Implementation — Customer Segmentation

| Item | Value |
|------|-------|
| File | `src/gold/04_customer_segmentation.sql` |
| Target table | `de_c1_coding_evaluation.gold.gold_customer_segmentation` |
| Sources | `silver_customers`, `silver_orders` |
| Join | Inner on `customer_id` |
| Write mode | `CREATE OR REPLACE TABLE` (Delta overwrite) |
| Local validation | Static SQL review — **PASS** |
| Databricks validation | **Pending** (Iteration 6) |

**SQL approach:** `silver_customers` inner join `silver_orders` on `customer_id`, `GROUP BY customer_id, customer_segment, lifetime_value`, `frequency = COUNT(DISTINCT order_id)`, `total_spend = SUM(quantity * unit_price)`. Five analytical columns only.

---

## Alignment with Repository Specification

| Source document | Alignment |
|-----------------|-----------|
| `data-model.md` § Gold Consumption | **Aligned** — themes, joins, aggregates match; Iteration 1b adds column names, grains, order-count definition |
| `design-notes.md` § Gold Layer Design | **Aligned** — four SQL themes preserved; formulas/time grains now finalized in this document |
| `requirements-analysis.md` | **Aligned** — four analytical datasets; metric definitions resolved here |
| `tool-specific/cursor-workflow/spec.md` § Gold Analytics Support | **Aligned** |

**No unresolved conflicts** between this contract and repository specification.

---

## Related Artifacts

- `data-model.md` — domain model and Gold consumption themes
- `design-notes.md` — high-level architecture
- `src/silver/SILVER_LAYER_NOTES.md` — Silver inputs and validated schemas
- `ai-prompts/gold-layer.md` — Cursor prompt history
- `tool-specific/cursor-workflow/task-breakdown.md` — Phase 5 task plan

---

## Iteration 6 Implementation — Orchestration + Validation

| Item | Value |
|------|-------|
| File | `src/gold/create_gold_tables.py` |
| Entry points | `run_gold_pipeline(spark=spark)`, `validate_gold_pipeline(spark=spark)`, `validate_idempotency(spark=spark)`, `evaluate_acceptance_criteria(spark=spark)` |
| SQL execution order | `01_sales_by_product.sql` → `02_revenue_by_customer.sql` → `03_daily_weekly_trends.sql` → `04_customer_segmentation.sql` |
| SQL loading | Read from `Path(__file__).resolve().parent`; comment-stripped statement split on `;`; executed via `spark.sql()` |
| Write mode | Delegated to SQL files (`CREATE OR REPLACE TABLE ... USING DELTA AS`) |
| Serverless | DataFrame / Spark SQL only — no RDD APIs |
| Local validation | `python3 -m py_compile src/gold/create_gold_tables.py` — **PASS** |
| Databricks validation | **Not performed in Cursor agent environment** (PySpark unavailable; Databricks CLI not installed) |

### Databricks Execution (notebook pattern)

```python
# Notebook cell — Gold Iteration 6 (Serverless)
# IMPORTANT: register module in sys.modules BEFORE exec_module (Databricks requirement)
import importlib.util, json, sys
from pathlib import Path

gold_dir = Path("/Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/src/gold")
for name in list(sys.modules):
    if name == "create_gold_tables" or name.startswith("create_gold_tables."):
        del sys.modules[name]
sys.path.insert(0, str(gold_dir))

spec = importlib.util.spec_from_file_location("create_gold_tables", gold_dir / "create_gold_tables.py")
create_gold_tables = importlib.util.module_from_spec(spec)
sys.modules["create_gold_tables"] = create_gold_tables
spec.loader.exec_module(create_gold_tables)

print("GOLD_SERVERLESS_COMPAT_VERSION =", create_gold_tables.GOLD_SERVERLESS_COMPAT_VERSION)

pipeline_result = create_gold_tables.run_gold_pipeline(spark=spark)
validation = create_gold_tables.validate_gold_pipeline(spark=spark)
idempotency = create_gold_tables.validate_idempotency(spark=spark)
acceptance = create_gold_tables.evaluate_acceptance_criteria(spark=spark)
acceptance["AC-10_idempotent"] = (
    idempotency["row_counts_match"] and idempotency["totals_match"]
)

print(json.dumps({
    "pipeline": pipeline_result,
    "row_counts": validation["row_counts"],
    "schema_match": {k: v["match"] for k, v in validation["schema"].items()},
    "grain": validation["grain"],
    "reconciliations": validation["reconciliations"],
    "trends": validation["trends"],
    "join_behavior": validation["join_behavior"],
    "segmentation": validation["segmentation"],
    "idempotency": idempotency,
    "acceptance": {k: v for k, v in acceptance.items() if k.startswith("AC-")},
}, indent=2, default=str))
```

**Prerequisite:** Silver curated tables after RI alignment (`SERVERLESS_COMPAT_VERSION = 10`): `silver_customers` 878 / `silver_products` 164 / `silver_orders` 3,646.

### Runtime validation evidence (Databricks Serverless — post Silver RI alignment)

**Execution:** `run_gold_pipeline(spark=spark)` + `validate_gold_pipeline` + `validate_idempotency` (`GOLD_SERVERLESS_COMPAT_VERSION = 1`).

#### Row counts

| Table | Rows |
|-------|------|
| `silver_customers` | 878 |
| `silver_products` | 164 |
| `silver_orders` | 3,646 |
| `gold_sales_by_product` | 164 |
| `gold_revenue_by_customer` | 792 |
| `gold_daily_weekly_trends` | 950 (818 day + 132 week) |
| `gold_customer_segmentation` | 792 |

#### Reconciliation (all **PASS**)

| Check | Silver | Gold | Match |
|-------|--------|------|-------|
| Revenue | 2,708,411.08 | sales / customer / daily trends / segmentation | **true** |
| Quantity | 10,899 | sales-by-product | **true** |
| Distinct orders (daily trend sum) | 2,052 | daily `order_count` sum | **true** |
| Frequency per customer | — | mismatch rows | **0** |
| Spend per customer | — | mismatch rows | **0** |

#### Idempotency (**PASS**)

| Check | Result |
|-------|--------|
| Row counts (run 1 vs run 2) | **Identical** |
| Sales + customer revenue totals | **2,708,411.08** both runs |
| `row_counts_match` | **true** |
| `totals_match` | **true** |

#### Acceptance criteria AC-1..AC-11

| AC | Criterion | Result |
|----|-----------|--------|
| AC-1 | Orchestrator on Serverless | **PASS** |
| AC-2 | Four Gold tables exist | **PASS** |
| AC-3 | Sales-by-product contract | **PASS** |
| AC-4 | Revenue-by-customer grain + columns | **PASS** |
| AC-5 | Daily/weekly trends contract | **PASS** |
| AC-6 | Segmentation contract | **PASS** |
| AC-7 | No helper columns | **PASS** (prior schema validation) |
| AC-8 | Silver entity tables only | **PASS** |
| AC-9 | Join keys match contract | **PASS** |
| AC-10 | Idempotent overwrite | **PASS** |
| AC-11 | Revenue/quantity reconciliation | **PASS** |

**FINAL DECISION (Iteration 6):** **ACCEPTED** — Phase 5 Gold **COMPLETE**.

---

## Silver RI Alignment Impact on Gold (post-fix)

**Context:** Gold Iteration 6 Databricks validation initially showed entity-level revenue gaps because `silver_orders` contained FKs absent from curated dimensions while RI used `canonical_valid_filter()` parents. Silver `SERVERLESS_COMPAT_VERSION = 10` aligns RI parent keys with curated dimension eligibility (`filter_valid_rows()`).

**Gold SQL:** **Unchanged** — entity tables still use `INNER JOIN` to `silver_customers` / `silver_products`.

**Required revalidation sequence:** **Complete** (2026-08-27 Databricks Serverless).

| Step | Result |
|------|--------|
| Silver `run_silver_pipeline` (`SERVERLESS_COMPAT_VERSION = 10`) | **PASS** — 878 / 164 / 3,646 |
| Reverse RI diagnostics | **0** orphan product + customer FKs |
| Gold `run_gold_pipeline` (no Gold SQL changes) | **PASS** |
| Entity Gold reconciles to `silver_orders` | **PASS** — revenue 2,708,411.08; quantity 10,899 |
| Gold idempotency | **PASS** |

**Gold ACCEPTED status:** **ACCEPTED** — Phase 5 Gold **COMPLETE**.
