# AI Prompts — Gold Layer

Evidence artifact for Phase 5 Gold implementation (Cursor-assisted development).

---

## Iteration 1: Gold Design & Requirements Extraction

**PROMPT SENT:**

> Phase 5 Gold Layer — requirements/design extraction only. Review repository docs and validated Silver. Produce structured design report. Do NOT implement Gold code.

**AI RESPONSE SUMMARY:**

Reviewed foundation docs (`data-model.md`, `design-notes.md`, `requirements-analysis.md`, `spec.md`), Silver validation evidence (`SILVER_LAYER_NOTES.md`), and data generation notes.

**Four analytical themes identified (repository-specified):**

1. Sales by product
2. Revenue by customer
3. Daily / weekly trends
4. Customer segmentation

**Deliverables planned by repository:** SQL files (`01`–`04`) + `create_gold_tables.py` + `ai-prompts/gold-layer.md`.

**Ambiguities flagged for Iteration 1b:**

- Gold schema / table names
- Output column names and types
- Daily vs weekly table structure
- Weekly calendar definition
- Order-count definition (`order_id` vs line grain)
- Frequency definition
- Zero-order entity inclusion
- Join types and write semantics

**FINAL DECISION:** Design extraction complete. Proceed to Iteration 1b refinement.

---

## Iteration 1b: Design Refinement / Freeze Gold Contract

**PROMPT SENT:**

> Gold Iteration 1b — resolve ambiguities and freeze Gold contract. Design only. No SQL, no `create_gold_tables.py`. Do not modify Bronze or Silver.

**AI RESPONSE SUMMARY:**

Created authoritative Gold design contract in `src/gold/GOLD_LAYER_NOTES.md`. Updated `tool-specific/cursor-workflow/task-breakdown.md` for Phase 5 iterations.

**Finalized decisions:**

| Area | Decision |
|------|----------|
| Catalog | `de_c1_coding_evaluation` |
| Schema | `gold` |
| Tables | `gold_sales_by_product`, `gold_revenue_by_customer`, `gold_daily_weekly_trends`, `gold_customer_segmentation` |
| Sources | `silver_customers`, `silver_products`, `silver_orders` only |
| Revenue | `sum(quantity * unit_price)` — derived in Gold, not stored in Silver |
| Order count | `count(distinct order_id)` |
| Frequency | `count(distinct order_id)` per customer |
| Weekly grain | Monday-start calendar week; `period_start` = Monday |
| Trends structure | Single table with `time_grain` ∈ {`day`, `week`} |
| Zero-order entities | Excluded from entity-grain Gold tables |
| Joins | Inner joins for entity analytical outputs |
| Write mode | Delta overwrite (idempotent) |
| Sanity check | `sum(total_revenue)` reconciles across product/customer Gold and `silver_orders` |

**Table contracts:**

| Table | Grain | Columns |
|-------|-------|---------|
| `gold_sales_by_product` | Per product (with orders) | `product_id`, `product_name`, `category`, `total_quantity`, `total_revenue` |
| `gold_revenue_by_customer` | Per customer (with orders) | `customer_id`, `total_revenue` |
| `gold_daily_weekly_trends` | Per (`time_grain`, `period_start`) | `time_grain`, `period_start`, `total_revenue`, `order_count` |
| `gold_customer_segmentation` | Per customer (with orders) | `customer_id`, `customer_segment`, `lifetime_value`, `frequency`, `total_spend` |

**Repository alignment check:**

| Document | Result |
|----------|--------|
| `data-model.md` § Gold Consumption | Aligned |
| `design-notes.md` § Gold Layer Design | Aligned (formulas/grains now finalized) |
| `requirements-analysis.md` | Aligned (metric definitions resolved) |
| `spec.md` § Gold Analytics Support | Aligned |

**Conflicts:** None identified.

**Remaining ambiguities for implementation:** None blocking the four Gold outputs. Minor implementation choices (exact `DECIMAL` precision for aggregated revenue columns, Spark SQL week-start function) deferred to coding iteration.

