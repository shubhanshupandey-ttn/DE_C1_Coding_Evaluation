-- Phase 6 Dashboard — visualization-ready queries
-- Catalog: de_c1_coding_evaluation | Schema: gold
-- Sources: Gold tables only (no Bronze/Silver)
-- Prerequisites: run Gold pipeline (create_gold_tables.py) before executing
--
-- Gold column contract:
--   gold_sales_by_product:        product_id, product_name, category, total_quantity, total_revenue
--   gold_revenue_by_customer:     customer_id, total_revenue
--   gold_daily_weekly_trends:     time_grain, period_start, total_revenue, order_count
--   gold_customer_segmentation:   customer_id, customer_segment, lifetime_value, frequency, total_spend
--
-- customer_segment (Premium/Standard/Basic) is a master-data attribute.
-- Behavioral segments (High-Value/Repeat/One-Time/Inactive) are derived in Section 5 from frequency + total_spend.
--
-- Execute ONE query block at a time (each block starts with "-- Query:").

----------------------------------------------------
-- 1. KPI CARDS
----------------------------------------------------

-- Query: overall_customer_kpis
-- Business question: What are headline customer portfolio metrics?
-- Viz: KPI cards | Fields: one row of scalar metrics
SELECT
    seg.total_customers,
    seg.total_spend,
    seg.avg_customer_spend,
    seg.avg_frequency,
    seg.avg_lifetime_value,
    ord.total_orders
FROM (
    SELECT
        COUNT(*) AS total_customers,
        SUM(total_spend) AS total_spend,
        AVG(total_spend) AS avg_customer_spend,
        AVG(frequency) AS avg_frequency,
        AVG(lifetime_value) AS avg_lifetime_value
    FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
) AS seg
CROSS JOIN (
    SELECT SUM(order_count) AS total_orders
    FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
    WHERE time_grain = 'day'
) AS ord;

----------------------------------------------------
-- 2. ORDER TRENDS
----------------------------------------------------

-- Query: weekly_order_trend
-- Business question: How are weekly order volumes trending?
-- Viz: line chart | X: week_start | Y: weekly_order_count
SELECT
    period_start AS week_start,
    order_count AS weekly_order_count
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
WHERE time_grain = 'week'
ORDER BY week_start;

-- Query: daily_order_trend
-- Business question: How are daily order volumes trending?
-- Viz: line chart | X: period_start | Y: order_count
SELECT
    period_start,
    order_count
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
WHERE time_grain = 'day'
ORDER BY period_start;

----------------------------------------------------
-- 3. TOP PRODUCTS
----------------------------------------------------

-- Query: top_products_by_revenue
-- Business question: Which products generate the most revenue?
-- Viz: horizontal bar chart | Y: product_name | X: total_revenue | Top 10, descending
SELECT
    product_id,
    product_name,
    category,
    total_revenue,
    total_quantity
FROM de_c1_coding_evaluation.gold.gold_sales_by_product
ORDER BY total_revenue DESC, product_id
LIMIT 10;

----------------------------------------------------
-- 4. CUSTOMER REVENUE DISTRIBUTION
----------------------------------------------------

-- Query: customer_revenue_distribution
-- Business question: How is customer revenue distributed across the customer base?
-- Viz: histogram | X: revenue bin (bin_min_revenue to bin_max_revenue) | Y: customer_count
-- Grain: one row per revenue bin (20 equal-count bins via NTILE)
WITH customer_revenue AS (
    SELECT
        customer_id,
        total_revenue
    FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer
),
binned AS (
    SELECT
        NTILE(20) OVER (ORDER BY total_revenue) AS revenue_bin,
        total_revenue
    FROM customer_revenue
)
SELECT
    revenue_bin,
    MIN(total_revenue) AS bin_min_revenue,
    MAX(total_revenue) AS bin_max_revenue,
    COUNT(*) AS customer_count
FROM binned
GROUP BY revenue_bin
ORDER BY revenue_bin;

----------------------------------------------------
-- 5. CUSTOMER BEHAVIORAL SEGMENTATION
----------------------------------------------------

