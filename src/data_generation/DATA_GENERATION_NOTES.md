# Data Generation Notes

Documentation for Phase 2 sample data: purpose, schemas, generation logic, defects, and execution.

## Dataset Purpose

Provide realistic **e-commerce retail** source files for the medallion pipeline:

- `data/customers.csv` — customer dimension
- `data/products.csv` — product dimension
- `data/orders.csv` — **order line items** (fact grain)

Valid rows support Gold analytics (sales by product, revenue by customer, trends, segmentation). Intentional defects support Silver quality checks in a later phase.

## Order Granularity Decision

**Selected model: order line items in a single `orders.csv`.**

| Approach | Why not / why yes |
|----------|-------------------|
| Order header only | Cannot represent multiple products per order without a separate line table |
| **Line-item rows (chosen)** | One row per product line; `order_id` groups lines; revenue = `quantity × unit_price`; supports referential integrity on `customer_id` and `product_id` |

Each row is uniquely identified by `order_line_id`. `order_id` is **not** unique in `orders.csv` (multiple lines per order).

## Physical Schemas

### customers.csv

| Column | Type (logical) | Required | Notes |
|--------|----------------|----------|-------|
| `customer_id` | INTEGER | Yes | Primary business key |
| `customer_name` | STRING | Yes | Full name |
| `email` | STRING | Yes | Contact email |
| `country` | STRING | Yes | Country name |
| `signup_date` | DATE (ISO `YYYY-MM-DD`) | Yes | Registration date |
| `customer_segment` | STRING | Yes | `Premium`, `Standard`, or `Basic` |
| `lifetime_value` | DECIMAL(12,2) | Yes | Historical value estimate (USD) |

### products.csv

| Column | Type (logical) | Required | Notes |
|--------|----------------|----------|-------|
| `product_id` | INTEGER | Yes | Primary business key |
| `product_name` | STRING | Yes | Display name |
| `category` | STRING | Yes | Product category |
| `unit_price` | DECIMAL(10,2) | Yes | List price (USD) |

### orders.csv (line items)

| Column | Type (logical) | Required | Notes |
|--------|----------------|----------|-------|
| `order_line_id` | INTEGER | Yes | Primary key — one row per line |
| `order_id` | INTEGER | Yes | Groups multiple lines into one order |
| `customer_id` | INTEGER | Yes | FK → `customers.customer_id` |
| `product_id` | INTEGER | Yes | FK → `products.product_id` |
| `order_date` | DATE (ISO) | Yes | Date of order |
| `quantity` | INTEGER | Yes | Units purchased (must be > 0 for valid rows) |
| `unit_price` | DECIMAL(10,2) | Yes | Price at order time (snapshot); should match product catalog for valid rows |

**Revenue (derived):** `line_revenue = quantity × unit_price` (not stored; computed in Silver/Gold).

## Relationships

```
customers (1) ──< orders (line items) >── (1) products
                      │
              order_id groups lines
```

- Valid lines reference `customer_id ∈ [1, num_customers]` and `product_id ∈ [1, num_products]`.
- Orphan FK defects use sentinel IDs `9999991` (customer) and `9999992` (product).

## Generation Approach

1. **Clean generation** — deterministic `random.Random(seed)` builds valid customers, products, and order lines.
2. **Defect injection** — documented mutations (customers/products) and appended bad order lines.
3. **CSV export** — UTF-8 CSV with headers to `data/`.

### Default volumes (seed `42`)

| Dataset | Valid rows | Extra rows from defects | Total rows |
|---------|------------|-------------------------|------------|
| customers | 1,000 | +6 duplicate-key rows | **1,006** |
| products | 200 | +6 duplicate-key rows | **206** |
| order lines | 5,000 | +163 defective lines | **5,163** |

Order lines are generated with 1–3 lines per `order_id` until 5,000 valid lines exist (~2,492 distinct `order_id` values in the valid set).

### Deterministic seed

Default seed: **`42`**. Same seed and CLI sizes produce identical CSVs (verified).

## How to Execute

From repository root:

```bash
# Default: 1000 customers, 200 products, 5000 order lines, seed 42
python3 src/data_generation/generate_sample_data.py

# Custom sizes
python3 src/data_generation/generate_sample_data.py \
  --seed 42 \
  --customers 1000 \
  --products 200 \
  --order-lines 5000 \
  --output-dir data
```

