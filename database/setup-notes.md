# Database Setup Notes — Source Schema Artifact

How reviewers should interpret and optionally use `database/schema.sql` with the committed seed CSVs.

---

## What this directory is

| Artifact | Role |
|----------|------|
| `schema.sql` | Documentary DDL for the **source** relational model (customers, products, order line items) |
| `seed-data-notes.md` | Provenance of `data/*.csv` and defect strategy |
| `setup-notes.md` | This file — setup flow and limitations |

**Implemented:** schema + seed/setup **documentation**  
**Not claimed:** provisioning of an external MySQL/PostgreSQL/SQL Server instance in this project

The **validated analytics pipeline** runs on **Databricks Serverless** (Unity Catalog `de_c1_coding_evaluation`). Bronze/Silver/Gold/Dashboard are Delta tables and SQL there — not tables created by this `schema.sql`.

---

## Distinctions

| Layer | Technology | Evidence |
|-------|------------|----------|
| Source schema (this directory) | Portable relational DDL + CSV files | `database/`, `data/` |
| Bronze / Silver / Gold | Databricks Delta Lake | `src/bronze/`, `src/silver/`, `src/gold/` |
| Dashboard | Databricks SQL dashboard | `src/dashboard/`, screenshots |
| End-to-end validation | `pipeline_validation.sql` | **26/26 PASS** on Databricks Serverless |

Do not conflate loading CSVs into a local RDBMS with executing the medallion pipeline on Databricks.

---

## Intended review flow

1. **Read** `database/schema.sql` — source table definitions and grain (order line items).
2. **Read** `database/seed-data-notes.md` — row counts, seed 42, D01–D17 defects.
3. **Inspect** committed CSVs under `data/` (headers and sample rows).
4. **Trace** into pipeline docs: `BRONZE_LAYER_NOTES.md` → `SILVER_LAYER_NOTES.md` → `GOLD_LAYER_NOTES.md`.
5. **Optional:** Load CSVs into a relational database that supports the DDL dialect (see below).

---

## Optional: load CSVs into a relational database

Only if you want a local **source** copy for inspection. **Not required** for Databricks pipeline execution.

### Prerequisites

- A SQL engine that accepts the DDL in `schema.sql` (written as PostgreSQL-compatible portable SQL)
- CSV files from `data/` (already in the repository)

### Suggested steps (PostgreSQL example)

```sql
-- 1. Apply schema (adjust schema name / connection as needed)
\i database/schema.sql
```

```bash
# 2. Load from repository root (paths relative to your client)
# Example using psql \copy — column order matches CSV headers

\copy source.customers FROM 'data/customers.csv' WITH (FORMAT csv, HEADER true);
\copy source.products  FROM 'data/products.csv'  WITH (FORMAT csv, HEADER true);
\copy source.orders    FROM 'data/orders.csv'    WITH (FORMAT csv, HEADER true);
```

```sql
-- 3. Validate row counts
SELECT 'customers' AS tbl, COUNT(*) FROM source.customers
UNION ALL SELECT 'products', COUNT(*) FROM source.products
UNION ALL SELECT 'orders', COUNT(*) FROM source.orders;
-- Expected: 1006, 206, 5163
```

### Loading notes

- Foreign keys are **not enforced** in `schema.sql` because seed data intentionally includes orphan keys (D11/D12) and other defects.
- Some values may not parse cleanly into strict DATE/DECIMAL types in all engines; Bronze ingests everything as STRING for that reason. For strict RDBMS loads, inspect failing rows or load to staging text columns first.
- **Do not** modify `data/*.csv` in the repository to make loads succeed.

---

## Connection to Bronze

Bronze ingestion reads the same CSV files directly (not via this RDBMS):

```bash
python3 src/bronze/ingest_all.py --dry-run
# Databricks: ingest_all.py with catalog de_c1_coding_evaluation
```

Bronze tables: `bronze.bronze_customers`, `bronze.bronze_products`, `bronze.bronze_orders` — all source columns as **STRING**, defects preserved.

---

## Validation performed (artifact-level)

| Check | Result |
|-------|--------|
| `schema.sql` columns match CSV headers | **PASS** |
| Column order matches `generate_sample_data.py` | **PASS** |
| Primary keys: `customer_id`, `product_id`, `order_line_id` | **PASS** |
| Order grain = line item | **PASS** |
| Logical FKs documented | **PASS** |
| Defect strategy documented (not implied clean) | **PASS** |
| External DB deployment | **Not executed / not claimed** |
| Pipeline code unchanged | **PASS** (Step 7 scope) |

---

## Limitations

- No connection strings, credentials, or provisioned database host exist in this repository.
- `COMMENT ON` syntax requires PostgreSQL or compatible engines; adapt comments for other dialects if needed.
- Pipeline validation (**26/26 PASS**) does not include loading this schema into an external RDBMS.
