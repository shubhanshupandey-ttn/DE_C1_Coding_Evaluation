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
| `_load_silver_common.py` | Fresh module loader for Databricks notebook runs |

**Design decisions followed:**

- Execution order: trim + type parse → completeness → uniqueness → type validation (per SILVER_LAYER_NOTES)
- Failures use quarantine-compatible schema (not written to Delta until Iteration 4)
- No referential integrity or business logic code added
- Bronze unchanged

**Local validation:**

| Check | Result |
|-------|--------|
| `py_compile` all Silver `.py` files | **PASS** |
| `test_silver_helpers.py` | **PASS** |

**Serverless compatibility (post-implementation refinements):**

Iteration 2 was validated on **Databricks Serverless**. Several compatibility fixes were applied during validation (no change to DQ rules or acceptance scope):

| Issue | Resolution |
|-------|------------|
| `df.rdd.isEmpty()` blocked on Serverless | Removed; use `filter().select()` + `unionByName()` |
| Array + explode failure builder (v3) | Reverted; produced false 100% completeness failures on Spark Connect |
| Global window for `_row_num` | Replaced with partitioned window + row-content hash tiebreaker |
| `to_date('NOT-A-DATE')` throws under ANSI SQL | Use SQL `try_to_date` via `F.expr` (NULL on invalid) |
| `F.try_cast` unavailable in notebook PySpark | Int/decimal parsing uses `when` + `rlike` + `.cast()` only on matched patterns |

Final validated marker: **`SERVERLESS_COMPAT_VERSION = 7`**

---

### Databricks Serverless validation (executed)

**Environment:**

| Setting | Value |
|---------|-------|
| Compute | Databricks Serverless |
| Catalog | `de_c1_coding_evaluation` |
| Bronze schema | `bronze` |
| Compat marker | `SERVERLESS_COMPAT_VERSION = 7` |

**Modules exercised:**

- `src/silver/silver_common.py`
- `src/silver/01_quality_completeness.py`
- `src/silver/02_quality_uniqueness.py`
- `src/silver/03_quality_type_validation.py`

**Note on failure-record semantics:** DQ outputs are **failure records per validation rule / failed field**, not necessarily one record per unique bad row. Defects may overlap across categories (completeness, uniqueness, type validation). Do not expect total failure counts to equal total unique defective rows.

---

#### Completeness validation

| Entity | Observed failures | Expected / documented evidence | Assessment |
|--------|-------------------|-------------------------------|------------|
| customers | **60** | 50 null/empty emails (D01) + 10 null/empty customer names (D02) = **60** | **Exact match** |
| products | **9** | 8 documented `product_name` completeness defects (D07) | **Close** — 8 injected nulls plus 1 additional blank/edge-case completeness failure observed in actual Bronze data; recorded as observed result, not adjusted to 8 |
| orders | **0** | No major completeness injections in Phase 2 | **Correct** |

Completeness validation **successfully executed** on Databricks Serverless.

---

#### Uniqueness validation

| Entity | Uniqueness key | Observed failures | Expected | Assessment |
|--------|----------------|-------------------|----------|------------|
| customers | `customer_id` | **6** | 6 (D03) | **Exact match** |
| products | `product_id` | **6** | 6 (D08) | **Exact match** |
| orders | `order_line_id` (**not** `order_id`) | **8** | 8 (D16) | **Exact match** |

- Non-canonical duplicate occurrences are flagged as failures; canonical first occurrence is retained deterministically.
- Order duplicate failure `business_key` values correctly show repeated keys such as `47`, `47`, `48`, `48`, `52`, `52`, `72`, `72` — expected for non-canonical `order_line_id` collisions.

**Serverless warning observed (not a validation failure):**

```
WARN WindowExpression: No Partition Defined for Window operation!
```

This warning appeared during an earlier uniqueness run (global window). Later implementation uses a **partitioned** window on the business key with hash tiebreaker. Uniqueness results above were obtained with functionally correct duplicate detection; the warning does not invalidate the observed counts.

Uniqueness validation **successfully executed** on Databricks Serverless.

---

#### Type validation

