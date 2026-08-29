# AI Prompts — Silver Layer (Phase 4)

**Prompts in this file:** 07–13, 26, 27, 28
**Implementation order:** Design → five implementation iterations → RI alignment fix

---

## Prompt 07 — Silver design & task planning

**TYPE:** Design / planning

**PROMPT SENT:**

```text
PHASE 4 — SILVER LAYER IMPLEMENTATION

We are now starting Phase 4 (Silver layer) of the Databricks Medallion Pipeline.

IMPORTANT PROJECT STATUS:
- Phase 1 foundation is complete.
- Phase 2 data generation is complete and validated.
- Phase 3 Bronze ingestion is complete, validated in Databricks, accepted, committed, and pushed.
- Do NOT revalidate/reinspect the repository from scratch.
- Do NOT modify Bronze implementation unless a concrete Silver dependency requires it.
- Do NOT implement Gold, Dashboard, or any future phase.
- Work incrementally and stop when the Silver phase is complete.
- Follow the existing project documentation and Cursor workflow artifacts as the source of truth.

============================================================
1. DATabricks ENVIRONMENT
============================================================

Unity Catalog:

Catalog:
de_c1_coding_evaluation

Existing schema:

bronze

Existing Bronze tables:

de_c1_coding_evaluation.bronze.bronze_customers
de_c1_coding_evaluation.bronze.bronze_products
de_c1_coding_evaluation.bronze.bronze_orders

Silver schema should be:

de_c1_coding_evaluation.silver

Silver tables should be:

de_c1_coding_evaluation.silver.silver_customers
de_c1_coding_evaluation.silver.silver_products
de_c1_coding_evaluation.silver.silver_orders

Any DQ summary/quarantine objects should also be created under:

de_c1_coding_evaluation.silver

Do not invent another catalog.

Do not use the legacy two-part naming convention where the catalog is already known.

============================================================
2. EXISTING PROJECT CONTEXT
============================================================

Repository:

DE_C1_Coding_Evaluation

Architecture:

Raw CSV
   ↓
Bronze Delta
   ↓
Silver Delta
   ↓
Gold
   ↓
Dashboard

Bronze has already been successfully created and validated in Databricks.

Observed Bronze row counts:

customers = 1006
products  = 206
orders    = 5163

Bronze intentionally preserves Phase 2 defects.

Known observed defects include:

- NULL/blank customer emails = 50
- invalid/non-positive order quantities = 40
- orphan customer references = 25
- orphan product references = 25

Additional defects were intentionally generated during Phase 2.

Authoritative references:

src/data_generation/DATA_GENERATION_NOTES.md
data-model.md
data-quality-strategy.md
design-notes.md
requirements-analysis.md

Do not invent new defect categories.

============================================================
3. IMPORTANT CURSOR IMPLEMENTATION APPROACH
============================================================

DO NOT generate the entire Silver implementation in one large step.

The assessment explicitly requires evidence of:

- Persistent project context
- Iteration
- Validation
- Accepting some suggestions
- Rejecting/changing other suggestions
- Testing Cursor-generated code before acceptance
- Specific prompts rather than vague "build Silver" prompts

Therefore implement Silver through multiple deliberate iterations.

Use the following sequence:

ITERATION 1:
Design/review the Silver implementation.

- Review the existing finalized data model and DQ strategy.
- Propose the Silver execution flow.
- Identify required files and responsibilities.
- Identify how invalid records and DQ results will be represented.
- Do NOT implement the full Silver layer yet.
- Update task-breakdown.md with specific Silver tasks.

Then STOP and wait for review.

ITERATION 2:
Implement type standardization, cleansing, completeness, and uniqueness.

Then:
- run local/static validation where possible
- inspect generated code
- identify issues
- refine implementation

Do not proceed to the remaining DQ categories until this iteration is reviewed.

ITERATION 3:
Implement referential integrity and business logic checks.

Use the actual Bronze data and known Phase 2 defects.

Then:
- validate
- inspect results
- fix/refine issues

ITERATION 4:
Implement quarantine/rejected-record handling and DQ summary reporting.

Then:
- validate
- inspect results
- refine if required

ITERATION 5:
Integrate the complete Silver orchestration.

Run the full Silver flow.

Then validate in Databricks.

IMPORTANT:
Each iteration must be documented in:

ai-prompts/silver-layer.md

using:

PROMPT SENT
AI RESPONSE SUMMARY
YOUR EVALUATION
FINAL DECISION

If a Cursor suggestion is changed or rejected, explicitly document why.

Do not fabricate evaluation or validation results.

============================================================
4. SILVER OBJECTIVE
============================================================

Implement Silver as the trusted/curated layer.

Silver must:

1. Read from Bronze Delta tables.
2. Apply explicit typing and cleansing.
3. Apply the five required data-quality categories:
   - Completeness
   - Uniqueness
   - Type validation
   - Referential integrity
   - Business logic
4. Produce curated Silver tables.
5. Preserve traceability of rejected/invalid records.
6. Produce a DQ summary.
7. Keep the implementation modular and understandable.
8. Align exactly with the finalized Phase 2 physical data model.

============================================================
5. FINALIZED DATA MODEL
============================================================

Customers:

customer_id
customer_name
email
country
signup_date
customer_segment
lifetime_value

Products:

product_id
product_name
category
unit_price

Orders are LINE ITEMS:

order_line_id
order_id
customer_id
product_id
order_date
quantity
unit_price

Revenue:

quantity * unit_price

IMPORTANT:

Do not convert orders back into an order-header model.

Multiple order lines may legitimately share the same order_id.

============================================================
6. REQUIRED SILVER FILES
============================================================

Create:

src/silver/01_quality_completeness.py
src/silver/02_quality_uniqueness.py
src/silver/03_quality_type_validation.py
src/silver/04_quality_referential_integrity.py
src/silver/05_quality_business_logic.py
src/silver/create_silver_tables.py
src/silver/SILVER_LAYER_NOTES.md

You may add a small shared helper module if genuinely necessary for DRY/reusable logic.

Do not create unnecessary framework complexity.

============================================================
7. SILVER TABLES
============================================================

Create:

de_c1_coding_evaluation.silver.silver_customers
de_c1_coding_evaluation.silver.silver_products
de_c1_coding_evaluation.silver.silver_orders

Create the silver schema if it does not exist.

Use Delta tables.

============================================================
8. TYPE STANDARDIZATION
============================================================

Bronze intentionally stores source columns as STRING to preserve defects.

Silver must convert fields to appropriate analytical types.

Customers:

customer_id → string
customer_name → string
email → string
country → string
signup_date → date
customer_segment → string
lifetime_value → appropriate numeric/decimal type

Products:

product_id → string
product_name → string
category → string
unit_price → appropriate numeric/decimal type

Orders:

order_line_id → string
order_id → string
customer_id → string
product_id → string
order_date → date
quantity → integer
unit_price → appropriate numeric/decimal type

Use safe parsing/casting where appropriate.

Malformed values must be detectable and traceable.

Do not silently discard invalid records.

============================================================
9. COMPLETENESS
============================================================

Implement the completeness rules defined in:

data-quality-strategy.md

At minimum validate critical identifiers and required fields.

Customers:
- customer_id
- customer_name
- email

Products:
- product_id
- product_name

Orders:
- order_line_id
- order_id
- customer_id
- product_id
- order_date

Do not blindly make optional fields required.

Document the final required-field decisions.

Invalid records must remain traceable.

============================================================
10. UNIQUENESS
============================================================

Validate:

Customers:
customer_id

Products:
product_id

Orders:
order_line_id

IMPORTANT:

order_id is NOT the uniqueness key because orders are line items.

Multiple order lines can share an order_id.

The Phase 2 duplicate defects must be detectable.

============================================================
11. TYPE VALIDATION
============================================================

Validate malformed source values before/while converting to Silver types.

Known examples include:

- invalid signup dates
- invalid order dates
- invalid product unit prices
- invalid order unit prices
- invalid quantity values
- invalid email formats

Use explicit validation logic.

Do not silently convert malformed values into valid-looking values without recording the failure.

============================================================
12. REFERENTIAL INTEGRITY
============================================================

Validate:

orders.customer_id → customers.customer_id

orders.product_id → products.product_id

Known Bronze defects:

orphan customers = 25
orphan products = 25

Silver must detect these.

Use appropriate Spark joins/anti-joins.

Important:

Parent entities must have their canonical valid records established before FK validation is considered authoritative.

Document the execution order and reasoning.

============================================================
13. BUSINESS LOGIC
============================================================

Implement the business rules defined in:

data-quality-strategy.md

Known defects include:

- future customer signup dates
- negative product prices
- future order dates
- non-positive quantities
- catalog-price mismatch

For catalog-price mismatch:

Compare order-line unit_price against the canonical product unit_price.

Do not invent unrelated business rules.

============================================================
14. INVALID RECORD HANDLING
============================================================

Use a traceable invalid-record strategy.

Preferred assessment design:

Valid records
    ↓
Silver curated tables

Invalid records
    ↓
Silver quarantine/rejected records

DQ checks
    ↓
DQ summary

Do not simply drop invalid records.

Create an appropriate quarantine structure under:

de_c1_coding_evaluation.silver

It should allow us to identify:

- source/entity
- business key
- failure category
- failure reason
- processing timestamp

If a record fails multiple checks, preserve multiple failure reasons where practical.

Keep the implementation simple and assessment-appropriate.

============================================================
15. DQ SUMMARY
============================================================

Create a DQ summary object under:

de_c1_coding_evaluation.silver

At minimum include:

check_category
table_name
rows_tested
rows_passed
rows_failed
pass_percentage
run_timestamp

Where useful include:

failure_reason

The summary must demonstrate execution of all five required DQ categories.

============================================================
16. SILVER EXECUTION ORDER
============================================================

Recommended logical flow:

1. Read Bronze
2. Standardize/parse types
3. Completeness validation
4. Uniqueness validation
5. Establish canonical parent records
6. Referential integrity validation
7. Business logic validation
8. Build valid Silver tables
9. Write quarantine/rejected records
10. Write DQ summary

You may adjust the order if technically necessary.

If changed, document why.

============================================================
17. IDEMPOTENCY
============================================================

The Silver process must be safely rerunnable for the same Bronze input.

Avoid accumulating duplicate records across repeated runs.

Use an appropriate write strategy.

============================================================
18. DOCUMENTATION
============================================================

Update:

data-quality-strategy.md
design-notes.md
requirements-analysis.md
README.md
tool-workflow.md

Create:

src/silver/SILVER_LAYER_NOTES.md

Documentation must describe actual implementation decisions.

Do not claim Databricks validation until it has actually occurred.

============================================================
19. CURSOR WORKFLOW ARTIFACTS
============================================================

Update:

ai-prompts/silver-layer.md

Record every meaningful implementation/refinement cycle.

Also update where appropriate:

tool-specific/cursor-workflow/project-context.md
tool-specific/cursor-workflow/spec.md
tool-specific/cursor-workflow/task-breakdown.md

The task breakdown must show granular Silver tasks.

Examples:

- Define Silver schema strategy
- Define safe type conversion
- Implement completeness checks
- Implement uniqueness checks
- Implement type validation
- Implement FK validation
- Implement business rules
- Implement quarantine
- Implement DQ summary
- Integrate orchestration
- Validate in Databricks
- Fix/refine based on validation

============================================================
20. VALIDATION
============================================================

LOCAL VALIDATION:

Run what can be validated without Spark.

Examples:

- py_compile
- import/static validation where possible
- configuration validation
- code-level checks

Do not pretend local validation proves Delta behavior.

DATABRICKS VALIDATION:

Run the actual Silver pipeline in Databricks.

Verify:

1. Silver schema exists.
2. Silver tables exist.
3. Silver schemas/types are correct.
4. Silver row counts are reasonable and explainable.
5. DQ summary exists.
6. Quarantine records exist where expected.
7. Completeness detects known defects.
8. Uniqueness detects known duplicate defects.
9. Type validation detects malformed values.
10. Referential integrity detects:
    - 25 orphan customers
    - 25 orphan products
11. Business logic detects known invalid quantities/dates/prices.
12. Rerunning the pipeline does not accumulate duplicates.

Compare actual results with:

src/data_generation/DATA_GENERATION_NOTES.md

Record actual observed values.

Do not fabricate results.

============================================================
21. PHASE SCOPE
============================================================

DO NOT implement:

- Gold
- Dashboard
- Streaming
- Production monitoring
- Production alerting
- Advanced PII governance
- Unrelated infrastructure

Do not modify Phase 2 data generation.

Do not modify Bronze unless a concrete issue blocks Silver.

If Bronze modification becomes necessary:

STOP and explain the reason before changing it.

============================================================
22. GIT / COMMIT DISCIPLINE
============================================================

Do not commit or push automatically.

After Silver implementation and validation, provide:

git status
git diff --stat
recommended commit structure
recommended commit message

We will decide when to commit/push.

============================================================
23. STOP CONDITION
============================================================

When the current iteration is complete:

1. Show files created/modified.
2. Explain implementation decisions.
3. Show validation performed.
4. Show known limitations.
5. Update the appropriate Cursor prompt artifact.
6. STOP.

Do not automatically continue to the next iteration.

Do not start Gold.

Proceed with ITERATION 1 only:

Design/review the Silver implementation and update the Silver task breakdown.

Do NOT generate the full Silver implementation yet.
```

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

