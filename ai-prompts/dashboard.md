# AI Prompts — Dashboard (Phase 6)

**Prompts in this file:** 21–23, 30
**Implementation order:** Query catalog → schema validation fix → evaluation dashboard completion

Related: `src/dashboard/dashboard_queries.sql`, `src/dashboard/DASHBOARD_GUIDE.md`, `src/gold/GOLD_LAYER_NOTES.md`

---

## Prompt 21 — Dashboard query catalog & guide

**TYPE:** Implementation

**PROMPT SENT:**

```text
You are now implementing **Phase 6 — Dashboard** for the `DE_C1_Coding_Evaluation` repository.

Phase 5 Gold is COMPLETE and ACCEPTED on Databricks Serverless.

## Frozen baseline

Do not use the pre-RI-fix numbers.

Current validated state:

* `SERVERLESS_COMPAT_VERSION = 10`
* `silver_customers = 878`
* `silver_products = 164`
* `silver_orders = 3646`
* Silver revenue = `2,708,411.08`
* Silver quantity = `10,899`
* Silver distinct orders = `2,052`

Gold is frozen and accepted:

* `gold_sales_by_product = 164 rows`
* `gold_revenue_by_customer = 792 rows`
* `gold_customer_segmentation = 792 rows`
* `gold_daily_weekly_trends = 950 rows`

  * 818 daily
  * 132 weekly
* Gold revenue = `2,708,411.08`
* Gold quantity = `10,899`
* Gold distinct orders = `2,052`
* Gold ↔ Silver reconciliation = PASS
* Gold idempotency = PASS
* AC-1 through AC-11 = PASS

---

# IMPORTANT: Phase 6 scope

Implement only the Dashboard layer.

The Dashboard is a **consumption layer over Gold**.

Architecture:

```text
Bronze
   ↓
Silver
   ↓
Gold
   ↓
Dashboard SQL
   ↓