| Entity | Observed failures | Breakdown | Assessment |
|--------|-------------------|-----------|------------|
| customers | **50** | 30 invalid email + 20 invalid `signup_date` | Matches D05 + D04 |
| products | **15** | 15 non-parseable `unit_price` | Matches D09 |
| orders | **30** | 30 invalid `order_date` | Matches D13 |
| **Total** | **95** | 50 + 15 + 30 | **Exact match** with documented Phase 2 type/format defect count |

**Validated behavior:**

- IDs remain **STRING**; numeric parseability validated separately
- Dates parsed safely (`try_to_date` — invalid → NULL in `*_typed` columns)
- Decimal/integer fields parsed safely (`when` + `rlike` + cast)
- Invalid values are **not** silently coerced; they become NULL in typed columns and produce explicit failure records
- Email format validation working

Type validation **successfully executed** on Databricks Serverless.

---

#### Serverless compatibility summary

| Check | Result |
|-------|--------|
| Completeness run on Serverless | **PASS** (no RDD error) |
| Uniqueness run on Serverless | **PASS** (no RDD error) |
| Type validation run on Serverless | **PASS** (no RDD error) |
| Implementation uses DataFrame APIs | **Yes** — no RDD-based processing in validated execution path |
| All Serverless limitations eliminated | **Not claimed** — only the above validations were performed |

---

**Issues encountered (implementation + validation):**

- Initial `df.rdd.isEmpty()` incompatible with Serverless
- v3 array+explode failure builder caused false completeness inflation (7× row count)
- Global window warning on uniqueness (addressed with partitioned ranking)
- ANSI `to_date` throw on `NOT-A-DATE`; resolved with `try_to_date` SQL expression
- `F.try_cast` not available in Databricks notebook PySpark bindings

**Refinements:**

- Pure-Python helpers separated for local testing without Spark
- Deterministic duplicate ranking: partition by business key; tiebreaker columns + row-content hash
- Fresh module loading pattern for Databricks notebooks (`_load_silver_common.py`)

**Accepted suggestions:**

- Shared `silver_common.py` module (per design)
- Quarantine-compatible failure schema for Iteration 4 compatibility
- Per-module `run_*_all()` for individual Databricks notebook testing

**Rejected / deferred:**

- Full `create_silver_tables.py` orchestration → Iteration 5
- Writing `silver_quarantine_records` Delta table → Iteration 4
- FK and business logic modules → Iteration 3

**YOUR EVALUATION:**

| Criterion | Result |
|-----------|--------|
| Local `py_compile` | **PASS** |
| Local helper tests | **PASS** |
| Databricks Serverless completeness | **PASS** — customers exact (60); products observed 9 (documented 8 + 1 edge case); orders 0 |
| Databricks Serverless uniqueness | **PASS** — 6 / 6 / 8 exact match |
| Databricks Serverless type validation | **PASS** — 95 total exact match with Phase 2 type/format defects |
| Results align with defect matrix | **Yes** (with documented products completeness observation) |
| Bronze unchanged | **Yes** |
| Iteration 3 not started | **Yes** |

**FINAL DECISION:** **ACCEPTED** — Silver Iteration 2 complete. Databricks Serverless validation performed and recorded. Proceed to Iteration 3 when approved.

---

## Iteration 3: Referential Integrity + Business Logic

**PROMPT SENT:**

> Silver Layer Iteration 3 ONLY: implement `04_quality_referential_integrity.py` and `05_quality_business_logic.py`.
> Reuse Iteration 2 patterns and Serverless-compatible DataFrame APIs.
> Canonical valid parent keys from Iteration 2 pass logic (not raw Bronze).
> D17 quarantine-only. No quarantine writes, DQ summary, orchestration, Gold, or Dashboard.
> Update documentation. STOP after Iteration 3.

**AI RESPONSE SUMMARY:**

| File | Purpose |
|------|---------|
| `04_quality_referential_integrity.py` | Orphan `customer_id` / `product_id` on orders vs canonical parents |
| `05_quality_business_logic.py` | Date, segment, price, quantity, catalog-price rules |
| `silver_common.py` | Minimal helpers: canonical parents, new check categories, segment validation |
| `test_silver_helpers.py` | Added `is_valid_customer_segment` test |