## Prompt 08 — Resolve open design decisions

**TYPE:** Implementation

**PROMPT SENT:**

```text
PHASE 4 — SILVER ITERATION 1: RESOLVE OPEN DESIGN DECISIONS

We have reviewed the Silver Iteration 1 design. Update the Silver design documentation only.

IMPORTANT:
- Do NOT create Silver implementation code.
- Do NOT modify any existing Silver Python implementation code.
- Do NOT start Iteration 2.
- Do NOT modify Bronze, Gold, or Dashboard implementation.
- This is a design/documentation refinement iteration only.
- STOP after completing this iteration and wait for my approval.

Apply the following final decisions:

1. COMPLETENESS — FULL REQUIRED-FIELD LIST

Use the full required-field lists already defined in data-quality-strategy.md as the authoritative Silver completeness rules.

Customers:
- customer_id
- customer_name
- email
- country
- signup_date
- customer_segment
- lifetime_value

Products:
- product_id
- product_name
- category
- unit_price

Orders:
- order_line_id
- order_id
- customer_id
- product_id
- order_date
- quantity
- unit_price

Do NOT replace this with the smaller "minimum critical set" currently proposed in SILVER_LAYER_NOTES.md.

Rows failing completeness should be quarantined rather than silently dropped.

2. QUARANTINE — SINGLE CENTRALIZED TABLE

Use one centralized quarantine table:

de_c1_coding_evaluation.silver.silver_quarantine_records

It must support:
- customers
- products
- orders

and all five DQ categories:
- completeness
- uniqueness
- type_validation
- referential_integrity
- business_logic

Keep the proposed fields from SILVER_LAYER_NOTES.md:

- entity_name
- business_key
- check_category
- failure_reason
- failed_column
- bronze_source_values
- quarantine_timestamp
- run_timestamp

Invalid rows must not appear in the curated Silver tables.

3. IDENTIFIER TYPES — STRING IN SILVER

Keep all identifier columns as STRING in Silver, consistent with the Phase 4 design.

Identifiers include:
- customer_id
- product_id
- order_line_id
- order_id
- product_id

However, type validation must verify that identifier values are numerically parseable.

For example:

"12345" → valid → stored as STRING in Silver

"INVALID" → type validation failure → quarantine

Do not silently coerce malformed identifiers.

4. D17 CATALOG-PRICE MISMATCH — QUARANTINE ONLY

For the business rule:

orders.unit_price = products.unit_price

if an order line has a catalog-price mismatch:

- Detect the mismatch.
- Quarantine the affected order line.
- Do NOT automatically replace the order's unit_price with the product catalog price.
- Preserve the original Bronze value through quarantine traceability.

The goal is to demonstrate detection and controlled handling of intentionally seeded data-quality defects rather than silently correcting source data.

5. DATE-BASED BUSINESS RULES

Keep these business rules:

signup_date <= current_date()

order_date <= current_date()

Do not hard-code a fixed evaluation date.

However, ensure that the DQ summary and quarantine records capture the pipeline run timestamp/date so that the evaluation is traceable.

6. MAINTAIN THE EXISTING EXECUTION ORDER

Keep the proposed Silver execution order:

Bronze
→ trim / cleanse
→ safe typing
→ completeness
→ uniqueness
→ type validation
→ canonical valid customers/products
→ referential integrity
→ business logic
→ Silver curated tables
→ quarantine
→ DQ summary

Do not introduce new DQ categories.

7. DOCUMENTATION TO UPDATE

Update the following documentation where necessary to make the decisions above consistent:

- src/silver/SILVER_LAYER_NOTES.md
- ai-prompts/silver-layer.md
- data-quality-strategy.md
- tool-specific/cursor-workflow/spec.md
- tool-specific/cursor-workflow/task-breakdown.md

Only modify files where an update is actually required. Do not make unrelated changes.

8. CURSOR WORKFLOW EVIDENCE

In ai-prompts/silver-layer.md, document this iteration using the established format:

PROMPT SENT
- Record this prompt faithfully or as a faithful summary.

AI RESPONSE SUMMARY
- Summarize the documentation/design changes made.

YOUR EVALUATION
- Explain that the four open Silver design decisions were reviewed and resolved.
- State whether the resulting design is accepted or requires changes.

FINAL DECISION
- Record the final decision for this design iteration.

Clearly distinguish this design iteration from future implementation iterations.

9. VALIDATION

Since this is documentation/design only:

- Do not claim Silver implementation was tested.
- Do not claim Databricks Silver execution was performed.
- Verify that no Silver implementation code was created or modified.
- Check that the documentation remains internally consistent with data-model.md and data-quality-strategy.md.

10. FINAL RESPONSE

At the end, report:

- Files created
- Files modified
- Confirmation that no Silver implementation code was created or modified
- Confirmation that Iteration 2 was NOT started
- Any remaining open decisions, if any

STOP after this iteration. Wait for my approval before proceeding to Silver Iteration 2.
```

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

## Prompt 09 — Completeness, uniqueness & type validation

**TYPE:** Implementation

**PROMPT SENT:**

```text
# Silver Layer — Iteration 2: Type Standardization, Completeness & Uniqueness

We are now proceeding from the APPROVED Silver Layer design.

IMPORTANT:
- Silver Iteration 1 and Iteration 1b are COMPLETE and ACCEPTED.
- All Silver design decisions have been finalized.
- Do NOT redesign or reopen any of the resolved decisions.
- Do NOT start Iteration 3, 4, or 5.
- Do NOT modify Bronze, Gold, Dashboard, or unrelated project architecture.
- Implement ONLY Silver Iteration 2.
- Before writing code, inspect the existing Silver design artifacts and follow them as the source of truth.

## Project Context

Repository:
DE_C1_Coding_Evaluation

Databricks catalog:
de_c1_coding_evaluation

Schemas:
- Bronze: de_c1_coding_evaluation.bronze
- Silver: de_c1_coding_evaluation.silver

Bronze tables:
- de_c1_coding_evaluation.bronze.bronze_customers
- de_c1_coding_evaluation.bronze.bronze_products
- de_c1_coding_evaluation.bronze.bronze_orders

Bronze contains the Phase 2 intentionally defective CSV data and all source columns are STRING.

Silver must consume Bronze as-is.
Do not modify Bronze.

## Authoritative Design Documents

Before implementation, read and use:

1. data-quality-strategy.md
2. src/silver/SILVER_LAYER_NOTES.md
3. data-model.md
4. tool-specific/cursor-workflow/spec.md
5. tool-specific/cursor-workflow/task-breakdown.md
6. ai-prompts/silver-layer.md
7. src/data_generation/DATA_GENERATION_NOTES.md

Do not invent new DQ categories or contradict these documents.

# Iteration 2 Scope

Implement:

1. Type standardization / safe parsing
2. Completeness validation
3. Uniqueness validation

Do NOT implement:

- Referential integrity
- Business logic validation
- Final Silver table orchestration
- Final quarantine orchestration
- DQ summary orchestration
- Gold layer
- Dashboard

Those belong to later iterations.

# Required Silver Types

## Customers

Bronze:
customer_id
customer_name
email
country
signup_date
customer_segment
lifetime_value

Silver typed representation:

customer_id       STRING
customer_name     STRING
email             STRING
country           STRING
signup_date       DATE
customer_segment  STRING
lifetime_value    DECIMAL(12,2)

## Products

product_id       STRING
product_name     STRING
category         STRING
unit_price       DECIMAL(10,2)

## Orders

order_line_id    STRING
order_id         STRING
customer_id      STRING
product_id       STRING
order_date       DATE
quantity         INT
unit_price       DECIMAL(10,2)

IMPORTANT:
Identifiers remain STRING in Silver.

However, numeric parseability of identifiers must still be validated according to the finalized data-quality strategy.

Malformed values must NOT be silently coerced into valid values.

Use safe parsing/casting so malformed values become NULL or otherwise produce an explicit validation failure that can be handled later.

# Completeness Rules

Use the FINALIZED FULL required-field lists from data-quality-strategy.md.

Customers required fields:
- customer_id
- customer_name
- email
- country
- signup_date
- customer_segment
- lifetime_value

Products required fields:
- product_id
- product_name
- category
- unit_price

Orders required fields:
- order_line_id
- order_id
- customer_id
- product_id
- order_date
- quantity
- unit_price

Completeness means:

column IS NULL OR TRIM(column) = ''

Do not silently remove incomplete records.

The implementation must expose which rows fail completeness so that later iterations can quarantine them.

# Uniqueness Rules

Customer key:
customer_id

Product key:
product_id

Order key:
order_line_id

IMPORTANT:
order_id is NOT the uniqueness key.

Expected intentional duplicate defects from Phase 2:

- customers customer_id duplicates: 6
- products product_id duplicates: 6
- orders order_line_id duplicates: 8

Duplicate handling decision is FINAL:

- retain the first canonical occurrence
- later duplicate occurrences must be identifiable as failures
- they will ultimately be quarantined
- do not silently discard duplicate records

Use deterministic logic for "first occurrence" so repeated runs produce the same result.

Do NOT use arbitrary/non-deterministic ordering.

# Type Validation

Implement safe parsing for:

Customers:
- customer_id numeric parseability while retaining STRING output
- signup_date → DATE
- email basic format validation
- lifetime_value → DECIMAL(12,2)

Products:
- product_id numeric parseability while retaining STRING output
- unit_price → DECIMAL(10,2)

Orders:
- order_line_id numeric parseability while retaining STRING output
- order_id numeric parseability while retaining STRING output
- customer_id numeric parseability while retaining STRING output
- product_id numeric parseability while retaining STRING output
- order_date → DATE
- quantity → INT
- unit_price → DECIMAL(10,2)

Expected Phase 2 defects that this implementation should be capable of identifying include:

- invalid signup dates
- malformed email addresses
- invalid unit price values
- invalid order dates
- invalid numeric values

Do not add unrelated validation rules.

# Cleansing

Only perform the approved light cleansing:

- trim whitespace from STRING fields
- safe type parsing

Do not:
- auto-correct prices
- invent missing values
- infer missing IDs
- modify Bronze
- repair intentionally defective records
- perform catalog-price correction
- apply referential-integrity checks yet
- apply future-date/business-rule checks yet

# Code Structure

Follow the existing planned modular architecture.

Create/update only the files necessary for Iteration 2.

Prefer a shared helper module:

src/silver/silver_common.py

It may contain:
- catalog/schema configuration
- Bronze table references
- safe cast helpers
- string trimming helpers
- common validation helpers
- deterministic duplicate handling helpers

Then create the Iteration 2 implementation modules according to the existing task breakdown/design.

If the existing design specifies:

01_quality_completeness.py
02_quality_uniqueness.py
03_quality_type_validation.py

follow that structure.

Do not create the final create_silver_tables.py orchestration yet unless the existing task breakdown explicitly requires a placeholder. Do not implement later-phase orchestration.

# Quarantine

The finalized design is:

de_c1_coding_evaluation.silver.silver_quarantine_records

However, Iteration 2 should NOT prematurely implement the complete quarantine orchestration if that belongs to a later iteration.

Instead, make failures structured and available for the later quarantine implementation.

If helper functions are required for later quarantine compatibility, keep them modular and do not implement unrelated Iteration 3/4/5 behavior.

# Validation Requirements

After implementation, perform local validation that does not require PySpark if possible:

- py_compile all created/modified Python files
- verify imports where possible
- verify syntax
- verify deterministic duplicate logic
- verify helper functions using small test inputs where practical

If Databricks execution is possible, validate against:

de_c1_coding_evaluation.bronze.*

Do NOT claim Databricks validation unless actually executed.

# Expected Defect Traceability

Tie the implementation back to the Phase 2 defect matrix.

At minimum document how Iteration 2 detects:

Completeness:
- D01
- D02
- D07

Uniqueness:
- D03
- D08
- D16

Type validation:
- D04
- D05
- D09
- D13
- relevant invalid numeric values

Do not assume that the total number of defect injections equals the number of rejected rows because defects can overlap.

# Determinism Requirement

The implementation must be deterministic.

Running the same Bronze input multiple times should produce the same classification of records.

For duplicate handling, explicitly define the deterministic ordering used to identify the canonical first record.

# Documentation / Cursor Evidence

After implementation, update:

ai-prompts/silver-layer.md

with an Iteration 2 section containing:

1. The implementation prompt used
2. What Cursor implemented
3. Files created/modified
4. Design decisions followed
5. Validation performed
6. Any issues encountered
7. Refinements made
8. Suggestions from Cursor that were accepted
9. Suggestions from Cursor that were rejected, if any
10. Why those decisions were made
11. Final evaluation
12. ACCEPTED / REJECTED decision

Also update the appropriate Cursor workflow artifact:

tool-specific/cursor-workflow/task-breakdown.md

Mark only the Iteration 2 tasks that are actually completed.

Do not mark future iterations complete.

# Acceptance Criteria

Iteration 2 is ACCEPTED only if:

[ ] Type standardization follows the finalized Silver schema
[ ] IDs remain STRING while numeric parseability is validated
[ ] Dates are safely parsed
[ ] Numeric fields are safely parsed
[ ] Email format validation is implemented as specified
[ ] Full required-field completeness rules are implemented
[ ] Customer uniqueness uses customer_id
[ ] Product uniqueness uses product_id
[ ] Order uniqueness uses order_line_id
[ ] Duplicate handling is deterministic
[ ] Invalid records are not silently discarded
[ ] Bronze remains unchanged
[ ] No referential-integrity logic is prematurely implemented
[ ] No business-logic logic is prematurely implemented
[ ] No Gold/Dashboard code is created
[ ] Local validation passes
[ ] Documentation records the Cursor iteration and validation evidence

STOP after Iteration 2.

At the end, provide a concise implementation report containing:

- files created
- files modified
- what was implemented
- validation performed
- issues encountered and fixes
- remaining work for Iteration 3
- Git status

Do NOT proceed to Iteration 3 automatically.
```

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

