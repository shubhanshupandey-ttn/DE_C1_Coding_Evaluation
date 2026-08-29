# AI Prompts — Documentation (Phase 1 & closure)

**Prompts in this file:** 01, 02, 03, 24, 31, 32, 33, 34, 35

## Global prompt index (01–35)

All prompt history lives in **phase files only** — each entry has **PROMPT SENT** (full text where available), **AI RESPONSE SUMMARY**, and **FINAL DECISION**.

| # | File | Title |
|---|------|-------|
| 01–03, 24, 31–35 | `documentation.md` | Kickoff, foundation, templates, validation, closure |
| 04 | `data-generation.md` | Data generation |
| 05–06, 25 | `bronze-layer.md` | Bronze ingest + Spark fix + doc update |
| 07–13, 26–28 | `silver-layer.md` | Silver design through RI alignment |
| 14–20, 29 | `gold-layer.md` | Gold design through orchestration |
| 21–23, 30 | `dashboard.md` | Dashboard SQL + validation + evaluation |

Minor operational messages (git checks, notebook cells, short confirmations) are not separate numbered prompts; outcomes are in the relevant phase prompt or `debugging.md`.

---

## Prompt 01 — Project kickoff (role definition + repository inspection)

**TYPE:** Original (session role + inspection only)

**PROMPT SENT:**

```text
You are the Lead Data Engineer, Databricks Architect, AI-assisted Software Engineer, and technical documentation owner for this project.
We are building a Databricks data engineering project in this repository:

databricks-medallion-pipeline/

The project will be developed incrementally. Do not implement the entire project now.

The following is the intended repository structure:

databricks-medallion-pipeline/
├── README.md
├── candidate-info.md
├── tool-workflow.md                    # Part A: AI Workflow Foundation
├── requirements-analysis.md
├── design-notes.md
├── data-model.md
├── data-quality-strategy.md
│
├── src/
│   ├── data_generation/
│   │   ├── generate_sample_data.py
│   │   └── DATA_GENERATION_NOTES.md
│   ├── bronze/
│   │   ├── 01_ingest_customers.py
│   │   ├── 02_ingest_orders.py
│   │   ├── 03_ingest_products.py
│   │   └── ingest_all.py
│   ├── silver/
│   │   ├── 01_quality_completeness.py
│   │   ├── 02_quality_uniqueness.py
│   │   ├── 03_quality_type_validation.py
│   │   ├── 04_quality_referential_integrity.py
│   │   ├── 05_quality_business_logic.py
│   │   └── create_silver_tables.py
│   ├── gold/
│   │   ├── 01_sales_by_product.sql
│   │   ├── 02_revenue_by_customer.sql
│   │   ├── 03_daily_weekly_trends.sql
│   │   ├── 04_customer_segmentation.sql
│   │   └── create_gold_tables.py
│   └── dashboard/
│       ├── dashboard_queries.sql
│       └── DASHBOARD_GUIDE.md
│
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   └── products.csv
│
├── database/
│   ├── schema.sql
│   ├── seed-data-notes.md
│   └── setup-notes.md
│
├── debugging-notes.md
├── reflection.md
├── final-ai-usage-summary.md
│
└── ai-prompts/
    ├── data-generation.md
    ├── bronze-layer.md
    ├── silver-layer.md
    ├── gold-layer.md
    ├── dashboard.md
    ├── debugging.md
    └── documentation.md

PROJECT OBJECTIVE

Build a complete, coherent Databricks medallion-architecture project covering:

Raw/sample data
    ↓
Bronze
    ↓
Silver + data quality
    ↓
Gold
    ↓
Analytics/dashboard

The project should demonstrate practical data engineering concepts rather than simply creating placeholder files.

The implementation must remain internally consistent across:
- requirements
- architecture/design
- data model
- generated data
- Bronze ingestion
- Silver transformations and quality checks
- Gold analytical datasets
- dashboard queries
- documentation

IMPORTANT DEVELOPMENT RULE

We will work incrementally.

Do NOT:
- implement Bronze, Silver, Gold, dashboard, etc. all at once
- invent requirements that have not yet been provided
- create fake implementations merely to populate the directory
- make architectural decisions that should be discussed later
- rewrite the entire repository unnecessarily

Wait for subsequent instructions before implementing individual project phases.

DOCUMENTATION MUST BE CREATED ALONGSIDE THE WORK

Documentation is not a final-stage activity.

We must avoid documentation debt.

Whenever a project phase is implemented, the relevant documentation must be created or updated as part of that same phase.

For example:

Data generation
→ implementation + DATA_GENERATION_NOTES.md + relevant ai-prompts entry

Bronze
→ Bronze code + relevant design/documentation + ai-prompts/bronze-layer.md

Silver
→ Silver code + data-quality documentation + ai-prompts/silver-layer.md

Gold
→ Gold SQL/Python + analytical/design documentation + ai-prompts/gold-layer.md

Dashboard
→ dashboard queries + DASHBOARD_GUIDE.md + ai-prompts/dashboard.md

PROMPT RECORDING REQUIREMENT

The prompts used to generate/implement each major project phase are themselves project artifacts.

Maintain:

ai-prompts/data-generation.md
ai-prompts/bronze-layer.md
ai-prompts/silver-layer.md
ai-prompts/gold-layer.md
ai-prompts/dashboard.md
ai-prompts/debugging.md
ai-prompts/documentation.md

When a phase is implemented, the actual implementation prompt/instruction used for that phase must be recorded in the corresponding file.

Do not wait until the end of the project to reconstruct the prompts.

Where useful, also record:
- important follow-up prompts
- debugging prompts
- prompts that caused meaningful design changes
- prompts used to improve or refactor an implementation

Do not fill these files with meaningless commentary. They should preserve the actual AI-assisted development trail.

DOCUMENTATION QUALITY

Documentation should explain the actual implementation rather than generic theory.

Where applicable, document:
- purpose
- assumptions
- architecture decisions
- data flow
- schema
- transformations
- data-quality rules
- important implementation decisions
- validation/testing performed
- known limitations
- debugging decisions
- AI-assisted development decisions

Documentation must remain synchronized with the actual code.

If implementation changes, update the relevant documentation.

AI-ASSISTED DEVELOPMENT RECORD

The project intentionally demonstrates responsible AI-assisted development.

Therefore, preserve meaningful evidence of how AI was used.

The final project should make it possible to understand:
- what was generated with AI
- what was reviewed/modified
- what was tested
- what debugging was required
- what important decisions were made by the developer

Do not fabricate human review or testing that did not actually occur.

GIT DISCIPLINE

This repository is already connected to GitHub.

Work should be organized into logical milestones.

After completing a meaningful milestone:
- inspect git status
- identify changed files
- ensure documentation and prompt artifacts are included
- provide a concise summary
- suggest a meaningful commit message

Do not automatically push to GitHub unless explicitly instructed.

Do not create meaningless commits for every tiny modification.

CODE QUALITY

Code should be:
- readable
- modular
- appropriately commented
- maintainable
- consistent with the rest of the repository
- suitable for a practical Databricks data engineering project

Avoid unnecessary complexity.

Do not introduce dependencies unless they are justified.

Do not hard-code credentials, secrets, tokens, passwords, or connection credentials.

FIRST TASK

For now, ONLY inspect the current repository.

Do not implement the project yet.

Determine:

1. Current repository structure.
2. Which files/directories already exist.
3. Which intended files are currently missing.
4. Current Git status.
5. Current branch.
6. Whether the repository already contains any configuration files.
7. Whether any existing files contain work that must be preserved.

Do not delete or overwrite existing work.

After inspection, report:

- Current state
- Existing files
- Missing intended files
- Git status
- Any observations or potential issues

Then STOP and wait for the next instruction.
```