**Rules implemented:**

**Referential integrity (`check_category = referential_integrity`):**

- `orders.customer_id` → canonical `customers.customer_id`
- `orders.product_id` → canonical `products.product_id`
- Left-join markers + non-blank FK filter (no RDD, no raw Bronze parent tables)

**Business logic (`check_category = business_logic`):**

| Entity | Rule | `failed_column` |
|--------|------|-----------------|
| customers | Future signup (`signup_date_typed > current_date()`) | `signup_date` |
| customers | Valid segment (`Premium`, `Standard`, `Basic`) | `customer_segment` |
| products | Non-negative `unit_price_typed` | `unit_price` |
| orders | `quantity_typed > 0` | `quantity` |
| orders | `order_date_typed <= current_date()` | `order_date` |
| orders | `unit_price_typed` matches canonical product catalog price | `unit_price` (D17 — no auto-correction) |

**Canonical parents:** prepared Bronze → pass completeness + type validation + `_dup_rank = 1`.

**Validation performed:**

| Check | Result |
|-------|--------|
| `py_compile` all Silver `.py` files | **PASS** |
| `test_silver_helpers.py` | **PASS** |
| Databricks Serverless `04` / `05` | **PASS** |

**Databricks Serverless observed results:**

| Module | Metric | Observed |
|--------|--------|----------|
| RI total | failure records | 1087 |
| RI | D11 (`customer_id=9999991` in JSON) | 25 |
| RI | D12 (`product_id=9999992` in JSON) | 25 |
| RI | non-D11/D12 (non-canonical parent) | 1037 |
| BL customers | future signup | 10 |
| BL products | negative price | 11 |
| BL orders | quantity | 40 |
| BL orders | future order_date | 15 |
| BL orders | catalog unit_price (total) | 222 |
| BL orders | D17 proxy (`order_date=2024-06-01`) | 18 |
| BL orders | other catalog mismatches | 204 |

**Issues/fixes during implementation:**

- Restored `parse_int_string` after accidental removal when adding segment helper
- `col_is_valid_customer_segment` uses `isin(list(VALID_CUSTOMER_SEGMENTS))` for Serverless compatibility

**Acceptance criteria:**

| Criterion | Status |
|-----------|--------|
| `04_quality_referential_integrity.py` created | **Yes** |
| `05_quality_business_logic.py` created | **Yes** |
| Canonical parent keys (not raw Bronze) | **Yes** |
| D11/D12 detected at injection volume (25+25) | **Yes** (via `bronze_source_values`) |
| D17 quarantine-only (no price correction) | **Yes** |
| Serverless-safe (no RDD APIs) | **Yes** |
| Quarantine writes | **No** (Iteration 4) |
| Orchestration / Silver table writes | **No** (Iteration 5) |
| Bronze unchanged | **Yes** |
| Databricks validation | **PASS** |

**YOUR EVALUATION:**

Iteration 3 correctly detects D11 (25), D12 (25), D06 (10), D14 (15), D15 (40), and D17 proxy (18≈20). Higher aggregate RI (1087) and catalog-price (222) totals are explained by canonical-parent FK semantics and order snapshot vs current catalog price — not implementation defects.

**FINAL DECISION:** **ACCEPTED** — Silver Iteration 3 complete. Proceed to Iteration 4 when approved.

---

## Iteration 4: Quarantine + DQ Summary Persistence

**PROMPT SENT:**

> Silver Layer Iteration 4 ONLY: persist `silver_quarantine_records` and `silver_dq_summary`.
> Consume Iteration 2/3 failure DataFrames. Delta overwrite (idempotent). Row-oriented summary metrics.
> No curated Silver tables, no orchestration beyond DQ persistence validation. STOP after Iteration 4.

**AI RESPONSE SUMMARY:**

| File | Purpose |
|------|---------|
| `06_write_dq_results.py` | Run all DQ checks, union failures, write quarantine + summary |
| `silver_common.py` | Minimal persistence helpers: table names, `write_delta_table`, `calculate_pass_percentage` |
| `test_silver_helpers.py` | Added tests for summary metric helpers |

**Functions provided:**

