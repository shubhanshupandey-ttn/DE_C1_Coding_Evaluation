# AI Prompts — Silver Layer

Evidence artifact for Phase 4 Silver implementation (Cursor-assisted development).

---

## Iteration 1: Silver Design & Task Planning

**PROMPT SENT:**

> Phase 4 SILVER LAYER — ITERATION 1 ONLY.
>
> Design/review Silver implementation against finalized data model and DQ strategy.
> Propose execution flow, required files, invalid-record representation, DQ summary design.
> Unity Catalog: `de_c1_coding_evaluation`; Bronze schema `bronze`; Silver schema `silver`.
> Silver tables: `silver_customers`, `silver_products`, `silver_orders`.
> Do NOT implement full Silver yet. Update `task-breakdown.md`. Document in `ai-prompts/silver-layer.md`. STOP.

**AI RESPONSE SUMMARY:**

Reviewed `data-quality-strategy.md`, `data-model.md`, `DATA_GENERATION_NOTES.md`, `design-notes.md`, and validated Bronze context (1,006 / 206 / 5,163 rows; known defects preserved).

**Proposed Silver design (summary):**

| Area | Decision |
|------|----------|
| Catalog / schema | `de_c1_coding_evaluation.silver` |
| Curated tables | `silver_customers`, `silver_products`, `silver_orders` (Delta, overwrite per run) |
| Quarantine | `silver_quarantine_records` — one row per failure event; traceable entity, key, category, reason |
| DQ summary | `silver_dq_summary` — per check category / table / run |
| Shared module | `silver_common.py` — catalog config, Bronze reads, typed casting helpers, write utilities |
| Orchestration | `create_silver_tables.py` — full pipeline entry point |
| DQ modules | Five files aligned to strategy (`01`–`05`) |
| Idempotency | Full overwrite of Silver + quarantine + DQ summary each run (no append accumulation) |
| Spark session | Reuse Bronze pattern (`resolve_spark`, notebook `spark=spark`) |
| Bronze changes | **None required** for Silver design |

**Proposed execution flow** (documented in `src/silver/SILVER_LAYER_NOTES.md`):

1. Read Bronze (STRING columns)
2. Trim / normalize string fields (no silent dropping)
3. Safe parse to typed Silver columns; retain parse-failure flags
4. Completeness → Uniqueness → Type validation (per entity)
5. Establish canonical valid `customers` / `products` parent keys
6. Referential integrity on `orders` (anti-join to canonical parents)
7. Business logic (dates, quantities, prices, segment, catalog-price match)
8. Write curated Silver tables (valid rows only)
9. Write quarantine records
10. Write DQ summary

**Required-field completeness (Iteration 1 design — aligned to Phase 4 spec + `data-quality-strategy.md`):**

| Entity | Required for completeness check |
|--------|--------------------------------|
| customers | `customer_id`, `customer_name`, `email` (minimum per spec); also `country`, `signup_date`, `customer_segment`, `lifetime_value` per existing DQ strategy |
| products | `product_id`, `product_name` (minimum); also `category`, `unit_price` per DQ strategy |
| orders | `order_line_id`, `order_id`, `customer_id`, `product_id`, `order_date` (minimum); also `quantity`, `unit_price` per DQ strategy |

**Uniqueness keys:** `customer_id`, `product_id`, `order_line_id` — **not** `order_id`.

**Known defect detection targets (from Phase 2 / Bronze validation):**

| Check | Expected detectable count (approx.) |
|-------|-------------------------------------|
| NULL/blank emails | 50 |
| Orphan `customer_id` on orders | 25 |
| Orphan `product_id` on orders | 25 |
| Non-positive `quantity` | 40 |
| Duplicate keys | per defect matrix D03, D08, D16 |
| Type / business logic | per defect matrix D04–D06, D09–D10, D13–D15, D17 |

**Files to implement (Iterations 2–5 — not created yet):**

- `src/silver/silver_common.py` (shared helpers)
- `src/silver/01_quality_completeness.py`
- `src/silver/02_quality_uniqueness.py`
- `src/silver/03_quality_type_validation.py`
- `src/silver/04_quality_referential_integrity.py`
- `src/silver/05_quality_business_logic.py`
- `src/silver/create_silver_tables.py`
- `src/silver/SILVER_LAYER_NOTES.md` (design draft created in Iteration 1)

**YOUR EVALUATION:**

_Initial Iteration 1 design — superseded by Iteration 1b design refinement (see below)._

**FINAL DECISION (Iteration 1 initial):** Design proposed; open decisions flagged for review.

---

## Iteration 1b: Resolve Open Design Decisions (Design Refinement)

**PROMPT SENT:**

> Phase 4 Silver Iteration 1 — resolve open design decisions. Update Silver design documentation only.
> Do NOT create or modify Silver implementation code. Do NOT start Iteration 2.
>
> Finalize:
> 1. Full completeness required-field list from `data-quality-strategy.md`
> 2. Single centralized quarantine table `silver_quarantine_records`
> 3. STRING identifiers in Silver with numeric-parse type validation
> 4. D17 catalog-price mismatch — quarantine only, no auto-correction
> 5. Date business rules use `current_date()`; `run_timestamp` for traceability
> 6. Keep existing execution order; no new DQ categories
>
> Update: `SILVER_LAYER_NOTES.md`, `ai-prompts/silver-layer.md`, `data-quality-strategy.md`, `spec.md`, `task-breakdown.md`. STOP.