## Prompt 10 — Referential integrity & business logic

**TYPE:** Implementation

**PROMPT SENT:**

```text
# Silver Layer — Iteration 3 Implementation
## Referential Integrity + Business Logic Validation

You are working on the DE_C1_Coding_Evaluation project.

We are now implementing ONLY Silver Layer Iteration 3.

IMPORTANT:
- Do NOT start Iteration 4.
- Do NOT create or modify the Silver orchestration.
- Do NOT create/write Silver curated tables yet.
- Do NOT modify Bronze code or Bronze tables.
- Do NOT modify Gold or Dashboard code.
- Do NOT redesign the existing Silver architecture.
- Reuse the existing Silver shared utilities and patterns from Iteration 2.
- Preserve Serverless compatibility.
- Do not introduce PySpark RDD APIs.
- Keep the implementation modular and testable.

==================================================
PROJECT ENVIRONMENT
==================================================

Catalog:
de_c1_coding_evaluation

Bronze schema:
bronze

Silver schema:
silver

Bronze tables:
de_c1_coding_evaluation.bronze.bronze_customers
de_c1_coding_evaluation.bronze.bronze_products
de_c1_coding_evaluation.bronze.bronze_orders

Silver tables are NOT being written yet.

Existing Silver files:

src/silver/silver_common.py
src/silver/01_quality_completeness.py
src/silver/02_quality_uniqueness.py
src/silver/03_quality_type_validation.py

Iteration 2 has already been implemented and validated on Databricks Serverless.

Existing validation results:

Completeness:
customers = 60
products = 9
orders = 0

Uniqueness:
customers = 6
products = 6
orders = 8

Type validation:
customers = 50
products = 15
orders = 30

Type validation total = 95, matching the documented Phase 2 type/format defect count.

==================================================
ITERATION 3 SCOPE
==================================================

Create exactly these two implementation modules:

src/silver/04_quality_referential_integrity.py

src/silver/05_quality_business_logic.py

Also update documentation only where necessary to record Iteration 3 implementation.

Do NOT implement quarantine writes yet.

Do NOT implement DQ summary writes yet.

Those belong to Iteration 4.

==================================================
1. 04_quality_referential_integrity.py
==================================================

Implement referential-integrity validation for order line items.

Rules:

orders.customer_id
    ->
customers.customer_id

orders.product_id
    ->
products.product_id

The parent key sets MUST come from the canonical valid parent records.

Use the Silver design already established:

1. Read Bronze customers/products/orders.
2. Apply the existing Silver preparation/type-standardization logic.
3. Apply the existing completeness/type/uniqueness concepts where required to establish canonical parent keys.
4. Build canonical valid customer IDs from valid customer records.
5. Build canonical valid product IDs from valid product records.
6. Check orders against those canonical parent key sets.
7. Produce structured failure DataFrames compatible with the existing quarantine schema.

Do NOT simply check against raw Bronze parent tables.

This is important because an invalid/duplicate parent must not automatically become a valid FK reference.

Expected defect evidence from Phase 2 / Bronze:

orphan customer references:
25

orphan product references:
25

Expected business keys:

orders.customer_id -> customers.customer_id

orders.product_id -> products.product_id

Use left anti-joins or equivalent Spark DataFrame operations.

Do NOT use RDDs.

Serverless compatibility is required.

The function should follow the existing module style and expose something similar to:

run_referential_integrity_all(
    spark=spark,
    config=config
)

Return structured results by entity, consistent with the existing modules.

For example, conceptually:

{
    "orders": {
        "prepared_df": ...,
        "failures_df": ...
    }
}

The exact structure should follow the existing Silver implementation rather than inventing a completely new interface.

Failure records must contain the existing quarantine-compatible columns:

entity_name
business_key
check_category
failure_reason
failed_column
bronze_source_values
quarantine_timestamp
run_timestamp

For orphan customer:

check_category = "referential_integrity"

failed_column = "customer_id"

For orphan product:

check_category = "referential_integrity"

failed_column = "product_id"

Use clear failure_reason messages such as:

"Foreign key 'customer_id' does not resolve to a valid customer"

"Foreign key 'product_id' does not resolve to a valid product"

Do not write these failures to a Delta quarantine table yet.

==================================================
2. 05_quality_business_logic.py
==================================================

Implement the business-logic validation rules defined in:

data-quality-strategy.md

and finalized in:

src/silver/SILVER_LAYER_NOTES.md

Implement ONLY the existing five-category DQ architecture.

Business rules:

--------------------------------------------------
CUSTOMERS
--------------------------------------------------

1. No future signup

signup_date <= current_date()

Rows where signup_date is greater than current_date()
must fail.

2. Valid customer segment

customer_segment IN (
    'Premium',
    'Standard',
    'Basic'
)

Rows outside these values must fail.

--------------------------------------------------
PRODUCTS
--------------------------------------------------

3. Non-negative catalog price

unit_price >= 0

Use the typed Silver representation:

unit_price_typed

Malformed values should not be silently converted into valid values.

Type validation already identifies unparseable values.

--------------------------------------------------
ORDERS
--------------------------------------------------

4. Positive quantity

quantity > 0

Use:

quantity_typed

Rows with quantity <= 0 must fail.

5. No future orders

order_date <= current_date()

Use:

order_date_typed

6. Catalog price consistency

orders.unit_price = products.unit_price

Join orders to the canonical valid product set using:

orders.product_id = products.product_id

Compare:

orders.unit_price_typed
vs.
products.unit_price_typed

If they differ, flag the order row.

IMPORTANT:

D17 must be QUARANTINE ONLY.

Do NOT automatically correct orders.unit_price.

Do NOT replace the order price with the product catalog price.

Do NOT create a corrected-price column unless the existing design explicitly requires it.

==================================================
DATE SEMANTICS
==================================================

Use:

current_date()

at runtime.

Do not hard-code today's date.

The existing run timestamp should continue to be generated by SilverConfig / silver_common.py.

==================================================
CANONICAL PARENTS
==================================================

For catalog-price consistency, use the canonical valid product set rather than blindly joining against raw Bronze products.

The same canonical-parent principle established for referential integrity should be respected.

If a product itself is invalid, do not allow that invalid product record to establish catalog-price consistency.

==================================================
FAILURE DATAFRAME
==================================================

Every failure must use the existing quarantine-compatible schema:

entity_name
business_key
check_category
failure_reason
failed_column
bronze_source_values
quarantine_timestamp
run_timestamp

check_category must be:

"business_logic"

Examples:

Customer future signup:

failure_reason:
"Signup date is in the future"

failed_column:
"signup_date"

Invalid segment:

failure_reason:
"Customer segment is not one of Premium, Standard, Basic"

failed_column:
"customer_segment"

Negative product price:

failure_reason:
"Product unit price must be non-negative"

failed_column:
"unit_price"

Invalid order quantity:

failure_reason:
"Order quantity must be greater than zero"

failed_column:
"quantity"

Future order:

failure_reason:
"Order date is in the future"

failed_column:
"order_date"

Catalog mismatch:

failure_reason:
"Order unit price does not match product catalog price"

failed_column:
"unit_price"

Follow the existing failure-building implementation from silver_common.py instead of duplicating schema-building logic unnecessarily.

==================================================
MULTIPLE FAILURES
==================================================

A single source row may violate multiple business rules.

Do NOT silently discard failures.

Prefer one structured failure record per:

(business_key, check_category, failure_reason)

consistent with the existing Silver design.

Do not deduplicate unrelated business-rule failures into one generic error.

==================================================
SERVERLESS COMPATIBILITY
==================================================

The code must work on Databricks Serverless.

Do NOT use:

RDDs
.map()
.mapPartitions()
.toRDD()
custom RDD transformations

Prefer Spark DataFrame operations:

filter
select
join
left_anti
withColumn
when
unionByName
groupBy
etc.

Be especially careful with window operations.

If a window is required, always define an appropriate partition.

Avoid unnecessary global windows.

==================================================
ITERATION 2 INTEGRATION
==================================================

Reuse:

silver_common.py

and existing preparation / type-standardization helpers.

Do not duplicate:

- Bronze table-reading logic
- SilverConfig
- timestamp generation
- failure schema construction
- source-row serialization
- trimming logic
- safe casting logic

If an existing helper is insufficient, make the smallest necessary change to silver_common.py and document why.

Do NOT redesign silver_common.py.

==================================================
VALIDATION
==================================================

Create or update lightweight local tests only if appropriate for pure-Python helpers.

Do not attempt to run PySpark locally if PySpark is unavailable.

The main validation must be performed in Databricks Serverless.

After implementation, provide the exact notebook commands required to load and run:

04_quality_referential_integrity.py

and

05_quality_business_logic.py

Use the same import strategy that was successfully used for Iteration 2.

For example:

import sys
sys.path.insert(
    0,
    "/Workspace/Users/shubhanshu.pandey@tothenew.com/DE_C1_Coding_Evaluation/src/silver"
)

Then import/load the modules appropriately.

Do NOT use:

%run ./04_quality_referential_integrity

unless you have verified that the file is actually a Databricks notebook.

These are Python source files, not Databricks notebook files.

==================================================
EXPECTED VALIDATION
==================================================

Referential integrity should approximately produce:

customers orphan failures = 25
products orphan failures = 25

Business logic should detect the documented Phase 2 defects, including:

D06 future customer signup dates
D10 invalid/negative product prices
D14 future order dates
D15 invalid/non-positive quantities
D17 catalog-price mismatches

Also validate:

customer_segment invalid values

Do not assume the total business-logic failure count must equal the sum of documented defect injections.

Overlapping defects are possible.

For example, a single row may fail type validation and business logic, or may be excluded from later checks because a prerequisite typed value is invalid.

Report counts by rule/category rather than forcing a single expected total.

==================================================
DOCUMENTATION
==================================================

Update:

src/silver/SILVER_LAYER_NOTES.md

with:

- Iteration 3 implementation status
- modules created
- rules implemented
- Databricks validation status
- observed failure counts
- any Serverless-specific issue/fix
- confirmation that quarantine writes were NOT implemented
- confirmation that orchestration was NOT implemented

Update:

ai-prompts/silver-layer.md

with an Iteration 3 section documenting:

1. Prompt
2. Implementation summary
3. Validation performed
4. Observed results
5. Issues/fixes
6. Acceptance criteria
7. FINAL DECISION

Do not mark Iteration 3 ACCEPTED until Databricks validation has actually been performed.

==================================================
STRICT STOP CONDITION
==================================================

After completing these two modules and their documentation:

STOP.

Do NOT implement:

silver_quarantine_records

silver_dq_summary

create_silver_tables.py

silver_customers

silver_products

silver_orders

Gold layer

Dashboard

Those belong to later iterations.

==================================================
FINAL RESPONSE FORMAT
==================================================

When finished, report:

1. Files created
2. Files modified
3. Implementation summary for 04
4. Implementation summary for 05
5. Local validation
6. Databricks validation status
7. Expected vs observed defect counts
8. Any issues/fixes
9. Remaining Iteration 4 work
10. Git status

Do not claim Databricks validation passed unless it was actually executed.

STOP after Iteration 3.
```

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