| Function | Purpose |
|----------|---------|
| `run_all_dq_checks(spark, config)` | Invoke all five DQ modules with shared `SilverConfig` |
| `collect_all_quarantine_failures(spark, dq_results)` | Union quarantine-compatible failure DataFrames |
| `build_dq_summary_df(spark, dq_results, config)` | Build row-oriented summary (13 rows) |
| `write_quarantine_records(spark, config, failures_df)` | Delta overwrite → `silver_quarantine_records` |
| `write_dq_summary(spark, config, summary_df)` | Delta overwrite → `silver_dq_summary` |
| `run_dq_persistence(spark, config)` | End-to-end persistence entry point |

**Design decisions:**

| Area | Decision |
|------|----------|
| Module numbering | `06_write_dq_results.py` (04/05 already used by RI and business logic) |
| Quarantine input | Reuse existing failure DataFrame schema from Iterations 2–3 |
| Summary `rows_failed` | Distinct `business_key` per category — not failure-record count |
| Summary `rows_tested` | Entity DataFrame row count from each DQ module's evaluated DataFrame |
| Write mode | Delta `overwrite` for both tables (idempotent per run) |
| Schema creation | `CREATE SCHEMA IF NOT EXISTS de_c1_coding_evaluation.silver` |
| Timestamps | Shared `SilverConfig.run_timestamp`; `quarantine_timestamp` from failure builders |
| DQ logic | No changes to `01`–`05` modules |

**Quarantine vs summary distinction:**

- **Quarantine table:** failure-record oriented — multiple rows per source record expected
- **Summary table:** row-oriented — one failed row counted once per category even if multiple rules fail

**Validation performed:**

| Check | Result |
|-------|--------|
| `py_compile` all Silver `.py` files | **PASS** |
| `test_silver_helpers.py` (incl. pass_percentage / summary metrics) | **PASS** |
| Databricks Serverless execution | **PASS** |

**Databricks Serverless observed results** (`SERVERLESS_COMPAT_VERSION = 8`):

| Check | Observed | Expected | Assessment |
|-------|----------|----------|------------|
| Quarantine total failure records | **1569** | 69+20+95+1087+298 | **Exact match** |
| Summary rows | **13** | 13 | **Exact match** |
| Table schemas | 8 + 8 columns | As designed | **PASS** |
| `pass_percentage` math (`pct_ok`) | all `true` | all `true` | **PASS** |
| Idempotency (2nd run) | 1569 → 1569 | no growth | **PASS** |
| D11 in quarantine | **25** | 25 | **Exact match** |
| D12 in quarantine | **25** | 25 | **Exact match** |
| D17 proxy in quarantine | **18** | ~20 | **PASS** |

**Quarantine failure-record counts by category / entity:**

| Category | customers | products | orders | Total |
|----------|-----------|----------|--------|-------|
| completeness | 60 | 9 | 0 | 69 |
| uniqueness | 6 | 6 | 8 | 20 |
| type_validation | 50 | 15 | 30 | 95 |
| referential_integrity | — | — | 1087 | 1087 |
| business_logic | 10 | 11 | 277 | 298 |

**DQ summary row-oriented `rows_failed` (distinct `business_key` per category):**

| Category | customers | products | orders |
|----------|-----------|----------|--------|
| completeness | 60 | 8 | 0 |
| uniqueness | 6 | 6 | 4 |
| type_validation | 50 | 15 | 30 |
| referential_integrity | — | — | 1029 |
| business_logic | 10 | 10 | 277 |

**Summary vs quarantine distinction (validated):**

- Products completeness: **9** failure records but **8** distinct failed rows (one product row fails multiple required-field rules).
- Products business logic: **11** failure records but **10** distinct failed rows.
- Orders uniqueness: **8** failure records but **4** distinct failed rows (duplicate `order_line_id` pairs).
- Orders RI: **1087** failure records but **1029** distinct failed rows (some orders fail both `customer_id` and `product_id` FK checks).

**Issues encountered:**

- `datetime.utcnow()` deprecation warning in notebook — fixed in `silver_common.py` (`datetime.now(timezone.utc)`).

**Acceptance criteria:**