No external Python packages required (stdlib only).

## Intentional Defect Matrix

| ID | Defect type | Dataset | Column | Count | Why introduced | Silver check | Planned handling |
|----|-------------|---------|--------|-------|----------------|--------------|------------------|
| D01 | Missing email | customers | `email` | 50 | Test required-field completeness | Completeness | Quarantine |
| D02 | Missing name | customers | `customer_name` | 10 | Test alternate required field | Completeness | Quarantine |
| D03 | Duplicate `customer_id` | customers | `customer_id` | 6 | Test key uniqueness | Uniqueness | Quarantine duplicates |
| D04 | Invalid signup date | customers | `signup_date` | 20 | Test date parsing | Type validation | Reject |
| D05 | Malformed email | customers | `email` | 30 | Test format validation | Type validation | Quarantine |
| D06 | Future signup date | customers | `signup_date` | 10 | Test business date rule | Business logic | Quarantine |
| D07 | Missing product name | products | `product_name` | 8 | Test completeness | Completeness | Quarantine |
| D08 | Duplicate `product_id` | products | `product_id` | 6 | Test key uniqueness | Uniqueness | Quarantine duplicates |
| D09 | Non-numeric unit price | products | `unit_price` | 15 | Test numeric type | Type validation | Reject |
| D10 | Negative unit price | products | `unit_price` | 10 | Test price business rule | Business logic | Quarantine |
| D11 | Orphan `customer_id` | orders | `customer_id` | 25 | Test FK to customers | Referential integrity | Quarantine |
| D12 | Orphan `product_id` | orders | `product_id` | 25 | Test FK to products | Referential integrity | Quarantine |
| D13 | Invalid order date | orders | `order_date` | 30 | Test date parsing | Type validation | Reject |
| D14 | Future order date | orders | `order_date` | 15 | Test business date rule | Business logic | Quarantine |
| D15 | Non-positive quantity | orders | `quantity` | 40 | Test quantity rule | Business logic | Quarantine |
| D16 | Duplicate `order_line_id` | orders | `order_line_id` | 8 | Test line-level uniqueness | Uniqueness | Quarantine |
| D17 | Catalog price mismatch | orders | `unit_price` | 20 | Line price ≠ product catalog price | Business logic | Quarantine or correct from catalog |

**Total defect injections:** 328 (some customer/product rows may receive more than one mutation if index samples overlap).

Defect counts are defined in `DEFECT_COUNTS` inside `generate_sample_data.py` and printed after each run.

## Mapping Defects → Silver Modules

| Silver module | Defect IDs |
|---------------|------------|
| `01_quality_completeness.py` | D01, D02, D07 |
| `02_quality_uniqueness.py` | D03, D08, D16 |
| `03_quality_type_validation.py` | D04, D05, D09, D13 |
| `04_quality_referential_integrity.py` | D11, D12 |
| `05_quality_business_logic.py` | D06, D10, D14, D15, D17 |

## Validation Performed (Phase 2)

| Check | Result |
|-------|--------|
| Generator runs without error | Pass |
| Three CSV files created in `data/` | Pass |
| Headers match physical schema | Pass |
| Re-run with seed 42 → identical file hashes | Pass |
| NULL emails = 50 | Pass |
| Orphan customer orders = 25 | Pass |
| Orphan product orders = 25 | Pass |
| Non-positive quantity rows = 40 | Pass |
| Python `py_compile` | Pass |

## Limitations & Assumptions

- Single currency (USD); no tax, shipping, or discounts.
- `unit_price` on order lines snapshots catalog price for valid rows; mismatches are intentional defects (D17).
- No order status (cancelled/returned) in this version.
- Customer `lifetime_value` is generated independently (not recomputed from orders).
- Defect injection uses fixed counts, not a percentage of volume.
- Overlapping mutations on the same row are possible but not explicitly tracked.

## Related Documents

- `data-model.md` — finalized physical model
- `data-quality-strategy.md` — field-level rules for Silver
- `ai-prompts/data-generation.md` — Cursor prompt history for this phase