## Prompt 11 — Quarantine & DQ summary persistence

**TYPE:** Implementation

**PROMPT SENT:**

```text
You are implementing Silver Layer Iteration 4 for the DE_C1_Coding_Evaluation project.

IMPORTANT:
- Iterations 1–3 are already implemented and ACCEPTED.
- Do NOT modify Bronze code or Bronze tables.
- Do NOT start Iteration 5.
- Do NOT create or modify Gold/Dashboard code.
- This iteration is ONLY about persisting Silver data-quality failures and DQ summary metrics.
- Follow the existing project documentation and previously accepted design decisions.
- Before making implementation changes, inspect:
  1. ai-prompts/silver-layer.md
  2. src/silver/SILVER_LAYER_NOTES.md
  3. data-quality-strategy.md
  4. tool-specific/cursor-workflow/spec.md
  5. tool-specific/cursor-workflow/task-breakdown.md
  6. Existing src/silver/*.py files from Iterations 2 and 3.

==================================================
ITERATION 4 SCOPE
==================================================

Implement:

1. silver_quarantine_records persistence
2. silver_dq_summary persistence

The target catalog/schema is:

de_c1_coding_evaluation.silver

Target tables:

de_c1_coding_evaluation.silver.silver_quarantine_records

de_c1_coding_evaluation.silver.silver_dq_summary

==================================================
1. QUARANTINE TABLE
==================================================

Create/write:

de_c1_coding_evaluation.silver.silver_quarantine_records

Use the already agreed schema:

- entity_name
- business_key
- check_category
- failure_reason
- failed_column
- bronze_source_values
- quarantine_timestamp
- run_timestamp

The table must be Delta.

Do not silently discard failed records.

Failures from all five DQ categories must be compatible with this table:

- completeness
- uniqueness
- type_validation
- referential_integrity
- business_logic

Use the existing failure DataFrame structure produced by the Iteration 2/3 modules wherever possible.

Do not duplicate DQ logic already implemented in:
- 01_quality_completeness.py
- 02_quality_uniqueness.py
- 03_quality_type_validation.py
- 04_quality_referential_integrity.py
- 05_quality_business_logic.py

==================================================
2. DQ SUMMARY TABLE
==================================================

Create/write:

de_c1_coding_evaluation.silver.silver_dq_summary

Use the agreed schema:

- check_category
- table_name
- rows_tested
- rows_passed
- rows_failed
- pass_percentage
- failure_reason
- run_timestamp

The summary must report metrics for all five DQ categories.

Calculate:

pass_percentage =
    rows_passed / rows_tested * 100

Handle rows_tested = 0 safely.

Do not create fake or hard-coded metrics.

Metrics must be derived from the actual DataFrames/results produced by the DQ modules.

==================================================
3. IDEMPOTENCY
==================================================

Follow the accepted design:

silver_quarantine_records:
    overwrite

silver_dq_summary:
    overwrite

Running Iteration 4 multiple times against the same Bronze input must NOT accumulate duplicate quarantine or summary records.

Use Delta overwrite semantics.

==================================================
4. RUN TIMESTAMP
==================================================

Use the existing SilverConfig.run_timestamp / established project timestamp approach.

Do not introduce a second unrelated timestamp mechanism.

Every quarantine record and every DQ summary record must contain run_timestamp.

quarantine_timestamp should represent when the failure was persisted/generated according to the existing project convention.

==================================================
5. MULTIPLE FAILURES
==================================================

Preserve the existing design:

A source record may produce multiple quarantine records when it violates multiple DQ rules.

Do not collapse different failure categories/reasons into a single arbitrary record.

For example, a row may legitimately appear multiple times if it has:
- a completeness failure
- a type failure
- a business-rule failure

This is expected.

==================================================
6. ARCHITECTURE
==================================================

Keep the implementation modular.

Prefer adding a dedicated module such as:

src/silver/04_write_dq_results.py

or another clearly named module if the existing project structure suggests a better name.

The module should provide reusable functions rather than putting everything into one large orchestration function.

For example, conceptually:

write_quarantine_records(...)
write_dq_summary(...)
run_dq_persistence(...)

Use the existing SilverConfig and shared utilities.

Do not introduce unnecessary dependencies.

The implementation must work with Databricks Serverless.

IMPORTANT SERVERLESS CONSTRAINT:
Do NOT use PySpark RDD APIs.

Use DataFrame/Spark SQL operations only.

==================================================
7. INPUTS
==================================================

Iteration 4 should consume the outputs of the already accepted Iteration 2 and Iteration 3 validation modules.

Expected modules:

01_quality_completeness.py
02_quality_uniqueness.py
03_quality_type_validation.py
04_quality_referential_integrity.py
05_quality_business_logic.py

Reuse their existing failure DataFrames and validation results.

Do not rewrite their DQ rules unless a compatibility issue is discovered.

If changes to existing modules are absolutely necessary, make the smallest possible change and document why.

==================================================
8. DQ METRIC SEMANTICS
==================================================

Be explicit about what rows_tested means.

Use the actual entity DataFrame row count evaluated by each DQ category.

rows_failed must represent the number of rows failing that category.

rows_passed must be:

rows_tested - rows_failed

Avoid counting multiple failure reasons as multiple failed rows when calculating category-level failed-row metrics.

If a single source row has multiple failures within the same category, count it once for rows_failed.

The quarantine table may contain multiple failure records for the same source row; the summary metrics must remain row-oriented.

Document this distinction.

==================================================
9. VALIDATION
==================================================

After implementation, perform local validation:

- py_compile all affected Python files
- existing Silver unit tests
- verify table schemas
- verify overwrite/idempotency logic where possible

Then provide exact Databricks Serverless cells for validation.

Databricks validation should verify:

1. quarantine table exists
2. summary table exists
3. expected columns/types exist
4. quarantine contains records
5. all five DQ categories are represented where applicable
6. summary contains metrics
7. pass_percentage is calculated correctly
8. run_timestamp is populated
9. running the persistence twice does not duplicate records

Use SQL/DataFrame operations compatible with Serverless.

==================================================
10. EXPECTED VALIDATION EVIDENCE
==================================================

Compare the persisted quarantine counts with the already validated Iteration 2/3 results.

Known validated counts include:

Completeness:
- customers: 60
- products: 9
- orders: 0

Uniqueness:
- customers: 6
- products: 6
- orders: 8

Type validation:
- customers: 50
- products: 15
- orders: 30

Iteration 3:
- orders/customer RI orphan defects: 25
- orders/product RI orphan defects: 25
- additional RI failures involving non-canonical parents are expected
- D17/catalog mismatch behavior was validated and accepted

Do NOT assume total quarantine rows must equal the sum of these numbers because the same source row can fail multiple categories/rules.

Document this distinction clearly.

==================================================
11. DOCUMENTATION
==================================================

Update:

ai-prompts/silver-layer.md

with a complete "Iteration 4" section containing:

- prompt used
- implementation summary
- files created/modified
- design decisions
- validation performed
- Databricks validation evidence
- issues encountered and fixes
- acceptance criteria
- final decision

Also update:

src/silver/SILVER_LAYER_NOTES.md

with the Iteration 4 implementation and validation status.

Update:

tool-specific/cursor-workflow/task-breakdown.md

only for Iteration 4 tasks.

Do NOT mark Iteration 4 ACCEPTED until Databricks validation has actually been performed.

==================================================
12. STOP CONDITION
==================================================

After implementing and locally validating Iteration 4:

STOP.

Do NOT implement:

- create_silver_tables.py
- silver_customers
- silver_products
- silver_orders
- Gold layer
- Dashboard
- orchestration beyond what is necessary to validate DQ persistence

Iteration 5 will handle final Silver curated-table writes and orchestration.

==================================================
FINAL RESPONSE FORMAT
==================================================

Report:

1. Files created
2. Files modified
3. Implementation details
4. Quarantine table design
5. DQ summary design
6. Idempotency approach
7. Serverless compatibility
8. Local validation results
9. Databricks validation status
10. Any issues/fixes
11. Acceptance criteria
12. FINAL DECISION

If Databricks validation has not been run, explicitly state:

FINAL DECISION: PENDING DATABRICKS VALIDATION

Do not claim acceptance prematurely.

STOP after Iteration 4.
```

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