| Criterion | Status |
|-----------|--------|
| `06_write_dq_results.py` created | **Yes** |
| Quarantine Delta overwrite | **Yes** |
| DQ summary Delta overwrite | **Yes** |
| All five DQ categories supported | **Yes** |
| Row-oriented summary metrics | **Yes** |
| Reuses Iteration 2/3 failure DataFrames | **Yes** |
| No changes to `01`–`05` DQ logic | **Yes** |
| Serverless-safe (no RDD APIs) | **Yes** |
| Bronze unchanged | **Yes** |
| Iteration 5 not started | **Yes** |
| Databricks validation | **PASS** |

**YOUR EVALUATION:**

Iteration 4 persistence matches all Iteration 2/3 failure-record baselines. Summary metrics are correctly row-oriented. Idempotency confirmed. D11/D12/D17 spot checks pass.

**FINAL DECISION:** **ACCEPTED** — Silver Iteration 4 complete. Proceed to Iteration 5 when approved.

---

## Iteration 5: Full Orchestration + Curated Silver Tables

**PROMPT SENT:**

> Silver Iteration 5 ONLY: implement `create_silver_tables.py` with `run_silver_pipeline(spark=spark)`.
> Reuse Iterations 2–4 DQ modules. Write curated `silver_customers/products/orders`.
> Delta overwrite, Serverless-safe, no Bronze/Gold/Dashboard changes. STOP after local validation.

**AI RESPONSE SUMMARY:**

| File | Purpose |
|------|---------|
| `create_silver_tables.py` | `run_silver_pipeline` — DQ → quarantine/summary → curated tables |
| `silver_common.py` | `SILVER_*_TABLE_NAME`, `entity_dq_categories()` |
| `test_silver_helpers.py` | Test for `entity_dq_categories()` |

**Orchestration (`run_silver_pipeline`):**

```
Bronze → run_all_dq_checks (01–05)
       → run_dq_persistence (quarantine + summary)
       → filter_valid_rows (anti-join failure keys per category)
       → select curated columns (*_typed → final types)
       → overwrite silver_customers / silver_products / silver_orders
```

**Curated validity:** Rows excluded if `business_key` appears in any applicable category `failures_df`. No DQ rule duplication — uses existing failure outputs only.

**Design decisions:**

| Area | Decision |
|------|----------|
| Valid-row filter | Left-anti join on distinct `business_key` per category failure set |
| Source DataFrame | `business_logic[*].prepared_df` (final typed state before curated projection) |
| DQ persistence | Reuse `06_write_dq_results.run_dq_persistence` with precomputed `dq_results` |
| Write mode | Delta `overwrite` for all five Silver tables |
| D17 | Quarantine-only — preserved, no price correction |
| Serverless | DataFrame APIs only; `SERVERLESS_COMPAT_VERSION = 9` |

**Validation performed:**

| Check | Result |
|-------|--------|
| `py_compile` all Silver `.py` files | **PASS** |
| `test_silver_helpers.py` | **PASS** |
| `create_silver_tables` import (notebook-style module load) | **PASS** |
| Databricks Serverless `run_silver_pipeline` | **PASS** |

**Databricks Serverless observed results** (`SERVERLESS_COMPAT_VERSION = 9`):

| Check | Observed | Assessment |
|-------|----------|------------|
| Pipeline execution | Success | **PASS** |
| Quarantine failure records | **1569** | Matches Iteration 4 |
| DQ summary rows | **13** | **PASS** |
| Idempotency | 1569 → 1569 | **PASS** |
| Curated `silver_customers` | **878** rows | **PASS** |
| Curated `silver_products` | **164** rows | **PASS** |
| Curated `silver_orders` | **3832** rows | **PASS** |
| Curated schemas | No helper columns | **PASS** |
| D11 / D12 / D17 proxy | 25 / 25 / 18 | **PASS** |

**Curated schemas (validated):**

