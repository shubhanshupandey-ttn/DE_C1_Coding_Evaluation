-- Gold Iteration 3: Revenue by Customer
-- Target: de_c1_coding_evaluation.gold.gold_revenue_by_customer
-- Sources: silver.silver_orders, silver.silver_customers
-- Grain: one row per customer with at least one Silver order
-- Write mode: CREATE OR REPLACE (Delta overwrite)

CREATE SCHEMA IF NOT EXISTS de_c1_coding_evaluation.gold;

CREATE OR REPLACE TABLE de_c1_coding_evaluation.gold.gold_revenue_by_customer
USING DELTA
AS
SELECT
    o.customer_id,
    SUM(o.quantity * o.unit_price) AS total_revenue
FROM de_c1_coding_evaluation.silver.silver_orders AS o
INNER JOIN de_c1_coding_evaluation.silver.silver_customers AS c
    ON o.customer_id = c.customer_id
GROUP BY
    o.customer_id;