**Validation performed:** Documentation only — no Databricks run.

**YOUR EVALUATION:**

_To be completed by developer._

**FINAL DECISION:** **ACCEPTED** — Gold design contract frozen. Implementation may proceed in Gold Iteration 2.

---

## Iteration 2: Sales by Product

**PROMPT SENT:**

> Gold Iteration 2 ONLY: implement `01_sales_by_product.sql` per frozen `GOLD_LAYER_NOTES.md` contract. No other Gold outputs. No Bronze/Silver changes.

**AI RESPONSE SUMMARY:**

Created `src/gold/01_sales_by_product.sql`:

- Sources: `de_c1_coding_evaluation.silver.silver_orders`, `silver_products`
- Inner join on `product_id`
- `GROUP BY product_id, product_name, category`
- `total_quantity = SUM(quantity)`, `total_revenue = SUM(quantity * unit_price)`
- Target: `de_c1_coding_evaluation.gold.gold_sales_by_product`
- Write: `CREATE OR REPLACE TABLE` (Delta overwrite)

**Validation performed (local):**

| Check | Result |
|-------|--------|
| SQL reads only specified Silver tables | **PASS** |
| No `SELECT *` | **PASS** |
| Five output columns only | **PASS** |
| Inner join (products without orders excluded) | **PASS** |
| Databricks execution | **Not performed** |

**FINAL DECISION:** Iteration 2 implementation complete. Databricks validation deferred to Iteration 6.

---

## Iteration 3: Revenue by Customer

**PROMPT SENT:**

> Gold Iteration 3 ONLY: implement `02_revenue_by_customer.sql` per frozen contract. Independent Silver reads only. No other Gold outputs.

**AI RESPONSE SUMMARY:**

Created `src/gold/02_revenue_by_customer.sql`:

- Sources: `silver_orders`, `silver_customers` (not `gold_sales_by_product`)
- Inner join on `customer_id`
- `GROUP BY customer_id`
- `total_revenue = SUM(quantity * unit_price)`
- Output columns: `customer_id`, `total_revenue` only
- Target: `de_c1_coding_evaluation.gold.gold_revenue_by_customer`
- Write: `CREATE OR REPLACE TABLE` (Delta overwrite)

**Validation performed (local):**

| Check | Result |
|-------|--------|
| Reads only specified Silver tables | **PASS** |
| No `SELECT *` | **PASS** |
| Two output columns only | **PASS** |
| No Gold/Bronze/quarantine references | **PASS** |
| Databricks execution | **Not performed** |

**FINAL DECISION:** Iteration 3 implementation complete. Databricks validation deferred to Iteration 6.

---

## Iteration 4: Daily / Weekly Trends

**PROMPT SENT:**

> Gold Iteration 4 ONLY: implement `03_daily_weekly_trends.sql` per frozen contract. `silver_orders` only. Daily + weekly in one table via UNION ALL.

**AI RESPONSE SUMMARY:**

Created `src/gold/03_daily_weekly_trends.sql`:

- Source: `silver_orders` only (no joins)
- Daily: `time_grain = 'day'`, `period_start = order_date`, group by `order_date`
- Weekly: `time_grain = 'week'`, `period_start = CAST(date_trunc('week', order_date) AS DATE)` (Monday-start)
- Metrics: `total_revenue = SUM(quantity * unit_price)`, `order_count = COUNT(DISTINCT order_id)`
- Combined via `UNION ALL`
- Target: `de_c1_coding_evaluation.gold.gold_daily_weekly_trends`
- Write: `CREATE OR REPLACE TABLE` (Delta overwrite)

**Validation performed (local):**

| Check | Result |
|-------|--------|
| Source is only `silver_orders` | **PASS** |
| Four output columns only | **PASS** |
| No `SELECT *` | **PASS** |
| No Bronze/quarantine/Gold references | **PASS** |
| `UNION ALL` daily + weekly | **PASS** |
| Databricks execution | **Not performed** |

