-- Gold Iteration 4: Daily / Weekly Trends
-- Target: de_c1_coding_evaluation.gold.gold_daily_weekly_trends
-- Source: silver.silver_orders only
-- Grain: one row per (time_grain, period_start)
-- Write mode: CREATE OR REPLACE (Delta overwrite)
--
-- Weekly period_start: Monday of calendar week (Spark date_trunc('week') → Monday)

CREATE SCHEMA IF NOT EXISTS de_c1_coding_evaluation.gold;

CREATE OR REPLACE TABLE de_c1_coding_evaluation.gold.gold_daily_weekly_trends
USING DELTA
AS
SELECT
    'day' AS time_grain,
    o.order_date AS period_start,
    SUM(o.quantity * o.unit_price) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS order_count
FROM de_c1_coding_evaluation.silver.silver_orders AS o
GROUP BY
    o.order_date

UNION ALL

SELECT
    'week' AS time_grain,
    CAST(date_trunc('week', o.order_date) AS DATE) AS period_start,
    SUM(o.quantity * o.unit_price) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS order_count
FROM de_c1_coding_evaluation.silver.silver_orders AS o
GROUP BY
    CAST(date_trunc('week', o.order_date) AS DATE);