Databricks SQL visualizations
```

Dashboard must read **Gold only**.

Do not introduce any direct Dashboard dependency on:

* Bronze
* Silver
* raw CSV files
* quarantine tables
* DQ summary tables

Do not recreate Gold business logic.

Do not modify Gold to make Dashboard easier.

---

# Files that are FROZEN

Do not modify anything under:

```text
src/bronze/
src/silver/
src/gold/
data/
src/data_generation/
```

In particular, do NOT modify:

```text
src/gold/*.sql
src/gold/create_gold_tables.py
src/gold/GOLD_LAYER_NOTES.md
```

Do not change:

* Gold grains
* Gold metric definitions
* Gold joins
* Gold aggregation logic
* Silver RI alignment
* Gold SQL
* Gold Python orchestration

If something appears inconsistent with Dashboard requirements, stop and report it rather than modifying the frozen layers.

---

# Step 1 — Inspect before modifying

Before creating anything, inspect the repository.

Read:

```text
requirements-analysis.md
design-notes.md
tool-workflow.md
data-model.md
README.md
src/gold/GOLD_LAYER_NOTES.md
src/gold/01_sales_by_product.sql
src/gold/02_revenue_by_customer.sql
src/gold/03_daily_weekly_trends.sql
src/gold/04_customer_segmentation.sql
tool-specific/cursor-workflow/task-breakdown.md
relevant repository instructions/rules
```

Also inspect:

```text
src/dashboard/
ai-prompts/
```

Determine:

1. Whether `src/dashboard/` already exists.
2. Whether `dashboard_queries.sql` already exists.
3. Whether `DASHBOARD_GUIDE.md` already exists.
4. Whether `ai-prompts/dashboard.md` already exists.
5. Whether any Dashboard implementation already exists elsewhere.
6. Whether repository documentation resolves the `DASHBOARD_GUIDE.md` location ambiguity.

Do not guess the location.

---

# Step 2 — Establish the actual Gold contract

Before writing Dashboard SQL, inspect the actual Gold SQL and `GOLD_LAYER_NOTES.md`.

For each Gold table establish the exact:

* FQN
* columns
* data types
* grain
* metric semantics

The Dashboard must use the actual schema.

The four approved Gold sources are:

```text
de_c1_coding_evaluation.gold.gold_sales_by_product

de_c1_coding_evaluation.gold.gold_revenue_by_customer

de_c1_coding_evaluation.gold.gold_daily_weekly_trends

de_c1_coding_evaluation.gold.gold_customer_segmentation
```

Do not assume column names from the Phase 6 prompt if the actual Gold implementation differs.

---

# Step 3 — Implement the Dashboard query catalog

Create:

```text
src/dashboard/dashboard_queries.sql
```

unless repository inspection proves a different required location.

Keep the query set **small and high-value**.

Organize the SQL into these four sections:

```text
1. Product Performance
2. Customer Revenue
3. Revenue / Trends
4. Customer Segmentation
```

Target approximately **8–10 visualization-ready queries**, unless repository requirements justify a different number.

Do not create dozens of redundant queries.

## Product Performance

Use:

```text
gold_sales_by_product
```

Provide useful visualization-oriented queries such as:

* Top products by revenue
* Top products by quantity
* Revenue by category, if `category` exists in the confirmed Gold schema

Use `ORDER BY` and a reasonable `LIMIT` only where appropriate for a visualization.

Do not introduce arbitrary business rules.

## Customer Revenue

Use:

```text
gold_revenue_by_customer
```

Provide useful views such as:

* Top customers by revenue
* Customer revenue distribution / ranking

Only use columns confirmed by the Gold contract.

## Revenue / Trends

Use:

```text
gold_daily_weekly_trends
```

Provide useful views for:

* Daily revenue trend
* Weekly revenue trend
* Daily order trend
* Weekly order trend

Respect the existing:

```text
time_grain
period_start
```

semantics.

Do NOT recreate weekly boundaries.

Do NOT derive weekly periods from dates independently.

## Customer Segmentation

Use:

```text
gold_customer_segmentation
```

Provide useful views such as:

* Customer count by segment
* Revenue by segment
* Average lifetime value by segment
* Average frequency by segment

Only use the actual Gold metrics.

---

# Step 4 — Dashboard SQL design rules

Every query must satisfy these rules.

### Rule A — Gold only

Every source table referenced by Dashboard SQL must be one of the four approved Gold objects.

No:

```text
silver.*
bronze.*
data/*.csv
```

references.

### Rule B — Consume existing Gold metrics

If Gold provides:

```text
total_revenue
total_quantity
order_count
lifetime_value
frequency
total_spend
```

consume those metrics.

Do not rebuild them from lower layers.

Additional aggregation is allowed when it is genuinely required for visualization.

For example:

```sql
SELECT
    category,
    SUM(total_revenue) AS total_revenue
FROM de_c1_coding_evaluation.gold.gold_sales_by_product
GROUP BY category
ORDER BY total_revenue DESC;
```

That is acceptable because it aggregates an existing Gold metric for presentation.

### Rule C — Preserve semantics

Do not:

* redefine revenue
* redefine order count
* redefine frequency
* redefine lifetime value
* redefine customer segments
* redefine weekly periods
* join Gold back to Silver to recover attributes
* reconstruct missing dimensions

### Rule D — Visualization readiness

Queries should return clean analytical result sets.

Prefer:

* descriptive aliases
* deterministic ordering
* appropriate aggregation
* no helper/debug columns
* no unnecessary technical columns

Avoid unnecessary parameters unless the repository already has a parameterization convention.

---

# Step 5 — Create the Dashboard guide

Create the repository-approved location for:

```text
DASHBOARD_GUIDE.md
```

The guide should contain:

## 1. Overview

Explain:

```text
Bronze → Silver → Gold → Dashboard
```

and that Dashboard consumes Gold only.

## 2. Prerequisites

Include:

* Databricks workspace
* access to `de_c1_coding_evaluation.gold`
* Databricks SQL / SQL editor
* validated Gold tables

## 3. Gold dependencies

Document the four exact Gold FQNs.

## 4. Query catalog

For every Dashboard query explain:

* query name
* source Gold table
* purpose
* output grain
* important output columns
* recommended visualization

## 5. Running the SQL

Explain how to:

1. Open Databricks SQL
2. Open/import `dashboard_queries.sql`
3. Execute individual queries
4. Use each result set to create a visualization
5. Add the queries to a SQL Dashboard if required by the repository

Do not invent UI instructions that depend on an unverified Databricks interface version.

## 6. Recommended visualizations

Map the queries to appropriate visualization types.

At minimum consider:

* bar chart
* histogram
* line chart
* pie/donut or bar chart for segmentation

Use the repository's original dashboard requirement as the source of truth where applicable.

## 7. Validation baselines

Document the current validated Gold baseline:

```text
Gold revenue: 2,708,411.08
Gold quantity: 10,899
Gold distinct orders: 2,052

gold_sales_by_product: 164 rows
gold_revenue_by_customer: 792 rows
gold_customer_segmentation: 792 rows
gold_daily_weekly_trends: 950 rows
    daily: 818
    weekly: 132
```

Do not substitute the old:

```text
2,830,321.54
11,464
3,832
```

values anywhere as current validation baselines.

## 8. Interpretation

Explain what each visualization represents without redefining Gold metrics.

## 9. Limitations / assumptions

Document any genuine limitations discovered during implementation.

Do not invent limitations.

---

# Step 6 — Create AI prompt history

Create:

```text
ai-prompts/dashboard.md
```

unless it already exists.

Follow the repository's established AI prompt documentation convention.

Record:

* Phase 6 implementation prompt
* important repository findings
* decisions made
* what was accepted
* what was rejected
* why
* validation performed

Do not fabricate Cursor responses or Databricks results.

Only document actual actions/results.

---

# Step 7 — Documentation status updates

Inspect whether the repository expects Phase 6 status updates in:

```text
README.md
requirements-analysis.md
design-notes.md
tool-specific/cursor-workflow/task-breakdown.md
```

Do not modify these automatically.

Only update them if the repository's established workflow clearly requires it.

If you modify any of them, report exactly what changed and why.

Do NOT modify frozen Silver/Gold documentation merely to make it appear current.

---

# Step 8 — Local validation

After implementation:

### SQL/static validation

Check:

* SQL syntax where a local validator is available
* all four FQNs are valid strings
* every query reads Gold only
* no Silver references
* no Bronze references
* no CSV references
* no accidental lower-layer joins
* no duplicate query sections
* no unnecessary helper columns

### Repository validation

Check:

* expected files exist
* Markdown is readable
* SQL sections correspond to the guide
* every documented query actually exists
* every query's documented source matches the SQL
* no secrets were introduced

Do not modify frozen layers to make validation pass.

---

# Step 9 — Databricks Serverless validation

Run the Dashboard SQL against the already validated Gold tables in Databricks Serverless.

Validate in this order:

## A. Gold source availability

Confirm all four tables exist and are queryable.

## B. Gold row counts

Confirm:

```text
gold_sales_by_product = 164
gold_revenue_by_customer = 792
gold_customer_segmentation = 792
gold_daily_weekly_trends = 950
```

And:

```text
daily trend rows = 818
weekly trend rows = 132
```

## C. Gold baseline reconciliation

Where applicable, confirm:

```text
Gold revenue = 2,708,411.08
Gold quantity = 10,899
Gold distinct orders = 2,052
```

Use existing Gold semantics.

Do not recreate these from Silver.

## D. Execute every Dashboard query

Every query in `dashboard_queries.sql` must execute successfully.

Record:

* success/failure
* returned schema
* row-count sanity
* relevant observations

Do not invent results.

## E. Source dependency validation

Confirm every Dashboard query references only:

```text
de_c1_coding_evaluation.gold.*
```

and specifically the approved four Gold objects.

---

# Step 10 — Dashboard acceptance

Use two categories.

## Explicit requirements

Validate only requirements actually supported by repository documentation, including:

* Dashboard artifacts exist
* Dashboard queries consume Gold
* required analytical themes are covered
* SQL is visualization-ready
* Dashboard guide exists at the repository-approved location
* prompt history exists if required by the workflow
* required visualizations are supported if the original requirement explicitly requires them

## Recommended validation checks

Additionally verify:

* all queries execute successfully on Serverless
* no Bronze/Silver dependencies
* Gold baseline remains unchanged
* query output grains are correct
* documented query behavior matches actual SQL
* no Gold business logic has been duplicated

Do not label inferred checks as formal project acceptance criteria.

---

# Step 11 — Do not prematurely mark Phase 6 complete

Implementation and validation are separate.

Do not claim:

```text
PHASE 6 COMPLETE
```

until:

1. files are implemented,
2. local/static validation passes,
3. Databricks Serverless validation is performed,
4. actual evidence is recorded,
5. documentation is updated as required.

If Databricks validation cannot be performed from Cursor, explicitly report:

```text
Implementation complete; Databricks validation pending.
```

Do not fabricate Databricks evidence.

---

# Final response required

After implementation, report exactly:

## 1. Files created

List every created file.

## 2. Files modified

List every modified existing file and why.

## 3. Files intentionally untouched

Confirm:

```text
src/bronze/
src/silver/
src/gold/
data/
src/data_generation/
```

remain untouched.

## 4. Dashboard query catalog

Give the final query names grouped by:

```text
Product Performance
Customer Revenue
Revenue / Trends
Customer Segmentation
```

## 5. Validation

Separate:

```text
Local/static validation
Databricks Serverless validation
```

Report actual results only.

## 6. Issues / ambiguities

Report any unresolved repository inconsistencies.

## 7. Final decision

Use exactly one of:

```text
PHASE 6 IMPLEMENTATION COMPLETE — VALIDATION COMPLETE

```

or

```text
PHASE 6 IMPLEMENTATION COMPLETE — DATABRICKS VALIDATION PENDING

```

or

```text
PHASE 6 BLOCKED — <reason>
```

Do not make changes outside the Dashboard scope.
```text
Bronze
   ↓
Silver
   ↓
Gold
   ↓
Dashboard SQL
   ↓
Databricks SQL visualizations
```

Dashboard must read **Gold only**.

Do not introduce any direct Dashboard dependency on:

* Bronze
* Silver
* raw CSV files
* quarantine tables
* DQ summary tables

Do not recreate Gold business logic.

Do not modify Gold to make Dashboard easier.

---

# Files that are FROZEN

Do not modify anything under:

```text
src/bronze/
src/silver/
src/gold/
data/
src/data_generation/
```

In particular, do NOT modify:

```text
src/gold/*.sql
src/gold/create_gold_tables.py
src/gold/GOLD_LAYER_NOTES.md
```

Do not change:

* Gold grains
* Gold metric definitions
* Gold joins
* Gold aggregation logic
* Silver RI alignment
* Gold SQL
* Gold Python orchestration

If something appears inconsistent with Dashboard requirements, stop and report it rather than modifying the frozen layers.

---

# Step 1 — Inspect before modifying

Before creating anything, inspect the repository.

Read:

```text
requirements-analysis.md
design-notes.md
tool-workflow.md
data-model.md
README.md
src/gold/GOLD_LAYER_NOTES.md
src/gold/01_sales_by_product.sql
src/gold/02_revenue_by_customer.sql
src/gold/03_daily_weekly_trends.sql
src/gold/04_customer_segmentation.sql
tool-specific/cursor-workflow/task-breakdown.md
relevant repository instructions/rules
```

Also inspect:

```text
src/dashboard/
ai-prompts/
```

Determine:

1. Whether `src/dashboard/` already exists.
2. Whether `dashboard_queries.sql` already exists.
3. Whether `DASHBOARD_GUIDE.md` already exists.
4. Whether `ai-prompts/dashboard.md` already exists.
5. Whether any Dashboard implementation already exists elsewhere.
6. Whether repository documentation resolves the `DASHBOARD_GUIDE.md` location ambiguity.

Do not guess the location.

---

# Step 2 — Establish the actual Gold contract

Before writing Dashboard SQL, inspect the actual Gold SQL and `GOLD_LAYER_NOTES.md`.

For each Gold table establish the exact:

* FQN
* columns
* data types
* grain
* metric semantics

The Dashboard must use the actual schema.

The four approved Gold sources are:

```text
de_c1_coding_evaluation.gold.gold_sales_by_product

de_c1_coding_evaluation.gold.gold_revenue_by_customer

de_c1_coding_evaluation.gold.gold_daily_weekly_trends

de_c1_coding_evaluation.gold.gold_customer_segmentation
```

Do not assume column names from the Phase 6 prompt if the actual Gold implementation differs.

---

# Step 3 — Implement the Dashboard query catalog

Create:

```text
src/dashboard/dashboard_queries.sql
```

unless repository inspection proves a different required location.

Keep the query set **small and high-value**.

Organize the SQL into these four sections:

```text
1. Product Performance
2. Customer Revenue
3. Revenue / Trends
4. Customer Segmentation
```

Target approximately **8–10 visualization-ready queries**, unless repository requirements justify a different number.

Do not create dozens of redundant queries.

## Product Performance

Use:

```text
gold_sales_by_product
```

Provide useful visualization-oriented queries such as:

* Top products by revenue
* Top products by quantity
* Revenue by category, if `category` exists in the confirmed Gold schema

Use `ORDER BY` and a reasonable `LIMIT` only where appropriate for a visualization.

Do not introduce arbitrary business rules.

## Customer Revenue

Use:

```text
gold_revenue_by_customer
```

Provide useful views such as:

* Top customers by revenue
* Customer revenue distribution / ranking

Only use columns confirmed by the Gold contract.

## Revenue / Trends

Use:

```text
gold_daily_weekly_trends
```

Provide useful views for:

* Daily revenue trend
* Weekly revenue trend
* Daily order trend
* Weekly order trend

Respect the existing:

```text
time_grain
period_start
```

semantics.

Do NOT recreate weekly boundaries.

Do NOT derive weekly periods from dates independently.

## Customer Segmentation

Use:

```text
gold_customer_segmentation
```

Provide useful views such as:

* Customer count by segment
* Revenue by segment
* Average lifetime value by segment
* Average frequency by segment

Only use the actual Gold metrics.

---

# Step 4 — Dashboard SQL design rules

Every query must satisfy these rules.

### Rule A — Gold only

Every source table referenced by Dashboard SQL must be one of the four approved Gold objects.

No:

```text
silver.*
bronze.*
data/*.csv
```

references.

### Rule B — Consume existing Gold metrics

If Gold provides:

```text
total_revenue
total_quantity
order_count
lifetime_value
frequency
total_spend
```

consume those metrics.

Do not rebuild them from lower layers.

Additional aggregation is allowed when it is genuinely required for visualization.

For example:

```sql
SELECT
    category,
    SUM(total_revenue) AS total_revenue
FROM de_c1_coding_evaluation.gold.gold_sales_by_product
GROUP BY category
ORDER BY total_revenue DESC;
```

That is acceptable because it aggregates an existing Gold metric for presentation.

### Rule C — Preserve semantics

Do not:

* redefine revenue
* redefine order count
* redefine frequency
* redefine lifetime value
* redefine customer segments
* redefine weekly periods
* join Gold back to Silver to recover attributes
* reconstruct missing dimensions

### Rule D — Visualization readiness

Queries should return clean analytical result sets.

Prefer:

* descriptive aliases
* deterministic ordering
* appropriate aggregation
* no helper/debug columns
* no unnecessary technical columns

Avoid unnecessary parameters unless the repository already has a parameterization convention.

---

# Step 5 — Create the Dashboard guide

Create the repository-approved location for:

```text
DASHBOARD_GUIDE.md
```

The guide should contain:

## 1. Overview

Explain:

```text
Bronze → Silver → Gold → Dashboard
```

and that Dashboard consumes Gold only.

## 2. Prerequisites

Include:

* Databricks workspace
* access to `de_c1_coding_evaluation.gold`
* Databricks SQL / SQL editor
* validated Gold tables

## 3. Gold dependencies

Document the four exact Gold FQNs.

## 4. Query catalog

For every Dashboard query explain:

* query name
* source Gold table
* purpose
* output grain
* important output columns
* recommended visualization

## 5. Running the SQL

Explain how to:

1. Open Databricks SQL
2. Open/import `dashboard_queries.sql`
3. Execute individual queries
4. Use each result set to create a visualization
5. Add the queries to a SQL Dashboard if required by the repository

Do not invent UI instructions that depend on an unverified Databricks interface version.

## 6. Recommended visualizations

Map the queries to appropriate visualization types.

At minimum consider:

* bar chart
* histogram
* line chart
* pie/donut or bar chart for segmentation

Use the repository's original dashboard requirement as the source of truth where applicable.

## 7. Validation baselines

Document the current validated Gold baseline:

```text
Gold revenue: 2,708,411.08
Gold quantity: 10,899
Gold distinct orders: 2,052

gold_sales_by_product: 164 rows
gold_revenue_by_customer: 792 rows
gold_customer_segmentation: 792 rows
gold_daily_weekly_trends: 950 rows
    daily: 818
    weekly: 132
```

Do not substitute the old:

```text
2,830,321.54
11,464
3,832
```

values anywhere as current validation baselines.

## 8. Interpretation

Explain what each visualization represents without redefining Gold metrics.

## 9. Limitations / assumptions

Document any genuine limitations discovered during implementation.

Do not invent limitations.

---

# Step 6 — Create AI prompt history

Create:

```text
ai-prompts/dashboard.md
```

unless it already exists.

Follow the repository's established AI prompt documentation convention.

Record:

* Phase 6 implementation prompt
* important repository findings
* decisions made
* what was accepted
* what was rejected
* why
* validation performed

Do not fabricate Cursor responses or Databricks results.

Only document actual actions/results.

---

# Step 7 — Documentation status updates

Inspect whether the repository expects Phase 6 status updates in:

```text
README.md
requirements-analysis.md
design-notes.md
tool-specific/cursor-workflow/task-breakdown.md
```

Do not modify these automatically.

Only update them if the repository's established workflow clearly requires it.

If you modify any of them, report exactly what changed and why.

Do NOT modify frozen Silver/Gold documentation merely to make it appear current.

---

# Step 8 — Local validation

After implementation:

### SQL/static validation

Check:

* SQL syntax where a local validator is available
* all four FQNs are valid strings
* every query reads Gold only
* no Silver references
* no Bronze references
* no CSV references
* no accidental lower-layer joins
* no duplicate query sections
* no unnecessary helper columns

### Repository validation

Check:

* expected files exist
* Markdown is readable
* SQL sections correspond to the guide
* every documented query actually exists
* every query's documented source matches the SQL
* no secrets were introduced

Do not modify frozen layers to make validation pass.

---

# Step 9 — Databricks Serverless validation

Run the Dashboard SQL against the already validated Gold tables in Databricks Serverless.

Validate in this order:

## A. Gold source availability

Confirm all four tables exist and are queryable.

## B. Gold row counts

Confirm:

```text
gold_sales_by_product = 164
gold_revenue_by_customer = 792
gold_customer_segmentation = 792
gold_daily_weekly_trends = 950
```

And:

```text
daily trend rows = 818
weekly trend rows = 132
```

## C. Gold baseline reconciliation

Where applicable, confirm:

```text
Gold revenue = 2,708,411.08
Gold quantity = 10,899
Gold distinct orders = 2,052
```

Use existing Gold semantics.

Do not recreate these from Silver.

## D. Execute every Dashboard query

Every query in `dashboard_queries.sql` must execute successfully.

Record:

* success/failure
* returned schema
* row-count sanity
* relevant observations

Do not invent results.

## E. Source dependency validation

Confirm every Dashboard query references only:

```text
de_c1_coding_evaluation.gold.*
```

and specifically the approved four Gold objects.

---

# Step 10 — Dashboard acceptance

Use two categories.

## Explicit requirements

Validate only requirements actually supported by repository documentation, including:

* Dashboard artifacts exist
* Dashboard queries consume Gold
* required analytical themes are covered
* SQL is visualization-ready
* Dashboard guide exists at the repository-approved location
* prompt history exists if required by the workflow
* required visualizations are supported if the original requirement explicitly requires them

## Recommended validation checks

Additionally verify:

* all queries execute successfully on Serverless
* no Bronze/Silver dependencies
* Gold baseline remains unchanged
* query output grains are correct
* documented query behavior matches actual SQL
* no Gold business logic has been duplicated

Do not label inferred checks as formal project acceptance criteria.

---

# Step 11 — Do not prematurely mark Phase 6 complete

Implementation and validation are separate.

Do not claim:

```text
PHASE 6 COMPLETE
```

until:

1. files are implemented,
2. local/static validation passes,
3. Databricks Serverless validation is performed,
4. actual evidence is recorded,
5. documentation is updated as required.

If Databricks validation cannot be performed from Cursor, explicitly report:

```text
Implementation complete; Databricks validation pending.
```

Do not fabricate Databricks evidence.

---

# Final response required

After implementation, report exactly:

## 1. Files created

List every created file.

## 2. Files modified

List every modified existing file and why.

## 3. Files intentionally untouched

Confirm:

```text
src/bronze/
src/silver/
src/gold/
data/
src/data_generation/
```

remain untouched.

## 4. Dashboard query catalog

Give the final query names grouped by:

```text
Product Performance
Customer Revenue
Revenue / Trends
Customer Segmentation
```

## 5. Validation

Separate:

```text
Local/static validation
Databricks Serverless validation
```

Report actual results only.

## 6. Issues / ambiguities

Report any unresolved repository inconsistencies.

## 7. Final decision

Use exactly one of:

```text
PHASE 6 IMPLEMENTATION COMPLETE — VALIDATION COMPLETE

```

or

```text
PHASE 6 IMPLEMENTATION COMPLETE — DATABRICKS VALIDATION PENDING

```

or

```text
PHASE 6 BLOCKED — <reason>
```

Do not make changes outside the Dashboard scope.
```

**Repository findings:**

| Item | Finding |
|------|---------|
| `src/dashboard/` | Did not exist before Phase 6 |
| `dashboard_queries.sql` | Did not exist |
| `DASHBOARD_GUIDE.md` | Did not exist; approved location `src/dashboard/DASHBOARD_GUIDE.md` (`requirements-analysis.md` § Dashboard, `tool-workflow.md` § Documentation) |
| `ai-prompts/dashboard.md` | Did not exist; required per `tool-workflow.md` |
| Gold contract | Four tables with columns/grains as in `GOLD_LAYER_NOTES.md` and `src/gold/01`–`04` SQL |
| `task-breakdown.md` | Phase 6 listed "Not started" |

**Decisions made:**

| Decision | Rationale |
|----------|-----------|
| 10 queries (not 12+) | Meets 8–10 target; avoids redundant overview tables |
| `customer_revenue_summary_kpis` as single-row aggregate | Supports KPI cards without duplicating top-N logic |
| Separate daily/weekly revenue and order trend queries | Clear visualization binding; respects `time_grain` filter |
| `segment_spend_share` uses window over `SUM(total_spend)` | Presentation aggregation of existing Gold metric |
| No Python orchestration for Dashboard | Phase scope is SQL + guide only; matches `requirements-analysis.md` artifacts |
| No Gold/Silver/Bronze changes | Frozen per project rules |

**Accepted:**

- Gold FQNs and column names from actual Gold implementation
- Section structure: Product Performance, Customer Revenue, Revenue/Trends, Customer Segmentation
- Post–RI-fix validation baselines in guide

**Rejected:**

- Joining Gold back to Silver for customer/product names beyond Gold columns
- Recreating weekly boundaries or segment logic in Dashboard SQL
- Modifying Gold to simplify Dashboard
- Using pre–RI-fix row counts/revenue as current baselines

### Implementation (Cursor agent — 2026-08-27)

| File | Action |
|------|--------|
| `src/dashboard/dashboard_queries.sql` | Created — 10 queries |
| `src/dashboard/DASHBOARD_GUIDE.md` | Created |
| `ai-prompts/dashboard.md` | Created (this file) |
| `tool-specific/cursor-workflow/task-breakdown.md` | Updated Phase 6 status only |

**Frozen layers:** `src/bronze/`, `src/silver/`, `src/gold/`, `data/`, `src/data_generation/` — **not modified**.

### Static / local validation

| Check | Result |
|-------|--------|
| Expected files exist | **PASS** |
| All queries reference only `de_c1_coding_evaluation.gold.*` | **PASS** (grep) |
| No `silver`, `bronze`, or `csv` references in dashboard SQL | **PASS** |
| 10 named queries in 4 sections | **PASS** |
| Guide documents all 10 queries | **PASS** |
| SQL section comments match guide query names | **PASS** |
| Secrets in artifacts | **None** |

### Databricks Serverless validation

| Check | Result |
|-------|--------|
| Gold source availability | **Not run from Cursor** |
| Gold row counts / baselines | **Not run from Cursor** |
| Execute all 10 dashboard queries | **Not run from Cursor** |

Operator checklist documented in `DASHBOARD_GUIDE.md` § Databricks validation checklist.

**FINAL DECISION:** **PHASE 6 IMPLEMENTATION COMPLETE — DATABRICKS VALIDATION PENDING**

---

## Cursor Evaluation Evidence (Phase 6)

| Requirement | Evidence |
|-------------|----------|
| Dashboard artifacts under `src/dashboard/` | `dashboard_queries.sql`, `DASHBOARD_GUIDE.md` |
| Gold-only consumption | Static grep + query review |
| Analytical themes covered | Product, customer revenue, trends, segmentation |
| Prompt history | `ai-prompts/dashboard.md` |
| Frozen layers respected | No edits under bronze/silver/gold/data/data_generation |

---

## Prompt 22 — Dashboard schema validation (`order_count`)

**TYPE:** Debugging / validation

**PROMPT SENT:**

```text
We are validating Phase 6 Dashboard in Databricks Serverless.

The Gold prerequisite validation has passed:

- gold_sales_by_product = 164 rows
- gold_revenue_by_customer = 792 rows
- gold_customer_segmentation = 792 rows
- gold_daily_weekly_trends = 950 rows
  - day = 818
  - week = 132
- Gold distinct orders = 2052

During Dashboard SQL execution, Databricks returned:

UNRESOLVED_COLUMN: order_count cannot be resolved.

The error specifically occurred against gold_sales_by_product, whose available columns are:

product_id
product_name
category
total_revenue
total_quantity

Therefore, do NOT modify Gold or Silver.

Inspect:

- src/dashboard/dashboard_queries.sql
- src/dashboard/DASHBOARD_GUIDE.md
- GOLD_LAYER_NOTES.md
- actual src/gold SQL/schema if needed

Find every Dashboard query that references order_count from gold_sales_by_product.

Determine whether order_count is actually required by the documented Dashboard requirement.

If it is not required, remove that metric from the Dashboard query and guide.

If the query is intended to provide a product-sales visualization, use only the metrics actually exposed by gold_sales_by_product:
- product_id
- product_name
- category
- total_revenue
- total_quantity

Do NOT recreate order_count from Silver or Bronze.

Do NOT add joins to Silver.
Do NOT modify Gold.
Do NOT invent a product-level order_count.

Also inspect ALL 10 Dashboard queries for similar schema mismatches before making the fix.

Make the smallest Dashboard-only correction necessary.

After the correction:
1. report exactly which query/query queries were changed;
2. explain why each change was necessary;
3. verify every referenced column against the actual Gold schema;
4. verify all four Gold FQNs remain the only data sources;
5. update DASHBOARD_GUIDE.md if its query description became inaccurate;
6. update ai-prompts/dashboard.md with the correction if that is the established project convention.

Do not change Bronze, Silver, Gold, data generation, or Gold metric definitions.
```

**AI RESPONSE SUMMARY:**

- Inspected `dashboard_queries.sql` — no `order_count` on `gold_sales_by_product` in repository SQL
- Root cause likely operator-added column or confusion from Gold metric listing
- Added schema-contract comments in SQL and `DASHBOARD_GUIDE.md` (Dashboard-only; no Gold/Silver changes)
- Full 10-query schema audit **PASS**

**Repository inspection:**

| Finding | Detail |
|---------|--------|
| Product queries in `dashboard_queries.sql` | **No** `order_count` reference on `gold_sales_by_product` |
| `order_count` usage | Only in trend queries (`gold_daily_weekly_trends`) — valid per Gold contract |
| Dashboard requirement | Product performance uses revenue/quantity/category; order trends use `gold_daily_weekly_trends` |
| Root cause | Likely operator-added `order_count` to a product query, or confusion from Phase 6 Rule B listing all Gold metrics together |

**Changes made (Dashboard-only):**

| File | Change |
|------|--------|
| `src/dashboard/dashboard_queries.sql` | Added Gold column-contract header; per-section column comments; `revenue_by_category` `ORDER BY SUM(total_revenue) DESC` for Spark clarity |
| `src/dashboard/DASHBOARD_GUIDE.md` | Clarified `order_count` is trends-only; added per-query column validation table |
| `ai-prompts/dashboard.md` | This iteration record |

**Queries changed:** None required removal of `order_count` from product queries (already absent). Minor hardening only on `revenue_by_category` ordering.

**Full schema audit (10 queries):** All column references match `GOLD_LAYER_NOTES.md` — **PASS**.

**Gold FQNs:** Only the four approved `de_c1_coding_evaluation.gold.*` tables referenced — **PASS**.

**FINAL DECISION:** Dashboard SQL aligned with Gold schema; re-run validation one query block at a time in Databricks.

---

## Prompt 23 — Evaluation dashboard completion

**TYPE:** Iteration / finalization

**PROMPT SENT:**

```text
We are completing the Databricks coding/evaluation project.

I need you to review the existing project code, especially:

1. dashboard_queries.sql
2. all Gold-layer SQL/models/tables
3. the evaluation/requirements document available in the project
4. any existing dashboard-related code or documentation

IMPORTANT:
Do not blindly rewrite existing SQL. First understand what has already been implemented and reuse existing Gold-layer tables and queries wherever possible.

====================================================
DASHBOARD REQUIREMENTS
====================================================

The dashboard needs at least 3 meaningful SQL-based visualizations/tiles and must include the required business views from the evaluation:

1. Top 10 products by revenue
   - Recommended visualization: horizontal bar chart
   - Product on Y-axis
   - Revenue on X-axis
   - Sort descending
   - Show top 10 only

2. Customer revenue distribution
   - Recommended visualization: histogram
   - Customer-level total revenue/spend on X-axis
   - Number of customers on Y-axis
   - Use appropriate bins

3. Customer segmentation
   - Recommended visualization: pie/donut chart
   - Required behavioral segmentation should be represented as:
       High-Value
       Repeat
       One-Time
       Inactive
   - Show customer count or appropriate revenue metric according to the Gold-layer requirement

Additionally, we already have useful dashboard queries/results for:

4. Daily order trend

5. Weekly order trend

6. Overall customer KPIs:
   - total_customers
   - total_spend
   - avg_customer_spend
   - avg_frequency
   - avg_lifetime_value
   - and total orders where available

7. Existing customer segment analysis:
   - Standard
   - Basic
   - Premium
   - customer_count
   - total_spend
   - avg_total_spend
   - avg_frequency
   - avg_lifetime_value
   - percentage of total spend

====================================================
EXISTING QUERIES
====================================================

The existing dashboard_queries.sql contains queries similar to:

-- Daily trend
SELECT
    period_start,
    order_count
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
WHERE time_grain = 'day'
ORDER BY period_start;

-- Weekly trend
SELECT
    period_start AS week_start,
    order_count AS weekly_order_count
FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
WHERE time_grain = 'week'
ORDER BY week_start;

-- Customer segment
SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    SUM(total_spend) AS total_spend,
    AVG(total_spend) AS avg_total_spend,
    AVG(frequency) AS avg_frequency,
    AVG(lifetime_value) AS avg_lifetime_value
FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
GROUP BY customer_segment
ORDER BY total_spend DESC;

-- Customer segment percentage
SELECT
    customer_segment,
    SUM(total_spend) AS total_spend,
    ROUND(
        100.0 * SUM(total_spend) / SUM(SUM(total_spend)) OVER (),
        2
    ) AS pct_of_total_spend
FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
GROUP BY customer_segment
ORDER BY total_spend DESC;

There is also an overall KPI query/result producing approximately:

total_customers = 792
total_spend = 2708411.08
avg_customer_spend = 3419.710960
avg_frequency = 2.590909090909091
avg_lifetime_value = 7548.671136

====================================================
IMPORTANT OBSERVATION
====================================================

Do NOT confuse:

Basic / Standard / Premium

with the required behavioral segmentation:

High-Value / Repeat / One-Time / Inactive.

First inspect the Gold-layer implementation and determine whether the required behavioral segmentation already exists in a Gold table.

If it exists:
    reuse it.

If it does not exist:
    determine which existing Gold tables contain the required customer/order information and implement the smallest appropriate SQL/model needed.

Do NOT unnecessarily modify upstream Silver/Gold transformations if the required information already exists.

====================================================
TASK 1 — AUDIT EXISTING DASHBOARD QUERIES
====================================================

Review dashboard_queries.sql and classify every existing query as:

A. Required dashboard visualization
B. Useful additional visualization
C. KPI/card query
D. Validation/query that should not become a dashboard tile
E. Duplicate/redundant query

For example, the query that calculates weekly totals from daily data may be useful for validation, but if the Gold table already contains weekly aggregation, don't create two identical dashboard visualizations.

Preserve working queries unless there is a concrete reason to change them.

====================================================
TASK 2 — IMPLEMENT MISSING REQUIRED QUERIES
====================================================

Add the missing dashboard SQL queries for:

A. Top 10 products by revenue

B. Customer revenue distribution

C. Required behavioral customer segmentation:
   High-Value / Repeat / One-Time / Inactive

Use existing Gold-layer tables wherever possible.

Before writing SQL, inspect the actual schemas and column names.

Do not invent column names.

Use the project's existing naming conventions.

Each query should be independently executable in Databricks SQL.

====================================================
TASK 3 — LOOK FOR REUSABLE VISUALIZATIONS
====================================================

After implementing the required queries, identify additional visualizations that can be built directly from our existing queries without unnecessary new ETL.

Consider:

1. Daily order trend
   - Line chart

2. Weekly order trend
   - Line chart
   - Prefer this as the main trend visualization because it is less noisy

3. Standard/Basic/Premium revenue contribution
   - Donut/pie chart using pct_of_total_spend

4. Standard/Basic/Premium customer count
   - Bar chart

5. Standard/Basic/Premium average customer spend
   - Bar chart

6. Standard/Basic/Premium average frequency
   - Bar chart

7. Standard/Basic/Premium average lifetime value
   - Bar chart

8. Overall KPI cards
   - Total customers
   - Total spend/revenue
   - Average customer spend
   - Average frequency
   - Average lifetime value
   - Total orders

9. Top products by revenue
   - Required horizontal bar chart

10. Customer revenue distribution
   - Required histogram

11. Behavioral segmentation
   - Required pie/donut chart

Do not create all of these automatically if that would make the dashboard cluttered.

Instead, recommend the strongest set of visualizations for a professional business dashboard.

====================================================
TASK 4 — RECOMMEND FINAL DASHBOARD LAYOUT
====================================================

Design a recommended dashboard layout.

Prefer something like:

ROW 1 — KPI CARDS
- Total Customers
- Total Revenue/Spend
- Total Orders
- Avg Customer Spend
- Avg Frequency
- Avg Lifetime Value

ROW 2 — BUSINESS TREND
- Weekly Order Trend
- Daily Order Trend or a secondary trend if useful

ROW 3 — PRODUCT PERFORMANCE
- Top 10 Products by Revenue

ROW 4 — CUSTOMER ANALYSIS
- Customer Revenue Distribution
- Behavioral Customer Segmentation

ROW 5 — OPTIONAL SEGMENT ANALYSIS
- Basic / Standard / Premium Revenue Contribution
- OR segment-level customer count/revenue/frequency

Explain which optional visualization is most useful and why.

====================================================
TASK 5 — CHECK DATA CONSISTENCY
====================================================

Validate that:

1. Weekly aggregation calculated from daily data agrees with the existing Gold weekly aggregation.

2. Customer segment revenue percentages sum to approximately 100%.

3. Overall customer spend agrees with the sum of segment spend.

4. Counts are logically consistent.

5. No duplicate aggregation is being introduced.

6. Top-10 revenue query is actually sorted descending and limited to 10.

7. Histogram query operates at CUSTOMER level, not order level.

8. Behavioral segmentation is based on the correct Gold-layer/customer behavior definition from the evaluation requirements.

If any inconsistency exists, report it instead of silently changing data.

====================================================
TASK 6 — SQL FILE ORGANIZATION
====================================================

Cleanly organize dashboard_queries.sql into sections:

----------------------------------------------------
-- 1. KPI CARDS
----------------------------------------------------

----------------------------------------------------
-- 2. ORDER TRENDS
----------------------------------------------------

----------------------------------------------------
-- 3. TOP PRODUCTS
----------------------------------------------------

----------------------------------------------------
-- 4. CUSTOMER REVENUE DISTRIBUTION
----------------------------------------------------

----------------------------------------------------
-- 5. CUSTOMER BEHAVIORAL SEGMENTATION
----------------------------------------------------

----------------------------------------------------
-- 6. CUSTOMER SEGMENT ANALYSIS
----------------------------------------------------

----------------------------------------------------
-- 7. VALIDATION QUERIES
----------------------------------------------------

For each dashboard query, add a short SQL comment explaining:

- What business question it answers
- Recommended visualization
- Important field(s) for X/Y/category

Do not add excessive comments.

====================================================
TASK 7 — DO NOT OVERENGINEER
====================================================

This is a coding/evaluation project.

Do NOT:

- introduce unnecessary frameworks
- create unnecessary Gold tables
- duplicate existing aggregations
- modify working ETL just for dashboard purposes
- invent data
- hardcode result values
- hardcode dates unless the requirement explicitly calls for it
- use Python/Pandas when Databricks SQL is sufficient
- create duplicate visualizations showing the same metric

Prefer simple, readable Databricks SQL.

====================================================
FINAL RESPONSE FROM YOU
====================================================

After making the changes, give me:

1. Files inspected
2. Existing dashboard queries that can be reused
3. Queries that were added
4. Any queries that were redundant
5. Final recommended dashboard tiles
6. Recommended visualization type for every tile
7. Any schema/data issues discovered
8. Exact files changed

Do not claim that a query works unless you have verified the relevant table/column names against the project.

Most importantly:
PRESERVE EXISTING WORK WHERE IT IS ALREADY CORRECT AND BUILD THE MISSING DASHBOARD REQUIREMENTS AROUND IT.
```

**Gold inspection:**

| Finding | Detail |
|---------|--------|
| Behavioral segments in Gold? | **No** — `customer_segment` is Premium/Standard/Basic only |
| Behavioral inputs in Gold | `frequency`, `total_spend` on `gold_customer_segmentation` |
| Inactive customers | Excluded from Gold segmentation grain (zero-order customers) |

**Queries added:**

- `customer_revenue_distribution` (histogram, customer-level from `gold_revenue_by_customer`)
- `behavioral_segment_summary` (derived from `frequency` + `total_spend`)
- `overall_customer_kpis` (replaces narrower `customer_revenue_summary_kpis`)
- 4 validation queries

**Queries reorganized:** 7 sections per evaluation spec; supplemental block preserves `top_products_by_quantity`, `revenue_by_category`, `top_customers_by_revenue`.

**Removed from primary dashboard path:** `daily_revenue_trend`, `weekly_revenue_trend`, `customer_revenue_summary_kpis` (superseded or not required for order-focused trends).

**FINAL DECISION:** Evaluation-required visualizations supported; behavioral segmentation is Dashboard-derived (Gold metrics only).
---

## Prompt 30 — Phase 6 — Dashboard design specification

**TYPE:** Design

**PROMPT SENT:**

```text
# Phase 6 — Dashboard: Design the Implementation Specification

You are working on the `DE_C1_Coding_Evaluation` repository.

## Context

Phase 5 Gold is COMPLETE and ACCEPTED on Databricks Serverless.

The validated post-RI-alignment state is:

* `SERVERLESS_COMPAT_VERSION = 10`
* `silver_customers = 878`
* `silver_products = 164`
* `silver_orders = 3646`
* Silver revenue = `2,708,411.08`
* Silver quantity = `10,899`
* Silver distinct orders = `2,052`

Gold is frozen and accepted:

* `gold_sales_by_product = 164 rows`
* `gold_revenue_by_customer = 792 rows`
* `gold_customer_segmentation = 792 rows`
* `gold_daily_weekly_trends = 950 rows`

  * 818 daily
  * 132 weekly
* Gold revenue = `2,708,411.08`
* Gold quantity = `10,899`
* Gold distinct orders = `2,052`
* Gold ↔ Silver reconciliation = PASS
* Gold idempotency = PASS
* AC-1 through AC-11 = PASS

IMPORTANT:

**Do not modify the Bronze, Silver, or Gold implementation.**

In particular, do NOT modify:

* `src/bronze/`
* `src/silver/`
* `src/gold/*.sql`
* `src/gold/create_gold_tables.py`
* Gold metric definitions
* Gold grains
* Gold join contracts

Gold is the frozen consumption layer for Dashboard.

---

# Phase 6 Objective

The next project phase is:

**Phase 6 — Dashboard**

The repository documentation indicates that Dashboard should provide:

1. visualization-ready SQL
2. a usage/implementation guide
3. prompt history

The Dashboard must consume the existing Gold tables and must NOT reimplement Silver/Gold business logic.

Expected artifacts:

```text
src/dashboard/
    dashboard_queries.sql
    DASHBOARD_GUIDE.md

ai-prompts/
    dashboard.md
```

The exact location of `DASHBOARD_GUIDE.md` must be determined by inspecting the repository documentation. There is currently an inconsistency between documents about whether it belongs under `src/dashboard/` or the repository root.

Do not resolve this by guessing.

Inspect:

* `requirements-analysis.md`
* `design-notes.md`
* `tool-workflow.md`
* `data-model.md`
* `README.md`
* `GOLD_LAYER_NOTES.md`
* `tool-specific/cursor-workflow/task-breakdown.md`
* relevant repository instructions/rules

---

# Gold sources available to Dashboard

Dashboard must consume these exact Gold objects:

```text
de_c1_coding_evaluation.gold.gold_sales_by_product

de_c1_coding_evaluation.gold.gold_revenue_by_customer

de_c1_coding_evaluation.gold.gold_daily_weekly_trends

de_c1_coding_evaluation.gold.gold_customer_segmentation
```

First inspect `GOLD_LAYER_NOTES.md` and the actual Gold SQL to establish the exact:

* columns
* data types
* grains
* metric definitions
* semantics

Do NOT assume columns beyond what the repository confirms.

---

# Dashboard analytical themes

The Dashboard should support these four themes:

## 1. Product Sales Performance

Source:

```text
gold_sales_by_product
```

Potential analytical views include:

* top products by revenue
* top products by quantity
* revenue by category
* product sales ranking

Do not blindly implement all of these until you inspect the repository requirements and Gold schema.

---

## 2. Customer Revenue

Source:

```text
gold_revenue_by_customer
```

Potential analytical views include:

* top customers by revenue
* customer revenue ranking
* revenue distribution

Again, determine the final query set from repository requirements and existing conventions.

---

## 3. Revenue / Order Trends

Source:

```text
gold_daily_weekly_trends
```

Potential analytical views include:

* daily revenue
* weekly revenue
* daily order count
* weekly order count
* revenue trend over time

Respect the existing `time_grain` and `period_start` semantics.

Do not independently redefine weekly boundaries.

---

## 4. Customer Segmentation

Source:

```text
gold_customer_segmentation
```

Potential analytical views include:

* customer count by segment
* revenue/spend by segment
* average lifetime value by segment
* average frequency by segment

Use the existing Gold definitions of:

* `customer_segment`
* `lifetime_value`
* `frequency`
* `total_spend`

Do not redefine these metrics from Silver.

---

# Critical architectural rules

## Rule 1 — Dashboard reads Gold only

Dashboard SQL must consume Gold.

Preferred:

```text
Gold
  ↓
Dashboard analytical query
  ↓
Visualization
```

Not:

```text
Silver
  ↓
Dashboard
```

and not:

```text
Bronze
  ↓
Dashboard
```

Do not introduce direct Dashboard dependencies on Bronze or Silver.

---

## Rule 2 — Do not recreate Gold metrics

If Gold already contains:

```text
total_revenue
total_quantity
order_count
lifetime_value
frequency
total_spend
```

Dashboard should consume those values rather than rebuilding them from Silver.

Additional aggregation is acceptable when needed for a visualization, for example:

```sql
SELECT category, SUM(total_revenue)
FROM gold_sales_by_product
GROUP BY category
```

But do not redefine the underlying business metric.

---

## Rule 3 — Preserve Gold grain

Before designing every query, identify the source Gold grain.

For example:

```text
gold_sales_by_product
    → one row per product

gold_revenue_by_customer
    → one row per customer

gold_customer_segmentation
    → one row per customer

gold_daily_weekly_trends
    → one row per time_grain + period_start
```

Confirm these from the repository rather than assuming them.

---

# What I want you to do NOW

Do NOT create or modify Dashboard files yet.

First inspect the repository and produce a **Phase 6 Dashboard Implementation Specification**.

Your response must contain the following sections.

## 1. Repository findings

Identify:

* current Dashboard-related files
* whether `src/dashboard/` exists
* whether `dashboard_queries.sql` already exists
* whether `DASHBOARD_GUIDE.md` already exists
* whether `ai-prompts/dashboard.md` exists
* relevant requirements from repository documentation

Clearly distinguish:

```text
explicit requirement
```

from:

```text
reasonable implementation choice
```

Do not invent requirements.

---

## 2. Gold contract summary

For each of the four Gold tables, report:

* exact FQN
* exact columns
* grain
* important metric definitions
* how Dashboard is expected to consume it

Use the actual repository files as the source of truth.

---

## 3. Proposed Dashboard query catalog

Design a concrete query catalog.

For each query provide:

* query name
* business purpose
* Gold source table
* expected output columns
* expected grain
* intended visualization
* why the query is useful

Prefer a small, high-value set rather than creating dozens of unnecessary queries.

Organize queries under:

```text
Product Performance
Customer Revenue
Revenue / Trends
Customer Segmentation
```

---

## 4. Query design rules

For each proposed query explicitly state:

* whether it directly reads Gold
* whether it performs an additional aggregation
* whether it introduces any new business logic
* why it is visualization-ready

Identify any query that could accidentally violate the frozen Gold contract.

---

## 5. Dashboard guide design

Propose the structure of `DASHBOARD_GUIDE.md`.

It should explain:

* prerequisites
* Gold dependencies
* how to execute `dashboard_queries.sql` in Databricks Serverless
* what each query produces
* recommended visualization type
* expected post-Phase-5 validation baselines
* interpretation of results
* limitations / assumptions

---

## 6. Databricks validation plan

Define exactly how Dashboard SQL should be validated in Databricks Serverless.

Include:

* execution sequence
* queries/results that should be checked
* schema checks
* row-count sanity checks
* reconciliation checks where appropriate
* confirmation that all queries read Gold only

Use the current validated baselines:

```text
Gold revenue: 2,708,411.08
Gold quantity: 10,899
Gold distinct orders: 2,052
Sales-by-product rows: 164
Revenue-by-customer rows: 792
Segmentation rows: 792
Trends rows: 950
Daily trend rows: 818
Weekly trend rows: 132
```

Do not invent expected results for new dashboard aggregations unless they can be derived from the existing Gold data.

---

## 7. Files to create

Provide the exact proposed file paths.

Expected candidates:

```text
src/dashboard/dashboard_queries.sql
src/dashboard/DASHBOARD_GUIDE.md
ai-prompts/dashboard.md
```

Also identify whether any existing documentation should be updated, such as:

```text
README.md
requirements-analysis.md
design-notes.md
tool-specific/cursor-workflow/task-breakdown.md
```

Do not modify them yet.

---

## 8. Files that must remain untouched

Explicitly list the files/directories that must remain unchanged because Gold is frozen.

At minimum:

```text
src/bronze/
src/silver/
src/gold/
data/
src/data_generation/
```

unless an explicit repository requirement proves otherwise.

---

## 9. Phase 6 acceptance criteria proposal

Because `task-breakdown.md` currently has no detailed Phase 6 acceptance table, propose a concise acceptance checklist derived ONLY from repository requirements.

Separate:

### Explicit acceptance requirements

from:

### Recommended validation checks

Do not falsely represent inferred checks as existing project requirements.

---

## 10. Implementation sequence

Give the recommended sequence:

```text
Repository inspection
        ↓
Phase 6 specification
        ↓
Create dashboard directory/files
        ↓
Implement dashboard_queries.sql
        ↓
Write DASHBOARD_GUIDE.md
        ↓
Record ai-prompts/dashboard.md
        ↓
Local/static validation
        ↓
Databricks Serverless validation
        ↓
Document actual evidence
        ↓
Mark Phase 6 complete
```

Adjust this sequence if repository documentation requires something different.

---

# Important constraints

1. Do NOT modify any files during this task.
2. Do NOT modify Gold SQL.
3. Do NOT modify Silver.
4. Do NOT create Dashboard files yet.
5. Do NOT invent missing requirements.
6. Do NOT use Silver/Gold totals from the pre-RI-fix state.
7. Do NOT propose a Python Dashboard orchestrator unless repository requirements explicitly require one.
8. Do NOT create charts or notebooks unless the repository explicitly requires them.
9. Do NOT use external web sources unless the repository explicitly requires external information.
10. Treat `GOLD_LAYER_NOTES.md` and actual Gold implementation as the authoritative source for Gold schema and semantics.
11. Treat the current post-RI-fix Databricks results above as the current validation baseline.

At the end, provide a concise:

**PHASE 6 IMPLEMENTATION DECISION**

with:

* recommended query count
* exact files to create
* exact files to modify, if any
* exact files to leave untouched
* unresolved repository ambiguities
* whether implementation is ready to begin

Do not implement anything yet.
```

**AI RESPONSE SUMMARY:**

Dashboard implementation spec produced before Prompt 21 code.

**FINAL DECISION:** ACCEPTED (documented)