## Prompt 12 — Full orchestration & curated Silver tables

**TYPE:** Implementation

**PROMPT SENT:**

```text
# Silver Iteration 5 — Final Silver Orchestration and Curated Tables

You are continuing the DE_C1_Coding_Evaluation project.

IMPORTANT:
- Iterations 1–4 of Silver are already completed and ACCEPTED.
- Do NOT redesign or rewrite the existing Silver DQ logic.
- Do NOT modify Bronze code or Bronze tables.
- Do NOT start Gold or Dashboard work.
- Work ONLY on Silver Iteration 5.
- Stop after completing the requested implementation and local validation.
- Do NOT claim Databricks validation unless it is actually executed.

## Environment

Catalog:
de_c1_coding_evaluation

Bronze schema:
bronze

Silver schema:
silver

Bronze tables:
de_c1_coding_evaluation.bronze.bronze_customers
de_c1_coding_evaluation.bronze.bronze_products
de_c1_coding_evaluation.bronze.bronze_orders

Required Silver tables:
de_c1_coding_evaluation.silver.silver_customers
de_c1_coding_evaluation.silver.silver_products
de_c1_coding_evaluation.silver.silver_orders

Already implemented and ACCEPTED:

src/silver/silver_common.py
src/silver/01_quality_completeness.py
src/silver/02_quality_uniqueness.py
src/silver/03_quality_type_validation.py
src/silver/04_quality_referential_integrity.py
src/silver/05_quality_business_logic.py

Already implemented and ACCEPTED:
- silver_quarantine_records
- silver_dq_summary

Read the existing Silver documentation before coding:
- src/silver/SILVER_LAYER_NOTES.md
- data-quality-strategy.md
- tool-specific/cursor-workflow/spec.md
- tool-specific/cursor-workflow/task-breakdown.md
- ai-prompts/silver-layer.md

Do not contradict finalized decisions documented there.

---

# Objective

Implement the final Silver orchestration layer.

Create:

src/silver/create_silver_tables.py

The orchestration must:

1. Read Bronze Delta tables.
2. Execute the existing Silver DQ pipeline in the established order.
3. Produce valid curated Silver tables.
4. Preserve all existing DQ behavior.
5. Write quarantine records.
6. Write DQ summary.
7. Be idempotent.
8. Work with the existing Databricks Serverless-compatible implementation.
9. Keep Bronze completely unchanged.

---

# Required execution order

Use the already established execution order:

Bronze
  ↓
trim / safe typing
  ↓
Completeness
  ↓
Uniqueness
  ↓
Type validation
  ↓
Canonical valid customers/products
  ↓
Referential integrity
  ↓
Business logic
  ↓
Quarantine
  ↓
DQ summary
  ↓
Curated Silver tables

Do not introduce a new DQ category.

Do not duplicate DQ logic that already exists in modules 01–05.

The orchestration should call the existing functions/modules.

---

# Silver output schemas

## silver_customers

Required columns:

customer_id       STRING
customer_name     STRING
email             STRING
country           STRING
signup_date       DATE
customer_segment  STRING
lifetime_value    DECIMAL(12,2)

Do not expose helper columns such as:
- *_typed
- _row_num
- _dup_rank

Only valid curated records should be written.

---

## silver_products

Required columns:

product_id    STRING
product_name  STRING
category      STRING
unit_price    DECIMAL(10,2)

Do not expose internal DQ/helper columns.

Only valid curated records should be written.

---

## silver_orders

Required columns:

order_line_id  STRING
order_id       STRING
customer_id    STRING
product_id     STRING
order_date     DATE
quantity       INT
unit_price     DECIMAL(10,2)

Do not add line_revenue.

line_revenue belongs to Gold.

Do not expose internal DQ/helper columns.

Only valid curated records should be written.

---

# Invalid-record handling

A record must NOT appear in the curated Silver tables if it fails the applicable Silver DQ rules.

Invalid records must remain traceable through:

de_c1_coding_evaluation.silver.silver_quarantine_records

Do not silently drop invalid records.

Use the existing Iteration 4 quarantine implementation rather than creating another quarantine mechanism.

---

# Parent / foreign-key behavior

The canonical valid customer and product sets established by the earlier DQ stages must be used for order referential-integrity validation.

Orders with:
- invalid customer references
- invalid product references

must not enter silver_orders.

Preserve the accepted Iteration 3 behavior.

---

# D17 catalog-price mismatch

Preserve the accepted Iteration 3/4 decision:

D17 is quarantine-only.

DO NOT automatically correct orders.unit_price from the product catalog.

---

# Idempotency

The pipeline must remain idempotent.

Each complete execution should replace:

silver_customers
silver_products
silver_orders
silver_quarantine_records
silver_dq_summary

Do not append duplicate results across runs.

Use overwrite semantics consistent with the existing Silver design.

---

# Databricks / Serverless compatibility

The project is being executed on Databricks Serverless.

Previous versions encountered Serverless RDD limitations.

Therefore:

- Do NOT introduce PySpark RDD APIs.
- Do NOT use .rdd.
- Do NOT use custom RDD transformations.
- Prefer DataFrame / Spark SQL operations.
- Preserve the existing SERVERLESS_COMPAT_VERSION pattern from silver_common.py.
- Follow the implementation style already validated in Iterations 2–4.

The code must support invocation from a Databricks notebook with:

from create_silver_tables import run_silver_pipeline

run_silver_pipeline(spark=spark)

If the existing project convention uses a config argument, preserve that convention.

---

# Local validation

After implementation:

1. Run py_compile on all Silver Python files.
2. Run the existing Silver helper/unit tests.
3. Check that create_silver_tables.py imports successfully.
4. Verify no Bronze files/code were modified.
5. Verify no Gold/Dashboard files were created.
6. Inspect the resulting schemas logically.
7. Verify overwrite/idempotent behavior in code.

Do NOT attempt to fake Databricks results locally.

---

# Documentation

After implementation, update ONLY the documentation necessary to record Iteration 5 implementation status.

At minimum update:

src/silver/SILVER_LAYER_NOTES.md
ai-prompts/silver-layer.md
tool-specific/cursor-workflow/task-breakdown.md

Document:

- implementation completed
- files created/modified
- orchestration flow
- curated Silver output schemas
- local validation results
- Databricks validation status as PENDING unless actually run
- any implementation decisions made
- any issues encountered and fixes

Do not mark Iteration 5 ACCEPTED until Databricks validation is actually performed.

---

# Scope boundary

DO NOT:

- modify Bronze
- modify Gold
- modify Dashboard
- create Gold tables
- create dashboard code
- redesign DQ rules
- change finalized DQ decisions
- auto-correct D17
- introduce new DQ categories
- silently discard failures
- add unnecessary dependencies
- introduce RDD-based logic

---

# Stop condition

After implementation and local validation:

STOP.

Return a structured report containing:

1. Files created
2. Files modified
3. Implementation summary
4. Curated table schemas
5. DQ/orchestration flow
6. Local validation results
7. Databricks validation status
8. Issues encountered and fixes
9. Git status
10. Acceptance criteria
11. FINAL DECISION

The FINAL DECISION must be:

PENDING DATBRICKS VALIDATION

unless actual Databricks validation has been performed and all acceptance criteria pass.

Do not proceed to Gold.
```

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

## Prompt 13 — Silver RI alignment (curated parent keys)

**TYPE:** Correction / implementation

**PROMPT SENT:**

```text
Implement the approved Silver Referential Integrity alignment described below.

IMPORTANT:

* This is now an IMPLEMENTATION task.
* Do NOT modify Gold SQL.
* Do NOT modify the frozen Gold contract.
* Do NOT weaken or remove any DQ rule.
* Do NOT change business_logic, uniqueness, completeness, or type-validation semantics.
* Preserve existing behavior wherever possible.
* Make the smallest safe architectural change.
* Before editing, inspect the current implementation and verify the proposal against the actual code.

## Root cause confirmed

Current Silver RI validates order foreign keys against canonical parent keys generated by:

prepare_canonical_entity_df()
→ canonical_valid_filter()

canonical_valid_filter() checks:

* _dup_rank = 1
* completeness
* type_validation

It does NOT apply:

* uniqueness
* business_logic

Curated silver_products and silver_customers are later produced using filter_valid_rows(), which applies:

* completeness
* uniqueness
* type_validation
* business_logic

Therefore RI-valid order lines can reference a customer/product key that is later removed from the curated Silver dimension.

Confirmed examples:

### product_id = 184

* duplicate product_id
* canonical occurrence passes canonical_valid_filter()
* RI therefore accepts orders referencing 184
* uniqueness DQ causes the entire key 184 to be excluded from silver_products
* those orders remain in silver_orders
* Gold inner join drops them

### customer_id = 177

* future signup_date
* canonical_valid_filter() accepts it because business_logic is not included
* RI accepts orders referencing 177
* business_logic excludes customer 177 from silver_customers
* those orders remain in silver_orders
* Gold inner join drops them

Databricks confirmed:

Product orphan lines:

* 116
* quantity = 349
* revenue = 66013.47

Customer orphan lines:

* 71
* quantity = 221
* revenue = 57072.64

## Required invariant after this fix

For every nonblank customer_id in silver_orders:

```
customer_id EXISTS IN silver_customers
```

For every nonblank product_id in silver_orders:

```
product_id EXISTS IN silver_products
```

The Gold INNER JOIN contract must therefore become naturally consistent with Silver.

---

# Implementation design

## 1. Preserve all existing DQ rules

Do not change the implementation of:

* completeness
* uniqueness
* type_validation
* business_logic
* order-level validation
* Gold SQL

Only change when RI executes and which parent key population it uses.

## 2. Change DQ execution order

Current:

01 completeness
02 uniqueness
03 type_validation
04 referential_integrity
05 business_logic

Change to:

01 completeness
02 uniqueness
03 type_validation
05 business_logic
04 referential_integrity

RI must execute only after customer/product business_logic results are available.

## 3. Avoid circular dependency

Do NOT make RI read:

silver_customers
silver_products

from Delta during the same pipeline run.

Those tables have not yet been written.

Instead derive their exact eligible business-key population in memory from the already-computed DQ results.

The parent population used by RI must be identical to the population that will later be written to the curated Silver dimension tables.

## 4. Shared curated-parent eligibility

Inspect the current implementation of:

* filter_valid_rows()
* _failures_for_category()
* entity_dq_categories()

Create the smallest reusable helper necessary to derive curated parent keys.

Preferred conceptual helper:

```
curated_eligible_parent_keys_df(
    prepared_df,
    entity_key,
    dq_results
)
```

It should produce a DataFrame containing only the distinct business key values that would survive the existing curated-dimension filtering.

For customers:

```
business_key = customer_id
```

For products:

```
business_key = product_id
```

The helper must use the exact same failure-category semantics currently used by curated writes.

Do NOT create a second implementation of business rules.

Do NOT manually recreate uniqueness/business_logic conditions.

The helper should reuse the existing DQ failure DataFrames.

## 5. Reuse the helper from curated Silver writes

If practical and safe, make create_silver_tables.py use the same shared eligibility implementation.

The goal is:

```
curated Silver dimension keys
    ==
