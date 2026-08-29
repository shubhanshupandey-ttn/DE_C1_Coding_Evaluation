-- Pipeline Validation Script — DE_C1_Coding_Evaluation
-- Catalog: de_c1_coding_evaluation
-- Execute on Databricks Serverless after Bronze → Silver → Gold pipelines have run.
-- Each section can be run independently. Review output columns: check_name, expected, actual, status.
--
-- Local alternatives (no Databricks):
--   python3 src/bronze/ingest_all.py --dry-run
--   python3 src/silver/test_silver_helpers.py
--   python3 src/gold/create_gold_tables.py  (requires Spark — Databricks only)

-- =============================================================================
-- A. BRONZE VALIDATION
-- =============================================================================

-- A1. Bronze tables exist and row counts match seed-42 CSV expectations
SELECT
    'bronze_row_counts' AS check_name,
    'customers=1006; products=206; orders=5163' AS expected,
    CONCAT(
        'customers=', CAST(c.cnt AS STRING),
        '; products=', CAST(p.cnt AS STRING),
        '; orders=', CAST(o.cnt AS STRING)
    ) AS actual,
    CASE
        WHEN c.cnt = 1006 AND p.cnt = 206 AND o.cnt = 5163 THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.bronze.bronze_customers) c
CROSS JOIN (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.bronze.bronze_products) p
CROSS JOIN (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.bronze.bronze_orders) o;

-- A2. Bronze required business columns present (customers) — uses information_schema (DESCRIBE not valid in subquery)
SELECT
    'bronze_customers_columns' AS check_name,
    '7' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) = 7 THEN 'PASS' ELSE 'FAIL' END AS status
FROM system.information_schema.columns
WHERE table_catalog = 'de_c1_coding_evaluation'
  AND table_schema = 'bronze'
  AND table_name = 'bronze_customers'
  AND column_name IN (
      'customer_id', 'customer_name', 'email', 'country',
      'signup_date', 'customer_segment', 'lifetime_value'
  );

-- A3. Intentional Bronze defects preserved (spot checks — D11/D12 orphans in orders)
SELECT
    'bronze_orphan_customer_ids' AS check_name,
    '>= 25 (D11)' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) >= 25 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.bronze.bronze_orders
WHERE customer_id = '9999991';

SELECT
    'bronze_orphan_product_ids' AS check_name,
    '>= 25 (D12)' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) >= 25 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.bronze.bronze_orders
WHERE product_id = '9999992';

-- =============================================================================
-- B. SILVER DATA QUALITY
-- =============================================================================

-- B1. Curated Silver row counts (post RI alignment, SERVERLESS_COMPAT_VERSION = 10)
SELECT
    'silver_curated_row_counts' AS check_name,
    'customers=878; products=164; orders=3646' AS expected,
    CONCAT(
        'customers=', CAST(c.cnt AS STRING),
        '; products=', CAST(p.cnt AS STRING),
        '; orders=', CAST(o.cnt AS STRING)
    ) AS actual,
    CASE
        WHEN c.cnt = 878 AND p.cnt = 164 AND o.cnt = 3646 THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.silver.silver_customers) c
CROSS JOIN (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.silver.silver_products) p
CROSS JOIN (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.silver.silver_orders) o;

-- B2. DQ summary table populated (13 category rows expected)
SELECT
    'silver_dq_summary_rows' AS check_name,
    '13' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) = 13 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.silver.silver_dq_summary;

-- B3. Intentional DQ failures detected — referential integrity (orders)
-- silver_dq_summary uses table_name (not entity_name): values are customers | products | orders
SELECT
    'silver_ri_orders_rows_failed' AS check_name,
    '> 0 (D11/D12 orphans expected)' AS expected,
    CAST(rows_failed AS STRING) AS actual,
    CASE WHEN rows_failed > 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.silver.silver_dq_summary
WHERE table_name = 'orders' AND check_category = 'referential_integrity';

-- B4. Intentional DQ failures detected — completeness (customers)
SELECT
    'silver_completeness_customers_rows_failed' AS check_name,
    '60 (D01/D02/D07)' AS expected,
    CAST(rows_failed AS STRING) AS actual,
    CASE WHEN rows_failed = 60 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.silver.silver_dq_summary
