# AI Prompts — Data Generation (Phase 2)

**Prompts in this file:** 04  
**Implementation order:** Sample data generation → CSV validation

Significant prompts include full **PROMPT SENT** text; results follow each prompt block.

---

## Prompt 04 — Phase 2 — Data generation

**TYPE:** Implementation

**PROMPT SENT:**

```text
We are now starting Phase 2 of the project: DATA GENERATION.

Do NOT re-inspect or re-scaffold the repository. Phase 1 is already complete and accepted.

The repository root is:
DE_C1_Coding_Evaluation

Phase 1 foundation documentation already exists and must be treated as the authoritative project baseline:

- README.md
- candidate-info.md
- tool-workflow.md
- requirements-analysis.md
- design-notes.md
- data-model.md
- data-quality-strategy.md
- ai-prompts/documentation.md

Before implementing anything, read those documents, especially:

- requirements-analysis.md
- design-notes.md
- data-model.md
- data-quality-strategy.md
- tool-workflow.md
- README.md

Also understand that this project is being developed specifically to demonstrate strong Cursor-assisted development.

==================================================
PHASE 2 — DATA GENERATION
==================================================

Implement ONLY the data-generation phase.

Create:

src/
└── data_generation/
    ├── generate_sample_data.py
    └── DATA_GENERATION_NOTES.md

and generate the corresponding source data:

data/
├── customers.csv
├── orders.csv
└── products.csv

Do NOT implement Bronze, Silver, Gold, Dashboard, or database setup yet.

==================================================
DATA MODEL DECISION
==================================================

Use a practical retail/e-commerce model suitable for a Databricks medallion pipeline.

Before writing the generator, resolve the previously open modeling question around order granularity.

Use a line-item-oriented orders dataset so that:

- one customer can have many orders
- one order can contain multiple products
- one product can appear in many orders
- revenue can be derived consistently from quantity × unit_price
- referential-integrity checks can later validate customer_id and product_id

Document this decision in data-model.md and explain why it was selected.

Establish the physical schemas now rather than leaving them TBD.

Use clear, realistic columns and appropriate data types when generated into the CSVs.

The schemas must support all planned Gold analytics:

- sales by product
- revenue by customer
- daily/weekly trends
- customer segmentation

They must also support all five planned Silver quality checks:

1. completeness
2. uniqueness
3. type validation
4. referential integrity
5. business logic

==================================================
INTENTIONAL DATA QUALITY DEFECTS
==================================================

The sample data must deliberately contain realistic bad records so that the later Silver phase has something meaningful to detect.

Include examples of:

- missing required values
- duplicate business keys
- invalid date/type values
- orphan customer/product references
- invalid business values such as non-positive quantity
- at least one additional realistic data-quality issue if useful

Do NOT randomly corrupt data without documenting it.

Create a deliberate defect matrix.

For every intentional defect type, document:

- defect type
- affected dataset
- affected column
- approximate number of records
- why it was introduced
- which future Silver quality check should detect it
- whether it should eventually be rejected, quarantined, or corrected

Do not implement the Silver handling yet.

The generated dataset should remain manageable for local development and Databricks testing while being large enough to demonstrate meaningful processing.

==================================================
GENERATOR REQUIREMENTS
==================================================

generate_sample_data.py should:

- be deterministic/reproducible using a configurable random seed
- allow dataset size to be configured
- generate customers, products and orders consistently
- preserve valid relationships for normal records
- deliberately inject documented bad records
- avoid hardcoded credentials or environment-specific secrets
- use clear functions rather than one giant script
- include useful comments/docstrings
- make it obvious which data is valid and which data is intentionally defective
- write CSVs into the repository's data/ directory
- print useful generation statistics

The generator should be executable from the repository root.

Use Python appropriately; do not introduce unnecessary dependencies.

==================================================
DOCUMENTATION — MUST HAPPEN IN THIS SAME TASK
==================================================

Do NOT treat documentation as a later task.

Create:

src/data_generation/DATA_GENERATION_NOTES.md

It must document:

- dataset purpose
- physical schemas
- generation approach
- row counts
- relationships
- deterministic seed
- intentional defect strategy
- defect counts
- mapping between defects and future Silver checks
- how to execute the generator
- limitations/assumptions

Update:

data-model.md

with the now-finalized physical model and order line-item decision.

Update:

data-quality-strategy.md

with the concrete fields/rules that can now be defined based on the generated schemas.

Update:

requirements-analysis.md

only where Phase 2 decisions resolve previously TBD requirements.

Update:

README.md

to reflect that data generation is now implemented, while Bronze and later phases remain not started.

==================================================
CURSOR-SPECIFIC EVIDENCE
==================================================

The project must also satisfy the Cursor-user assessment expectations.

Create the directory:

tool-specific/cursor-workflow/

with:

- project-context.md
- spec.md
- cursor-rules-or-instructions.md
- task-breakdown.md

These are evidence artifacts, not generic documentation.

For this phase:

project-context.md
------------------
Document how the existing project context was supplied to Cursor, including the role of the Phase 1 foundation documents as persistent project context.

spec.md
--------
Document the data-generation specification Cursor is implementing, including schemas, relationships, reproducibility, defect strategy, and constraints.

cursor-rules-or-instructions.md
-------------------------------
Record the project instructions/rules being used for Cursor-assisted development, including:
- respect existing architecture
- implement incrementally
- do not invent requirements
- no secrets
- documentation must accompany implementation
- validate generated code
- preserve prompt/evaluation evidence
- do not implement future phases prematurely

task-breakdown.md
-----------------
Break Phase 2 into explicit tasks/subtasks and mark their status.

==================================================
AI PROMPT ARTIFACT
==================================================

Create:

ai-prompts/data-generation.md

Record this prompt using the established structure from ai-prompts/documentation.md:

PROMPT SENT
AI RESPONSE SUMMARY
YOUR EVALUATION
FINAL DECISION

Also record meaningful follow-up/refinement prompts and outcomes in this file.

Do not fabricate evaluation results. If validation reveals a problem, document the actual iteration.

==================================================
VALIDATION
==================================================

After implementation:

1. Run the generator.
2. Confirm all three CSV files exist.
3. Inspect schemas and representative records.
4. Verify relationships among valid records.
5. Verify intentional defects actually exist.
6. Verify documented defect counts match the generated data.
7. Run the generator again with the same seed and verify reproducibility.
8. Check Python syntax/errors.
9. Review generated code against the existing project documents.
10. Run git diff and git status.

Do not claim anything was validated unless you actually performed the validation.

If something fails, fix it and document the iteration.

==================================================
IMPORTANT SCOPE RULE
==================================================

Do NOT create:

- src/bronze/
- src/silver/
- src/gold/
- src/dashboard/

Do NOT implement Bronze ingestion yet.

Do NOT create Gold SQL.

Do NOT create dashboard queries.

Do NOT create database implementation artifacts.

This task ends when Phase 2 data generation and its associated documentation/Cursor evidence are complete and validated.

Do NOT commit or push to GitHub.

At the end, provide a concise implementation report containing:

- files created
- files updated
- dataset schemas
- generated row counts
- intentional defect counts
- validation performed
- issues encountered and fixes
- git status
- anything requiring my review/decision

Then STOP.
```

