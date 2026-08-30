-- =============================================================================
-- DE_C1_Coding_Evaluation — Source relational schema (documentary)
-- =============================================================================
--
-- Purpose:
--   Defines the logical source data model that matches the committed CSV files
--   under data/ (customers.csv, products.csv, orders.csv).
--
-- Dialect:
--   Portable ANSI-style DDL with PostgreSQL-compatible syntax where helpful.
--   No external RDBMS deployment is evidenced in this repository; this script
--   documents the source contract for reviewers and optional local loading.
--
-- Grain:
--   orders = ORDER LINE ITEMS (one row per order_line_id), NOT one row per order.
--
-- Intentional defects:
--   Committed seed CSVs include documented D01–D17 defects (see
--   src/data_generation/DATA_GENERATION_NOTES.md). Foreign-key constraints are
--   documented logically but NOT enforced below so defective rows can be loaded.
--
-- Pipeline:
--   CSV seed data -> Bronze (STRING ingest) -> Silver (DQ) -> Gold -> Dashboard
--   This schema does NOT replace the Databricks medallion implementation.
-- =============================================================================

-- Optional schema namespace (adjust or remove for your RDBMS)
CREATE SCHEMA IF NOT EXISTS source;

-- -----------------------------------------------------------------------------
-- customers — dimension (maps to data/customers.csv)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS source.customers (
    customer_id       INTEGER        NOT NULL,
    customer_name     VARCHAR(255)   NOT NULL,
    email             VARCHAR(320)   NOT NULL,
    country           VARCHAR(100)   NOT NULL,
    signup_date       DATE           NOT NULL,
    customer_segment  VARCHAR(20)    NOT NULL,  -- Premium | Standard | Basic
    lifetime_value    DECIMAL(12, 2) NOT NULL,
    CONSTRAINT pk_customers PRIMARY KEY (customer_id)
);

COMMENT ON TABLE source.customers IS
    'Customer dimension. Source file: data/customers.csv (1,006 rows, seed 42).';

COMMENT ON COLUMN source.customers.customer_id IS 'Primary business key (INTEGER in CSV).';
COMMENT ON COLUMN source.customers.lifetime_value IS
    'Historical value estimate (USD); not derived from orders in Phase 2 generator.';

-- -----------------------------------------------------------------------------
-- products — dimension (maps to data/products.csv)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS source.products (
    product_id    INTEGER        NOT NULL,
    product_name  VARCHAR(255)   NOT NULL,
    category      VARCHAR(100)   NOT NULL,
    unit_price    DECIMAL(10, 2) NOT NULL,
    CONSTRAINT pk_products PRIMARY KEY (product_id)
);

COMMENT ON TABLE source.products IS
    'Product dimension. Source file: data/products.csv (206 rows, seed 42).';

-- -----------------------------------------------------------------------------
-- orders — order LINE ITEMS (maps to data/orders.csv)
-- -----------------------------------------------------------------------------
-- Logical relationships (NOT enforced — intentional orphan FKs in seed data):
--   orders.customer_id -> customers.customer_id  (D11 uses sentinel 9999991)
--   orders.product_id  -> products.product_id   (D12 uses sentinel 9999992)
-- order_id groups multiple lines; it is NOT unique in this table.
CREATE TABLE IF NOT EXISTS source.orders (
    order_line_id  INTEGER        NOT NULL,
    order_id       INTEGER        NOT NULL,
    customer_id    INTEGER        NOT NULL,
    product_id     INTEGER        NOT NULL,
    order_date     DATE           NOT NULL,
    quantity       INTEGER        NOT NULL,
    unit_price     DECIMAL(10, 2) NOT NULL,
    CONSTRAINT pk_orders PRIMARY KEY (order_line_id)
);

COMMENT ON TABLE source.orders IS
    'Order line-item fact. Source file: data/orders.csv (5,163 rows, seed 42). '
    'Revenue is derived as quantity * unit_price (not stored).';

COMMENT ON COLUMN source.orders.order_line_id IS 'Primary key — one row per line item.';
COMMENT ON COLUMN source.orders.order_id IS 'Groups multiple line items into one customer order.';
COMMENT ON COLUMN source.orders.unit_price IS
    'Unit price snapshot at order time; may differ from products.unit_price (D17).';

-- -----------------------------------------------------------------------------
-- Column inventory (authoritative CSV header order)
-- -----------------------------------------------------------------------------
-- customers:  customer_id, customer_name, email, country, signup_date,
--             customer_segment, lifetime_value
-- products:   product_id, product_name, category, unit_price
-- orders:     order_line_id, order_id, customer_id, product_id, order_date,
--             quantity, unit_price
