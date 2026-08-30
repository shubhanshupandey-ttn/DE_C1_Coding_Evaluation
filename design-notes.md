# Design Notes

High-level architecture and design direction for the Databricks Medallion Pipeline. **Current status:** Bronze (Phase 3), Silver + DQ (Phase 4), Gold (Phase 5), Dashboard (Phase 6), and pipeline validation are **implemented and Databricks-validated** (see `VALIDATION_REPORT.md`).

## Architecture Overview

Medallion flow from generated CSVs through analytics:

```
data/  (customers.csv, orders.csv, products.csv)
   │
   │  src/data_generation/generate_sample_data.py
   ▼
BRONZE  (src/bronze/)     — raw ingestion, minimal transformation
   ▼
SILVER  (src/silver/)     — cleanse, conform, DATA QUALITY CHECKS
   ▼
GOLD    (src/gold/)       — analytical aggregates / KPIs
   ▼
DASHBOARD (src/dashboard/) — visualization-ready SQL + guide
```

**Design goals:** practical Databricks patterns, clear layer separation, quality in Silver, end-to-end consistency across customers / orders / products.

---

## Data Model & Schema

Logical entities (detail in `data-model.md`):

| Entity | Role | Planned source |
|--------|------|----------------|
| **customers** | Buyers; dimension for segmentation and revenue-by-customer | `data/customers.csv` |
| **orders** | Purchase transactions; fact table for trends and sales | `data/orders.csv` |
| **products** | Sellable items; dimension for sales-by-product | `data/products.csv` |

**Relationships (logical):**

- Customer **1 → many** order line items
- Product **many → many** orders via line items
- **`order_id`** groups multiple lines; **`order_line_id`** is the row-level primary key

Physical schemas finalized in Phase 2 — see `data-model.md`.

---

## Bronze Layer Design

| Aspect | Implementation (Phase 3) |
|--------|--------------------------|
| **Purpose** | Land raw-ish source data with minimal change |
| **Inputs** | CSV files from `data/` |
| **Outputs** | Delta tables: `bronze.bronze_customers`, `bronze.bronze_products`, `bronze.bronze_orders` |
| **Scripts** | `01_ingest_customers.py`, `02_ingest_orders.py`, `03_ingest_products.py`, `ingest_all.py`, `bronze_common.py` |
| **Source column types** | **STRING** (preserves invalid dates, malformed values, empty strings) |
| **Metadata** | `_ingestion_timestamp`, `_source_file` |
| **Write mode** | `overwrite` (default) — full reload for dev/assessment |
| **Schema bootstrap** | `CREATE SCHEMA IF NOT EXISTS bronze` |
| **Quality** | None — no filtering or remediation of Phase 2 defects |

**Optional:** `--catalog <name>` for Unity Catalog qualified names.

**Not in Bronze:** type casting, deduplication, FK validation, quarantine, business rules.

See `src/bronze/BRONZE_LAYER_NOTES.md` for execution and validation details.

---

## Silver Layer Design

**Status:** Implemented (Phase 4). Authoritative execution and validation evidence: `src/silver/SILVER_LAYER_NOTES.md`.

| Aspect | Design direction |
|--------|----------------|
| **Purpose** | Cleansed, typed, analyst-trusted tables |
| **Inputs** | Bronze tables |
| **Outputs** | Silver entity tables via `create_silver_tables.py` |
| **Transformations** | Standardize types, trim strings, apply null handling rules |
| **Quality modules** | Five scripts aligned to `data-quality-strategy.md` |

| Module | Category |
|--------|----------|
| `01_quality_completeness.py` | Required fields present |
| `02_quality_uniqueness.py` | No duplicate business keys |
| `03_quality_type_validation.py` | Valid types and formats |
| `04_quality_referential_integrity.py` | FK relationships valid |
| `05_quality_business_logic.py` | Domain rules (amounts, dates, etc.) |