WHERE table_name = 'customers' AND check_category = 'completeness';

-- B5. Post-fix referential integrity — no orphan FKs in curated orders
SELECT
    'silver_orphan_product_fks' AS check_name,
    '0' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.silver.silver_orders o
LEFT JOIN de_c1_coding_evaluation.silver.silver_products p
    ON o.product_id = p.product_id
WHERE p.product_id IS NULL;

SELECT
    'silver_orphan_customer_fks' AS check_name,
    '0' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.silver.silver_orders o
LEFT JOIN de_c1_coding_evaluation.silver.silver_customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- B6. Quarantine table non-empty (intentional defects captured)
SELECT
    'silver_quarantine_non_empty' AS check_name,
    '> 0' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.silver.silver_quarantine_records;

-- =============================================================================
-- C. GOLD VALIDATION
-- =============================================================================

-- C1. Gold table row counts
SELECT
    'gold_row_counts' AS check_name,
    'sales=164; customer=792; segmentation=792; trends=950' AS expected,
    CONCAT(
        'sales=', CAST(s.cnt AS STRING),
        '; customer=', CAST(c.cnt AS STRING),
        '; segmentation=', CAST(g.cnt AS STRING),
        '; trends=', CAST(t.cnt AS STRING)
    ) AS actual,
    CASE
        WHEN s.cnt = 164 AND c.cnt = 792 AND g.cnt = 792 AND t.cnt = 950 THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.gold.gold_sales_by_product) s
CROSS JOIN (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer) c
CROSS JOIN (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.gold.gold_customer_segmentation) g
CROSS JOIN (SELECT COUNT(*) AS cnt FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends) t;

-- C2. Gold trend grain split (818 daily + 132 weekly)
SELECT
    'gold_trend_grain_split' AS check_name,
    'day=818; week=132' AS expected,
    CONCAT(
        'day=', CAST(SUM(CASE WHEN time_grain = 'day' THEN 1 ELSE 0 END) AS STRING),
        '; week=', CAST(SUM(CASE WHEN time_grain = 'week' THEN 1 ELSE 0 END) AS STRING)
    ) AS actual,
    CASE
        WHEN SUM(CASE WHEN time_grain = 'day' THEN 1 ELSE 0 END) = 818
         AND SUM(CASE WHEN time_grain = 'week' THEN 1 ELSE 0 END) = 132
        THEN 'PASS' ELSE 'FAIL'
    END AS status
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends;

-- C3. Gold sales-by-product — no duplicate products
SELECT
    'gold_sales_by_product_unique_grain' AS check_name,
    '0 duplicate product_id' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM (
    SELECT product_id
    FROM de_c1_coding_evaluation.gold.gold_sales_by_product
    GROUP BY product_id
    HAVING COUNT(*) > 1
) dups;

-- C4. Gold revenue-by-customer — no duplicate customers
SELECT
    'gold_revenue_by_customer_unique_grain' AS check_name,
    '0 duplicate customer_id' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM (
    SELECT customer_id
    FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer
    GROUP BY customer_id
    HAVING COUNT(*) > 1
) dups;

-- =============================================================================
-- D. RECONCILIATION
-- =============================================================================