**AI RESPONSE SUMMARY:**

Inspected `DE_C1_Coding_Evaluation`. Found only `.gitignore` and git metadata. No `databricks-medallion-pipeline/` subdirectory. Branch `main`, clean working tree, synced with `origin/main`. All planned pipeline artifacts missing.

**YOUR EVALUATION:**

✓ **Accepted** — Accurate baseline; no implementation performed.

**FINAL DECISION:** ACCEPTED

---

## Prompt 02 — Phase 1 project foundation

**TYPE:** Original

**PROMPT SENT:**

```text
We have completed the repository inspection.

Use the CURRENT REPOSITORY ROOT as the project root.

Do NOT create a nested `databricks-medallion-pipeline/` directory.

The repository root itself is the project.

Now begin Phase 1: PROJECT FOUNDATION.

Create the following foundation files:

README.md
candidate-info.md
tool-workflow.md
requirements-analysis.md
design-notes.md
data-model.md
data-quality-strategy.md
ai-prompts/documentation.md

Do NOT create the implementation code, sample data, Bronze, Silver, Gold, dashboard, or database files yet.

The purpose of this phase is to establish the project's foundation before implementation begins.

IMPORTANT:
The content must describe the actual project we are going to build, not generic Databricks documentation.

PROJECT DIRECTION

We are building a practical Databricks medallion-architecture data engineering project:

Raw/sample data
    ↓
Bronze
    ↓
Silver + data quality
    ↓
Gold
    ↓
Analytics/dashboard

The project will use Python, SQL, and Databricks-oriented data engineering practices.

The final implementation will contain:

src/data_generation/
src/bronze/
src/silver/
src/gold/
src/dashboard/

along with:

data/
database/
ai-prompts/

The detailed implementation will be provided in later phases.

DOCUMENTATION REQUIREMENT

Documentation is part of the implementation process.

Do not create vague placeholder documentation.

Each foundation document should contain useful project-specific content based on the currently established project direction.

Where a future implementation detail has not yet been decided, explicitly mark it as:

"To be finalized during implementation."

Do not invent technical decisions simply to make the document appear complete.

REQUIRED DOCUMENT PURPOSES

README.md

Create the initial project README.

Include:
- project purpose
- high-level architecture
- planned repository structure
- technology/tooling context
- development approach
- current project status
- note that implementation is being developed incrementally

Do not claim that components have already been implemented.

candidate-info.md

Create a placeholder for project/candidate information.

Do not invent personal information.

Clearly identify fields that need to be supplied later.

tool-workflow.md

This is Part A: AI Workflow Foundation.

Document how AI-assisted development is being incorporated into this project.

Explain the intended workflow at a practical level:
- requirements/design
- AI-assisted implementation
- developer review
- validation/testing
- debugging
- documentation
- Git/version control

Do not fabricate completed AI interactions.

requirements-analysis.md

Document the currently established project requirements.

Separate:
- confirmed requirements
- implementation requirements
- items still to be finalized

Do not invent business requirements that have not been established.

design-notes.md

Document the current high-level architecture and design direction.

Include:
- medallion architecture
- data flow
- separation of Bronze/Silver/Gold responsibilities
- role of data quality
- role of analytical/dashboard layer

Clearly distinguish established decisions from future decisions.

data-model.md

Document the initial logical data model around:

customers
orders
products

Describe their likely relationships only where supported by the project structure.

Do not invent detailed columns unless they are explicitly required.

Mark detailed schema decisions as pending where necessary.

data-quality-strategy.md

Establish the intended data-quality framework.

The project explicitly contains quality checks for:

- completeness
- uniqueness
- type validation
- referential integrity
- business logic

Explain what each category is intended to validate.

Do not yet implement the checks.

ai-prompts/documentation.md

Create the documentation prompt artifact.

Record the prompt/instruction used for this documentation-foundation phase.

This file should establish the convention that future major implementation prompts are preserved in:

ai-prompts/data-generation.md
ai-prompts/bronze-layer.md
ai-prompts/silver-layer.md
ai-prompts/gold-layer.md
ai-prompts/dashboard.md
ai-prompts/debugging.md
ai-prompts/documentation.md

IMPORTANT DOCUMENTATION RULE

Do not wait until the end of the project to create documentation.

For every subsequent implementation phase:

implementation + documentation + prompt artifact

must be treated as one unit of work.

QUALITY CONTROL

Before finishing:

1. Verify that all requested foundation files exist.
2. Check that the documents do not claim unimplemented functionality is complete.
3. Check that terminology is consistent across the documents.
4. Check that the architecture described in the documents is consistent with the planned repository structure.
5. Check that no secrets, credentials, tokens, or personal information have been invented.
6. Check git status.

Do NOT commit or push anything.

At the end, provide:
- files created
- brief purpose of each
- any assumptions made
- anything explicitly marked as "To be finalized during implementation"
- git status

Then STOP and wait for the next instruction.
```

