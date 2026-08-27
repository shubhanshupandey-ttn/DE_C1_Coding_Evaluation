# Dashboard Guide — Phase 6

Consumption layer for **Gold** analytical tables on Databricks. Dashboard SQL does not read Bronze, Silver, raw CSV files, quarantine tables, or DQ summary tables.

---

## 1. Overview

```text
Bronze  →  Silver  →  Gold  →  Dashboard SQL  →  Databricks SQL visualizations
```

| Layer | Role |
|-------|------|
| Bronze | Raw ingest |
| Silver | Cleansed, validated entities and order lines |
| Gold | Pre-computed aggregates and dimensions for analytics |
| **Dashboard** | Visualization-ready `SELECT` queries over Gold only |

Business logic (revenue, order counts, segments, weekly boundaries) is defined in Gold. Dashboard queries **consume** those metrics; they do not redefine them or join back to lower layers.

**Artifacts:**

| File | Purpose |
|------|---------|
| `src/dashboard/dashboard_queries.sql` | Query catalog (10 queries, 4 themes) |
| `src/dashboard/DASHBOARD_GUIDE.md` | This guide |

---

## 2. Prerequisites

- Databricks workspace with access to catalog `de_c1_coding_evaluation`
- **Gold schema** populated (`de_c1_coding_evaluation.gold.*`)
- Gold pipeline run successfully (`src/gold/create_gold_tables.py` on Serverless or equivalent)
- Databricks SQL (SQL editor or SQL warehouse) for ad hoc execution and visualizations

---

## 3. Gold dependencies

Dashboard reads **only** these four Gold tables:

| FQN | Grain | Key columns |
|-----|-------|-------------|
| `de_c1_coding_evaluation.gold.gold_sales_by_product` | One row per product with ≥1 order | `product_id`, `product_name`, `category`, `total_quantity`, `total_revenue` |
| `de_c1_coding_evaluation.gold.gold_revenue_by_customer` | One row per customer with ≥1 order | `customer_id`, `total_revenue` |
| `de_c1_coding_evaluation.gold.gold_daily_weekly_trends` | One row per (`time_grain`, `period_start`) | `time_grain` (`'day'` \| `'week'`), `period_start`, `total_revenue`, `order_count` |
| `de_c1_coding_evaluation.gold.gold_customer_segmentation` | One row per customer with ≥1 order | `customer_id`, `customer_segment`, `lifetime_value`, `frequency`, `total_spend` |

**Trend semantics:** Weekly rows use `time_grain = 'week'` with `period_start` = Monday of the calendar week (Spark `date_trunc('week')`). Do not recompute week boundaries in Dashboard SQL.

**Global totals:** Use entity Gold tables or KPI queries — do **not** sum daily and weekly trend rows together (double-counting).

**Column scope:** `order_count` exists only on `gold_daily_weekly_trends`. `gold_sales_by_product` exposes `total_quantity` and `total_revenue` only — do not reference `order_count` (or any other column) from the product table.

---

## 4. Query catalog

All queries live in `dashboard_queries.sql`. Execute one block at a time in Databricks SQL.

### 1. Product Performance (`gold_sales_by_product`)

| Query | Purpose | Output grain | Key columns | Recommended viz |
|-------|---------|--------------|---------------|-----------------|
| `top_products_by_revenue` | Top 10 products by revenue | Product | `product_name`, `category`, `total_revenue`, `total_quantity` | Horizontal bar chart |
| `top_products_by_quantity` | Top 10 products by units sold | Product | `product_name`, `category`, `total_quantity`, `total_revenue` | Horizontal bar chart |
| `revenue_by_category` | Revenue and quantity by product category | Category | `category`, `product_count`, `total_quantity`, `total_revenue` | Bar or donut chart |

### 2. Customer Revenue (`gold_revenue_by_customer`)

| Query | Purpose | Output grain | Key columns | Recommended viz |
|-------|---------|--------------|---------------|-----------------|
| `top_customers_by_revenue` | Top 10 customers by revenue | Customer | `customer_id`, `total_revenue` | Bar chart |
| `customer_revenue_summary_kpis` | Portfolio KPIs (count, sum, avg, min, max) | Single summary row | `customer_count`, `total_revenue`, `avg_revenue_per_customer`, … | Counter / KPI cards |

### 3. Revenue / Trends (`gold_daily_weekly_trends`)

