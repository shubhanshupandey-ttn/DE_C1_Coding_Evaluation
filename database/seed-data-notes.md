# Seed Data Notes — Source CSV Datasets

Documents the **seed / sample source data** for `DE_C1_Coding_Evaluation` and how it relates to `database/schema.sql`.

---

## Purpose

The committed CSV files under `data/` are the project's **authoritative seed datasets**. They represent the relational source model documented in `database/schema.sql` and feed the medallion pipeline:

```text
CSV seed data (data/)
    -> Bronze raw ingest (STRING columns, defects preserved)
    -> Silver validation / DQ
    -> Gold analytics
    -> Dashboard (Gold-only)
```

The `database/` directory documents the **source-side contract**. It does not replace Bronze, Silver, or Gold on Databricks.

---

## Seed source

| File | Role | Rows (data) |
|------|------|-------------|
| `data/customers.csv` | Customer dimension | **1,006** |
| `data/products.csv` | Product dimension | **206** |
| `data/orders.csv` | Order **line items** (fact) | **5,163** |

Row counts verified from committed files (header + data rows). Do not regenerate or alter these files for submission.

---

## Generator

| Item | Location |
|------|----------|
| Script | `src/data_generation/generate_sample_data.py` |
| Design notes | `src/data_generation/DATA_GENERATION_NOTES.md` |
| Prompt history | `ai-prompts/data-generation.md` (Prompt 04) |

Stdlib-only Python. Default CLI produces the committed volumes when run with seed **42**.

---

## Seed

**Default random seed: `42`**

Reproducibility is documented in `DATA_GENERATION_NOTES.md` (re-run with same seed and sizes yields identical output).

Example:

```bash
python3 src/data_generation/generate_sample_data.py --seed 42
```

---

## Schema alignment

CSV headers match `database/schema.sql` and `generate_sample_data.py` column lists:

| Dataset | Primary key | Grain |
|---------|-------------|-------|
| customers | `customer_id` | One row per customer |
| products | `product_id` | One row per product |
| orders | `order_line_id` | One row per **line item**; `order_id` groups lines |

Logical foreign keys on orders:

- `customer_id` → `customers.customer_id`
- `product_id` → `products.product_id`

---

## Intentional defects (D01–D17)

Seed data is **not clean by design**. The generator injects **17 defect types** (328 injections) so Silver DQ modules can detect completeness, uniqueness, type, referential integrity, and business-logic failures.

Full matrix: `src/data_generation/DATA_GENERATION_NOTES.md` (do not treat source data as production-quality).

Examples:

| ID | Defect | Approx. count |
|----|--------|---------------|
| D01 | NULL/empty emails | 50 |
| D11 | Orphan `customer_id` (9999991) | 25 |
| D12 | Orphan `product_id` (9999992) | 25 |
| D17 | Catalog price mismatch on orders | ~20 |

Bronze preserves these defects (STRING ingest). Silver quarantines or excludes invalid rows per `data-quality-strategy.md`.

---

## Reproducibility

1. Clone repository (includes committed `data/*.csv`), **or**
2. Run `generate_sample_data.py` with `--seed 42` and documented default sizes (1,000 / 200 / 5,000 valid lines + defect rows → 1,006 / 206 / 5,163 total).

MD5/hash verification evidence: `ai-prompts/data-generation.md` validation log.

---

## What is NOT in seed data

The following are **not** columns in the committed CSVs (do not add them when loading into `schema.sql` tables):

- `total_amount`, `order_status`, `payment_date` on orders
- `cost`, `stock_quantity`, `reorder_level` on products
- One-row-per-order header table (pipeline uses line-item grain only)

Derived metrics (`line_revenue = quantity × unit_price`) are computed in Silver/Gold, not stored in CSV.