**AI RESPONSE SUMMARY:**

Created eight foundation documents with project-specific medallion architecture, requirements, logical data model, five-category DQ framework (strategy only), and AI workflow (`tool-workflow.md`). Explicitly marked pipeline phases as not started.

**YOUR EVALUATION:**

- ✓ Project-specific content, not generic boilerplate
- ✓ Clear "not started" status for implementation
- ✓ Consistent entity names and layer structure
- ✓ Prompt artifact convention established

**FINAL DECISION:** Foundation docs accepted as Phase 1 baseline.

---

## Prompt 03 — Align docs with submission templates

**TYPE:** Iteration (documentation)

**PROMPT SENT:**

```text
Submission Templates 
these as starting structures for required artifacts — they are a floor, not a limit.
Candidate Information
File: candidate-info.md
# Candidate Information

**Name:** [Your Name]  
**Role:** [SE / SSE / ATL/TL / other]  
**Primary Technology Stack:** Python / PySpark, SQL, Databricks  
**Primary AI Tool Used:** Cursor / Claude / other  
**Project Option Selected:** Data Pipeline (Medallion Architecture)  
**Assessment Start Date:** [Date]  
**Submission Date:** [Date]

## Tools & Environment
- Databricks: Community Edition / other
- Languages: Python, PySpark, SQL
- Libraries: PySpark, Delta Lake, pandas
- AI Tool: [Cursor / Claude]

## Setup Summary
[Quick reference for how to run the pipeline — expanded in README.md]
Requirement Analysis
File: requirements-analysis.md
# Requirement Analysis

## Problem Statement
[Your understanding of the e-commerce sales pipeline problem in your own words]

## Functional Requirements
- [requirements]

## Non-Functional Requirements
- [non functional requirements]

## Assumptions
- [assumptions]

## Edge Cases
- [edge cases]

## Clarifications Needed
- [carifications]
Design Notes
File: design-notes.md
# Design Notes

## Architecture Overview
- [High-level design of Bronze → Silver → Gold → Dashboard]
## Data Model & Schema
- [Descriptions of customers, orders, products tables]
## Bronze Layer Design
- [bronze layer]
## Silver Layer Design
- [silver layer]

## Gold Layer Design
- [gold layer]
## Data Quality Validation Strategy
- [data quality]
## Debugging Approach
- [debugging]
Data Quality Strategy
File: data-quality-strategy.md
# Data Quality Strategy

## Quality Checks Overview

### 1. Completeness Check
- **What:** No NULLs in critical fields
- **How:** COUNT NULL values in email, customer_id, product_id
- **Threshold:** >99% complete
- **Result:** Flag rows with NULLs

### 2. Uniqueness Check
- **What:** No duplicate rows
- **How:** Check for duplicate order_id, customer_id
- **Threshold:** 100% unique
- **Result:** Flag duplicate rows

### 3. Referential Integrity
- **What:** Foreign keys exist in parent tables
- **How:** Check customer_id in customers, product_id in products
- **Threshold:** >99.9% valid
- **Result:** Flag orphan records

## Quality Metrics Report
[How you'll present % passed per check]

## Sample Data Quality Issues
[List the ~700 intentional issues in your sample data]
AI Prompts — Organized by Activity
Files: ai-prompts/{activity}.md
For each activity, capture prompt history showing:
Prompt text (or summary)
AI response (summary or key excerpt)
What you accepted (and why)
What you changed (and why)
What you rejected (and why)
Example: ai-prompts/data-generation.md
# AI Prompts — Data Generation

## Prompt 1: Initial Data Generation Script

**PROMPT SENT:**
"Generate Python script to create realistic e-commerce customer data.
I need 10,000 rows with these fields: customer_id (INT), customer_name (STRING),
email (STRING), country (STRING), signup_date (DATE between 2020-2024),
customer_segment (Premium/Standard/Basic), lifetime_value (DECIMAL).
Include realistic values like actual names, valid email formats, and random dates."

**AI RESPONSE SUMMARY:**
[Cursor generated Python script using faker library to create realistic data]

**YOUR EVALUATION:**
✓ **What was good:**
- Used faker for realistic names and emails
- Date range correct (2020-2026)
- Customer segments randomized properly

✗ **What needed fixing:**
- Some customers had signup_date in future
- No intentional quality issues (needed 50 NULL emails, 10 duplicates, etc.)
- Missing lifetime_value calculations

△ **Missing:**
- No NULL values as needed for quality testing

## Iteration 1: Adding Quality Issues

**PROMPT SENT:**
"Modify the script to introduce intentional quality issues for testing:
- 50 rows with NULL email
- 10 rows with duplicate customer_id
- 30 rows with signup_date > today()
Keep the rest realistic. Add comments explaining the quality issues."

**AI RESPONSE SUMMARY:**
[Cursor modified script to add quality issues and comments]

**YOUR EVALUATION:**
✓ **ACCEPTED** - Modifications correct, quality issues intentional and commented

**FINAL DECISION:** Use this version as `generate_sample_data.py`

---

## Prompt 2: Order Data Generation

**PROMPT SENT:**
"Generate Python script for 100,000 realistic e-commerce order rows...
[similar structure for orders]"

**[Continue pattern for each major prompt]**
Reflection
File: reflection.md
# Reflection
## What I Built
-
## How I Used AI (Across the Lifecycle)
-
## What AI Helped With Most
-
## What AI Got Wrong
-
## How I Validated AI Output
-
## What I Would Improve Next
-
## Reusable Workflow

these are instructuions for doc creation , referring these do you wish to modify docs ?
```

**AI RESPONSE SUMMARY:**

Restructured foundation docs to match submission section layouts (Problem Statement, Functional/Non-Functional Requirements, What/How/Threshold/Result for DQ checks, PROMPT SENT / AI RESPONSE / YOUR EVALUATION format). Preserved honest "not implemented" status.

**YOUR EVALUATION:**

- ✓ Accept template-aligned structure

**FINAL DECISION:** ACCEPTED — template alignment retained as project baseline.


---

## Prompt 24 — Final validation review

**TYPE:** Validation

**PROMPT SENT:**