**AI RESPONSE SUMMARY:**

- Implemented `generate_sample_data.py` with clean generation + defect injection (`DEFECT_COUNTS`)
- Chose **order line-item** model: `order_line_id` PK, `order_id` groups lines
- Generated CSVs: 1,006 customers, 206 products, 5,163 order lines (default seed 42)
- 17 defect types, 328 injections, mapped to Silver modules
- Created `DATA_GENERATION_NOTES.md`, updated foundation docs, Cursor workflow artifacts
- Fixed duplicate-row injection counts (6 customer/product dup rows) and argparse typo during validation

**YOUR EVALUATION:**

- ✓ **What was good:**
  - Line-item order model supports multi-product orders and revenue derivation
  - Defect matrix is explicit with Silver check mapping
  - Reproducibility verified (MD5 match on re-run with seed 42)
  - Stdlib-only; no unnecessary dependencies

- △ **What may need review:**
  - Default volumes (1K/200/5K) — confirm acceptable for assessment
  - Overlapping mutations on same customer row possible (documented)
  - `lifetime_value` not derived from orders (documented limitation)

- ✗ **Issues found during validation:**
  - Initial duplicate defect count reported 3 instead of 6 — **fixed** in generator
  - Argparse indentation typo — **fixed**

**FINAL DECISION:** **ACCEPTED** — Generator, CSVs, defect matrix, and reproducibility validated. Committed datasets: `data/customers.csv` (1,006 rows), `data/products.csv` (206), `data/orders.csv` (5,163); seed **42**.

---

## Validation Log (actual)

| Step | Command / action | Result |
|------|------------------|--------|
| Syntax | `python3 -m py_compile src/data_generation/generate_sample_data.py` | Pass |
| Generate | `python3 src/data_generation/generate_sample_data.py` | Pass |
| Row counts | customers=1006, products=206, orders=5163 | Pass |
| NULL emails | count=50 | Pass |
| Orphan FKs | customer=25, product=25 | Pass |
| Reproducibility | Re-run seed 42, MD5 hashes match | Pass |
