-- Gold Iteration 2: Sales by Product
-- Target: de_c1_coding_evaluation.gold.gold_sales_by_product
-- Sources: silver.silver_orders, silver.silver_products
-- Grain: one row per product with at least one Silver order line
-- Write mode: CREATE OR REPLACE (Delta overwrite)

CREATE SCHEMA IF NOT EXISTS de_c1_coding_evaluation.gold;

CREATE OR REPLACE TABLE de_c1_coding_evaluation.gold.gold_sales_by_product
USING DELTA
AS
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS total_quantity,
    SUM(o.quantity * o.unit_price) AS total_revenue
FROM de_c1_coding_evaluation.silver.silver_orders AS o
INNER JOIN de_c1_coding_evaluation.silver.silver_products AS p
    ON o.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category;