```text
We have completed the Databricks implementation and dashboard for the DE_C1_Coding_Evaluation project.

Before making any changes, inspect the existing repository thoroughly and understand its current structure and implementation. Do NOT create arbitrary files or change working pipeline/dashboard logic unnecessarily.

The Databricks dashboard is already implemented with these pages:
1. Executive Overview
2. Product Performance
3. Customer Insights

The dashboard consumes the existing Gold tables only:
- de_c1_coding_evaluation.gold.gold_sales_by_product
- de_c1_coding_evaluation.gold.gold_revenue_by_customer
- de_c1_coding_evaluation.gold.gold_daily_weekly_trends
- de_c1_coding_evaluation.gold.gold_customer_segmentation

The dashboard has already been validated visually in Databricks. Do NOT redesign or add dashboard pages unless the repository requirements explicitly require it.

TASK:
Perform a FINAL VALIDATION REVIEW of the complete project.

First inspect:
- README.md
- requirements-analysis.md
- design-notes.md
- tool-workflow.md
- data-model.md
- data-quality-strategy.md
- GOLD_LAYER_NOTES.md
- existing source code
- existing tests
- existing dashboard files
- relevant repository instructions/rules
- any existing documentation related to the evaluation

Also inspect the actual Bronze/Silver/Gold SQL/code so that validation is based on the implemented project rather than assumptions.

Then determine:

1. What validation/test artifacts already exist.
2. What required validation artifacts are missing.
3. Whether existing tests adequately cover:
   - completeness
   - uniqueness
   - referential integrity
   - business-rule validation
   - Gold-layer aggregation correctness
   - reconciliation between Gold tables
4. Whether the intentional data-quality issues introduced during data generation are actually tested and caught.
5. Whether the dashboard SQL uses Gold tables only.
6. Whether dashboard queries reimplement any Gold business logic incorrectly.
7. Whether all required project artifacts from the evaluation specification exist.
8. Whether README/setup instructions are sufficient to reproduce the project.
9. Whether there are inconsistencies between documentation and implementation.

IMPORTANT ARCHITECTURAL RULES:
- Dashboard must consume Gold only.
- Do not introduce Bronze/Silver dependencies into dashboard SQL.
- Do not recreate Gold business metrics in the dashboard.
- Additional aggregation of existing Gold metrics for visualization is acceptable.
- Do not modify working Bronze/Silver/Gold logic merely for cosmetic reasons.
- Do not invent columns, metrics, tables, or requirements.
- Use the actual repository implementation and documentation as the source of truth.

Known Gold tables:

de_c1_coding_evaluation.gold.gold_sales_by_product

de_c1_coding_evaluation.gold.gold_revenue_by_customer

de_c1_coding_evaluation.gold.gold_daily_weekly_trends

de_c1_coding_evaluation.gold.gold_customer_segmentation

Known validation results from Databricks that should be considered when checking reconciliation:

Total Gold segmentation spend:
2708411.08

Total Gold revenue by customer:
2708411.08

Customer-segment spend percentages:
Standard = 47.80%
Basic = 30.55%
Premium = 21.65%
Total = 100.00%

Behavioral segmentation:
Repeat = 386 customers, 1094641.95 spend, 40.42%
One-Time = 207 customers, 264634.54 spend, 9.77%
High-Value = 199 customers, 1349134.59 spend, 49.81%

Total revenue:
2708411.08

Dashboard currently contains:
- Executive Overview
- Product Performance
- Customer Insights

Required dashboard concepts include:
- Top products by revenue
- Customer revenue distribution
- Customer segmentation
- Product/category analysis
- Customer behavior analysis

Do NOT blindly assume these are the only requirements; verify against the repository/evaluation documentation.

AFTER REVIEW:

Create/update only the necessary validation artifacts in the repository.

Prefer reusing the repository's existing structure and conventions.

For validation SQL, create a clearly organized validation script if one does not already exist. It should contain executable checks for:

A. BRONZE VALIDATION
- expected source tables/data exist
- row counts are non-zero
- required columns exist where practical

B. SILVER DATA QUALITY
- null/completeness checks
- duplicate/uniqueness checks
- referential integrity checks
- business-rule checks
- intentional bad records are detected

C. GOLD VALIDATION
- gold_sales_by_product aggregation checks
- gold_revenue_by_customer aggregation checks
- gold_daily_weekly_trends consistency checks
- gold_customer_segmentation consistency checks

D. RECONCILIATION
Verify that equivalent revenue totals reconcile across Gold outputs.

For example, validate the relationship between:
gold_revenue_by_customer
gold_customer_segmentation
gold_sales_by_product

Do not assume the exact relationship if the schema/grain does not support it; inspect the implementation first.

E. DASHBOARD VALIDATION
Verify dashboard SQL references only the approved Gold objects.

Also verify:
- Top 10 revenue query sorts correctly by total_revenue DESC
- Top 10 quantity query sorts correctly by total_quantity DESC
- customer behavioral segmentation follows the documented logic
- customer revenue distribution uses the intended Gold customer-revenue data
- no unnecessary Silver/Bronze dependency exists

IMPORTANT:
Do not just write tests. For every important validation, document:
- what is being tested
- expected result
- actual result if it can be determined from existing repository evidence
- PASS/FAIL
- explanation of any known discrepancy

If a validation requires Databricks execution and cannot be executed from Cursor, clearly mark it as:
"REQUIRES DATABRICKS EXECUTION"
rather than pretending it passed.

Do not fabricate test results.

Finally produce a concise final validation report containing:

1. Repository structure reviewed
2. Tests already present
3. Tests added
4. Tests requiring Databricks execution
5. Dashboard validation status
6. Gold reconciliation status
7. Documentation gaps
8. Missing evaluation artifacts
9. Recommended next actions

Do not modify unrelated files.
Do not modify the existing working dashboard unless a concrete requirement violation is discovered.
Do not change business logic without explaining why first.

Start by inspecting the repository and report your findings BEFORE making modifications.
```

**AI RESPONSE SUMMARY:**

- Inspected Bronze → Silver → Gold → Dashboard implementation
- Created `src/validation/pipeline_validation.sql` (26 checks: sections A–E)
- Created `VALIDATION_REPORT.md`
- Local: `test_silver_helpers.py` PASS; `ingest_all.py --dry-run` PASS

