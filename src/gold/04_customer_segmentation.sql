-- Gold Iteration 5: Customer Segmentation
-- Target: de_c1_coding_evaluation.gold.gold_customer_segmentation
-- Sources: silver.silver_customers, silver.silver_orders
-- Grain: one row per customer with at least one Silver order
-- Write mode: CREATE OR REPLACE (Delta overwrite)

CREATE SCHEMA IF NOT EXISTS de_c1_coding_evaluation.gold;

CREATE OR REPLACE TABLE de_c1_coding_evaluation.gold.gold_customer_segmentation
USING DELTA
AS
SELECT
    c.customer_id,
    c.customer_segment,
    c.lifetime_value,
    COUNT(DISTINCT o.order_id) AS frequency,
    SUM(o.quantity * o.unit_price) AS total_spend
FROM de_c1_coding_evaluation.silver.silver_customers AS c
INNER JOIN de_c1_coding_evaluation.silver.silver_orders AS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.customer_segment,
    c.lifetime_value;