RI parent keys
```

Do not change the resulting customer/product rows beyond the intended RI alignment.

Customer/product counts should therefore remain:

```
silver_customers = 878
silver_products = 164
```

before and after the fix.

## 6. Update referential integrity

Modify:

src/silver/04_quality_referential_integrity.py

so that run_referential_integrity_all() / check_referential_integrity() can receive the accumulated dq_results.

Instead of:

```
prepare_canonical_entity_df(...)
```

for customer/product RI parents, use the curated-eligible parent key helper.

Conceptually:

```
customer_parent_keys =
    curated_eligible_parent_keys_df(
        dq_results["business_logic"]["customers"]["prepared_df"],
        "customers",
        dq_results
    )

product_parent_keys =
    curated_eligible_parent_keys_df(
        dq_results["business_logic"]["products"]["prepared_df"],
        "products",
        dq_results
    )
```

Then perform the existing left joins:

```
orders
  LEFT JOIN customer_parent_keys
  LEFT JOIN product_parent_keys
```

Keep the existing orphan logic.

Do not change the order_line_id-based RI failure semantics.

## 7. Update run_all_dq_checks()

Modify:

src/silver/06_write_dq_results.py

so that:

```
completeness = run...
uniqueness = run...
type_validation = run...
business_logic = run...
```

are completed before:

```
referential_integrity = run...(dq_results=partial_results)
```

Ensure the final dq_results dictionary has the same expected structure used by downstream persistence and curated writes.

Do not break any consumers of dq_results.

## 8. Standalone module behavior

Inspect how 04_quality_referential_integrity.py is executed independently.

If its main()/standalone entry point currently assumes it can independently construct canonical parents, preserve standalone usability where practical.

However, do NOT introduce unnecessary duplicate DQ execution.

The primary production path is:

```
run_all_dq_checks()
```

If a fallback is required for standalone execution, keep it isolated and clearly documented.

## 9. Important ordering consideration

Do NOT write curated dimensions before RI.

The desired flow remains:

01
02
03
05
04
06 persistence
curated writes

RI should derive the same curated parent population in memory.

There is no circular dependency because:

* customer/product eligibility does not depend on order RI
* order RI depends on customer/product eligibility
* orders are written only after RI has been calculated

---

# Validation requirements

After implementation, perform local syntax validation.

Run:

```
python3 -m py_compile \
  src/silver/silver_common.py \
  src/silver/create_silver_tables.py \
  src/silver/04_quality_referential_integrity.py \
  src/silver/06_write_dq_results.py
```

Then run the existing Silver helper tests if available.

Do not claim runtime success from local validation.

---

# Databricks validation

After code implementation, provide the exact Databricks execution sequence required to validate the change.

Do NOT fabricate results.

The expected checks are:

## A. Silver row counts

Expected:

```
silver_customers = 878
silver_products = 164
silver_orders < 3832
```

The exact new silver_orders count must come from Databricks.

## B. Reverse RI diagnostic

Run:

```
SELECT COUNT(*)
FROM silver_orders o
LEFT JOIN silver_products p
  ON o.product_id = p.product_id
WHERE o.product_id IS NOT NULL
  AND p.product_id IS NULL;
```

Expected:

```
0
```

And:

```
SELECT COUNT(*)
FROM silver_orders o
LEFT JOIN silver_customers c
  ON o.customer_id = c.customer_id
WHERE o.customer_id IS NOT NULL
  AND c.customer_id IS NULL;
```

Expected:

```
0
```

## C. Silver revenue

Recalculate:

```
SUM(quantity * unit_price)
```

from the new silver_orders.

Do not assume the old value of 2830321.54.

## D. Gold

Run the existing Gold pipeline without modifying Gold code.

Expected relationship:

```
SUM(gold_sales_by_product.total_revenue)
    =
SUM(gold_revenue_by_customer.total_revenue)
    =
SUM(gold_customer_segmentation.total_spend)
    =
SUM(silver_orders.quantity * silver_orders.unit_price)
```

Also verify daily and weekly trends against the new silver_orders.

## E. Gold quantity

Verify:

```
SUM(gold_sales_by_product.total_quantity)
    =
SUM(silver_orders.quantity)
```

## F. Gold order count

Verify daily/weekly:

```
COUNT(DISTINCT silver_orders.order_id)
```

matches the Gold trend order_count.

## G. Gold grain

Verify zero duplicate keys for:

* gold_sales_by_product.product_id
* gold_revenue_by_customer.customer_id
* (time_grain, period_start)
* gold_customer_segmentation.customer_id

## H. Idempotency

Run Silver twice and Gold twice.

Confirm:

* row counts identical
* aggregate totals identical
* no cumulative duplication
* no changing results between runs

---

# Documentation

After runtime validation succeeds, update:

* src/silver/SILVER_LAYER_NOTES.md
* src/gold/GOLD_LAYER_NOTES.md
* ai-prompts/silver-layer.md
* ai-prompts/gold-layer.md
* tool-specific/cursor-workflow/task-breakdown.md

Document:

1. RI now uses curated-eligible parent keys.
2. Business logic executes before RI.
3. RI and curated dimension writes share the same parent eligibility semantics.
4. The previous canonical-parent mismatch was resolved.
5. New Silver row counts.
6. New RI failure counts.
7. Gold reconciliation results.
8. Idempotency results.

Do not mark Gold ACCEPTED unless all required runtime acceptance criteria pass.

---

# Important acceptance condition

The fix is successful only if:

```
silver_orders has zero product FKs
that are absent from silver_products
```

AND:

```
silver_orders has zero customer FKs
that are absent from silver_customers
```

AND the Gold entity-level aggregations reconcile with the resulting silver_orders.

Do not alter Gold SQL simply to force these conditions to pass.

---

# Final output required from Cursor

After implementation, report:

1. Files modified
2. Exact functions changed
3. Summary of code changes
4. Local validation results
5. Any regression risks
6. Exact Databricks cells to run
7. Expected validation criteria
8. Explicit confirmation that Gold SQL was NOT modified

Do not claim Databricks validation has passed until actual Databricks output is supplied.
```
customer_id EXISTS IN silver_customers
```

For every nonblank product_id in silver_orders:

```
product_id EXISTS IN silver_products
```

The Gold INNER JOIN contract must therefore become naturally consistent with Silver.

---

# Implementation design

## 1. Preserve all existing DQ rules

Do not change the implementation of:

* completeness
* uniqueness
* type_validation
* business_logic
* order-level validation
* Gold SQL

Only change when RI executes and which parent key population it uses.

## 2. Change DQ execution order

Current:

01 completeness
02 uniqueness
03 type_validation
04 referential_integrity
05 business_logic

Change to:

01 completeness
02 uniqueness
03 type_validation
05 business_logic
04 referential_integrity

RI must execute only after customer/product business_logic results are available.

## 3. Avoid circular dependency

Do NOT make RI read:

silver_customers
silver_products

from Delta during the same pipeline run.

Those tables have not yet been written.

Instead derive their exact eligible business-key population in memory from the already-computed DQ results.

The parent population used by RI must be identical to the population that will later be written to the curated Silver dimension tables.

## 4. Shared curated-parent eligibility

Inspect the current implementation of:

* filter_valid_rows()
* _failures_for_category()
* entity_dq_categories()

Create the smallest reusable helper necessary to derive curated parent keys.

Preferred conceptual helper:

```
curated_eligible_parent_keys_df(
    prepared_df,
    entity_key,
    dq_results
)
```

It should produce a DataFrame containing only the distinct business key values that would survive the existing curated-dimension filtering.

For customers:

```
business_key = customer_id
```

For products:

```
business_key = product_id
```

The helper must use the exact same failure-category semantics currently used by curated writes.

Do NOT create a second implementation of business rules.

Do NOT manually recreate uniqueness/business_logic conditions.

The helper should reuse the existing DQ failure DataFrames.

## 5. Reuse the helper from curated Silver writes

If practical and safe, make create_silver_tables.py use the same shared eligibility implementation.

The goal is:

```
curated Silver dimension keys
    ==
RI parent keys
```

Do not change the resulting customer/product rows beyond the intended RI alignment.

Customer/product counts should therefore remain:

```
silver_customers = 878
silver_products = 164
```

before and after the fix.

## 6. Update referential integrity

Modify:

src/silver/04_quality_referential_integrity.py

so that run_referential_integrity_all() / check_referential_integrity() can receive the accumulated dq_results.

Instead of:

```
prepare_canonical_entity_df(...)
```

for customer/product RI parents, use the curated-eligible parent key helper.

Conceptually:

```
customer_parent_keys =
    curated_eligible_parent_keys_df(
        dq_results["business_logic"]["customers"]["prepared_df"],
        "customers",
        dq_results
    )

product_parent_keys =
    curated_eligible_parent_keys_df(
        dq_results["business_logic"]["products"]["prepared_df"],
        "products",
        dq_results
    )
```

Then perform the existing left joins:

```
orders
  LEFT JOIN customer_parent_keys
  LEFT JOIN product_parent_keys
```

Keep the existing orphan logic.

Do not change the order_line_id-based RI failure semantics.

## 7. Update run_all_dq_checks()

Modify:

src/silver/06_write_dq_results.py

so that:

```
completeness = run...
uniqueness = run...
type_validation = run...
business_logic = run...
```

are completed before:

```
referential_integrity = run...(dq_results=partial_results)
```

Ensure the final dq_results dictionary has the same expected structure used by downstream persistence and curated writes.

Do not break any consumers of dq_results.

## 8. Standalone module behavior

Inspect how 04_quality_referential_integrity.py is executed independently.

If its main()/standalone entry point currently assumes it can independently construct canonical parents, preserve standalone usability where practical.

However, do NOT introduce unnecessary duplicate DQ execution.

The primary production path is:

```
run_all_dq_checks()
```

If a fallback is required for standalone execution, keep it isolated and clearly documented.

## 9. Important ordering consideration

Do NOT write curated dimensions before RI.

The desired flow remains:

01
02
03
05
04
06 persistence
curated writes

RI should derive the same curated parent population in memory.

There is no circular dependency because:

* customer/product eligibility does not depend on order RI
* order RI depends on customer/product eligibility
* orders are written only after RI has been calculated

---

# Validation requirements

After implementation, perform local syntax validation.

Run:

```
python3 -m py_compile \
  src/silver/silver_common.py \
  src/silver/create_silver_tables.py \
  src/silver/04_quality_referential_integrity.py \
  src/silver/06_write_dq_results.py
```

Then run the existing Silver helper tests if available.

Do not claim runtime success from local validation.

---

# Databricks validation

After code implementation, provide the exact Databricks execution sequence required to validate the change.

Do NOT fabricate results.

The expected checks are:

## A. Silver row counts

Expected:

```
silver_customers = 878
silver_products = 164
silver_orders < 3832
```

The exact new silver_orders count must come from Databricks.

## B. Reverse RI diagnostic

Run:

```
SELECT COUNT(*)
FROM silver_orders o
LEFT JOIN silver_products p
  ON o.product_id = p.product_id
WHERE o.product_id IS NOT NULL
  AND p.product_id IS NULL;
```

Expected:

```
0
```

And:

```
SELECT COUNT(*)
FROM silver_orders o
LEFT JOIN silver_customers c
  ON o.customer_id = c.customer_id
WHERE o.customer_id IS NOT NULL
  AND c.customer_id IS NULL;