**ARTIFACTS CREATED/MODIFIED:**

- `src/validation/pipeline_validation.sql`
- `VALIDATION_REPORT.md`

**VALIDATION / TESTING:**

- First Databricks run: 20 PASS, 3 SQL errors (schema/query issues in validation script only)
- After fixes: **26 / 26 PASS** on Databricks Serverless (2026-08-30)

**YOUR EVALUATION:**

- Failures were validation-script issues (`DESCRIBE` in subquery; `entity_name` vs `table_name`), not pipeline defects
- No Bronze/Silver/Gold/Dashboard logic changes required

**FINAL DECISION:** ACCEPTED — **26/26 PASS** final status

**Follow-up (not a separate numbered prompt):** Operator re-run exposed 3 validation-SQL defects (`DESCRIBE` in subquery; `entity_name` vs `table_name`). Fixes documented in `debugging.md` Debug 12–13 and git `1965d50`. Exact follow-up prompt text was not preserved.

---

*Smaller post-validation documentation updates (README/requirements status) are recorded in git history; not numbered as separate implementation prompts.*
---

## Prompt 31 — Next phase routing (task-breakdown)

**TYPE:** Planning

**PROMPT SENT:**

```text
Inspect the repository's `tool-specific/cursor-workflow/task-breakdown.md` and determine exactly what comes after the now-completed Phase 5 Gold.

Context:

* Phase 5 Gold is COMPLETE / ACCEPTED.
* Silver RI alignment is validated on Databricks Serverless.
* Gold Iteration 6 is validated on Databricks Serverless.
* AC-1 through AC-11 all PASS.
* Silver:

  * silver_customers = 878
  * silver_products = 164
  * silver_orders = 3,646
  * orphan product FKs = 0
  * orphan customer FKs = 0
* Silver revenue = 2,708,411.08
* Gold entity/trend revenue = 2,708,411.08
* Gold quantity = 10,899
* Distinct orders = 2,052
* Idempotency PASS.
* Gold SQL was not modified.

Do NOT modify any files.

Read:

1. tool-specific/cursor-workflow/task-breakdown.md
2. relevant project documentation needed to understand the current completion state

Then report:

1. The exact next phase/iteration name and number.
2. Its objective.
3. Its acceptance criteria.
4. Files that are expected to change.
5. Files that must NOT be changed unless explicitly required.
6. What needs to be implemented.
7. What needs to be validated locally.
8. What needs to be validated on Databricks Serverless.
9. Dependencies on the completed Silver/Gold work.
10. Any ambiguity or inconsistency you find in the task breakdown.

Important:

* Do not implement anything.
* Do not change documentation.
* Do not invent requirements.
* Treat Phase 5 Gold as frozen and accepted.
* Base the answer on the repository's actual task breakdown and documentation.
```

**AI RESPONSE SUMMARY:**

Confirmed Phase 6 Dashboard as next step.

**FINAL DECISION:** ACCEPTED (documented)
---

## Prompt 32 — Post-validation README / requirements update

**TYPE:** Documentation

**PROMPT SENT:**

```text
We have now completed Databricks validation of the entire pipeline.

IMPORTANT VALIDATION RESULT:
- src/validation/pipeline_validation.sql: 26/26 PASS
- Executed successfully on Databricks Serverless
- Bronze, Silver/DQ, Gold, reconciliation, and dashboard validation all passed
- No pipeline or dashboard implementation changes are required.

Now update ONLY:
1. README.md
2. requirements-analysis.md

Use the current repository implementation and VALIDATION_REPORT.md as the source of truth.

Requirements:

1. Inspect the actual implementation before editing.
2. Remove or update stale statements saying that Bronze, Silver, Gold, Dashboard, validation, etc. are "not started", if those statements are no longer accurate.
3. Accurately describe the implemented medallion architecture:
   - data generation
   - Bronze
   - Silver
   - data quality/quarantine
   - Gold
   - dashboard
   - validation
4. Accurately reflect that the Databricks validation suite is COMPLETE with 26/26 PASS.
5. Preserve the existing structure, terminology, and intent of the documents wherever possible.
6. Do not invent functionality.
7. Do not change Python/SQL pipeline code.
8. Do not change dashboard SQL.
9. Do not change dashboard pages.
10. Do not alter validation logic.
11. Do not remove useful existing documentation.
12. If a requirement is genuinely not implemented, leave it clearly marked as incomplete rather than falsely marking it complete.

After editing, provide:
- files modified
- sections modified
- stale statements corrected
- requirements now confirmed complete
- any remaining gaps
```

**AI RESPONSE SUMMARY:**

Updated README and requirements-analysis after 26/26 PASS.

**FINAL DECISION:** ACCEPTED (documented)
---

## Prompt 33 — Reflection requirements review

**TYPE:** Review

**PROMPT SENT:**

```text
Review the original project requirements and the existing reflection.md.

Do not modify anything yet.

Determine exactly what reflection questions/sections the evaluation requires.

For each required section, report:
1. Section/question
2. What the existing reflection.md currently contains
3. What information from the implemented project can be used to answer it
4. What information is still missing and would require my input

Use the actual implementation and VALIDATION_REPORT.md as evidence.

Do not invent personal experiences, challenges, decisions, or lessons that are not supported by the repository.
```

**AI RESPONSE SUMMARY:**

Audited reflection.md submission requirements vs repo.

**FINAL DECISION:** ACCEPTED (documented)
---

## Prompt 34 — AI prompts / provenance audit

**TYPE:** Audit

**PROMPT SENT:**

