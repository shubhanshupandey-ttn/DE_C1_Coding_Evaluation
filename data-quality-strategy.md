# Data Quality Strategy

Data quality framework for the **Silver layer**, aligned with Phase 2 sample data schemas. Silver checks are **implemented and Databricks-validated** (see `SILVER_LAYER_NOTES.md`, `ai-prompts/silver-layer.md`, `VALIDATION_REPORT.md`).

## Quality Checks Overview

---

### 1. Completeness Check

| Attribute | Definition |
|-----------|------------|
| **What** | No NULL or empty values in required fields |
| **How** | Count rows where `column IS NULL OR TRIM(column) = ''` per table |
| **Threshold** | ≥ 99% of rows complete per required field (target; tune in Silver) |
| **Result** | Flag or quarantine failing rows; report pass % |

**Required fields:**

| Table | Required columns |
|-------|------------------|
| customers | `customer_id`, `customer_name`, `email`, `country`, `signup_date`, `customer_segment`, `lifetime_value` |
| products | `product_id`, `product_name`, `category`, `unit_price` |
| orders | `order_line_id`, `order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `unit_price` |

**Sample defects to detect:** D01, D02, D07 (see `DATA_GENERATION_NOTES.md`)

**Planned handling:** Quarantine incomplete rows.

---

### 2. Uniqueness Check

| Attribute | Definition |
|-----------|------------|
| **What** | Primary business keys are unique within each entity table |
| **How** | `GROUP BY key HAVING COUNT(*) > 1` |
| **Threshold** | 100% unique keys in Silver output |
| **Result** | Flag duplicates; retain one canonical row or quarantine extras |

**Keys:**

| Table | Unique key |
|-------|------------|
| customers | `customer_id` |
| products | `product_id` |
| orders | `order_line_id` (not `order_id`) |

**Sample defects to detect:** D03, D08, D16

**Planned handling:** Quarantine duplicate rows beyond the first occurrence.

---

### 3. Type Validation Check

| Attribute | Definition |
|-----------|------------|
| **What** | Values parse to expected types and formats |
| **How** | Cast to target types; validate date pattern and email pattern where applicable |
| **Threshold** | ≥ 99% parseable per typed column (target) |
| **Result** | Flag rows that fail casting or format rules |

**Rules:**

| Table | Column | Expected type / format |
|-------|--------|------------------------|
| customers | `customer_id` | STRING; numerically parseable |
| customers | `signup_date` | ISO date `YYYY-MM-DD` |
| customers | `email` | Contains `@` and domain (basic format) |
| customers | `lifetime_value` | Decimal ≥ 0 |
| products | `product_id` | STRING; numerically parseable |
| products | `unit_price` | Decimal numeric |
| orders | `order_line_id`, `order_id`, `customer_id`, `product_id` | STRING; numerically parseable |
| orders | `order_date` | ISO date `YYYY-MM-DD` |
| orders | `quantity` | Integer |
| orders | `unit_price` | Decimal numeric |

**Silver storage:** identifier columns remain STRING after validation. Malformed identifiers (e.g. `"INVALID"`) fail type validation and are quarantined.

**Sample defects to detect:** D04, D05, D09, D13

**Planned handling:** Reject or quarantine unparseable rows.

---

### 4. Referential Integrity Check

| Attribute | Definition |
|-----------|------------|
| **What** | Foreign keys in orders resolve to parent dimension keys |
| **How** | Left anti-join orders to customers/products on FK columns |
| **Threshold** | ≥ 99.9% valid FK references (target) |
| **Result** | Flag orphan order lines |

**Rules:**

| Child | FK | Parent | Parent key |
|-------|-----|--------|------------|
| orders | `customer_id` | customers | `customer_id` |
| orders | `product_id` | products | `product_id` |

**Sample defects to detect:** D11 (`customer_id = 9999991`), D12 (`product_id = 9999992`)

**Planned handling:** Quarantine orphan order lines.

---

### 5. Business Logic Check

| Attribute | Definition |
|-----------|------------|
| **What** | Domain rules beyond structural validity |
| **How** | Rule filters on cleansed typed data |
| **Threshold** | ≥ 99% pass per rule (target) |
| **Result** | Flag or quarantine violating rows |

**Rules:**

| Rule | Table | Logic |
|------|-------|-------|
| Positive quantity | orders | `quantity > 0` |
| No future signup | customers | `signup_date <= current_date()` |
| No future orders | orders | `order_date <= current_date()` |
| Non-negative catalog price | products | `unit_price >= 0` |
| Catalog price consistency | orders | `orders.unit_price = products.unit_price` for same `product_id` |
| Valid segment | customers | `customer_segment IN ('Premium','Standard','Basic')` |

**Sample defects to detect:** D06, D10, D14, D15, D17

**D17 handling (finalized):** Detect mismatch and **quarantine** the order line. Do **not** auto-replace order `unit_price` with product catalog price. Preserve original Bronze value in quarantine traceability.

**Date rules:** `signup_date <= current_date()` and `order_date <= current_date()` use runtime `current_date()` (no hard-coded evaluation date). `run_timestamp` on quarantine and DQ summary provides pipeline-run traceability.

**Planned handling:** Quarantine all business-logic failures.

---

## Quality Metrics Report

Planned Silver output (example):

| Check | Table | Rows tested | Rows passed | Rows failed | Pass % |
|-------|-------|-------------|-------------|-------------|--------|
| Completeness | customers | 1,006 | TBD | TBD | TBD |
| Uniqueness | customers | 1,006 | TBD | TBD | TBD |
| Type validation | orders | 5,163 | TBD | TBD | TBD |
| Referential integrity | orders | 5,163 | TBD | TBD | TBD |
| Business logic | orders | 5,163 | TBD | TBD | TBD |

Baseline defect counts documented in `src/data_generation/DATA_GENERATION_NOTES.md`.

---

## Sample Data Quality Issues (Phase 2)

| Issue type | Target check | Documented count |
|------------|--------------|------------------|
| NULL / empty required fields | Completeness | 68 (50 email + 10 name + 8 product name) |
| Duplicate primary keys | Uniqueness | 20 (6 + 6 + 8 line-id collisions) |
| Invalid type / format | Type validation | 95 |
| Orphan FK references | Referential integrity | 50 |
| Invalid business values | Business logic | 95 |

Full defect matrix: `DATA_GENERATION_NOTES.md` (17 defect types, 328 injections).

---

## Execution Model (Finalized — design)

```
Bronze tables
     ▼
Trim / cleanse + safe typing
     ├── 01_quality_completeness.py
     ├── 02_quality_uniqueness.py
     ├── 03_quality_type_validation.py
     ├── Canonical valid customers / products
     ├── 04_quality_referential_integrity.py
     └── 05_quality_business_logic.py
     ▼
Silver curated tables (valid rows only)
     +
silver_quarantine_records (invalid rows — single centralized table)
     +
silver_dq_summary (per-run metrics)
```

**Design decisions finalized** (see `src/silver/SILVER_LAYER_NOTES.md`):

- Quarantine: `de_c1_coding_evaluation.silver.silver_quarantine_records`
- DQ summary: `de_c1_coding_evaluation.silver.silver_dq_summary`
- Write mode: overwrite per run (idempotent)
- Implementation: custom PySpark (not Deequ)

---

## Traceability

| Artifact | Role |
|----------|------|
| `src/data_generation/DATA_GENERATION_NOTES.md` | Defect seeding evidence |
| `data-model.md` | Schema and keys |
| `src/silver/*.py` | Implementation (not started) |
| `ai-prompts/silver-layer.md` | Prompts + design iterations |
