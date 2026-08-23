# Specification — Phase 2 Data Generation

Specification implemented by Cursor-assisted development in Phase 2.

## Objective

Generate reproducible sample CSVs (`customers`, `products`, `orders`) for a Databricks medallion pipeline, with documented intentional quality defects for future Silver validation.

## Scope

### In scope

- `src/data_generation/generate_sample_data.py`
- `src/data_generation/DATA_GENERATION_NOTES.md`
- `data/customers.csv`, `data/products.csv`, `data/orders.csv`
- Updates to `data-model.md`, `data-quality-strategy.md`, `requirements-analysis.md`, `README.md`
- `ai-prompts/data-generation.md`
- Cursor workflow evidence in `tool-specific/cursor-workflow/`

### Out of scope

- Bronze, Silver, Gold, dashboard, database implementation
- External dependencies (stdlib only)
- Secrets or environment-specific paths

## Data Model

### Granularity

**Order line items** in `orders.csv`:

- `order_line_id` — unique per row (PK)
- `order_id` — groups 1–3 lines per order
- Revenue derived as `quantity × unit_price`

### Schemas

See `data-model.md` and `DATA_GENERATION_NOTES.md` for full column lists.

## Relationships (valid data)

- `orders.customer_id` → `customers.customer_id`
- `orders.product_id` → `products.product_id`
- Valid ID ranges: customers `1..N`, products `1..M`

## Reproducibility

| Parameter | Default |
|-----------|---------|
| `--seed` | `42` |
| `--customers` | `1000` |
| `--products` | `200` |
| `--order-lines` | `5000` |
| `--output-dir` | `<repo>/data` |

Same seed + sizes → identical CSV output (verified).

## Defect Strategy

17 defect types, 328 total injections, mapped to five Silver check categories. Full matrix in `DATA_GENERATION_NOTES.md`.

Categories covered:

1. Completeness — null/empty required fields
2. Uniqueness — duplicate PKs (`customer_id`, `product_id`, `order_line_id`)
3. Type validation — invalid dates, emails, non-numeric prices
4. Referential integrity — orphan FKs (`9999991`, `9999992`)
5. Business logic — future dates, negative prices, non-positive quantity, catalog price mismatch

## Generator Constraints

- Modular functions (generate clean → inject defects → write CSV)
- Deterministic `random.Random(seed)`
- Print row counts and defect statistics
- Executable from repository root
- No hardcoded credentials

## Gold Analytics Support

Schemas must support:

- Sales by product (`product_id`, `category`, sum quantity/revenue)
- Revenue by customer (`customer_id`, sum line revenue)
- Daily/weekly trends (`order_date`)
- Customer segmentation (`customer_segment`, `lifetime_value`, order aggregates)

## Acceptance Criteria

- [x] Three CSV files generated
- [x] Schemas documented
- [x] Defect matrix with counts and Silver mapping
- [x] Reproducibility verified (seed 42)
- [x] Documentation and prompt artifacts created
- [x] No Bronze/Silver/Gold code created

## Validation Evidence

Recorded in `DATA_GENERATION_NOTES.md` and Phase 2 implementation report.

---

# Specification — Phase 4 Silver (Iteration 1 — Design Finalized)

**Status:** Design finalized (Iteration 1b). **No Silver Python implementation yet.**

## Objective

Transform Bronze Delta tables into curated, typed Silver tables with five DQ categories, quarantine traceability, and DQ summary reporting.

## Environment

| Item | Value |
|------|-------|
| Catalog | `de_c1_coding_evaluation` |
| Bronze inputs | `bronze.bronze_customers`, `bronze_products`, `bronze_orders` |
| Silver schema | `silver` |
| Silver outputs | `silver_customers`, `silver_products`, `silver_orders` |
| Quarantine | `silver_quarantine_records` (single centralized table) |
| DQ summary | `silver_dq_summary` |

## Finalized Design Decisions

| Area | Decision |
|------|----------|
| Completeness | Full required-field lists from `data-quality-strategy.md` |
| Quarantine | Single table for all entities and five DQ categories |
| Identifiers | STRING in Silver; numeric parse validated in type check |
| D17 catalog-price | Quarantine only — no auto-correction |
| Date rules | `current_date()` at runtime; `run_timestamp` for traceability |
| Execution order | Bronze → trim → type → completeness → uniqueness → type validation → canonical parents → FK → business logic → Silver → quarantine → DQ summary |
| Idempotency | Overwrite all Silver objects per run |

## Iteration Plan

1. **Iteration 1 + 1b:** Design + resolve open decisions — **complete**
2. Iteration 2: Types, completeness, uniqueness — **not started**
3. Iteration 3: Type validation, FK, business logic — pending
4. Iteration 4: Quarantine + DQ summary — pending
5. Iteration 5: Orchestration + Databricks validation — pending

See `src/silver/SILVER_LAYER_NOTES.md` and `tool-specific/cursor-workflow/task-breakdown.md`.