-- D1. Entity revenue reconciliation across Gold tables (tolerance 0.01)
WITH totals AS (
    SELECT
        (SELECT SUM(total_revenue) FROM de_c1_coding_evaluation.gold.gold_sales_by_product) AS sales_revenue,
        (SELECT SUM(total_revenue) FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer) AS customer_revenue,
        (SELECT SUM(total_spend) FROM de_c1_coding_evaluation.gold.gold_customer_segmentation) AS segmentation_spend,
        (SELECT SUM(total_revenue) FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends WHERE time_grain = 'day') AS daily_revenue,
        (SELECT SUM(total_revenue) FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends WHERE time_grain = 'week') AS weekly_revenue
)
SELECT
    'gold_revenue_reconciliation' AS check_name,
    'all = 2708411.08' AS expected,
    CONCAT(
        'sales=', CAST(ROUND(sales_revenue, 2) AS STRING),
        '; customer=', CAST(ROUND(customer_revenue, 2) AS STRING),
        '; segmentation=', CAST(ROUND(segmentation_spend, 2) AS STRING),
        '; daily=', CAST(ROUND(daily_revenue, 2) AS STRING),
        '; weekly=', CAST(ROUND(weekly_revenue, 2) AS STRING)
    ) AS actual,
    CASE
        WHEN ABS(sales_revenue - 2708411.08) < 0.01
         AND ABS(customer_revenue - 2708411.08) < 0.01
         AND ABS(segmentation_spend - 2708411.08) < 0.01
         AND ABS(daily_revenue - 2708411.08) < 0.01
         AND ABS(weekly_revenue - 2708411.08) < 0.01
        THEN 'PASS' ELSE 'FAIL'
    END AS status
FROM totals;

-- D2. Gold quantity reconciliation
SELECT
    'gold_quantity_reconciliation' AS check_name,
    'total_quantity = 10899' AS expected,
    CAST(SUM(total_quantity) AS STRING) AS actual,
    CASE WHEN SUM(total_quantity) = 10899 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.gold.gold_sales_by_product;

-- D3. Gold distinct orders (daily trend sum)
SELECT
    'gold_distinct_orders_daily_trends' AS check_name,
    '2052' AS expected,
    CAST(SUM(order_count) AS STRING) AS actual,
    CASE WHEN SUM(order_count) = 2052 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
WHERE time_grain = 'day';

-- D4. Weekly trend totals match daily (same underlying orders — not double-counted across grains)
SELECT
    'gold_weekly_order_count_matches_daily' AS check_name,
    'weekly sum = daily sum = 2052' AS expected,
    CONCAT(
        'daily=', CAST(d.daily_orders AS STRING),
        '; weekly=', CAST(w.weekly_orders AS STRING)
    ) AS actual,
    CASE WHEN d.daily_orders = 2052 AND w.weekly_orders = 2052 THEN 'PASS' ELSE 'FAIL' END AS status
FROM (
    SELECT SUM(order_count) AS daily_orders
    FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
    WHERE time_grain = 'day'
) d
CROSS JOIN (
    SELECT SUM(order_count) AS weekly_orders
    FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
    WHERE time_grain = 'week'
) w;

-- D5. Premium/Standard/Basic spend share sums to ~100%
SELECT
    'gold_master_segment_pct_sum' AS check_name,
    '100.00' AS expected,
    CAST(ROUND(SUM(pct_of_total_spend), 2) AS STRING) AS actual,
    CASE WHEN ABS(SUM(pct_of_total_spend) - 100.0) < 0.05 THEN 'PASS' ELSE 'FAIL' END AS status
FROM (
    SELECT
        ROUND(100.0 * SUM(total_spend) / SUM(SUM(total_spend)) OVER (), 2) AS pct_of_total_spend
    FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
    GROUP BY customer_segment
) shares;

-- D6. Revenue-by-customer matches segmentation spend per customer
SELECT
    'gold_customer_revenue_equals_segmentation_spend' AS check_name,
    '0 mismatched customers' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer r
INNER JOIN de_c1_coding_evaluation.gold.gold_customer_segmentation s
    ON r.customer_id = s.customer_id
WHERE ABS(r.total_revenue - s.total_spend) > 0.0001;

-- =============================================================================
-- E. DASHBOARD VALIDATION (Gold-source checks for dashboard query logic)
-- =============================================================================