-- Query: behavioral_segment_summary
-- Business question: How many customers fall into each behavioral segment?
-- Viz: pie/donut chart | Category: behavioral_segment | Value: customer_count (or total_spend)
-- Logic (Dashboard-layer, Gold metrics only):
--   High-Value  = total_spend >= 75th percentile of total_spend
--   Repeat      = frequency >= 2 and not High-Value
--   One-Time    = frequency = 1 and not High-Value
--   Inactive    = zero-order customers (not present in gold_customer_segmentation)
WITH spend_threshold AS (
    SELECT approx_percentile(total_spend, 0.75) AS high_value_spend_threshold
    FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
),
classified AS (
    SELECT
        s.customer_id,
        s.total_spend,
        s.frequency,
        CASE
            WHEN s.total_spend >= t.high_value_spend_threshold THEN 'High-Value'
            WHEN s.frequency >= 2 THEN 'Repeat'
            WHEN s.frequency = 1 THEN 'One-Time'
            ELSE 'Inactive'
        END AS behavioral_segment
    FROM de_c1_coding_evaluation.gold.gold_customer_segmentation AS s
    CROSS JOIN spend_threshold AS t
)
SELECT
    behavioral_segment,
    COUNT(*) AS customer_count,
    SUM(total_spend) AS total_spend,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_customers,
    ROUND(100.0 * SUM(total_spend) / SUM(SUM(total_spend)) OVER (), 2) AS pct_of_total_spend
FROM classified
GROUP BY behavioral_segment
ORDER BY customer_count DESC;

----------------------------------------------------
-- 6. CUSTOMER SEGMENT ANALYSIS (Premium / Standard / Basic)
----------------------------------------------------

-- Query: segment_summary
-- Business question: How do Premium/Standard/Basic segments compare on spend and behavior?
-- Viz: grouped bar chart | Category: customer_segment | Metrics: customer_count, total_spend, averages
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
-- Business question: What share of total spend does each Premium/Standard/Basic segment contribute?
-- Viz: donut/pie chart | Category: customer_segment | Value: pct_of_total_spend
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

----------------------------------------------------
-- SUPPLEMENTAL (optional tiles — not required by evaluation)
----------------------------------------------------

-- Query: top_products_by_quantity
-- Business question: Which products sell the most units?
-- Viz: horizontal bar chart | Y: product_name | X: total_quantity
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
-- Business question: How is product revenue distributed across categories?
-- Viz: bar or donut chart | Category: category | Value: total_revenue
SELECT
    category,
    COUNT(*) AS product_count,
    SUM(total_quantity) AS total_quantity,
    SUM(total_revenue) AS total_revenue
FROM de_c1_coding_evaluation.gold.gold_sales_by_product
GROUP BY category
ORDER BY SUM(total_revenue) DESC;

-- Query: top_customers_by_revenue
-- Business question: Who are the highest-revenue customers?
-- Viz: bar chart | Category: customer_id | Value: total_revenue
SELECT
    customer_id,
    total_revenue
FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer
ORDER BY total_revenue DESC, customer_id
LIMIT 10;

----------------------------------------------------
-- 7. VALIDATION QUERIES (not dashboard tiles)
----------------------------------------------------

-- Query: validation_daily_weekly_order_totals
-- Business question: Do daily and weekly Gold trend grains reconcile to the same order total?
SELECT
    time_grain,
    SUM(order_count) AS total_order_count,
    SUM(total_revenue) AS total_revenue
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
GROUP BY time_grain
ORDER BY time_grain;

-- Query: validation_segment_spend_reconciliation
-- Business question: Does segment spend sum to overall customer spend?
SELECT
    SUM(total_spend) AS segment_total_spend
FROM de_c1_coding_evaluation.gold.gold_customer_segmentation;

-- Query: validation_segment_pct_sum
-- Business question: Do Premium/Standard/Basic spend shares sum to ~100%?
SELECT
    ROUND(SUM(pct_of_total_spend), 2) AS pct_sum
FROM (
    SELECT
        ROUND(
            100.0 * SUM(total_spend) / SUM(SUM(total_spend)) OVER (),
            2
        ) AS pct_of_total_spend
    FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
    GROUP BY customer_segment
) AS shares;

-- Query: validation_revenue_by_customer_vs_segmentation
-- Business question: Does customer revenue match segmentation spend?
SELECT
    SUM(r.total_revenue) AS revenue_by_customer_total,
    SUM(s.total_spend) AS segmentation_total_spend
FROM de_c1_coding_evaluation.gold.gold_revenue_by_customer AS r
INNER JOIN de_c1_coding_evaluation.gold.gold_customer_segmentation AS s
    ON r.customer_id = s.customer_id;