**Finalized during implementation:** quarantine (`silver_quarantine_records`), DQ summary (`silver_dq_summary`), check order, and reporting — see `SILVER_LAYER_NOTES.md` and `data-quality-strategy.md`.

---

## Gold Layer Design

**Status:** Implemented (Phase 5). Authoritative contract and validation: `src/gold/GOLD_LAYER_NOTES.md`.

| Aspect | Design direction |
|--------|----------------|
| **Purpose** | Pre-computed analytics for reporting |
| **Inputs** | Trusted Silver tables |
| **Outputs** | Four Gold Delta tables in `de_c1_coding_evaluation.gold` |
| **Implementation** | Primarily SQL (`.sql` files) + `create_gold_tables.py` |

**Authoritative contract:** `src/gold/GOLD_LAYER_NOTES.md` (Iteration 1b — finalized).

| Table | Theme |
|-------|-------|
| `gold_sales_by_product` | Product-level sales metrics |
| `gold_revenue_by_customer` | Customer-level revenue |
| `gold_daily_weekly_trends` | Daily and weekly time-series trends |
| `gold_customer_segmentation` | Customer segments with behavioral aggregates |

**Planned SQL files:**

| File | Maps to |
|------|---------|
| `01_sales_by_product.sql` | `gold_sales_by_product` |
| `02_revenue_by_customer.sql` | `gold_revenue_by_customer` |
| `03_daily_weekly_trends.sql` | `gold_daily_weekly_trends` |
| `04_customer_segmentation.sql` | `gold_customer_segmentation` |

Metric formulas, time grains, column names, and write semantics are **finalized** in `GOLD_LAYER_NOTES.md`.

---

## Data Quality Validation Strategy

Quality runs primarily in **Silver** (not Bronze, not as a substitute in Gold).

| Category | What it validates | Where documented |
|----------|-------------------|------------------|
| Completeness | No NULLs in critical fields | `data-quality-strategy.md` |
| Uniqueness | No duplicate business keys | `data-quality-strategy.md` |
| Type validation | Values match expected types/ranges | `data-quality-strategy.md` |
| Referential integrity | FKs resolve to parent tables | `data-quality-strategy.md` |
| Business logic | Domain rules (positive qty, valid dates, etc.) | `data-quality-strategy.md` |

Gold assumes Silver inputs meet agreed thresholds. See `data-quality-strategy.md` for What / How / Threshold / Result per check. Observed pass/fail metrics: `SILVER_LAYER_NOTES.md` and `VALIDATION_REPORT.md`.

---

## Debugging Approach

Recorded in `debugging-notes.md` and `ai-prompts/debugging.md` (Bronze Spark session, Silver Serverless compatibility, RI alignment, dashboard schema clarification, validation SQL fixes).

| Step | Action |
|------|--------|
| 1 | Reproduce with concrete job output, row samples, or error messages (redact secrets) |
| 2 | Isolate layer (generation → Bronze → Silver → Gold → dashboard) |
| 3 | Compare record counts and schemas between layers |
| 4 | Use AI for hypothesis/fix suggestions **after** sharing actual errors |
| 5 | Document root cause and resolution for non-trivial issues |

---

## Technology Direction

| Topic | Established | To be finalized |
|-------|-------------|-----------------|
| Platform | Databricks lakehouse / medallion | Workspace config |
| Languages | Python, PySpark, SQL | — |
| Table format | Delta Lake (typical) | Partitioning, optimization |
| Orchestration | Layer scripts + entry points | Jobs, bundles, scheduling |
| Config | No secrets in repo | Parameterization |

---

## Consistency Checklist (phases 2–6)

- [x] Entity names match `data-model.md`
- [x] Quality rules match `data-quality-strategy.md`
- [x] Gold metrics align with Silver fields
- [x] Dashboard queries reference existing Gold objects
- [x] Prompts recorded in correct `ai-prompts/` file