```text
Review the original DE_C1_Coding_Evaluation requirements and the current repository, especially:

- ai-prompts/
- data/
- DATA_GENERATION_NOTES.md
- tool-specific/cursor-workflow/
- project-context.md
- spec.md
- cursor-rules-or-instructions.md
- task-breakdown.md
- VALIDATION_REPORT.md
- final-ai-usage-summary.md
- README.md
- requirements-analysis.md

IMPORTANT SUBMISSION REQUIREMENT:

The final submission must preserve the prompt history used by everyone/AI tools during creation of this project, together with the generated datasets.

Therefore, treat ai-prompts/ as an IMPORTANT AUDIT/PROVENANCE ARTIFACT, not merely as a high-level description of AI usage.

Do NOT modify anything yet.

First perform a complete audit of the AI prompt history and dataset provenance.

==================================================
PART 1 — AI PROMPT HISTORY AUDIT
==================================================

Inspect the entire ai-prompts/ directory recursively.

Create an inventory of every prompt file/artifact, including:

- filename/path
- phase/layer it relates to
- purpose of the prompt
- whether it appears to be an original prompt, iteration, correction, validation prompt, debugging prompt, or finalization prompt
- whether the resulting implementation/artifact can be identified
- whether the prompt history appears complete for that phase
- whether any important prompt appears to be missing

Preserve the ACTUAL prompt wording wherever it exists.

Do NOT summarize away the actual prompts.

The final submission should allow an evaluator to understand the sequence of AI-assisted development from the prompt history itself.

==================================================
PART 2 — PROMPT → OUTPUT/ARTIFACT TRACEABILITY
==================================================

For each identifiable prompt or prompt group, determine:

1. What was requested?
2. What AI-generated output/artifact resulted?
3. What repository file(s) contain that result?
4. Was the result subsequently reviewed, modified, corrected, tested, or rejected?
5. What validation/evidence supports the final result?

Where the repository contains evidence, cite the exact file/path.

Do NOT invent missing relationships.

If a prompt's resulting artifact cannot be confidently established, explicitly mark it as "traceability not established".

==================================================
PART 3 — DATASET PROVENANCE
==================================================

Inspect the generated datasets and all documentation related to their generation.

Document the actual generated datasets, including where supported:

- dataset/file name
- purpose
- schema/columns
- row count
- generation method
- seed
- intentional defects/injections
- relationship between datasets
- generation script
- generation notes/documentation
- downstream Bronze/Silver/Gold usage

In particular, preserve the provenance of the generated datasets rather than merely stating that datasets were generated.

The current project evidence indicates generated datasets including customers, products, and order-line data. Verify the actual values directly from the repository before documenting them.

Do not invent dataset statistics.

==================================================
PART 4 — AI DEVELOPMENT PROCESS
==================================================

Inspect the repository evidence for how AI was actually used during development.

Document, where evidence exists:

- requirements analysis
- architecture/design
- data generation
- Bronze implementation
- Silver implementation
- data-quality rules
- quarantine/DQ handling
- Gold implementation
- dashboard SQL
- dashboard design
- validation
- debugging
- documentation
- final review

For each area distinguish between:

A. AI-generated/proposed work
B. Developer review or modification
C. Testing/validation performed
D. Final accepted implementation
E. Rejected/changed AI suggestions, if documented

Do not fabricate developer actions or AI usage that cannot be supported.

==================================================
PART 5 — COMPLETENESS OF ai-prompts/
==================================================

Determine whether ai-prompts/ is detailed enough to satisfy the requirement:

"The prompt history that everyone has used to create the project along with the generated datasets should be included as an important artefact."

Classify the result as:

- COMPLETE
- MOSTLY COMPLETE — minor gaps
- INCOMPLETE — significant prompt history missing

For every gap, identify exactly what is missing.

Do NOT create reconstructed prompts and present them as historical prompts.

If historical prompts exist elsewhere in the repository, identify where they are and whether they should be consolidated/referenced.

==================================================
PART 6 — final-ai-usage-summary.md
==================================================

After completing the audit above, inspect the existing final-ai-usage-summary.md.

Determine whether it adequately documents:

1. AI tools used
2. Purpose of AI usage
3. Actual prompt history
4. Iterative prompting
5. AI-generated artifacts
6. Developer review/modification
7. Validation/testing
8. Debugging iterations
9. Dataset generation prompts/provenance
10. Final accepted/rejected outputs
11. Links/paths to the detailed prompt history in ai-prompts/
12. Links/paths to generated datasets and dataset-generation documentation

IMPORTANT:

The final-ai-usage-summary.md should NOT replace the detailed prompt history.

Instead:

- ai-prompts/ = detailed historical prompt evidence
- final-ai-usage-summary.md = structured summary/index of that evidence

The summary should point the evaluator to the detailed prompts and generated datasets.

If the existing ai-prompts/ content is already sufficient, preserve it rather than unnecessarily rewriting it.

==================================================
PART 7 — REQUIRED OUTPUT BEFORE EDITING
==================================================

Do NOT edit any files yet.

Return a report containing:

A. AI prompt inventory
B. Dataset inventory/provenance
C. Prompt → artifact traceability
D. AI usage by project phase
E. Missing prompt-history evidence
F. Missing dataset-provenance evidence
G. Assessment of whether ai-prompts/ satisfies the submission requirement
H. Specific changes recommended for final-ai-usage-summary.md
I. Any additional artifacts that should be added
J. Any information that cannot be established from repository evidence and therefore requires user input

Most importantly:

DO NOT fabricate historical prompts.

If actual prompt history exists, preserve the actual wording and identify it.
If something is missing, clearly mark it as missing rather than reconstructing it as if it were historical evidence.
```

**AI RESPONSE SUMMARY:**

Full ai-prompts and dataset provenance audit (Parts A–J).

**FINAL DECISION:** ACCEPTED (documented)
---

## Prompt 35 — Step 4 — submission closure artifacts

**TYPE:** Closure

**PROMPT SENT:**