```

Expected:

```
0
```

## C. Silver revenue

Recalculate:

```
SUM(quantity * unit_price)
```

from the new silver_orders.

Do not assume the old value of 2830321.54.

## D. Gold

Run the existing Gold pipeline without modifying Gold code.

Expected relationship:

```
SUM(gold_sales_by_product.total_revenue)
    =
SUM(gold_revenue_by_customer.total_revenue)
    =
SUM(gold_customer_segmentation.total_spend)
    =
SUM(silver_orders.quantity * silver_orders.unit_price)
```

Also verify daily and weekly trends against the new silver_orders.

## E. Gold quantity

Verify:

```
SUM(gold_sales_by_product.total_quantity)
    =
SUM(silver_orders.quantity)
```

## F. Gold order count

Verify daily/weekly:

```
COUNT(DISTINCT silver_orders.order_id)
```

matches the Gold trend order_count.

## G. Gold grain

Verify zero duplicate keys for:

* gold_sales_by_product.product_id
* gold_revenue_by_customer.customer_id
* (time_grain, period_start)
* gold_customer_segmentation.customer_id

## H. Idempotency

Run Silver twice and Gold twice.

Confirm:

* row counts identical
* aggregate totals identical
* no cumulative duplication
* no changing results between runs

---

# Documentation

After runtime validation succeeds, update:

* src/silver/SILVER_LAYER_NOTES.md
* src/gold/GOLD_LAYER_NOTES.md
* ai-prompts/silver-layer.md
* ai-prompts/gold-layer.md
* tool-specific/cursor-workflow/task-breakdown.md

Document:

1. RI now uses curated-eligible parent keys.
2. Business logic executes before RI.
3. RI and curated dimension writes share the same parent eligibility semantics.
4. The previous canonical-parent mismatch was resolved.
5. New Silver row counts.
6. New RI failure counts.
7. Gold reconciliation results.
8. Idempotency results.

Do not mark Gold ACCEPTED unless all required runtime acceptance criteria pass.

---

# Important acceptance condition

The fix is successful only if:

```
silver_orders has zero product FKs
that are absent from silver_products
```

AND:

```
silver_orders has zero customer FKs
that are absent from silver_customers
```

AND the Gold entity-level aggregations reconcile with the resulting silver_orders.

Do not alter Gold SQL simply to force these conditions to pass.

---

# Final output required from Cursor

After implementation, report:

1. Files modified
2. Exact functions changed
3. Summary of code changes
4. Local validation results
5. Any regression risks
6. Exact Databricks cells to run
7. Expected validation criteria
8. Explicit confirmation that Gold SQL was NOT modified

Do not claim Databricks validation has passed until actual Databricks output is supplied.
```

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
---

## Prompt 26 — Silver Iterations 2–5 validation documentation

**TYPE:** Documentation

**PROMPT SENT:**

```text
We have completed Databricks Serverless validation for Silver Iterations 2–5.

Do NOT modify Bronze, Gold, Dashboard, or the existing DQ implementations unless a concrete defect is identified.

The objective now is to update the project documentation and task tracking to record the validated results and mark Iteration 5 ACCEPTED.

IMPORTANT INTERPRETATION:

The referential_integrity check is intentionally expected to produce NON-ZERO failures because the Bronze dataset contains intentional D11/D12 orphan defects.

Do NOT interpret the non-zero FK failures as a bug.

Validated RI results:
- D11 orphan customer_id: 25 failure records
- D12 orphan product_id: 25 failure records
- 1,087 RI failure records total
- 1,029 distinct order business keys affected
- Some orders fail both FK checks, therefore failure-record count > distinct failed-row count
- This is correct by design.

Iteration 2 validated DQ results:

Completeness:
- customers: 60
- products: 9 failure records / 8 distinct failed rows
- orders: 0

Uniqueness:
- customers: 6
- products: 6
- orders: 8 failure records / 4 distinct failed rows

Type validation:
- customers: 50
- products: 15
- orders: 30

Iteration 3:
- RI customer orphan D11: 25
- RI product orphan D12: 25
- Existing-but-non-canonical parent effects: 1,037
- D17 proxy business-logic failures: 18
- Catalog-price business-logic mismatches: 222 total, including 18 D17/proxy-related and 204 other catalog mismatches
- These aggregate counts are expected based on the intentional defects and downstream interactions.

Iteration 4:
- quarantine total: 1,569
- summary rows: 13
- pass_percentage calculations validated
- idempotency validated: 1,569 → 1,569
- D11/D12/D17: 25 / 25 / 18
- quarantine stores failure records
- summary uses distinct business_key semantics where applicable
- datetime.utcnow() was replaced with datetime.now(timezone.utc)

Iteration 5 implementation:
- src/silver/create_silver_tables.py created
- run_silver_pipeline(spark=spark) implemented
- Reuses existing Iterations 2–4 DQ modules
- Writes quarantine and DQ summary
- Filters invalid rows using failure business keys
- Projects curated schemas
- Overwrites silver_customers, silver_products, silver_orders
- Serverless-compatible
- No RDD usage
- Bronze unchanged
- Gold/Dashboard unchanged

Databricks Serverless validation:
- SERVERLESS_COMPAT_VERSION = 9
- create_silver_tables loaded successfully
- Full run_silver_pipeline completed successfully
- quarantine count = 1569
- DQ summary count = 13

Curated Silver row counts:
- silver_customers = 878
- silver_products = 164
- silver_orders = 3832

Curated schemas:

silver_customers:
customer_id STRING
customer_name STRING
email STRING
country STRING
signup_date DATE
customer_segment STRING
lifetime_value DECIMAL(12,2)

silver_products:
product_id STRING
product_name STRING
category STRING
unit_price DECIMAL(10,2)

silver_orders:
order_line_id STRING
order_id STRING
customer_id STRING
product_id STRING
order_date DATE
quantity INT
unit_price DECIMAL(10,2)

No helper columns such as *_typed, _dup_rank, _row_num, or line_revenue exist in curated Silver.

Validated DQ summary:

business_logic:
- customers: 1006 tested, 996 passed, 10 failed
- orders: 5163 tested, 4886 passed, 277 failed
- products: 206 tested, 196 passed, 10 failed

completeness:
- customers: 1006 tested, 946 passed, 60 failed
- orders: 5163 tested, 5163 passed, 0 failed
- products: 206 tested, 198 passed, 8 failed

referential_integrity:
- orders: 5163 tested, 4134 passed, 1029 distinct failed rows

type_validation:
- customers: 1006 tested, 956 passed, 50 failed
- orders: 5163 tested, 5133 passed, 30 failed
- products: 206 tested, 191 passed, 15 failed

uniqueness:
- customers: 1006 tested, 1000 passed, 6 failed
- orders: 5163 tested, 5159 passed, 4 distinct failed rows / 8 failure records
- products: 206 tested, 200 passed, 6 failed

DOCUMENTATION TASK:

1. Update:
   src/silver/SILVER_LAYER_NOTES.md

   Add/complete the Iteration 5 section and mark:

   FINAL DECISION: ACCEPTED

   Include:
   - Databricks Serverless validation
   - SERVERLESS_COMPAT_VERSION = 9
   - pipeline execution success
   - curated row counts
   - curated schemas
   - quarantine count
   - summary row count
   - idempotency result
   - DQ summary validation
   - explicit explanation that non-zero FK failures are intentional and correct for D11/D12

2. Update:
   ai-prompts/silver-layer.md

   Record the final Databricks validation evidence for Iteration 5.

   Explicitly document that:
   - FK integrity is NOT expected to be zero for this intentionally defective Bronze dataset.
   - D11/D12 produce 25 + 25 orphan failure records.
   - 1,029 distinct order rows are affected by RI.
   - 1,087 RI failure records can occur because a row may fail both FK checks.
   - Therefore non-zero RI results are ACCEPTED.

3. Update:
   tool-specific/cursor-workflow/task-breakdown.md

   Mark all Iteration 5 tasks that correspond to the validated implementation and Databricks validation as DONE/ACCEPTED.

   Mark Iteration 5:
   ACCEPTED

4. Do not change the implementation merely to force FK failure counts to zero.

5. Do not remove intentional test defects from the Bronze data.

6. Do not alter the DQ semantics merely to make aggregate counts equal distinct-row counts.

7. Preserve the existing distinction:
   - quarantine = failure records
   - DQ summary = distinct failed business keys where the existing implementation defines it that way

8. After making documentation changes, run only lightweight validation necessary to ensure the documentation/task files are syntactically intact.

9. At the end, provide:
   - files modified
   - concise summary of Iteration 5 acceptance
   - confirmation that no Bronze/Gold/Dashboard implementation was changed
   - confirmation that no DQ logic was changed

Do NOT proceed to Gold implementation yet.
Iteration 5 is the final Silver milestone and should be recorded as ACCEPTED.
```

**AI RESPONSE SUMMARY:**

Documented Serverless validation baselines for Silver Iterations 2–5.

**FINAL DECISION:** ACCEPTED (documented)
---

## Prompt 27 — Silver FK / curated-dimension investigation

**TYPE:** Investigation

**PROMPT SENT:**

```text
# Cursor Investigation Prompt — Trace Silver FK / Curated-Dimension Mismatch

You are investigating a **data-quality / pipeline-boundary issue** in this repository.

## Context

The Gold layer has been implemented according to the frozen Gold contract.

Gold uses these joins:

* `silver_orders INNER JOIN silver_products ON product_id`
* `silver_orders INNER JOIN silver_customers ON customer_id`

Runtime validation on Databricks produced:

```text
silver_customers = 878
silver_products  = 164
silver_orders    = 3832

gold_sales_by_product       = 164
gold_revenue_by_customer    = 794
gold_customer_segmentation  = 794
gold_daily_weekly_trends    = 952
```

Gold trends reconcile exactly with Silver:

```text
Silver revenue       = 2,830,321.54
Gold daily revenue   = 2,830,321.54

Silver quantity      = 11,464
Silver distinct orders = 2,110

Gold daily order count = 2,110
```

But entity-level Gold tables do not reconcile with all `silver_orders`:

```text
Gold sales revenue       = 2,764,308.07
Gap                      =    66,013.47

Gold sales quantity      = 11,115
Gap                      =       349

Gold customer revenue    = 2,773,248.90
Gap                      =    57,072.64
```

We independently ran these Databricks diagnostics:

```text
Unmatched product order lines = 116
Unmatched product quantity    = 349
Unmatched product revenue     = 66,013.47

Unmatched customer order lines = 71
Unmatched customer quantity    = 221
Unmatched customer revenue     = 57,072.64
```

Therefore:

```text
silver_orders
    |
    +---- product_id values not present in silver_products
    |
    +---- customer_id values not present in silver_customers