| Table | Columns |
|-------|---------|
| `silver_customers` | `customer_id` STRING, `customer_name` STRING, `email` STRING, `country` STRING, `signup_date` DATE, `customer_segment` STRING, `lifetime_value` DECIMAL(12,2) |
| `silver_products` | `product_id` STRING, `product_name` STRING, `category` STRING, `unit_price` DECIMAL(10,2) |
| `silver_orders` | `order_line_id` STRING, `order_id` STRING, `customer_id` STRING, `product_id` STRING, `order_date` DATE, `quantity` INT, `unit_price` DECIMAL(10,2) |

**Validated DQ summary:**

| Category | Entity | tested | passed | failed |
|----------|--------|--------|--------|--------|
| completeness | customers | 1006 | 946 | 60 |
| completeness | products | 206 | 198 | 8 |
| completeness | orders | 5163 | 5163 | 0 |
| uniqueness | customers | 1006 | 1000 | 6 |
| uniqueness | products | 206 | 200 | 6 |
| uniqueness | orders | 5163 | 5159 | 4 |
| type_validation | customers | 1006 | 956 | 50 |
| type_validation | products | 206 | 191 | 15 |
| type_validation | orders | 5163 | 5133 | 30 |
| referential_integrity | orders | 5163 | 4134 | **1029** |
| business_logic | customers | 1006 | 996 | 10 |
| business_logic | products | 206 | 196 | 10 |
| business_logic | orders | 5163 | 4886 | 277 |

**Referential integrity — intentional non-zero failures (ACCEPTED, not a bug):**

FK integrity is **not** expected to be zero for this intentionally defective Bronze dataset:

| RI evidence | Value |
|-------------|-------|
| D11 orphan `customer_id` failure records | **25** |
| D12 orphan `product_id` failure records | **25** |
| Total RI quarantine failure records | **1087** |
| Distinct failed order rows (summary `rows_failed`) | **1029** |
| Orders failing both FK checks | Some rows | Explains 1087 > 1029 |

Non-zero RI results confirm D11/D12 detection and canonical-parent FK semantics — **ACCEPTED**.

**Quarantine vs summary (preserved):**

- Quarantine stores **failure records** (1,569 total).
- Summary uses **distinct `business_key`** per category where applicable (e.g. orders uniqueness: 8 records / 4 rows; orders RI: 1087 records / 1029 rows).

**Acceptance criteria:**

| Criterion | Status |
|-----------|--------|
| `create_silver_tables.py` created | **Yes** |
| `run_silver_pipeline(spark=spark)` entry point | **Yes** |
| Reuses Iterations 2–4 DQ modules | **Yes** |
| Curated schemas match spec | **Yes** |
| No helper columns in output | **Yes** |
| Quarantine + summary written | **Yes** |
| Delta overwrite idempotency | **Yes** |
| Serverless-safe (no RDD) | **Yes** |
| Bronze unchanged | **Yes** |
| Gold/Dashboard not started | **Yes** |
| Databricks validation | **PASS** |

**YOUR EVALUATION:**

Full Silver pipeline validated on Databricks Serverless. Curated row counts (878 / 164 / 3832) are consistent with quarantining all DQ failures. RI non-zero results are intentional (D11/D12 + canonical-parent semantics). Phase 4 Silver layer complete.

**FINAL DECISION:** **ACCEPTED** — Silver Iteration 5 complete. Phase 4 Silver **complete**. Gold not started.

---

## RI Alignment Fix — Curated Parent Keys (`SERVERLESS_COMPAT_VERSION = 10`)

**TYPE:** Correction / implementation

**PROMPT SENT — VERBATIM (recovered):**

> Full text: `ai-prompts/verbatim-recoveries.md` — recovery key `silver-ri-alignment`.

**Context:** Gold Iteration 6 Databricks validation exposed order FKs in `silver_orders` that were absent from curated `silver_customers` / `silver_products` because RI used `canonical_valid_filter()` parents while curated dimensions used full `filter_valid_rows()`.

**Implementation:**

| File | Change |
|------|--------|
| `silver_common.py` | `SERVERLESS_COMPAT_VERSION = 10`; added `failures_for_category()`, `filter_valid_rows()`, `curated_eligible_parent_keys_df()` |
| `create_silver_tables.py` | Imports shared `filter_valid_rows` from `silver_common` |
| `04_quality_referential_integrity.py` | RI parents from `curated_eligible_parent_keys_df()`; optional `dq_results` param |
| `06_write_dq_results.py` | Order: 01→02→03→05→04 |