**AI RESPONSE SUMMARY:**

Updated design documentation to reflect all six finalized decisions:

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Completeness | Full required-field lists from `data-quality-strategy.md` |
| 2 | Quarantine | Single table `de_c1_coding_evaluation.silver.silver_quarantine_records` |
| 3 | Identifier types | STRING in Silver; numeric parseability validated in type check |
| 4 | D17 | Quarantine only; preserve Bronze values; no auto-correction |
| 5 | Date rules | Runtime `current_date()`; `run_timestamp` on quarantine/DQ summary |
| 6 | Execution order | Unchanged; five DQ categories only |

Removed "open decisions" section from `SILVER_LAYER_NOTES.md`. Updated `data-quality-strategy.md` type-validation rules, D17 handling, and execution model. Updated `spec.md` and `task-breakdown.md`.

**No Silver Python code created or modified.**

**YOUR EVALUATION:**

The four open Silver design decisions from Iteration 1 were reviewed and resolved per developer instruction:

1. ✓ Full completeness field list (not minimum subset)
2. ✓ Single centralized quarantine table
3. ✓ STRING identifiers with numeric-parse validation
4. ✓ D17 quarantine-only (no auto-correction)

Additional clarifications applied: runtime `current_date()` for date rules; `run_timestamp` traceability; execution order unchanged.

The resulting design is **internally consistent** with `data-model.md` and `data-quality-strategy.md` and is **ready for Iteration 2 implementation** pending developer approval.

**FINAL DECISION:** **ACCEPTED** — Silver design finalized for implementation. Iteration 2 (code) not started.

---

## Iteration 2: Type Standardization, Completeness & Uniqueness

**PROMPT SENT:**

> Phase 4 Silver Iteration 2: implement type standardization/safe parsing, completeness, uniqueness only.
> Use finalized design from SILVER_LAYER_NOTES.md and data-quality-strategy.md.
> Catalog `de_c1_coding_evaluation`, Bronze schema `bronze`.
> IDs remain STRING with numeric-parse validation. Full completeness field lists.
> Deterministic duplicate handling (first canonical occurrence).
> Do NOT implement FK, business logic, orchestration, quarantine write, DQ summary, Gold, Dashboard.
> Update ai-prompts/silver-layer.md and task-breakdown.md. STOP after Iteration 2.

**AI RESPONSE SUMMARY:**

Implemented:

| File | Purpose |
|------|---------|
| `silver_common.py` | Config, Bronze reads, trim/typed columns, failure builders, deterministic ranking |
| `01_quality_completeness.py` | Full required-field completeness per DQ strategy |
| `02_quality_uniqueness.py` | PK uniqueness (`customer_id`, `product_id`, `order_line_id`) |
| `03_quality_type_validation.py` | ID parseability, dates, decimals, ints, email format |
| `test_silver_helpers.py` | Local unit tests for pure-Python parse/validation helpers |

**Design decisions followed:**

- Execution order: trim + type parse → completeness → uniqueness → type validation (per SILVER_LAYER_NOTES)
- Failures use quarantine-compatible schema (not written to Delta until Iteration 4)
- No referential integrity or business logic code added
- Bronze unchanged

**Validation performed (local):**

| Check | Result |
|-------|--------|
| `py_compile` all Silver `.py` files | **PASS** |
| `test_silver_helpers.py` | **PASS** |
| Databricks execution against Bronze | **Not performed** (no PySpark in Cursor env) |

**Issues encountered:**

- Removed unused imports during review (`02_quality_uniqueness.py`, `silver_common.py`)
- `build_failure_df` uses `rdd.isEmpty()` — acceptable for module-level runs; orchestration may optimize in Iteration 5

**Refinements:**

- Pure-Python helpers (`is_numeric_identifier`, `is_valid_email_format`, etc.) separated for local testing without Spark
- Deterministic duplicate tiebreakers: sorted column names + `_row_num` from stable window order

**Accepted suggestions:**

- Shared `silver_common.py` module (per design)
- Quarantine-compatible failure schema for Iteration 4 compatibility
- Per-module `main()` for individual Databricks notebook testing

**Rejected / deferred:**

- Full `create_silver_tables.py` orchestration → Iteration 5
- Writing `silver_quarantine_records` Delta table → Iteration 4
- FK and business logic modules → Iteration 3

**YOUR EVALUATION:**

_To be completed by developer after Databricks module testing._

Iteration 2 modules implement the approved completeness, uniqueness, and type-validation rules. Failures are structured for later quarantine. Local helper tests pass. Databricks validation against Bronze tables is required before final acceptance.

**FINAL DECISION:** _Pending developer review and Databricks module run._

---

## Iteration 3: (Not started)

_Referential integrity and business logic — pending._

---

## Iteration 4: (Not started)

_Quarantine + DQ summary — pending._

---

## Iteration 5: (Not started)

_Full orchestration + Databricks validation — pending._

---

## Cursor Evaluation Evidence (Phase 4 — in progress)

| Requirement | Iteration 1 evidence |
|-------------|---------------------|
| Persistent context | Foundation docs + Bronze validation + `tool-specific/cursor-workflow/*` |
| Iteration | Deliberate 5-iteration plan; Iteration 1 design + 1b refinement before code |
| Validation | Iteration 2: local `py_compile` + helper tests PASS; Databricks pending |
| Human review | Iteration 1b design ACCEPTED; Iteration 2 pending Databricks run |
