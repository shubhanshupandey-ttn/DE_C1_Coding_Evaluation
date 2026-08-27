-- Phase 6 Dashboard — visualization-ready queries
-- Catalog: de_c1_coding_evaluation | Schema: gold
-- Sources: Gold tables only (no Bronze/Silver)
-- Prerequisites: run Gold pipeline (create_gold_tables.py) before executing
--
-- Gold column contract (do not reference columns outside these lists):
--   gold_sales_by_product:        product_id, product_name, category, total_quantity, total_revenue
--                                 (NO order_count — use gold_daily_weekly_trends for order metrics)
--   gold_revenue_by_customer:     customer_id, total_revenue
--   gold_daily_weekly_trends:     time_grain, period_start, total_revenue, order_count
--   gold_customer_segmentation:   customer_id, customer_segment, lifetime_value, frequency, total_spend
--
-- Execute ONE query block at a time (each block starts with "-- Query:").

-- =============================================================================
-- 1. Product Performance (gold_sales_by_product)
-- Columns: product_id, product_name, category, total_quantity, total_revenue
-- =============================================================================

-- Query: top_products_by_revenue
-- Purpose: Rank products by total revenue for bar-chart visualization
SELECT
    product_id,
    product_name,
    category,
    total_quantity,
    total_revenue
FROM de_c1_coding_evaluation.gold.gold_sales_by_product
ORDER BY total_revenue DESC, product_id
LIMIT 10;

-- Query: top_products_by_quantity
-- Purpose: Rank products by units sold for bar-chart visualization
SELECT
    product_id,
    product_name,
    category,
    total_quantity,
    total_revenue
FROM de_c1_coding_evaluation.gold.gold_sales_by_product
ORDER BY total_quantity DESC, product_id
LIMIT 10;

-- Query: revenue_by_category
-- Purpose: Category-level revenue mix (aggregates existing Gold metrics)
SELECT
    category,
    COUNT(*) AS product_count,
    SUM(total_quantity) AS total_quantity,
    SUM(total_revenue) AS total_revenue
FROM de_c1_coding_evaluation.gold.gold_sales_by_product
GROUP BY category
ORDER BY SUM(total_revenue) DESC;

-- =============================================================================
-- 2. Customer Revenue (gold_revenue_by_customer)
-- Columns: customer_id, total_revenue
-- =============================================================================

-- Query: top_customers_by_revenue
-- Purpose: Rank customers by total revenue for bar-chart visualization
SELECT
    customer_id,
    total_revenue
FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer
ORDER BY total_revenue DESC, customer_id
LIMIT 10;

-- Query: customer_revenue_summary_kpis
-- Purpose: Portfolio-level customer revenue KPI cards
SELECT
    COUNT(*) AS customer_count,
    SUM(total_revenue) AS total_revenue,
    AVG(total_revenue) AS avg_revenue_per_customer,
    MAX(total_revenue) AS max_revenue,
    MIN(total_revenue) AS min_revenue
FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer;

-- =============================================================================
-- 3. Revenue / Trends (gold_daily_weekly_trends)
-- Columns: time_grain, period_start, total_revenue, order_count
-- =============================================================================

-- Query: daily_revenue_trend
-- Purpose: Daily revenue time series (line chart)
SELECT
    period_start,
    total_revenue,
    order_count
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
WHERE time_grain = 'day'
ORDER BY period_start;

-- Query: weekly_revenue_trend
-- Purpose: Weekly revenue time series; period_start is Monday-start week
SELECT
    period_start,
    total_revenue,
    order_count
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
WHERE time_grain = 'week'
ORDER BY period_start;

-- Query: daily_order_trend
-- Purpose: Daily business order count time series (line chart)
SELECT
    period_start,
    order_count
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
WHERE time_grain = 'day'
ORDER BY period_start;

-- Query: weekly_order_trend
-- Purpose: Weekly business order count time series (line chart)
SELECT
    period_start,
    order_count
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
WHERE time_grain = 'week'
ORDER BY period_start;

-- =============================================================================
-- 4. Customer Segmentation (gold_customer_segmentation)
-- Columns: customer_id, customer_segment, lifetime_value, frequency, total_spend
-- =============================================================================

-- Query: segment_summary
-- Purpose: Customers and spend behavior aggregated by segment
SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    SUM(total_spend) AS total_spend,
    AVG(total_spend) AS avg_total_spend,
    AVG(frequency) AS avg_frequency,
    AVG(lifetime_value) AS avg_lifetime_value
FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
GROUP BY customer_segment
ORDER BY total_spend DESC;

-- Query: segment_spend_share
-- Purpose: Spend share by segment for pie or bar chart
SELECT
    customer_segment,
    SUM(total_spend) AS total_spend,
    ROUND(
        100.0 * SUM(total_spend) / SUM(SUM(total_spend)) OVER (),
        2
    ) AS pct_of_total_spend
FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
GROUP BY customer_segment
ORDER BY total_spend DESC;