**Local validation:** `py_compile` + `test_silver_helpers.py` — **PASS**

**Databricks revalidation:** **PASS** — orphan FK diagnostics 0; `silver_orders` 3,646; revenue 2,708,411.08.

**Gold revalidation:** **PASS** — entity Gold reconciles; idempotency **PASS**; Phase 5 Gold **ACCEPTED**.

**FINAL DECISION (RI alignment):** **ACCEPTED**.

### Databricks revalidation cells

```python
# Silver RI alignment — re-run full pipeline (Serverless)
import importlib.util, json, sys
from pathlib import Path

silver_dir = Path("/Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/src/silver")
for name in list(sys.modules):
    if name.startswith(("silver_common", "quality_", "referential", "business", "write_dq", "create_silver", "_load")):
        del sys.modules[name]
sys.path.insert(0, str(silver_dir))

spec = importlib.util.spec_from_file_location("silver_common", silver_dir / "silver_common.py")
silver_common = importlib.util.module_from_spec(spec)
sys.modules["silver_common"] = silver_common
spec.loader.exec_module(silver_common)
print("SERVERLESS_COMPAT_VERSION =", silver_common.SERVERLESS_COMPAT_VERSION)

spec = importlib.util.spec_from_file_location("create_silver_tables", silver_dir / "create_silver_tables.py")
create_silver_tables = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create_silver_tables)

result = create_silver_tables.run_silver_pipeline(spark=spark)
for entity_key in ("customers", "products", "orders"):
    print(entity_key, result["curated"][entity_key].count())
```

```sql
-- B. Reverse RI diagnostics (expect 0)
SELECT COUNT(*)
FROM de_c1_coding_evaluation.silver.silver_orders o
LEFT JOIN de_c1_coding_evaluation.silver.silver_products p ON o.product_id = p.product_id
WHERE o.product_id IS NOT NULL AND p.product_id IS NULL;

SELECT COUNT(*)
FROM de_c1_coding_evaluation.silver.silver_orders o
LEFT JOIN de_c1_coding_evaluation.silver.silver_customers c ON o.customer_id = c.customer_id
WHERE o.customer_id IS NOT NULL AND c.customer_id IS NULL;

-- C. Silver revenue
SELECT SUM(quantity * unit_price) FROM de_c1_coding_evaluation.silver.silver_orders;
```

```python
# D–H. Re-run Gold pipeline + validation (no Gold code changes)
# Register in sys.modules BEFORE exec_module (fixes AttributeError on Databricks)
import importlib.util, json, sys
from pathlib import Path

gold_dir = Path("/Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/src/gold")
for name in list(sys.modules):
    if name == "create_gold_tables" or name.startswith("create_gold_tables."):
        del sys.modules[name]
sys.path.insert(0, str(gold_dir))

spec = importlib.util.spec_from_file_location("create_gold_tables", gold_dir / "create_gold_tables.py")
create_gold_tables = importlib.util.module_from_spec(spec)
sys.modules["create_gold_tables"] = create_gold_tables
spec.loader.exec_module(create_gold_tables)

create_gold_tables.run_gold_pipeline(spark=spark)
validation = create_gold_tables.validate_gold_pipeline(spark=spark)
idempotency = create_gold_tables.validate_idempotency(spark=spark)
print(json.dumps({"row_counts": validation["row_counts"], "reconciliations": validation["reconciliations"]}, indent=2, default=str))
```

**FINAL DECISION (RI alignment):** **ACCEPTED** — Databricks + Gold revalidation **PASS**.

---

## Cursor Evaluation Evidence (Phase 4 — complete)

| Requirement | Evidence |
|-------------|----------|
| Persistent context | Foundation docs + Bronze validation + `tool-specific/cursor-workflow/*` |
| Iteration | Deliberate 5-iteration plan; all five Silver iterations implemented and validated |
| Validation | Iterations 2–5: Databricks Serverless **PASS** |
| Human review | Iterations 1b, 2, 3, 4, 5 **ACCEPTED** — Phase 4 Silver **complete** |