| Query | Purpose | Output grain | Key columns | Recommended viz |
|-------|---------|--------------|---------------|-----------------|
| `daily_revenue_trend` | Daily revenue and orders over time | Day (`period_start`) | `period_start`, `total_revenue`, `order_count` | Line chart (revenue); optional second series for orders |
| `weekly_revenue_trend` | Weekly revenue and orders | Week (`period_start` = Monday) | `period_start`, `total_revenue`, `order_count` | Line chart |
| `daily_order_trend` | Daily distinct order count | Day | `period_start`, `order_count` | Line chart |
| `weekly_order_trend` | Weekly distinct order count | Week | `period_start`, `order_count` | Line chart |

Filter `time_grain` in SQL — do not mix daily and weekly rows in one chart without an explicit grain dimension.

### 4. Customer Segmentation (`gold_customer_segmentation`)

| Query | Purpose | Output grain | Key columns | Recommended viz |
|-------|---------|--------------|---------------|-----------------|
| `segment_summary` | Customers and spend metrics by segment | Segment | `customer_segment`, `customer_count`, `total_spend`, `avg_total_spend`, `avg_frequency`, `avg_lifetime_value` | Grouped bar chart |
| `segment_spend_share` | Spend share by segment | Segment | `customer_segment`, `total_spend`, `pct_of_total_spend` | Pie, donut, or bar chart |

**Metric notes (from Gold):**

- `total_revenue` / `total_spend`: `SUM(quantity * unit_price)` at Silver order-line grain, aggregated in Gold.
- `order_count`: `COUNT(DISTINCT order_id)` per trend period — **only** on `gold_daily_weekly_trends`.
- `frequency`: `COUNT(DISTINCT order_id)` per customer — **only** on `gold_customer_segmentation`.
- `total_quantity`: units sold — **only** on `gold_sales_by_product` (product-level volume proxy; not order count).
- `lifetime_value`: Customer attribute from Silver (not recomputed in Dashboard).
- `customer_segment`: Customer attribute from Silver (not redefined in Dashboard).

---

## 5. Running the SQL

1. Open **Databricks** → **SQL** (or a notebook with `%sql` on a SQL warehouse).
2. Confirm Gold tables exist:  
   `SHOW TABLES IN de_c1_coding_evaluation.gold;`
3. Open or paste contents of `src/dashboard/dashboard_queries.sql`.
4. Run **one query block** at a time (each block starts with `-- Query: <name>`).
5. From the result grid, use **Add visualization** (or equivalent) to bind columns to chart types listed above.
6. To build a **SQL Dashboard**: save each query as a query object, add visualizations, then assemble them on a dashboard page. Exact UI labels may vary by workspace version; use the query result + visualization workflow your workspace provides.

---

## 6. Recommended visualizations

| Theme | Query | Chart type |
|-------|-------|------------|
| Product | `top_products_by_revenue`, `top_products_by_quantity` | Bar chart (`product_name` vs metric) |
| Product | `revenue_by_category` | Bar or donut (`category` vs `total_revenue`) |
| Customer | `top_customers_by_revenue` | Bar chart |
| Customer | `customer_revenue_summary_kpis` | KPI counters |
| Trends | `daily_revenue_trend`, `weekly_revenue_trend` | Line chart (`period_start` on X) |
| Trends | `daily_order_trend`, `weekly_order_trend` | Line chart |
| Segmentation | `segment_summary` | Grouped bar (metrics by `customer_segment`) |
| Segmentation | `segment_spend_share` | Pie/donut or bar (`pct_of_total_spend`) |

---

## 7. Validation baselines

Use these **post–Silver RI alignment** values when sanity-checking Gold inputs (not pre-fix baselines).

| Metric | Value |
|--------|-------|
| Gold revenue (`SUM` entity tables / reconciliation) | **2,708,411.08** |
| Gold quantity (`gold_sales_by_product`) | **10,899** |
| Gold distinct orders (daily trends `SUM(order_count)` or segmentation frequency logic) | **2,052** |

| Gold table | Row count |
|------------|-----------|
| `gold_sales_by_product` | **164** |
| `gold_revenue_by_customer` | **792** |
| `gold_customer_segmentation` | **792** |
| `gold_daily_weekly_trends` | **950** (818 daily + 132 weekly) |