```text
# Step 4 — Finalize AI Prompt History, Dataset Provenance & Submission Closure Artifacts

You are working on the DE_C1_Coding_Evaluation repository.

The pipeline implementation, dashboard, and end-to-end validation are already complete.

IMPORTANT CURRENT STATUS:
- Pipeline validation is COMPLETE: 26 / 26 checks PASS on Databricks Serverless.
- Dashboard validation is PASS.
- Gold reconciliation is PASS.
- Bronze/Silver/Gold implementation is complete.
- Dashboard consists of 3 implemented pages.
- Generated datasets are present under data/.
- ai-prompts/ already contains substantial phase-by-phase prompt history.
- Do NOT modify working Bronze/Silver/Gold/Dashboard implementation unless you discover an actual validation failure.
- This task is primarily about FINAL SUBMISSION DOCUMENTATION, PROVENANCE, TRACEABILITY, and CLOSURE.

## PRIMARY REQUIREMENT

The final repository must preserve an auditable record of:

1. The AI prompts used to create/develop the project.
2. The generated datasets used by the project.
3. The relationship between prompts → generated artifacts → validation → final accepted implementation.
4. AI-assisted debugging and validation activities.
5. Human/developer review and final decisions.
6. Any prompt-history gaps that cannot be established from the repository.

The evaluator specifically requires an artefact containing the prompt history used during project creation together with the generated datasets.

Therefore, treat `ai-prompts/` + `data/` + provenance documentation as a formal submission artifact, not merely informal documentation.

---

# PART A — AUDIT EXISTING AI PROMPT HISTORY

First inspect the entire repository, especially:

- ai-prompts/
- data/
- src/
- DATA_GENERATION_NOTES.md
- BRONZE_LAYER_NOTES.md
- SILVER_LAYER_NOTES.md
- GOLD_LAYER_NOTES.md
- DASHBOARD_GUIDE.md
- VALIDATION_REPORT.md
- README.md
- requirements-analysis.md
- data-model.md
- data-quality-strategy.md
- reflection.md
- final-ai-usage-summary.md (if present)
- debugging-notes.md (if present)
- tool-specific/cursor-workflow/
- git history if available

Do NOT assume that an existing summary is equivalent to a historical prompt.

For every existing `ai-prompts/*.md` file, determine:

- phase
- prompt number/iteration
- whether PROMPT SENT is verbatim or a faithful summary
- AI RESPONSE SUMMARY
- YOUR EVALUATION
- FINAL DECISION
- generated/modified artifacts
- validation evidence
- whether developer review is documented

Preserve existing accurate history.

Do not rewrite existing prompt history unnecessarily.

---

# PART B — PRESERVE PROMPT HISTORY

The `ai-prompts/` directory is the PRIMARY detailed prompt provenance artifact.

Ensure it covers the major development phases:

1. Foundation / requirements
2. Data generation
3. Bronze
4. Silver
5. Gold
6. Dashboard
7. Debugging
8. Validation
9. Final documentation / closure

For every prompt that is actually available in repository history or provided source material:

Use this structure:

## Prompt N — <short description>

**TYPE:** Original / Iteration / Debugging / Validation / Correction

**PROMPT SENT:**

> <exact original prompt where available>

If exact wording is NOT available:

**PROMPT SENT — FAITHFUL SUMMARY:**

> <clearly labeled faithful summary>

Do NOT present reconstructed wording as an original prompt.

**AI RESPONSE SUMMARY:**
- ...

**ARTIFACTS CREATED/MODIFIED:**
- ...

**VALIDATION / TESTING:**
- ...

**YOUR EVALUATION:**
- ...

**FINAL DECISION:**
- ACCEPTED / MODIFIED / REJECTED / DEFERRED

---

# PART C — CLOSE THE KNOWN PROMPT-HISTORY GAPS

Audit specifically for these known gaps:

1. ai-prompts/debugging.md
2. validation-phase prompt history
3. Silver RI alignment prompt
4. Gold Iteration 6 prompt
5. Dashboard Iteration 1 prompt
6. Dashboard Iteration 3 prompt
7. Data-generation original prompt
8. Original project kickoff prompt
9. Recent README/requirements documentation prompts
10. Any closure/reflection/final-summary prompts

For each gap:

- Search repository/git history/conversation-accessible material for the actual prompt.
- If actual wording is available, preserve it.
- If only a faithful summary is available, explicitly label it as a summary.
- If it cannot be established, DO NOT invent it.

For example:

**PROMPT SENT — NOT AVAILABLE IN REPOSITORY**

The original prompt text could not be established from repository evidence. Related implementation and validation evidence is documented here...

This is preferable to fabricated historical text.

---

# PART D — CREATE / COMPLETE ai-prompts/debugging.md

Create:

`ai-prompts/debugging.md`

if it does not already exist.

Consolidate debugging history from:

- Bronze Spark/session issues
- Databricks `!python` / Spark Connect issues
- Silver Serverless compatibility issues
- Silver RI alignment issue
- Quarantine/DQ-summary issues
- Dashboard `order_count` issue
- Validation SQL issues
- Any other documented debugging iterations

IMPORTANT:

This file is a CROSS-REFERENCE/CONSOLIDATION artifact.

Do not falsely claim that every consolidated item came from a standalone debugging prompt.

Where the original debugging prompt exists, preserve it.

Where debugging was documented only inside another phase file, reference that file.

---

# PART E — CREATE / COMPLETE VALIDATION PROMPT HISTORY

Create:

`ai-prompts/validation.md`

if appropriate.

Document the AI-assisted work that resulted in:

- src/validation/pipeline_validation.sql
- VALIDATION_REPORT.md

Include:

- prompt history where available
- AI response summary
- changes made to validation SQL
- the three validation-query corrections
- final Databricks execution
- final result: 26 / 26 PASS

If the original validation prompt is unavailable, clearly state:

"Original validation prompt text was not preserved in the repository; this entry documents the resulting artifact and available implementation evidence only."

Do not fabricate a prompt.

---

# PART F — DATASET PROVENANCE MUST BE EXPLICIT

The generated datasets are part of the required provenance artifact.

Document the relationship:

AI prompt
    ↓
generate_sample_data.py
    ↓
generated CSV datasets
    ↓
Bronze ingestion
    ↓
Silver DQ / quarantine
    ↓
Gold aggregation
    ↓
Dashboard

Explicitly document:

### Generated datasets

- data/customers.csv
- data/products.csv
- data/orders.csv

For each dataset record:

- purpose
- schema
- row count
- generator script
- generation seed
- generation parameters
- intentional defects
- defect IDs
- downstream usage

Current known committed dataset counts:

- customers.csv — 1,006 data rows
- products.csv — 206 data rows
- orders.csv — 5,163 data rows

Generation:

- default seed = 42
- generation script = src/data_generation/generate_sample_data.py
- Python standard library only
- clean generation followed by intentional defect injection

Document the D01–D17 defect matrix using the existing
DATA_GENERATION_NOTES.md and generator implementation.

Do not invent additional defects or statistics.

---

# PART G — DATASET → PROMPT TRACEABILITY

Create a clear traceability table showing:

| Prompt / Phase | AI-assisted activity | Dataset/artifact produced | Validation |
|---|---|---|---|
| Data generation | Sample-data generation | data/*.csv | row counts / defect checks / reproducibility |
| Bronze | Ingestion | Bronze tables | ingestion + defect preservation |
| Silver | DQ + cleansing | Silver curated/quarantine | DQ validation |
| Gold | Aggregations | Gold tables | reconciliation |
| Dashboard | Gold-only analytics | dashboard SQL/pages | dashboard validation |
| Validation | End-to-end checks | pipeline_validation.sql | 26/26 PASS |

This table should make it obvious to an evaluator that the generated datasets are not orphaned files: they are the actual source data used throughout the pipeline.

---

# PART H — CREATE final-ai-usage-summary.md

Create:

`final-ai-usage-summary.md`

This is an INDEX and EXECUTIVE SUMMARY.

Do NOT duplicate all prompt history into this file.

It should point the evaluator to the detailed `ai-prompts/` files.

Include:

## 1. AI tools used

Only state tools that can be established from repository evidence.

Do not guess.

## 2. Purpose of AI usage

Summarize use of AI for:

- requirements/design
- data generation
- pipeline implementation
- debugging
- dashboard SQL/design
- validation
- documentation

## 3. Prompt history index

Table:

| Phase | Detailed prompt file | Main artifacts | Status |
|---|---|---|---|

Include all `ai-prompts/*.md`.

## 4. Iterative development

Summarize the documented iterations:

- Data generation
- Bronze
- Silver
- Gold
- Dashboard
- Debugging
- Validation

## 5. AI-generated / AI-assisted artifacts

Map prompts to:

- src/data_generation/
- src/bronze/
- src/silver/
- src/gold/
- src/dashboard/
- src/validation/
- documentation

## 6. Human review

Explain that AI output was reviewed, modified where necessary, tested, and accepted/rejected based on validation.

Link/reference the `YOUR EVALUATION` and `FINAL DECISION` sections.

## 7. Validation

Reference:

- VALIDATION_REPORT.md
- src/validation/pipeline_validation.sql
- layer notes
- final 26/26 PASS result

## 8. Debugging

Reference:

- ai-prompts/debugging.md
- bronze-layer.md
- silver-layer.md
- dashboard.md

Clearly distinguish original prompt evidence from consolidated summaries.

## 9. Dataset provenance

Explicitly reference:

- data/customers.csv
- data/products.csv
- data/orders.csv
- src/data_generation/generate_sample_data.py
- src/data_generation/DATA_GENERATION_NOTES.md
- seed 42
- intentional defect matrix D01–D17

## 10. Known provenance limitations

Clearly list any prompts whose exact original wording could not be recovered.

Do NOT hide these gaps.

Do NOT reconstruct them and label them as original.

---

# PART I — COMPLETE debugging-notes.md

If required by the submission structure, create:

`debugging-notes.md`

This should be a concise chronological debugging log.

Include:

- issue
- symptom/error
- investigation
- resolution
- affected files
- validation after fix

Cross-reference the detailed prompt history rather than duplicating large prompts.

---

# PART J — REFLECTION

Complete `reflection.md` if it is currently only a placeholder.

Base it strictly on the actual project evidence.

Include:

- what was learned
- where AI was useful
- where human review was required
- important debugging lessons
- data-quality lessons
- Databricks implementation lessons
- what would be improved in a future implementation

Do not fabricate experiences that are not supported by the repository history.

---

# PART K — README / DOCUMENTATION STATUS

Inspect:

- README.md
- requirements-analysis.md
- data-quality-strategy.md
- tool-specific/cursor-workflow/spec.md
- tool-specific/cursor-workflow/project-context.md
- tool-specific/cursor-workflow/task-breakdown.md

Update stale "not started" status statements ONLY where the current implementation evidence clearly establishes completion.

Do not redesign documentation unnecessarily.

Do not change implementation code.

---

# PART L — FINAL PROVENANCE CHECK

At the end, verify that an evaluator can answer all of these questions from the repository:

1. What AI tools were used?
2. What prompts were used?
3. Where is the detailed prompt history?
4. Which prompts generated the datasets?
5. Where are the generated datasets?
6. What seed generated them?
7. What defects were intentionally injected?
8. Which pipeline artifacts were created from those datasets?
9. Which AI iterations were used for Bronze/Silver/Gold/Dashboard?
10. What debugging occurred?
11. What validation work was AI-assisted?
12. What was human-reviewed?
13. What was accepted/rejected/modified?
14. What is the final validation result?
15. Which historical prompt details could not be recovered?

The evaluator should be able to trace:

PROMPT HISTORY
      ↓
DATASET GENERATION
      ↓
BRONZE
      ↓
SILVER + DQ
      ↓
GOLD
      ↓
DASHBOARD
      ↓
VALIDATION
      ↓
FINAL SUBMISSION

---

# IMPORTANT SAFETY / ACCURACY RULES

1. Do NOT fabricate historical prompts.
2. Do NOT turn a reconstructed prompt into a verbatim prompt.
3. Clearly distinguish:
   - VERBATIM PROMPT
   - FAITHFUL SUMMARY
   - REPOSITORY-DERIVED CONTEXT
   - UNKNOWN / NOT RECOVERABLE
4. Do not alter working pipeline logic.
5. Do not alter dashboard logic merely for documentation.
6. Do not change generated datasets.
7. Do not regenerate the datasets unless required for validation.
8. Preserve existing correct prompt history.
9. Do not invent AI tools or models.
10. Do not invent developer decisions.
11. Use the existing validation evidence.
12. Final validation remains 26/26 PASS.
13. The generated datasets under data/ must remain committed and traceable to the generation script.
14. `ai-prompts/` is the detailed historical record; `final-ai-usage-summary.md` is only the evaluator-facing index/summary.

---

# FINAL OUTPUT

After making the documentation changes, provide:

1. Files created
2. Files modified
3. Prompt-history coverage
4. Dataset-provenance coverage
5. Remaining historical gaps, if any
6. Confirmation that no pipeline/dashboard implementation was changed
7. Final validation status: 26/26 PASS
```

**AI RESPONSE SUMMARY:**

Created closure artifacts: debugging.md, validation index, final-ai-usage-summary, reflection.

**FINAL DECISION:** ACCEPTED (documented)