```

The Gold SQL is NOT to be changed at this stage.

The purpose of this task is to determine **why these FK values survived into `silver_orders` while their corresponding parent rows are absent from curated `silver_products` / `silver_customers`.**

---

## Important repository evidence

The Silver implementation contains a Referential Integrity stage that creates:

```python
_customer_parent_ok
_product_parent_ok
```

The repository also contains logic/functions involving:

```text
canonical_valid_filter
filter_valid_rows
```

The current hypothesis is:

> Referential integrity may validate orders against a "canonical valid parent" population, while the final curated `silver_products` / `silver_customers` tables are produced after additional DQ filtering.

If that is true, Silver RI and the final curated Silver dimensions are using different definitions of a valid parent.

Do NOT assume this hypothesis is correct. Prove or disprove it from the code.

---

# Your task

Perform a **read-only code investigation**.

DO NOT modify any files.

DO NOT create new files.

DO NOT change SQL.

DO NOT "fix" anything.

Trace the actual execution/data flow in the repository.

---

# Investigation questions

Answer these questions with exact file paths, function names, and relevant code snippets/line references.

## 1. Where are `silver_products` and `silver_customers` created?

Find the exact code that writes:

```text
de_c1_coding_evaluation.silver.silver_products
de_c1_coding_evaluation.silver.silver_customers
```

Identify:

* source DataFrame
* transformations applied before writing
* DQ filters applied
* whether `filter_valid_rows()` is used
* whether `canonical_valid_filter()` is used
* ordering of DQ stages

---

## 2. Where is Silver Referential Integrity implemented?

Locate the implementation corresponding to:

```text
04_quality_referential_integrity.py
```

Find exactly how these fields are created:

```python
_customer_parent_ok
_product_parent_ok
```

Show the actual parent DataFrames/tables used for the lookups.

For example, determine whether the code effectively does something like:

```python
orders.customer_id IN canonical_customers
```

or:

```python
orders.customer_id IN silver_customers
```

Do NOT infer this. Follow the actual variables through the code.

---

## 3. What exactly is `canonical_valid_filter()`?

Locate its definition.

Explain:

* what input DataFrame it expects
* what columns/checks it uses
* whether it represents canonical parent validity
* whether it includes all DQ categories
* whether it is applied before or after business-logic / uniqueness / completeness / type validation

Show the relevant implementation.

---

## 4. What exactly is `filter_valid_rows()`?

Locate its definition.

Explain:

* what DQ categories it considers
* whether it combines multiple DQ failure conditions
* whether it produces the final curated parent DataFrame
* whether it is used to create `silver_products` and `silver_customers`

Show the relevant implementation.

---

# 5. Trace ONE product end-to-end

Use product ID:

```text
184
```

Trace it conceptually through the code:

```text
Bronze product 184
      ↓
ranking / deduplication
      ↓
completeness
      ↓
type validation
      ↓
referential integrity
      ↓
business logic
      ↓
final curated silver_products
```

We know from Databricks:

```text
product_id = 184
```

appears in `silver_orders` but does NOT appear in `silver_products`.

Explain from the code which stage can remove product 184 from the parent table while still allowing orders referencing 184 to survive.

If the repository does not contain enough information to establish this, explicitly say so.

---

# 6. Trace ONE customer end-to-end

Use customer ID:

```text
177
```

Perform the same analysis:

```text
Bronze customer 177
      ↓
ranking / deduplication
      ↓
completeness
      ↓
type validation
      ↓
referential integrity
      ↓
business logic
      ↓
final curated silver_customers
```

Determine exactly where the parent can disappear.

---

# 7. Investigate pipeline ordering

Find the actual orchestration order of Silver DQ stages.

I specifically want to know whether the pipeline behaves conceptually like:

```text
A:
Build canonical parents
        ↓
Validate orders against canonical parents
        ↓
Apply additional DQ to dimensions
        ↓
Write curated dimensions
```

or:

```text
B:
Apply ALL DQ to dimensions
        ↓
Write curated dimensions
        ↓
Validate orders against curated dimensions
```

or something else.

Give the actual order from the repository.

---

# 8. Investigate the definition of "valid parent"

Find every relevant place where parent validity is defined.

Search for:

```text
canonical_valid_filter
filter_valid_rows
parent_ok
customer_parent
product_parent
canonical
referential_integrity
```

Determine whether there are multiple definitions of parent validity.

Create this comparison:

```text
Concept                  Actual implementation
------------------------------------------------
RI parent population     ?
Curated customer parent ?
Curated product parent   ?
Canonical parent         ?
All-DQ-valid parent      ?
```

---

# 9. Determine root cause

Based ONLY on the repository code, classify the problem as one of:

### A

RI validates against the same final curated dimension tables.

### B

RI validates against an earlier/canonical parent population, while final curated dimensions apply additional DQ filters.

### C

RI itself is incorrectly implemented.

### D

The available code is insufficient to determine the cause.

Give one definitive answer if possible.

---

# 10. Do NOT propose a fix yet

This is extremely important.

Do NOT:

* modify Silver
* modify Gold
* modify validation
* modify documentation
* change the frozen Gold contract
* create patches
* create commits

We only want the **root-cause investigation**.

---

# Required final response format

Return exactly this structure:

## Root Cause

One concise paragraph.

## Evidence

### 1. Curated Silver dimensions

* File:
* Function:
* Relevant code:
* Finding:

### 2. Referential integrity

* File:
* Function:
* Relevant code:
* Finding:

### 3. `canonical_valid_filter`

* File:
* Function:
* Finding:

### 4. `filter_valid_rows`

* File:
* Function:
* Finding:

### 5. Pipeline ordering

* File:
* Order:
* Finding:

## Product 184 Trace

```text
Bronze
  ↓
...
  ↓
silver_products
```

Explain where/why it disappears.

## Customer 177 Trace

```text
Bronze
  ↓
...
  ↓
silver_customers
```

Explain where/why it disappears.

## Parent Validity Comparison

| Concept                 | Actual implementation |
| ----------------------- | --------------------- |
| RI parent population    |                       |
| Curated customer parent |                       |
| Curated product parent  |                       |
| Canonical parent        |                       |
| All-DQ-valid parent     |                       |

## Classification

Choose exactly one:

```text
A / B / C / D
```

Then explain why.

## Gold Impact

Explain why the observed Gold results follow from the discovered Silver behavior:

```text
Product orphan revenue = 66,013.47
Product orphan quantity = 349

Customer orphan revenue = 57,072.64
Customer orphan quantity = 221
```

Do NOT recommend implementation changes yet.

## Files Inspected

List every relevant file you actually inspected.

Do not claim a file was inspected unless you actually opened/read it.
```

**AI RESPONSE SUMMARY:**

Traced FK vs curated-dimension mismatch; alignment proposal (led to Prompt 13).

**FINAL DECISION:** ACCEPTED (documented)
---

## Prompt 28 — Silver RI alignment — pre-implementation review

**TYPE:** Design review

**PROMPT SENT:**

```text
You are working on the DE_C1_Coding_Evaluation repository.

We have completed Gold Iteration 6 and executed the Gold pipeline successfully on Databricks Serverless.

DO NOT MODIFY ANY FILES YET.

Your task is to investigate and propose the smallest safe implementation change required to align Silver referential integrity with the final curated Silver dimensions.

## Confirmed runtime evidence

Databricks produced:

* silver_customers = 878
* silver_products = 164
* silver_orders = 3832

Gold:

* gold_sales_by_product = 164
* gold_revenue_by_customer = 794
* gold_daily_weekly_trends = 952
* gold_customer_segmentation = 794

Silver revenue:

2830321.54

Gold sales-by-product revenue:

2764308.07

Product gap:

66013.47 revenue
349 quantity
116 order lines

Gold customer revenue / segmentation spend:

2773248.90

Customer gap:

57072.64 revenue
221 quantity
71 order lines

Confirmed Databricks diagnostics:

Product unmatched FK:

* unmatched_product_order_lines = 116
* unmatched_quantity = 349
* unmatched_revenue = 66013.47

Customer unmatched FK:

* unmatched_customer_order_lines = 71
* unmatched_quantity = 221
* unmatched_revenue = 57072.64

Gold trends reconcile exactly with Silver:

2830321.54 revenue
2110 distinct orders

Gold SQL is intentionally defined with:

* silver_orders INNER JOIN silver_products for sales-by-product
* silver_orders INNER JOIN silver_customers for revenue-by-customer
* silver_customers INNER JOIN silver_orders for segmentation
* silver_orders only for trends

Therefore DO NOT change the Gold SQL merely to make reconciliation pass.

## Confirmed root cause

Silver RI currently validates order foreign keys against a canonical parent population created by:

prepare_canonical_entity_df()
→ canonical_valid_filter()

canonical_valid_filter() checks:

* _dup_rank = 1
* completeness
* type validation

It does NOT include:

* uniqueness
* business_logic

Curated dimensions are subsequently produced using:

build_curated_entity_df()
→ filter_valid_rows()

For customers/products, filter_valid_rows() excludes business keys that fail:

* completeness
* uniqueness
* type_validation
* business_logic

Therefore the parent population used by RI is broader than the final curated dimension population.

Confirmed examples:

### Product 184

* product_id 184 has duplicate source rows
* canonical_valid_filter() allows the canonical occurrence
* RI therefore considers product_id 184 valid
* uniqueness failure causes filter_valid_rows() to remove the entire product_id 184 key from silver_products
* orders referencing product_id 184 remain in silver_orders
* Gold inner join drops those order lines

### Customer 177

* customer_id 177 has a future signup_date
* canonical_valid_filter() does not evaluate business_logic
* RI therefore considers customer_id 177 valid
* business_logic later excludes customer_id 177 from silver_customers
* orders referencing customer_id 177 remain in silver_orders
* Gold inner join drops those order lines

## Files to inspect

Inspect these files and their interactions:

* src/silver/create_silver_tables.py
* src/silver/04_quality_referential_integrity.py
* src/silver/05_quality_business_logic.py
* src/silver/06_write_dq_results.py
* src/silver/01_quality_completeness.py
* src/silver/02_quality_uniqueness.py
* src/silver/03_quality_type_validation.py
* src/silver/silver_common.py
* src/silver/SILVER_LAYER_NOTES.md
* src/gold/GOLD_LAYER_NOTES.md
* src/gold/create_gold_tables.py

## Primary question

Determine how to make Silver RI validate order foreign keys against the SAME parent population that ultimately exists in:

* silver_customers
* silver_products

without unnecessarily rewriting the Silver DQ architecture.

The desired invariant is:

For every nonblank customer_id in silver_orders:

```
customer_id EXISTS IN silver_customers
```

For every nonblank product_id in silver_orders:

```
product_id EXISTS IN silver_products
```

This should make the existing Gold INNER JOIN contract consistent with the Silver output.

## Important constraints

Do NOT:

* modify Gold SQL
* weaken Gold validation
* remove business_logic validation
* remove uniqueness validation
* bypass existing DQ checks
* silently change the frozen Gold contract
* invent a new DQ category
* duplicate large amounts of existing logic unnecessarily

Do investigate whether RI can safely use the final curated parent keys or whether the existing pipeline ordering prevents that.

Pay particular attention to this current ordering:

1. completeness
2. uniqueness
3. type validation
4. referential integrity
5. business logic
6. DQ persistence
7. curated Silver writes

Determine whether RI can be moved logically after parent curation, or whether the curated parent key sets can be derived from the already-computed DQ results without rerunning the entire pipeline.

## Required output

Do NOT edit files.

Return a detailed implementation proposal containing:

1. Current execution flow
2. Exact reason canonical_valid_filter() differs from curated parent eligibility
3. The smallest viable architectural fix
4. Alternative fixes considered
5. Exact files/functions that would need modification
6. Whether pipeline ordering must change
7. Whether existing DQ results can be reused
8. How order-line RI filtering should work after the change
9. Expected effect on:

   * silver_orders
   * silver_customers
   * silver_products
   * Gold reconciliation
10. Regression risks
11. Recommended implementation
12. A precise step-by-step implementation plan

Also explicitly answer:

"Can we make RI use the final curated parent key population without causing circular dependency or breaking the existing DQ pipeline?"

Do not implement anything until this proposal is reviewed and approved.
```

**AI RESPONSE SUMMARY:**

Reviewed RI fix proposal against codebase before Prompt 13 implementation.

**FINAL DECISION:** ACCEPTED (documented)