-- E1. Top 10 products by revenue — exactly 10 rows, sorted descending
WITH top10 AS (
    SELECT total_revenue
    FROM de_c1_coding_evaluation.gold.gold_sales_by_product
    ORDER BY total_revenue DESC, product_id
    LIMIT 10
),
ordered AS (
    SELECT
        total_revenue,
        LAG(total_revenue) OVER (ORDER BY total_revenue DESC) AS prev_revenue
    FROM top10
)
SELECT
    'dashboard_top10_revenue_sort' AS check_name,
    '10 rows; each <= previous' AS expected,
    CONCAT(
        'rows=', CAST((SELECT COUNT(*) FROM top10) AS STRING),
        '; violations=', CAST((SELECT COUNT(*) FROM ordered WHERE prev_revenue IS NOT NULL AND total_revenue > prev_revenue) AS STRING)
    ) AS actual,
    CASE
        WHEN (SELECT COUNT(*) FROM top10) = 10
         AND (SELECT COUNT(*) FROM ordered WHERE prev_revenue IS NOT NULL AND total_revenue > prev_revenue) = 0
        THEN 'PASS' ELSE 'FAIL'
    END AS status;

-- E2. Top 10 products by quantity — sorted descending
WITH top10 AS (
    SELECT total_quantity
    FROM de_c1_coding_evaluation.gold.gold_sales_by_product
    ORDER BY total_quantity DESC, product_id
    LIMIT 10
),
ordered AS (
    SELECT
        total_quantity,
        LAG(total_quantity) OVER (ORDER BY total_quantity DESC) AS prev_qty
    FROM top10
)
SELECT
    'dashboard_top10_quantity_sort' AS check_name,
    '10 rows; each <= previous' AS expected,
    CONCAT(
        'rows=', CAST((SELECT COUNT(*) FROM top10) AS STRING),
        '; violations=', CAST((SELECT COUNT(*) FROM ordered WHERE prev_qty IS NOT NULL AND total_quantity > prev_qty) AS STRING)
    ) AS actual,
    CASE
        WHEN (SELECT COUNT(*) FROM top10) = 10
         AND (SELECT COUNT(*) FROM ordered WHERE prev_qty IS NOT NULL AND total_quantity > prev_qty) = 0
        THEN 'PASS' ELSE 'FAIL'
    END AS status;

-- E3. Customer revenue distribution source — customer-level grain (792 rows)
SELECT
    'dashboard_histogram_customer_grain' AS check_name,
    '792 customer rows' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) = 792 THEN 'PASS' ELSE 'FAIL' END AS status
FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer;

-- E4. Behavioral segmentation — documented logic produces 3 segments for customers-with-orders
WITH spend_threshold AS (
    SELECT approx_percentile(total_spend, 0.75) AS high_value_spend_threshold
    FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
),
classified AS (
    SELECT
        CASE
            WHEN s.total_spend >= t.high_value_spend_threshold THEN 'High-Value'
            WHEN s.frequency >= 2 THEN 'Repeat'
            WHEN s.frequency = 1 THEN 'One-Time'
            ELSE 'Inactive'
        END AS behavioral_segment
    FROM de_c1_coding_evaluation.gold.gold_customer_segmentation s
    CROSS JOIN spend_threshold t
)
SELECT
    'dashboard_behavioral_segment_count' AS check_name,
    '3 segments (Inactive absent — zero-order customers excluded from Gold)' AS expected,
    CAST(COUNT(DISTINCT behavioral_segment) AS STRING) AS actual,
    CASE WHEN COUNT(DISTINCT behavioral_segment) = 3 THEN 'PASS' ELSE 'FAIL' END AS status
FROM classified;

-- E5. Behavioral segmentation customer count sums to 792
WITH spend_threshold AS (
    SELECT approx_percentile(total_spend, 0.75) AS high_value_spend_threshold
    FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
),
classified AS (
    SELECT
        CASE
            WHEN s.total_spend >= t.high_value_spend_threshold THEN 'High-Value'
            WHEN s.frequency >= 2 THEN 'Repeat'
            WHEN s.frequency = 1 THEN 'One-Time'
            ELSE 'Inactive'
        END AS behavioral_segment
    FROM de_c1_coding_evaluation.gold.gold_customer_segmentation s
    CROSS JOIN spend_threshold t
)
SELECT
    'dashboard_behavioral_customer_total' AS check_name,
    '792' AS expected,
    CAST(COUNT(*) AS STRING) AS actual,
    CASE WHEN COUNT(*) = 792 THEN 'PASS' ELSE 'FAIL' END AS status
FROM classified;