**FINAL DECISION:** Iteration 4 implementation complete. Databricks validation deferred to Iteration 6.

---

## Iteration 5: Customer Segmentation

**PROMPT SENT:**

> Gold Iteration 5 ONLY: implement `04_customer_segmentation.sql` per frozen `GOLD_LAYER_NOTES.md`. Inner join Silver customers and orders. Five output columns. No orchestration.

**AI RESPONSE SUMMARY:**

Created `src/gold/04_customer_segmentation.sql`:

- Sources: `silver_customers`, `silver_orders`
- Inner join on `customer_id`
- `GROUP BY customer_id, customer_segment, lifetime_value`
- `frequency = COUNT(DISTINCT order_id)`
- `total_spend = SUM(quantity * unit_price)`
- Target: `de_c1_coding_evaluation.gold.gold_customer_segmentation`
- Write: `CREATE OR REPLACE TABLE` (Delta overwrite)

**Validation performed (local):**

| Check | Result |
|-------|--------|
| Only specified Silver tables | **PASS** |
| Inner join on `customer_id` | **PASS** |
| Five output columns only | **PASS** |
| `COUNT(DISTINCT order_id)` for frequency | **PASS** |
| No `SELECT *` / Bronze / quarantine / Gold refs | **PASS** |
| Databricks execution | **Not performed** |

**FINAL DECISION:** Iteration 5 implementation complete. Databricks validation deferred to Iteration 6.

---

## Iteration 6: Orchestration + Databricks validation

> Gold Iteration 6 — implement `create_gold_tables.py`, run on Databricks Serverless, validate all four Gold tables, reconcile against Silver, test idempotency, update documentation.

### Implementation (Cursor agent — 2026-08-26)

| Item | Detail |
|------|--------|
| File created | `src/gold/create_gold_tables.py` |
| Functions | `run_gold_pipeline`, `validate_gold_pipeline`, `validate_idempotency`, `evaluate_acceptance_criteria` |
| SQL order | `01` → `02` → `03` → `04` (files in `src/gold/`, not duplicated in Python) |
| Serverless | Spark SQL only; `GOLD_SERVERLESS_COMPAT_VERSION = 1` |
| Local validation | `py_compile` **PASS** |

### Static validation

| Check | Result |
|-------|--------|
| Four SQL files executed in order | **PASS** (code review) |
| No RDD APIs | **PASS** |
| No Bronze/Silver/quarantine reads in Gold SQL | **PASS** |
| Expected column contracts in `EXPECTED_COLUMNS` | **PASS** |
| Validation helpers for schema, grain, reconciliation, trends, joins, segmentation, idempotency | **PASS** |

### Databricks validation

| Check | Result |
|-------|--------|
| `run_gold_pipeline(spark=spark)` on Serverless | **Not performed** (PySpark/Databricks CLI unavailable in Cursor agent environment) |
| Runtime row counts | **Not recorded** |
| Reconciliation queries | **Not executed** |
| Idempotency (two runs) | **Not executed** |
| AC-1..AC-11 | **Pending** |

Notebook execution pattern documented in `src/gold/GOLD_LAYER_NOTES.md` § Iteration 6.

**FINAL DECISION:** Orchestration implementation **complete**. Databricks Serverless runtime validation **not performed** in this environment. **Phase 5 Gold — NOT YET ACCEPTED.**

---

## Cursor Evaluation Evidence (Phase 5 — in progress)

| Requirement | Evidence |
|-------------|----------|
| Persistent context | Foundation docs + Silver validation + `GOLD_LAYER_NOTES.md` |
| Iteration | Deliberate multi-iteration plan; design before code |
| Validation | Iterations 2–5 local SQL review **PASS**; Iteration 6 orchestration `py_compile` **PASS**; Databricks runtime **pending** |
| Human review | Iteration 1b **ACCEPTED**; Phase 5 completion requires Databricks evidence |