**Do not use** legacy pre–RI-fix totals (`2,830,321.54` revenue, `11,464` quantity, `3,832` orders) as current baselines.

---

## 8. Interpretation

| Visualization | What it shows |
|---------------|---------------|
| Top products | Highest-revenue or highest-volume products from Gold sales aggregate |
| Revenue by category | Share of product revenue across categories (sum of Gold product metrics) |
| Top customers | Customers with highest `total_revenue` from Gold |
| Customer KPIs | Distribution summary over all customers with orders |
| Daily/weekly trends | Revenue and distinct order counts over time at the grain stored in Gold |
| Segment summary | How many customers per segment and average spend, frequency, and lifetime value |
| Segment spend share | Percent of total `total_spend` attributed to each segment |

---

## 9. Limitations / assumptions

- **Gold-only:** No customer names or product attributes beyond what Gold exposes (`product_name`, `category` on sales-by-product only; revenue-by-customer is `customer_id` only).
- **No product-level `order_count`:** `gold_sales_by_product` does not include `order_count`. Product performance queries use `total_quantity` and `total_revenue` only. Order-count trends use `gold_daily_weekly_trends`.
- **Trend double-counting:** Daily and weekly trend tables are separate grains; never add their revenue or order totals for a global KPI.
- **Segment `lifetime_value`:** Sourced from Silver customer master; Dashboard does not validate or recompute it against `total_spend`.
- **Empty periods:** Trend tables include only periods with at least one order (Gold definition); charts may show gaps if rendered with a continuous date axis in the BI tool.
- **Databricks validation:** Serverless execution of all dashboard queries should be confirmed in the target workspace before marking Phase 6 fully validated.

---

## Databricks validation checklist (operator)

Run after Gold pipeline is current:

```sql
-- A. Source availability
SHOW TABLES IN de_c1_coding_evaluation.gold;

-- B. Row counts
SELECT 'gold_sales_by_product' AS t, COUNT(*) AS n FROM de_c1_coding_evaluation.gold.gold_sales_by_product
UNION ALL SELECT 'gold_revenue_by_customer', COUNT(*) FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer
UNION ALL SELECT 'gold_customer_segmentation', COUNT(*) FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
UNION ALL SELECT 'gold_daily_weekly_trends', COUNT(*) FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends;

SELECT time_grain, COUNT(*) FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends GROUP BY time_grain;

-- C. Baseline reconciliation
SELECT SUM(total_revenue) FROM de_c1_coding_evaluation.gold.gold_sales_by_product;
SELECT SUM(total_quantity) FROM de_c1_coding_evaluation.gold.gold_sales_by_product;
SELECT SUM(order_count) FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends WHERE time_grain = 'day';
```

Then execute each named query in `dashboard_queries.sql` **one block at a time** and confirm success.

---

## Per-query Gold column validation

| Query | Gold source | Columns referenced | Valid |
|-------|-------------|-------------------|-------|
| `top_products_by_revenue` | `gold_sales_by_product` | `product_id`, `product_name`, `category`, `total_quantity`, `total_revenue` | Yes |
| `top_products_by_quantity` | `gold_sales_by_product` | `product_id`, `product_name`, `category`, `total_quantity`, `total_revenue` | Yes |
| `revenue_by_category` | `gold_sales_by_product` | `category`, `total_quantity`, `total_revenue` | Yes |
| `top_customers_by_revenue` | `gold_revenue_by_customer` | `customer_id`, `total_revenue` | Yes |
| `customer_revenue_summary_kpis` | `gold_revenue_by_customer` | `total_revenue` | Yes |
| `daily_revenue_trend` | `gold_daily_weekly_trends` | `time_grain`, `period_start`, `total_revenue`, `order_count` | Yes |
| `weekly_revenue_trend` | `gold_daily_weekly_trends` | `time_grain`, `period_start`, `total_revenue`, `order_count` | Yes |
| `daily_order_trend` | `gold_daily_weekly_trends` | `time_grain`, `period_start`, `order_count` | Yes |
| `weekly_order_trend` | `gold_daily_weekly_trends` | `time_grain`, `period_start`, `order_count` | Yes |
| `segment_summary` | `gold_customer_segmentation` | `customer_segment`, `total_spend`, `frequency`, `lifetime_value` | Yes |
| `segment_spend_share` | `gold_customer_segmentation` | `customer_segment`, `total_spend` | Yes |
