# Data Model

Physical and logical data model for the Databricks Medallion Pipeline. **Finalized in Phase 2 (data generation).**

## Domain Overview

Simplified **retail / e-commerce** model:

- **Customers** place **orders**
- Each **order** contains one or more **line items** (products)
- **Products** are referenced on each line

## Granularity Decision (Phase 2)

**`orders.csv` stores order line items**, not order headers alone.

| Design choice | Rationale |
|---------------|-----------|
| Grain = one row per line item | Supports multiple products per order naturally |
| `order_line_id` as primary key | Uniqueness checks apply at line level |
| `order_id` groups lines | Supports order-level analysis while keeping normalized facts |
| `unit_price` on each line | Enables `revenue = quantity × unit_price` and catalog consistency checks |

Rejected alternative: separate header and line CSV files — unnecessary complexity for this assessment scope.

## Entity-Relationship Diagram

```
┌─────────────────┐       ┌──────────────────────────────┐       ┌─────────────────┐
│    customers    │ 1   * │  orders (line items)         │ *   1 │    products     │
│  customer_id PK │───────│  order_line_id PK            │───────│  product_id PK  │
└─────────────────┘       │  order_id (logical grouping) │       └─────────────────┘
                          │  customer_id FK              │
                          │  product_id FK               │
                          └──────────────────────────────┘
```

## Physical Schemas

### customers (`data/customers.csv`)

| Column | Type | PK/FK | Nullable (Silver target) | Description |
|--------|------|-------|--------------------------|-------------|
| `customer_id` | INTEGER | PK | No | Unique customer identifier |
| `customer_name` | STRING | | No | Customer full name |
| `email` | STRING | | No | Email address |
| `country` | STRING | | No | Country |
| `signup_date` | DATE | | No | Account signup date |
| `customer_segment` | STRING | | No | `Premium`, `Standard`, `Basic` |
| `lifetime_value` | DECIMAL(12,2) | | No | Estimated lifetime value (USD) |

### products (`data/products.csv`)

| Column | Type | PK/FK | Nullable (Silver target) | Description |
|--------|------|-------|--------------------------|-------------|
| `product_id` | INTEGER | PK | No | Unique product identifier |
| `product_name` | STRING | | No | Product name |
| `category` | STRING | | No | Merchandise category |
| `unit_price` | DECIMAL(10,2) | | No | Catalog list price (USD) |

### orders — line items (`data/orders.csv`)

| Column | Type | PK/FK | Nullable (Silver target) | Description |
|--------|------|-------|--------------------------|-------------|
| `order_line_id` | INTEGER | PK | No | Unique line identifier |
| `order_id` | INTEGER | | No | Order header / basket identifier |
| `customer_id` | INTEGER | FK → customers | No | Purchasing customer |
| `product_id` | INTEGER | FK → products | No | Product on this line |
| `order_date` | DATE | | No | Order date |
| `quantity` | INTEGER | | No | Units purchased |
| `unit_price` | DECIMAL(10,2) | | No | Unit price at time of order |

**Derived metric:** `line_revenue = quantity × unit_price`

## Keys & Integrity Rules

| Rule | Enforcement layer |
|------|-------------------|
| `customer_id` unique in customers | Silver uniqueness |
| `product_id` unique in products | Silver uniqueness |
| `order_line_id` unique in orders | Silver uniqueness |
| `orders.customer_id` exists in customers | Silver referential integrity |
| `orders.product_id` exists in products | Silver referential integrity |
| `order_id` may repeat | Expected — not a uniqueness key |

## Gold Consumption

| Gold theme | Primary fields |
|------------|----------------|
| Sales by product | `orders` ⋈ `products` — group by `product_id`, `product_name`, `category`; sum `quantity`, sum `quantity * unit_price` |
| Revenue by customer | `orders` ⋈ `customers` — group by `customer_id`; sum `quantity * unit_price` |
| Daily / weekly trends | `orders.order_date` — aggregate revenue and order counts by day/week |
| Customer segmentation | `customers.customer_segment`, `lifetime_value` + order aggregates (frequency, total spend) |

## Medallion Mapping

| Layer | Objects |
|-------|---------|
| Bronze | `bronze.bronze_customers`, `bronze.bronze_orders`, `bronze.bronze_products` |
| Silver | Cleansed entity tables at same grain as source (not started) |
| Gold | Aggregated metric tables (not started) |

## Resolved Modeling Questions

| Question | Decision |
|----------|----------|
| Order granularity | Line-item model in `orders.csv` |
| Revenue | Derived from `quantity × unit_price` on each line |
| Currency | Single currency (USD) |
| Order status | Out of scope for Phase 2 |
| SCD / history | Type 1 only (no slowly changing dimensions) |

## Change Log

| Date | Change |
|------|--------|
| Phase 1 | Initial logical model; schema TBD |
| Phase 2 | Physical schemas finalized; line-item orders adopted |
| Phase 3 | Bronze Delta tables: `bronze.bronze_*`; source columns ingested as STRING |
