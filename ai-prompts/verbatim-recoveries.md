# Verbatim Prompt Recoveries

> **Provenance note:** These prompts were recovered from project development session records during final submission closure (2026-08-30). They were **not** all originally filed in `ai-prompts/` at the time of implementation. Where an `ai-prompts/<phase>.md` file already contains a **PROMPT SENT** block, that file remains the primary phase artifact; this document supplements gaps with **verbatim** wording.
>
> **Phase 1 foundation prompts** (repository inspection, foundation docs, submission templates) are already recorded in `ai-prompts/documentation.md` with verbatim or near-verbatim text.
>
> Do not treat text in this file as retroactively replacing earlier faithful summaries unless explicitly cross-referenced.

---


## Original Project Kickoff (Aug 21, 2026)

**Recovery key:** `original-project-kickoff`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> You are the Lead Data Engineer, Databricks Architect, AI-assisted Software Engineer, and technical documentation owner for this project.
> We are building a Databricks data engineering project in this repository:
> 
> databricks-medallion-pipeline/
> 
> The project will be developed incrementally. Do not implement the entire project now.
> 
> The following is the intended repository structure:
> 
> databricks-medallion-pipeline/
> ├── README.md
> ├── candidate-info.md
> ├── tool-workflow.md                    # Part A: AI Workflow Foundation
> ├── requirements-analysis.md
> ├── design-notes.md
> ├── data-model.md
> ├── data-quality-strategy.md
> │
> ├── src/
> │   ├── data_generation/
> │   │   ├── generate_sample_data.py
> │   │   └── DATA_GENERATION_NOTES.md
> │   ├── bronze/
> │   │   ├── 01_ingest_customers.py
> │   │   ├── 02_ingest_orders.py
> │   │   ├── 03_ingest_products.py
> │   │   └── ingest_all.py
> │   ├── silver/
> │   │   ├── 01_quality_completeness.py
> │   │   ├── 02_quality_uniqueness.py
> │   │   ├── 03_quality_type_validation.py
> │   │   ├── 04_quality_referential_integrity.py
> │   │   ├── 05_quality_business_logic.py
> │   │   └── create_silver_tables.py
> │   ├── gold/
> │   │   ├── 01_sales_by_product.sql
> │   │   ├── 02_revenue_by_customer.sql
> │   │   ├── 03_daily_weekly_trends.sql
> │   │   ├── 04_customer_segmentation.sql
> │   │   └── create_gold_tables.py
> │   └── dashboard/
> │       ├── dashboard_queries.sql
> │       └── DASHBOARD_GUIDE.md
> │
> ├── data/
> │   ├── customers.csv
> │   ├── orders.csv
> │   └── products.csv
> │
> ├── database/
> │   ├── schema.sql
> │   ├── seed-data-notes.md
> │   └── setup-notes.md
> │
> ├── debugging-notes.md
> ├── reflection.md
> ├── final-ai-usage-summary.md
> │
> └── ai-prompts/
>     ├── data-generation.md
>     ├── bronze-layer.md
>     ├── silver-layer.md
>     ├── gold-layer.md
>     ├── dashboard.md
>     ├── debugging.md
>     └── documentation.md
> 
> PROJECT OBJECTIVE
> 
> Build a complete, coherent Databricks medallion-architecture project covering:
> 
> Raw/sample data
>     ↓
> Bronze
>     ↓
> Silver + data quality
>     ↓
> Gold
>     ↓
> Analytics/dashboard
> 
> The project should demonstrate practical data engineering concepts rather than simply creating placeholder files.
> 
> The implementation must remain internally consistent across:
> - requirements
> - architecture/design
> - data model
> - generated data
> - Bronze ingestion
> - Silver transformations and quality checks
> - Gold analytical datasets
> - dashboard queries
> - documentation
> 
> IMPORTANT DEVELOPMENT RULE
> 
> We will work incrementally.
> 
> Do NOT:
> - implement Bronze, Silver, Gold, dashboard, etc. all at once
> - invent requirements that have not yet been provided
> - create fake implementations merely to populate the directory
> - make architectural decisions that should be discussed later
> - rewrite the entire repository unnecessarily
> 
> Wait for subsequent instructions before implementing individual project phases.
> 
> DOCUMENTATION MUST BE CREATED ALONGSIDE THE WORK
> 
> Documentation is not a final-stage activity.
> 
> We must avoid documentation debt.
> 
> Whenever a project phase is implemented, the relevant documentation must be created or updated as part of that same phase.
> 
> For example:
> 
> Data generation
> → implementation + DATA_GENERATION_NOTES.md + relevant ai-prompts entry
> 
> Bronze
> → Bronze code + relevant design/documentation + ai-prompts/bronze-layer.md
> 
> Silver
> → Silver code + data-quality documentation + ai-prompts/silver-layer.md
> 
> Gold
> → Gold SQL/Python + analytical/design documentation + ai-prompts/gold-layer.md
> 
> Dashboard
> → dashboard queries + DASHBOARD_GUIDE.md + ai-prompts/dashboard.md
> 
> PROMPT RECORDING REQUIREMENT
> 
> The prompts used to generate/implement each major project phase are themselves project artifacts.
> 
> Maintain:
> 
> ai-prompts/data-generation.md
> ai-prompts/bronze-layer.md
> ai-prompts/silver-layer.md
> ai-prompts/gold-layer.md
> ai-prompts/dashboard.md
> ai-prompts/debugging.md
> ai-prompts/documentation.md
> 
> When a phase is implemented, the actual implementation prompt/instruction used for that phase must be recorded in the corresponding file.
> 
> Do not wait until the end of the project to reconstruct the prompts.
> 
> Where useful, also record:
> - important follow-up prompts
> - debugging prompts
> - prompts that caused meaningful design changes
> - prompts used to improve or refactor an implementation
> 
> Do not fill these files with meaningless commentary. They should preserve the actual AI-assisted development trail.
> 
> DOCUMENTATION QUALITY
> 
> Documentation should explain the actual implementation rather than generic theory.
> 
> Where applicable, document:
> - purpose
> - assumptions
> - architecture decisions
> - data flow
> - schema
> - transformations
> - data-quality rules
> - important implementation decisions
> - validation/testing performed
> - known limitations
> - debugging decisions
> - AI-assisted development decisions
> 
> Documentation must remain synchronized with the actual code.
> 
> If implementation changes, update the relevant documentation.
> 
> AI-ASSISTED DEVELOPMENT RECORD
> 
> The project intentionally demonstrates responsible AI-assisted development.
> 
> Therefore, preserve meaningful evidence of how AI was used.
> 
> The final project should make it possible to understand:
> - what was generated with AI
> - what was reviewed/modified
> - what was tested
> - what debugging was required
> - what important decisions were made by the developer
> 
> Do not fabricate human review or testing that did not actually occur.
> 
> GIT DISCIPLINE
> 
> This repository is already connected to GitHub.
> 
> Work should be organized into logical milestones.
> 
> After completing a meaningful milestone:
> - inspect git status
> - identify changed files
> - ensure documentation and prompt artifacts are included
> - provide a concise summary
> - suggest a meaningful commit message
> 
> Do not automatically push to GitHub unless explicitly instructed.
> 
> Do not create meaningless commits for every tiny modification.
> 
> CODE QUALITY
> 
> Code should be:
> - readable
> - modular
> - appropriately commented
> - maintainable
> - consistent with the rest of the repository
> - suitable for a practical Databricks data engineering project
> 
> Avoid unnecessary complexity.
> 
> Do not introduce dependencies unless they are justified.
> 
> Do not hard-code credentials, secrets, tokens, passwords, or connection credentials.
> 
> FIRST TASK
> 
> For now, ONLY inspect the current repository.
> 
> Do not implement the project yet.
> 
> Determine:
> 
> 1. Current repository structure.
> 2. Which files/directories already exist.
> 3. Which intended files are currently missing.
> 4. Current Git status.
> 5. Current branch.
> 6. Whether the repository already contains any configuration files.
> 7. Whether any existing files contain work that must be preserved.
> 
> Do not delete or overwrite existing work.
> 
> After inspection, report:
> 
> - Current state
> - Existing files
> - Missing intended files
> - Git status
> - Any observations or potential issues
> 
> Then STOP and wait for the next instruction.


---


## Phase 2 — Data Generation

**Recovery key:** `phase2-data-generation`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> We are now starting Phase 2 of the project: DATA GENERATION.
> 
> Do NOT re-inspect or re-scaffold the repository. Phase 1 is already complete and accepted.
> 
> The repository root is:
> DE_C1_Coding_Evaluation
> 
> Phase 1 foundation documentation already exists and must be treated as the authoritative project baseline:
> 
> - README.md
> - candidate-info.md
> - tool-workflow.md
> - requirements-analysis.md
> - design-notes.md
> - data-model.md
> - data-quality-strategy.md
> - ai-prompts/documentation.md
> 
> Before implementing anything, read those documents, especially:
> 
> - requirements-analysis.md
> - design-notes.md
> - data-model.md
> - data-quality-strategy.md
> - tool-workflow.md
> - README.md
> 
> Also understand that this project is being developed specifically to demonstrate strong Cursor-assisted development.
> 
> ==================================================
> PHASE 2 — DATA GENERATION
> ==================================================
> 
> Implement ONLY the data-generation phase.
> 
> Create:
> 
> src/
> └── data_generation/
>     ├── generate_sample_data.py
>     └── DATA_GENERATION_NOTES.md
> 
> and generate the corresponding source data:
> 
> data/
> ├── customers.csv
> ├── orders.csv
> └── products.csv
> 
> Do NOT implement Bronze, Silver, Gold, Dashboard, or database setup yet.
> 
> ==================================================
> DATA MODEL DECISION
> ==================================================
> 
> Use a practical retail/e-commerce model suitable for a Databricks medallion pipeline.
> 
> Before writing the generator, resolve the previously open modeling question around order granularity.
> 
> Use a line-item-oriented orders dataset so that:
> 
> - one customer can have many orders
> - one order can contain multiple products
> - one product can appear in many orders
> - revenue can be derived consistently from quantity × unit_price
> - referential-integrity checks can later validate customer_id and product_id
> 
> Document this decision in data-model.md and explain why it was selected.
> 
> Establish the physical schemas now rather than leaving them TBD.
> 
> Use clear, realistic columns and appropriate data types when generated into the CSVs.
> 
> The schemas must support all planned Gold analytics:
> 
> - sales by product
> - revenue by customer
> - daily/weekly trends
> - customer segmentation
> 
> They must also support all five planned Silver quality checks:
> 
> 1. completeness
> 2. uniqueness
> 3. type validation
> 4. referential integrity
> 5. business logic
> 
> ==================================================
> INTENTIONAL DATA QUALITY DEFECTS
> ==================================================
> 
> The sample data must deliberately contain realistic bad records so that the later Silver phase has something meaningful to detect.
> 
> Include examples of:
> 
> - missing required values
> - duplicate business keys
> - invalid date/type values
> - orphan customer/product references
> - invalid business values such as non-positive quantity
> - at least one additional realistic data-quality issue if useful
> 
> Do NOT randomly corrupt data without documenting it.
> 
> Create a deliberate defect matrix.
> 
> For every intentional defect type, document:
> 
> - defect type
> - affected dataset
> - affected column
> - approximate number of records
> - why it was introduced
> - which future Silver quality check should detect it
> - whether it should eventually be rejected, quarantined, or corrected
> 
> Do not implement the Silver handling yet.
> 
> The generated dataset should remain manageable for local development and Databricks testing while being large enough to demonstrate meaningful processing.
> 
> ==================================================
> GENERATOR REQUIREMENTS
> ==================================================
> 
> generate_sample_data.py should:
> 
> - be deterministic/reproducible using a configurable random seed
> - allow dataset size to be configured
> - generate customers, products and orders consistently
> - preserve valid relationships for normal records
> - deliberately inject documented bad records
> - avoid hardcoded credentials or environment-specific secrets
> - use clear functions rather than one giant script
> - include useful comments/docstrings
> - make it obvious which data is valid and which data is intentionally defective
> - write CSVs into the repository's data/ directory
> - print useful generation statistics
> 
> The generator should be executable from the repository root.
> 
> Use Python appropriately; do not introduce unnecessary dependencies.
> 
> ==================================================
> DOCUMENTATION — MUST HAPPEN IN THIS SAME TASK
> ==================================================
> 
> Do NOT treat documentation as a later task.
> 
> Create:
> 
> src/data_generation/DATA_GENERATION_NOTES.md
> 
> It must document:
> 
> - dataset purpose
> - physical schemas
> - generation approach
> - row counts
> - relationships
> - deterministic seed
> - intentional defect strategy
> - defect counts
> - mapping between defects and future Silver checks
> - how to execute the generator
> - limitations/assumptions
> 
> Update:
> 
> data-model.md
> 
> with the now-finalized physical model and order line-item decision.
> 
> Update:
> 
> data-quality-strategy.md
> 
> with the concrete fields/rules that can now be defined based on the generated schemas.
> 
> Update:
> 
> requirements-analysis.md
> 
> only where Phase 2 decisions resolve previously TBD requirements.
> 
> Update:
> 
> README.md
> 
> to reflect that data generation is now implemented, while Bronze and later phases remain not started.
> 
> ==================================================
> CURSOR-SPECIFIC EVIDENCE
> ==================================================
> 
> The project must also satisfy the Cursor-user assessment expectations.
> 
> Create the directory:
> 
> tool-specific/cursor-workflow/
> 
> with:
> 
> - project-context.md
> - spec.md
> - cursor-rules-or-instructions.md
> - task-breakdown.md
> 
> These are evidence artifacts, not generic documentation.
> 
> For this phase:
> 
> project-context.md
> ------------------
> Document how the existing project context was supplied to Cursor, including the role of the Phase 1 foundation documents as persistent project context.
> 
> spec.md
> --------
> Document the data-generation specification Cursor is implementing, including schemas, relationships, reproducibility, defect strategy, and constraints.
> 
> cursor-rules-or-instructions.md
> -------------------------------
> Record the project instructions/rules being used for Cursor-assisted development, including:
> - respect existing architecture
> - implement incrementally
> - do not invent requirements
> - no secrets
> - documentation must accompany implementation
> - validate generated code
> - preserve prompt/evaluation evidence
> - do not implement future phases prematurely
> 
> task-breakdown.md
> -----------------
> Break Phase 2 into explicit tasks/subtasks and mark their status.
> 
> ==================================================
> AI PROMPT ARTIFACT
> ==================================================
> 
> Create:
> 
> ai-prompts/data-generation.md
> 
> Record this prompt using the established structure from ai-prompts/documentation.md:
> 
> PROMPT SENT
> AI RESPONSE SUMMARY
> YOUR EVALUATION
> FINAL DECISION
> 
> Also record meaningful follow-up/refinement prompts and outcomes in this file.
> 
> Do not fabricate evaluation results. If validation reveals a problem, document the actual iteration.
> 
> ==================================================
> VALIDATION
> ==================================================
> 
> After implementation:
> 
> 1. Run the generator.
> 2. Confirm all three CSV files exist.
> 3. Inspect schemas and representative records.
> 4. Verify relationships among valid records.
> 5. Verify intentional defects actually exist.
> 6. Verify documented defect counts match the generated data.
> 7. Run the generator again with the same seed and verify reproducibility.
> 8. Check Python syntax/errors.
> 9. Review generated code against the existing project documents.
> 10. Run git diff and git status.
> 
> Do not claim anything was validated unless you actually performed the validation.
> 
> If something fails, fix it and document the iteration.
> 
> ==================================================
> IMPORTANT SCOPE RULE
> ==================================================
> 
> Do NOT create:
> 
> - src/bronze/
> - src/silver/
> - src/gold/
> - src/dashboard/
> 
> Do NOT implement Bronze ingestion yet.
> 
> Do NOT create Gold SQL.
> 
> Do NOT create dashboard queries.
> 
> Do NOT create database implementation artifacts.
> 
> This task ends when Phase 2 data generation and its associated documentation/Cursor evidence are complete and validated.
> 
> Do NOT commit or push to GitHub.
> 
> At the end, provide a concise implementation report containing:
> 
> - files created
> - files updated
> - dataset schemas
> - generated row counts
> - intentional defect counts
> - validation performed
> - issues encountered and fixes
> - git status
> - anything requiring my review/decision
> 
> Then STOP.


---


## Phase 3 — Bronze Layer

**Recovery key:** `phase3-bronze`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> We are now starting PHASE 3 — BRONZE LAYER IMPLEMENTATION.
> 
> Do NOT re-inspect or re-scaffold the repository. Phase 1 foundation and Phase 2 data generation are already complete.
> 
> Use the existing project documentation as the source of truth, especially:
> 
> - requirements-analysis.md
> - design-notes.md
> - data-model.md
> - data-quality-strategy.md
> - tool-workflow.md
> - README.md
> - src/data_generation/DATA_GENERATION_NOTES.md
> - tool-specific/cursor-workflow/project-context.md
> - tool-specific/cursor-workflow/spec.md
> - tool-specific/cursor-workflow/cursor-rules-or-instructions.md
> - tool-specific/cursor-workflow/task-breakdown.md
> - data/customers.csv
> - data/products.csv
> - data/orders.csv
> 
> ==================================================
> PHASE 3 OBJECTIVE
> ==================================================
> 
> Implement ONLY the Bronze layer of the Databricks medallion pipeline.
> 
> The Bronze layer must ingest the three generated CSV datasets:
> 
> - data/customers.csv
> - data/products.csv
> - data/orders.csv
> 
> into corresponding Bronze Delta tables/objects in Databricks.
> 
> Planned implementation files:
> 
> src/bronze/
> ├── 01_ingest_customers.py
> ├── 02_ingest_orders.py
> ├── 03_ingest_products.py
> └── ingest_all.py
> 
> ==================================================
> ARCHITECTURAL REQUIREMENTS
> ==================================================
> 
> Follow the established architecture:
> 
> Raw/sample CSV
>       ↓
> Bronze
>       ↓
> Silver
>       ↓
> Gold
>       ↓
> Dashboard
> 
> Bronze responsibilities:
> 
> - ingest source data
> - preserve source values as much as practical
> - perform only minimal structural handling
> - add useful ingestion metadata where appropriate
> - avoid business cleansing
> - avoid Silver-level data-quality remediation
> - avoid Gold aggregations
> 
> IMPORTANT:
> 
> The intentionally defective records created during Phase 2 MUST NOT be removed or "fixed" in Bronze.
> 
> The Bronze layer should preserve those records so that the Silver data-quality implementation can detect them.
> 
> Do not move quality rules into Bronze merely because the input contains bad records.
> 
> ==================================================
> DATA MODEL
> ==================================================
> 
> Use the finalized Phase 2 schemas documented in data-model.md.
> 
> customers.csv:
> 
> customer_id
> customer_name
> email
> country
> signup_date
> customer_segment
> lifetime_value
> 
> products.csv:
> 
> product_id
> product_name
> category
> unit_price
> 
> orders.csv:
> 
> order_line_id
> order_id
> customer_id
> product_id
> order_date
> quantity
> unit_price
> 
> Orders represent LINE ITEMS.
> 
> Revenue is:
> 
> quantity × unit_price
> 
> Do not change this model.
> 
> ==================================================
> IMPLEMENTATION EXPECTATIONS
> ==================================================
> 
> For each entity:
> 
> 1. Read the corresponding CSV.
> 2. Create/write the corresponding Bronze Delta table/object.
> 3. Preserve the source schema and values as much as practical.
> 4. Add appropriate ingestion metadata if consistent with the architecture, such as:
>    - ingestion timestamp
>    - source file/path
> 5. Make the implementation reusable and reasonably parameterized.
> 6. Avoid hardcoded credentials or secrets.
> 7. Use Databricks/PySpark patterns appropriate for this project.
> 8. Keep the three ingestion scripts independently understandable.
> 9. Provide ingest_all.py as the orchestration entry point.
> 
> Do NOT implement:
> 
> - Silver transformations
> - data-quality checks
> - quarantine logic
> - Gold SQL
> - dashboard logic
> - streaming
> - unnecessary production infrastructure
> - Databricks Asset Bundles unless already required by the existing project specification
> 
> ==================================================
> PATH / ENVIRONMENT HANDLING
> ==================================================
> 
> Before choosing paths or table names, inspect the existing documentation for any established convention.
> 
> If a Databricks-specific path/catalog/schema/table naming decision is still genuinely unresolved, choose the simplest assessment-appropriate approach and DOCUMENT the decision rather than inventing a complex architecture.
> 
> Do not introduce Unity Catalog configuration, external locations, volumes, jobs, or infrastructure unless required by the existing project requirements.
> 
> ==================================================
> VALIDATION
> ==================================================
> 
> After implementation, validate the code as far as the current environment allows.
> 
> At minimum:
> 
> - Python syntax/compile validation
> - verify imports where possible
> - inspect schemas
> - verify expected Bronze entities exist
> - verify row counts against the generated CSVs
> - verify intentionally defective records have NOT been silently removed
> - verify Bronze preserves the Phase 2 source data
> - test ingest_all.py appropriately if the Databricks environment is available
> 
> If Databricks execution is NOT available from the current Cursor environment, do NOT fabricate execution results.
> 
> Clearly distinguish:
> 
> - validated locally
> - validated in Databricks
> - unable to validate because environment access is unavailable
> 
> ==================================================
> ITERATION / REVIEW
> ==================================================
> 
> Do not blindly accept your first implementation.
> 
> After generating the Bronze implementation:
> 
> 1. Review it against data-model.md and design-notes.md.
> 2. Check that Bronze is not accidentally performing Silver responsibilities.
> 3. Check that all three entities are handled consistently.
> 4. Check error handling and path/table configuration.
> 5. Fix any issues found.
> 6. Perform validation again after fixes.
> 
> Document meaningful iteration/fixes because this project is specifically demonstrating responsible Cursor-assisted development.
> 
> ==================================================
> DOCUMENTATION — REQUIRED IN THIS SAME PHASE
> ==================================================
> 
> This is critical.
> 
> Implementation + validation + documentation + AI prompt artifact are ONE unit of work.
> 
> Do not finish the code and leave documentation for later.
> 
> Update/create the appropriate documentation as part of this phase:
> 
> 1. ai-prompts/bronze-layer.md
> 
> Record this implementation prompt and meaningful follow-up/refinement prompts using the established structure:
> 
> PROMPT SENT
> AI RESPONSE SUMMARY
> YOUR EVALUATION
> FINAL DECISION
> 
> Do not fabricate the developer evaluation. Where a human decision is still required, explicitly mark it as pending.
> 
> 2. Update README.md
> 
> Mark Bronze implementation status appropriately and describe what is actually implemented.
> 
> 3. Update tool-workflow.md
> 
> Mark the Bronze phase status and record that implementation, review, validation, and prompt documentation were completed.
> 
> 4. Update design-notes.md
> 
> Replace only the Bronze portions that were previously marked as TBD where the implementation has now made an actual decision.
> 
> 5. Create/update any Bronze-specific documentation only if justified by the existing project structure.
> 
> Do NOT prematurely update Silver, Gold, or Dashboard implementation status.
> 
> ==================================================
> GIT
> ==================================================
> 
> Do NOT push anything.
> 
> Do NOT commit yet unless explicitly instructed.
> 
> At the end, report:
> 
> - files created
> - files modified
> - implementation decisions made
> - validation performed
> - validation limitations
> - issues found and fixes
> - documentation/prompt artifacts updated
> - remaining human decisions, if any
> - git status
> 
> STOP after Phase 3 Bronze is complete.
> 
> Do NOT start Silver.


---


## Phase 4 — Silver Layer

**Recovery key:** `phase4-silver`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> PHASE 4 — SILVER LAYER IMPLEMENTATION
> 
> We are now starting Phase 4 (Silver layer) of the Databricks Medallion Pipeline.
> 
> IMPORTANT PROJECT STATUS:
> - Phase 1 foundation is complete.
> - Phase 2 data generation is complete and validated.
> - Phase 3 Bronze ingestion is complete, validated in Databricks, accepted, committed, and pushed.
> - Do NOT revalidate/reinspect the repository from scratch.
> - Do NOT modify Bronze implementation unless a concrete Silver dependency requires it.
> - Do NOT implement Gold, Dashboard, or any future phase.
> - Work incrementally and stop when the Silver phase is complete.
> - Follow the existing project documentation and Cursor workflow artifacts as the source of truth.
> 
> ============================================================
> 1. DATabricks ENVIRONMENT
> ============================================================
> 
> Unity Catalog:
> 
> Catalog:
> de_c1_coding_evaluation
> 
> Existing schema:
> 
> bronze
> 
> Existing Bronze tables:
> 
> de_c1_coding_evaluation.bronze.bronze_customers
> de_c1_coding_evaluation.bronze.bronze_products
> de_c1_coding_evaluation.bronze.bronze_orders
> 
> Silver schema should be:
> 
> de_c1_coding_evaluation.silver
> 
> Silver tables should be:
> 
> de_c1_coding_evaluation.silver.silver_customers
> de_c1_coding_evaluation.silver.silver_products
> de_c1_coding_evaluation.silver.silver_orders
> 
> Any DQ summary/quarantine objects should also be created under:
> 
> de_c1_coding_evaluation.silver
> 
> Do not invent another catalog.
> 
> Do not use the legacy two-part naming convention where the catalog is already known.
> 
> ============================================================
> 2. EXISTING PROJECT CONTEXT
> ============================================================
> 
> Repository:
> 
> DE_C1_Coding_Evaluation
> 
> Architecture:
> 
> Raw CSV
>    ↓
> Bronze Delta
>    ↓
> Silver Delta
>    ↓
> Gold
>    ↓
> Dashboard
> 
> Bronze has already been successfully created and validated in Databricks.
> 
> Observed Bronze row counts:
> 
> customers = 1006
> products  = 206
> orders    = 5163
> 
> Bronze intentionally preserves Phase 2 defects.
> 
> Known observed defects include:
> 
> - NULL/blank customer emails = 50
> - invalid/non-positive order quantities = 40
> - orphan customer references = 25
> - orphan product references = 25
> 
> Additional defects were intentionally generated during Phase 2.
> 
> Authoritative references:
> 
> src/data_generation/DATA_GENERATION_NOTES.md
> data-model.md
> data-quality-strategy.md
> design-notes.md
> requirements-analysis.md
> 
> Do not invent new defect categories.
> 
> ============================================================
> 3. IMPORTANT CURSOR IMPLEMENTATION APPROACH
> ============================================================
> 
> DO NOT generate the entire Silver implementation in one large step.
> 
> The assessment explicitly requires evidence of:
> 
> - Persistent project context
> - Iteration
> - Validation
> - Accepting some suggestions
> - Rejecting/changing other suggestions
> - Testing Cursor-generated code before acceptance
> - Specific prompts rather than vague "build Silver" prompts
> 
> Therefore implement Silver through multiple deliberate iterations.
> 
> Use the following sequence:
> 
> ITERATION 1:
> Design/review the Silver implementation.
> 
> - Review the existing finalized data model and DQ strategy.
> - Propose the Silver execution flow.
> - Identify required files and responsibilities.
> - Identify how invalid records and DQ results will be represented.
> - Do NOT implement the full Silver layer yet.
> - Update task-breakdown.md with specific Silver tasks.
> 
> Then STOP and wait for review.
> 
> ITERATION 2:
> Implement type standardization, cleansing, completeness, and uniqueness.
> 
> Then:
> - run local/static validation where possible
> - inspect generated code
> - identify issues
> - refine implementation
> 
> Do not proceed to the remaining DQ categories until this iteration is reviewed.
> 
> ITERATION 3:
> Implement referential integrity and business logic checks.
> 
> Use the actual Bronze data and known Phase 2 defects.
> 
> Then:
> - validate
> - inspect results
> - fix/refine issues
> 
> ITERATION 4:
> Implement quarantine/rejected-record handling and DQ summary reporting.
> 
> Then:
> - validate
> - inspect results
> - refine if required
> 
> ITERATION 5:
> Integrate the complete Silver orchestration.
> 
> Run the full Silver flow.
> 
> Then validate in Databricks.
> 
> IMPORTANT:
> Each iteration must be documented in:
> 
> ai-prompts/silver-layer.md
> 
> using:
> 
> PROMPT SENT
> AI RESPONSE SUMMARY
> YOUR EVALUATION
> FINAL DECISION
> 
> If a Cursor suggestion is changed or rejected, explicitly document why.
> 
> Do not fabricate evaluation or validation results.
> 
> ============================================================
> 4. SILVER OBJECTIVE
> ============================================================
> 
> Implement Silver as the trusted/curated layer.
> 
> Silver must:
> 
> 1. Read from Bronze Delta tables.
> 2. Apply explicit typing and cleansing.
> 3. Apply the five required data-quality categories:
>    - Completeness
>    - Uniqueness
>    - Type validation
>    - Referential integrity
>    - Business logic
> 4. Produce curated Silver tables.
> 5. Preserve traceability of rejected/invalid records.
> 6. Produce a DQ summary.
> 7. Keep the implementation modular and understandable.
> 8. Align exactly with the finalized Phase 2 physical data model.
> 
> ============================================================
> 5. FINALIZED DATA MODEL
> ============================================================
> 
> Customers:
> 
> customer_id
> customer_name
> email
> country
> signup_date
> customer_segment
> lifetime_value
> 
> Products:
> 
> product_id
> product_name
> category
> unit_price
> 
> Orders are LINE ITEMS:
> 
> order_line_id
> order_id
> customer_id
> product_id
> order_date
> quantity
> unit_price
> 
> Revenue:
> 
> quantity * unit_price
> 
> IMPORTANT:
> 
> Do not convert orders back into an order-header model.
> 
> Multiple order lines may legitimately share the same order_id.
> 
> ============================================================
> 6. REQUIRED SILVER FILES
> ============================================================
> 
> Create:
> 
> src/silver/01_quality_completeness.py
> src/silver/02_quality_uniqueness.py
> src/silver/03_quality_type_validation.py
> src/silver/04_quality_referential_integrity.py
> src/silver/05_quality_business_logic.py
> src/silver/create_silver_tables.py
> src/silver/SILVER_LAYER_NOTES.md
> 
> You may add a small shared helper module if genuinely necessary for DRY/reusable logic.
> 
> Do not create unnecessary framework complexity.
> 
> ============================================================
> 7. SILVER TABLES
> ============================================================
> 
> Create:
> 
> de_c1_coding_evaluation.silver.silver_customers
> de_c1_coding_evaluation.silver.silver_products
> de_c1_coding_evaluation.silver.silver_orders
> 
> Create the silver schema if it does not exist.
> 
> Use Delta tables.
> 
> ============================================================
> 8. TYPE STANDARDIZATION
> ============================================================
> 
> Bronze intentionally stores source columns as STRING to preserve defects.
> 
> Silver must convert fields to appropriate analytical types.
> 
> Customers:
> 
> customer_id → string
> customer_name → string
> email → string
> country → string
> signup_date → date
> customer_segment → string
> lifetime_value → appropriate numeric/decimal type
> 
> Products:
> 
> product_id → string
> product_name → string
> category → string
> unit_price → appropriate numeric/decimal type
> 
> Orders:
> 
> order_line_id → string
> order_id → string
> customer_id → string
> product_id → string
> order_date → date
> quantity → integer
> unit_price → appropriate numeric/decimal type
> 
> Use safe parsing/casting where appropriate.
> 
> Malformed values must be detectable and traceable.
> 
> Do not silently discard invalid records.
> 
> ============================================================
> 9. COMPLETENESS
> ============================================================
> 
> Implement the completeness rules defined in:
> 
> data-quality-strategy.md
> 
> At minimum validate critical identifiers and required fields.
> 
> Customers:
> - customer_id
> - customer_name
> - email
> 
> Products:
> - product_id
> - product_name
> 
> Orders:
> - order_line_id
> - order_id
> - customer_id
> - product_id
> - order_date
> 
> Do not blindly make optional fields required.
> 
> Document the final required-field decisions.
> 
> Invalid records must remain traceable.
> 
> ============================================================
> 10. UNIQUENESS
> ============================================================
> 
> Validate:
> 
> Customers:
> customer_id
> 
> Products:
> product_id
> 
> Orders:
> order_line_id
> 
> IMPORTANT:
> 
> order_id is NOT the uniqueness key because orders are line items.
> 
> Multiple order lines can share an order_id.
> 
> The Phase 2 duplicate defects must be detectable.
> 
> ============================================================
> 11. TYPE VALIDATION
> ============================================================
> 
> Validate malformed source values before/while converting to Silver types.
> 
> Known examples include:
> 
> - invalid signup dates
> - invalid order dates
> - invalid product unit prices
> - invalid order unit prices
> - invalid quantity values
> - invalid email formats
> 
> Use explicit validation logic.
> 
> Do not silently convert malformed values into valid-looking values without recording the failure.
> 
> ============================================================
> 12. REFERENTIAL INTEGRITY
> ============================================================
> 
> Validate:
> 
> orders.customer_id → customers.customer_id
> 
> orders.product_id → products.product_id
> 
> Known Bronze defects:
> 
> orphan customers = 25
> orphan products = 25
> 
> Silver must detect these.
> 
> Use appropriate Spark joins/anti-joins.
> 
> Important:
> 
> Parent entities must have their canonical valid records established before FK validation is considered authoritative.
> 
> Document the execution order and reasoning.
> 
> ============================================================
> 13. BUSINESS LOGIC
> ============================================================
> 
> Implement the business rules defined in:
> 
> data-quality-strategy.md
> 
> Known defects include:
> 
> - future customer signup dates
> - negative product prices
> - future order dates
> - non-positive quantities
> - catalog-price mismatch
> 
> For catalog-price mismatch:
> 
> Compare order-line unit_price against the canonical product unit_price.
> 
> Do not invent unrelated business rules.
> 
> ============================================================
> 14. INVALID RECORD HANDLING
> ============================================================
> 
> Use a traceable invalid-record strategy.
> 
> Preferred assessment design:
> 
> Valid records
>     ↓
> Silver curated tables
> 
> Invalid records
>     ↓
> Silver quarantine/rejected records
> 
> DQ checks
>     ↓
> DQ summary
> 
> Do not simply drop invalid records.
> 
> Create an appropriate quarantine structure under:
> 
> de_c1_coding_evaluation.silver
> 
> It should allow us to identify:
> 
> - source/entity
> - business key
> - failure category
> - failure reason
> - processing timestamp
> 
> If a record fails multiple checks, preserve multiple failure reasons where practical.
> 
> Keep the implementation simple and assessment-appropriate.
> 
> ============================================================
> 15. DQ SUMMARY
> ============================================================
> 
> Create a DQ summary object under:
> 
> de_c1_coding_evaluation.silver
> 
> At minimum include:
> 
> check_category
> table_name
> rows_tested
> rows_passed
> rows_failed
> pass_percentage
> run_timestamp
> 
> Where useful include:
> 
> failure_reason
> 
> The summary must demonstrate execution of all five required DQ categories.
> 
> ============================================================
> 16. SILVER EXECUTION ORDER
> ============================================================
> 
> Recommended logical flow:
> 
> 1. Read Bronze
> 2. Standardize/parse types
> 3. Completeness validation
> 4. Uniqueness validation
> 5. Establish canonical parent records
> 6. Referential integrity validation
> 7. Business logic validation
> 8. Build valid Silver tables
> 9. Write quarantine/rejected records
> 10. Write DQ summary
> 
> You may adjust the order if technically necessary.
> 
> If changed, document why.
> 
> ============================================================
> 17. IDEMPOTENCY
> ============================================================
> 
> The Silver process must be safely rerunnable for the same Bronze input.
> 
> Avoid accumulating duplicate records across repeated runs.
> 
> Use an appropriate write strategy.
> 
> ============================================================
> 18. DOCUMENTATION
> ============================================================
> 
> Update:
> 
> data-quality-strategy.md
> design-notes.md
> requirements-analysis.md
> README.md
> tool-workflow.md
> 
> Create:
> 
> src/silver/SILVER_LAYER_NOTES.md
> 
> Documentation must describe actual implementation decisions.
> 
> Do not claim Databricks validation until it has actually occurred.
> 
> ============================================================
> 19. CURSOR WORKFLOW ARTIFACTS
> ============================================================
> 
> Update:
> 
> ai-prompts/silver-layer.md
> 
> Record every meaningful implementation/refinement cycle.
> 
> Also update where appropriate:
> 
> tool-specific/cursor-workflow/project-context.md
> tool-specific/cursor-workflow/spec.md
> tool-specific/cursor-workflow/task-breakdown.md
> 
> The task breakdown must show granular Silver tasks.
> 
> Examples:
> 
> - Define Silver schema strategy
> - Define safe type conversion
> - Implement completeness checks
> - Implement uniqueness checks
> - Implement type validation
> - Implement FK validation
> - Implement business rules
> - Implement quarantine
> - Implement DQ summary
> - Integrate orchestration
> - Validate in Databricks
> - Fix/refine based on validation
> 
> ============================================================
> 20. VALIDATION
> ============================================================
> 
> LOCAL VALIDATION:
> 
> Run what can be validated without Spark.
> 
> Examples:
> 
> - py_compile
> - import/static validation where possible
> - configuration validation
> - code-level checks
> 
> Do not pretend local validation proves Delta behavior.
> 
> DATABRICKS VALIDATION:
> 
> Run the actual Silver pipeline in Databricks.
> 
> Verify:
> 
> 1. Silver schema exists.
> 2. Silver tables exist.
> 3. Silver schemas/types are correct.
> 4. Silver row counts are reasonable and explainable.
> 5. DQ summary exists.
> 6. Quarantine records exist where expected.
> 7. Completeness detects known defects.
> 8. Uniqueness detects known duplicate defects.
> 9. Type validation detects malformed values.
> 10. Referential integrity detects:
>     - 25 orphan customers
>     - 25 orphan products
> 11. Business logic detects known invalid quantities/dates/prices.
> 12. Rerunning the pipeline does not accumulate duplicates.
> 
> Compare actual results with:
> 
> src/data_generation/DATA_GENERATION_NOTES.md
> 
> Record actual observed values.
> 
> Do not fabricate results.
> 
> ============================================================
> 21. PHASE SCOPE
> ============================================================
> 
> DO NOT implement:
> 
> - Gold
> - Dashboard
> - Streaming
> - Production monitoring
> - Production alerting
> - Advanced PII governance
> - Unrelated infrastructure
> 
> Do not modify Phase 2 data generation.
> 
> Do not modify Bronze unless a concrete issue blocks Silver.
> 
> If Bronze modification becomes necessary:
> 
> STOP and explain the reason before changing it.
> 
> ============================================================
> 22. GIT / COMMIT DISCIPLINE
> ============================================================
> 
> Do not commit or push automatically.
> 
> After Silver implementation and validation, provide:
> 
> git status
> git diff --stat
> recommended commit structure
> recommended commit message
> 
> We will decide when to commit/push.
> 
> ============================================================
> 23. STOP CONDITION
> ============================================================
> 
> When the current iteration is complete:
> 
> 1. Show files created/modified.
> 2. Explain implementation decisions.
> 3. Show validation performed.
> 4. Show known limitations.
> 5. Update the appropriate Cursor prompt artifact.
> 6. STOP.
> 
> Do not automatically continue to the next iteration.
> 
> Do not start Gold.
> 
> Proceed with ITERATION 1 only:
> 
> Design/review the Silver implementation and update the Silver task breakdown.
> 
> Do NOT generate the full Silver implementation yet.


---


## Silver RI Alignment — Implementation

**Recovery key:** `silver-ri-alignment`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> Implement the approved Silver Referential Integrity alignment described below.
> 
> IMPORTANT:
> 
> * This is now an IMPLEMENTATION task.
> * Do NOT modify Gold SQL.
> * Do NOT modify the frozen Gold contract.
> * Do NOT weaken or remove any DQ rule.
> * Do NOT change business_logic, uniqueness, completeness, or type-validation semantics.
> * Preserve existing behavior wherever possible.
> * Make the smallest safe architectural change.
> * Before editing, inspect the current implementation and verify the proposal against the actual code.
> 
> ## Root cause confirmed
> 
> Current Silver RI validates order foreign keys against canonical parent keys generated by:
> 
> prepare_canonical_entity_df()
> → canonical_valid_filter()
> 
> canonical_valid_filter() checks:
> 
> * _dup_rank = 1
> * completeness
> * type_validation
> 
> It does NOT apply:
> 
> * uniqueness
> * business_logic
> 
> Curated silver_products and silver_customers are later produced using filter_valid_rows(), which applies:
> 
> * completeness
> * uniqueness
> * type_validation
> * business_logic
> 
> Therefore RI-valid order lines can reference a customer/product key that is later removed from the curated Silver dimension.
> 
> Confirmed examples:
> 
> ### product_id = 184
> 
> * duplicate product_id
> * canonical occurrence passes canonical_valid_filter()
> * RI therefore accepts orders referencing 184
> * uniqueness DQ causes the entire key 184 to be excluded from silver_products
> * those orders remain in silver_orders
> * Gold inner join drops them
> 
> ### customer_id = 177
> 
> * future signup_date
> * canonical_valid_filter() accepts it because business_logic is not included
> * RI accepts orders referencing 177
> * business_logic excludes customer 177 from silver_customers
> * those orders remain in silver_orders
> * Gold inner join drops them
> 
> Databricks confirmed:
> 
> Product orphan lines:
> 
> * 116
> * quantity = 349
> * revenue = 66013.47
> 
> Customer orphan lines:
> 
> * 71
> * quantity = 221
> * revenue = 57072.64
> 
> ## Required invariant after this fix
> 
> For every nonblank customer_id in silver_orders:
> 
> ```
> customer_id EXISTS IN silver_customers
> ```
> 
> For every nonblank product_id in silver_orders:
> 
> ```
> product_id EXISTS IN silver_products
> ```
> 
> The Gold INNER JOIN contract must therefore become naturally consistent with Silver.
> 
> ---
> 
> # Implementation design
> 
> ## 1. Preserve all existing DQ rules
> 
> Do not change the implementation of:
> 
> * completeness
> * uniqueness
> * type_validation
> * business_logic
> * order-level validation
> * Gold SQL
> 
> Only change when RI executes and which parent key population it uses.
> 
> ## 2. Change DQ execution order
> 
> Current:
> 
> 01 completeness
> 02 uniqueness
> 03 type_validation
> 04 referential_integrity
> 05 business_logic
> 
> Change to:
> 
> 01 completeness
> 02 uniqueness
> 03 type_validation
> 05 business_logic
> 04 referential_integrity
> 
> RI must execute only after customer/product business_logic results are available.
> 
> ## 3. Avoid circular dependency
> 
> Do NOT make RI read:
> 
> silver_customers
> silver_products
> 
> from Delta during the same pipeline run.
> 
> Those tables have not yet been written.
> 
> Instead derive their exact eligible business-key population in memory from the already-computed DQ results.
> 
> The parent population used by RI must be identical to the population that will later be written to the curated Silver dimension tables.
> 
> ## 4. Shared curated-parent eligibility
> 
> Inspect the current implementation of:
> 
> * filter_valid_rows()
> * _failures_for_category()
> * entity_dq_categories()
> 
> Create the smallest reusable helper necessary to derive curated parent keys.
> 
> Preferred conceptual helper:
> 
> ```
> curated_eligible_parent_keys_df(
>     prepared_df,
>     entity_key,
>     dq_results
> )
> ```
> 
> It should produce a DataFrame containing only the distinct business key values that would survive the existing curated-dimension filtering.
> 
> For customers:
> 
> ```
> business_key = customer_id
> ```
> 
> For products:
> 
> ```
> business_key = product_id
> ```
> 
> The helper must use the exact same failure-category semantics currently used by curated writes.
> 
> Do NOT create a second implementation of business rules.
> 
> Do NOT manually recreate uniqueness/business_logic conditions.
> 
> The helper should reuse the existing DQ failure DataFrames.
> 
> ## 5. Reuse the helper from curated Silver writes
> 
> If practical and safe, make create_silver_tables.py use the same shared eligibility implementation.
> 
> The goal is:
> 
> ```
> curated Silver dimension keys
>     ==
> RI parent keys
> ```
> 
> Do not change the resulting customer/product rows beyond the intended RI alignment.
> 
> Customer/product counts should therefore remain:
> 
> ```
> silver_customers = 878
> silver_products = 164
> ```
> 
> before and after the fix.
> 
> ## 6. Update referential integrity
> 
> Modify:
> 
> src/silver/04_quality_referential_integrity.py
> 
> so that run_referential_integrity_all() / check_referential_integrity() can receive the accumulated dq_results.
> 
> Instead of:
> 
> ```
> prepare_canonical_entity_df(...)
> ```
> 
> for customer/product RI parents, use the curated-eligible parent key helper.
> 
> Conceptually:
> 
> ```
> customer_parent_keys =
>     curated_eligible_parent_keys_df(
>         dq_results["business_logic"]["customers"]["prepared_df"],
>         "customers",
>         dq_results
>     )
> 
> product_parent_keys =
>     curated_eligible_parent_keys_df(
>         dq_results["business_logic"]["products"]["prepared_df"],
>         "products",
>         dq_results
>     )
> ```
> 
> Then perform the existing left joins:
> 
> ```
> orders
>   LEFT JOIN customer_parent_keys
>   LEFT JOIN product_parent_keys
> ```
> 
> Keep the existing orphan logic.
> 
> Do not change the order_line_id-based RI failure semantics.
> 
> ## 7. Update run_all_dq_checks()
> 
> Modify:
> 
> src/silver/06_write_dq_results.py
> 
> so that:
> 
> ```
> completeness = run...
> uniqueness = run...
> type_validation = run...
> business_logic = run...
> ```
> 
> are completed before:
> 
> ```
> referential_integrity = run...(dq_results=partial_results)
> ```
> 
> Ensure the final dq_results dictionary has the same expected structure used by downstream persistence and curated writes.
> 
> Do not break any consumers of dq_results.
> 
> ## 8. Standalone module behavior
> 
> Inspect how 04_quality_referential_integrity.py is executed independently.
> 
> If its main()/standalone entry point currently assumes it can independently construct canonical parents, preserve standalone usability where practical.
> 
> However, do NOT introduce unnecessary duplicate DQ execution.
> 
> The primary production path is:
> 
> ```
> run_all_dq_checks()
> ```
> 
> If a fallback is required for standalone execution, keep it isolated and clearly documented.
> 
> ## 9. Important ordering consideration
> 
> Do NOT write curated dimensions before RI.
> 
> The desired flow remains:
> 
> 01
> 02
> 03
> 05
> 04
> 06 persistence
> curated writes
> 
> RI should derive the same curated parent population in memory.
> 
> There is no circular dependency because:
> 
> * customer/product eligibility does not depend on order RI
> * order RI depends on customer/product eligibility
> * orders are written only after RI has been calculated
> 
> ---
> 
> # Validation requirements
> 
> After implementation, perform local syntax validation.
> 
> Run:
> 
> ```
> python3 -m py_compile \
>   src/silver/silver_common.py \
>   src/silver/create_silver_tables.py \
>   src/silver/04_quality_referential_integrity.py \
>   src/silver/06_write_dq_results.py
> ```
> 
> Then run the existing Silver helper tests if available.
> 
> Do not claim runtime success from local validation.
> 
> ---
> 
> # Databricks validation
> 
> After code implementation, provide the exact Databricks execution sequence required to validate the change.
> 
> Do NOT fabricate results.
> 
> The expected checks are:
> 
> ## A. Silver row counts
> 
> Expected:
> 
> ```
> silver_customers = 878
> silver_products = 164
> silver_orders < 3832
> ```
> 
> The exact new silver_orders count must come from Databricks.
> 
> ## B. Reverse RI diagnostic
> 
> Run:
> 
> ```
> SELECT COUNT(*)
> FROM silver_orders o
> LEFT JOIN silver_products p
>   ON o.product_id = p.product_id
> WHERE o.product_id IS NOT NULL
>   AND p.product_id IS NULL;
> ```
> 
> Expected:
> 
> ```
> 0
> ```
> 
> And:
> 
> ```
> SELECT COUNT(*)
> FROM silver_orders o
> LEFT JOIN silver_customers c
>   ON o.customer_id = c.customer_id
> WHERE o.customer_id IS NOT NULL
>   AND c.customer_id IS NULL;
> ```
> 
> Expected:
> 
> ```
> 0
> ```
> 
> ## C. Silver revenue
> 
> Recalculate:
> 
> ```
> SUM(quantity * unit_price)
> ```
> 
> from the new silver_orders.
> 
> Do not assume the old value of 2830321.54.
> 
> ## D. Gold
> 
> Run the existing Gold pipeline without modifying Gold code.
> 
> Expected relationship:
> 
> ```
> SUM(gold_sales_by_product.total_revenue)
>     =
> SUM(gold_revenue_by_customer.total_revenue)
>     =
> SUM(gold_customer_segmentation.total_spend)
>     =
> SUM(silver_orders.quantity * silver_orders.unit_price)
> ```
> 
> Also verify daily and weekly trends against the new silver_orders.
> 
> ## E. Gold quantity
> 
> Verify:
> 
> ```
> SUM(gold_sales_by_product.total_quantity)
>     =
> SUM(silver_orders.quantity)
> ```
> 
> ## F. Gold order count
> 
> Verify daily/weekly:
> 
> ```
> COUNT(DISTINCT silver_orders.order_id)
> ```
> 
> matches the Gold trend order_count.
> 
> ## G. Gold grain
> 
> Verify zero duplicate keys for:
> 
> * gold_sales_by_product.product_id
> * gold_revenue_by_customer.customer_id
> * (time_grain, period_start)
> * gold_customer_segmentation.customer_id
> 
> ## H. Idempotency
> 
> Run Silver twice and Gold twice.
> 
> Confirm:
> 
> * row counts identical
> * aggregate totals identical
> * no cumulative duplication
> * no changing results between runs
> 
> ---
> 
> # Documentation
> 
> After runtime validation succeeds, update:
> 
> * src/silver/SILVER_LAYER_NOTES.md
> * src/gold/GOLD_LAYER_NOTES.md
> * ai-prompts/silver-layer.md
> * ai-prompts/gold-layer.md
> * tool-specific/cursor-workflow/task-breakdown.md
> 
> Document:
> 
> 1. RI now uses curated-eligible parent keys.
> 2. Business logic executes before RI.
> 3. RI and curated dimension writes share the same parent eligibility semantics.
> 4. The previous canonical-parent mismatch was resolved.
> 5. New Silver row counts.
> 6. New RI failure counts.
> 7. Gold reconciliation results.
> 8. Idempotency results.
> 
> Do not mark Gold ACCEPTED unless all required runtime acceptance criteria pass.
> 
> ---
> 
> # Important acceptance condition
> 
> The fix is successful only if:
> 
> ```
> silver_orders has zero product FKs
> that are absent from silver_products
> ```
> 
> AND:
> 
> ```
> silver_orders has zero customer FKs
> that are absent from silver_customers
> ```
> 
> AND the Gold entity-level aggregations reconcile with the resulting silver_orders.
> 
> Do not alter Gold SQL simply to force these conditions to pass.
> 
> ---
> 
> # Final output required from Cursor
> 
> After implementation, report:
> 
> 1. Files modified
> 2. Exact functions changed
> 3. Summary of code changes
> 4. Local validation results
> 5. Any regression risks
> 6. Exact Databricks cells to run
> 7. Expected validation criteria
> 8. Explicit confirmation that Gold SQL was NOT modified
> 
> Do not claim Databricks validation has passed until actual Databricks output is supplied.


---


## Gold Iteration 6 — Orchestration & Validation

**Recovery key:** `gold-iteration-6`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> Implement **Gold Iteration 6 — Orchestration, Databricks execution, and final validation**.
> 
> The Gold design contract is already frozen in:
> 
> `src/gold/GOLD_LAYER_NOTES.md`
> 
> The four Gold SQL implementations are already complete:
> 
> * `src/gold/01_sales_by_product.sql`
> * `src/gold/02_revenue_by_customer.sql`
> * `src/gold/03_daily_weekly_trends.sql`
> * `src/gold/04_customer_segmentation.sql`
> 
> Do NOT redesign the Gold layer. Do NOT change the frozen business definitions.
> 
> ## Objective
> 
> Complete Gold Phase 5 by:
> 
> 1. Creating `src/gold/create_gold_tables.py`
> 2. Orchestrating execution of all four Gold SQL scripts
> 3. Making the orchestration compatible with Databricks Serverless
> 4. Running the complete Gold pipeline on Databricks
> 5. Validating all four Gold tables
> 6. Performing aggregate reconciliation/sanity checks
> 7. Performing idempotency validation
> 8. Updating Gold documentation with actual Databricks evidence
> 9. Marking Gold Phase 5 complete only if all acceptance criteria pass
> 
> ---
> 
> # 1. Frozen Gold contract — DO NOT CHANGE
> 
> Use `src/gold/GOLD_LAYER_NOTES.md` as the authoritative contract.
> 
> Catalog:
> 
> `de_c1_coding_evaluation`
> 
> Schema:
> 
> `gold`
> 
> Gold tables:
> 
> `de_c1_coding_evaluation.gold.gold_sales_by_product`
> 
> `de_c1_coding_evaluation.gold.gold_revenue_by_customer`
> 
> `de_c1_coding_evaluation.gold.gold_daily_weekly_trends`
> 
> `de_c1_coding_evaluation.gold.gold_customer_segmentation`
> 
> Silver inputs:
> 
> `de_c1_coding_evaluation.silver.silver_customers`
> 
> `de_c1_coding_evaluation.silver.silver_products`
> 
> `de_c1_coding_evaluation.silver.silver_orders`
> 
> Revenue:
> 
> `line_revenue = quantity * unit_price`
> 
> Order count:
> 
> `COUNT(DISTINCT order_id)`
> 
> Frequency:
> 
> `COUNT(DISTINCT order_id)` per customer
> 
> Weekly period:
> 
> Monday-start calendar week using the implementation already present in `03_daily_weekly_trends.sql`.
> 
> Entity-grain tables exclude products/customers with zero Silver orders.
> 
> Write mode:
> 
> `CREATE OR REPLACE TABLE ... USING DELTA AS`
> 
> ---
> 
> # 2. Create orchestration file
> 
> Create:
> 
> `src/gold/create_gold_tables.py`
> 
> The orchestrator must execute the four existing SQL files in this order:
> 
> 1. `01_sales_by_product.sql`
> 2. `02_revenue_by_customer.sql`
> 3. `03_daily_weekly_trends.sql`
> 4. `04_customer_segmentation.sql`
> 
> Do not duplicate the SQL logic inside the Python file.
> 
> The SQL files remain the authoritative implementation of each Gold transformation.
> 
> Prefer a simple Serverless-compatible approach.
> 
> Do NOT introduce RDD APIs.
> 
> Do NOT add unnecessary dependencies.
> 
> Do NOT modify the existing Gold SQL implementations unless a real runtime incompatibility is discovered.
> 
> If the repository already has an established orchestration pattern in Bronze/Silver, inspect and follow that pattern where appropriate, while preserving the Gold contract.
> 
> ---
> 
> # 3. Serverless compatibility
> 
> The orchestration must run on Databricks Serverless.
> 
> Avoid:
> 
> * RDD APIs
> * unsupported Spark APIs
> * unnecessary filesystem assumptions
> * environment-specific local paths
> * hard-coded developer-machine paths
> 
> Use Spark SQL / supported Databricks APIs.
> 
> If SQL files need to be loaded by Python, make the approach compatible with the repository's existing Databricks execution model.
> 
> Do not assume a local filesystem path that will not exist in Databricks.
> 
> ---
> 
> # 4. Do not modify previous layers
> 
> Do NOT modify:
> 
> * `src/bronze/`
> * `src/silver/`
> * Bronze documentation
> * Silver implementation
> * Silver DQ logic
> * Silver quarantine logic
> 
> Do NOT read Bronze or Silver quarantine/DQ summary tables from Gold.
> 
> Gold must consume only the trusted Silver entity tables.
> 
> ---
> 
> # 5. Execute on Databricks
> 
> Run the orchestration on the repository's Databricks Serverless environment.
> 
> Record actual execution evidence.
> 
> Do not claim PASS based only on static inspection.
> 
> The final documentation must distinguish:
> 
> * static validation
> * actual Databricks execution
> * actual query results
> 
> If execution fails, diagnose the failure and fix only the Gold implementation/orchestration issue necessary to satisfy the frozen contract.
> 
> Do not fabricate counts.
> 
> ---
> 
> # 6. Validate all four Gold tables
> 
> After successful execution, validate:
> 
> ### A. Table existence
> 
> Confirm all four tables exist:
> 
> * `gold_sales_by_product`
> * `gold_revenue_by_customer`
> * `gold_daily_weekly_trends`
> * `gold_customer_segmentation`
> 
> ### B. Schema validation
> 
> Confirm the exact analytical columns.
> 
> #### Sales by product
> 
> Exactly:
> 
> * `product_id`
> * `product_name`
> * `category`
> * `total_quantity`
> * `total_revenue`
> 
> #### Revenue by customer
> 
> Exactly:
> 
> * `customer_id`
> * `total_revenue`
> 
> #### Daily/weekly trends
> 
> Exactly:
> 
> * `time_grain`
> * `period_start`
> * `total_revenue`
> * `order_count`
> 
> #### Customer segmentation
> 
> Exactly:
> 
> * `customer_id`
> * `customer_segment`
> * `lifetime_value`
> * `frequency`
> * `total_spend`
> 
> No helper columns.
> 
> No `SELECT *` output.
> 
> ### C. Grain validation
> 
> Validate:
> 
> Sales by product:
> one row per product.
> 
> Revenue by customer:
> one row per customer.
> 
> Trends:
> one row per (`time_grain`, `period_start`).
> 
> Segmentation:
> one row per customer with at least one Silver order.
> 
> Check for duplicate grain keys.
> 
> ---
> 
> # 7. Validate business formulas
> 
> Run actual Databricks reconciliation queries.
> 
> ## Revenue reconciliation
> 
> Calculate the Silver source total:
> 
> `SUM(quantity * unit_price)` from:
> 
> `de_c1_coding_evaluation.silver.silver_orders`
> 
> Compare against:
> 
> `SUM(total_revenue)` from `gold_sales_by_product`
> 
> and:
> 
> `SUM(total_revenue)` from `gold_revenue_by_customer`
> 
> and the corresponding sum across the daily/weekly trends at ONE time grain only.
> 
> Do not add daily and weekly revenue together because that would double-count the same business revenue.
> 
> The values should reconcile within the documented numeric precision/rounding tolerance.
> 
> ## Quantity reconciliation
> 
> Compare:
> 
> `SUM(quantity)` from Silver orders
> 
> against:
> 
> `SUM(total_quantity)` from `gold_sales_by_product`
> 
> ## Order-count reconciliation
> 
> For trends, validate:
> 
> `COUNT(DISTINCT order_id)` from Silver
> 
> against the total business-order count represented by the daily trend.
> 
> Do not sum daily and weekly counts together.
> 
> ## Frequency reconciliation
> 
> Validate customer segmentation:
> 
> `frequency = COUNT(DISTINCT order_id)` per customer.
> 
> Compare the Gold result against an independent aggregation directly from Silver.
> 
> ## Total-spend reconciliation
> 
> Validate:
> 
> `total_spend = SUM(quantity * unit_price)` per customer.
> 
> Compare segmentation results against an independent Silver aggregation.
> 
> ---
> 
> # 8. Validate join behavior
> 
> Because Gold uses inner joins, validate that Gold entity tables contain only customers/products with matching Silver orders.
> 
> Check that:
> 
> * every Gold product exists in Silver products
> * every Gold customer exists in Silver customers
> * every Gold product has at least one Silver order
> * every Gold customer has at least one Silver order
> 
> Do not introduce new RI enforcement logic.
> 
> ---
> 
> # 9. Validate row counts
> 
> Record actual Databricks row counts for:
> 
> * Silver customers
> * Silver products
> * Silver orders
> * Gold sales by product
> * Gold revenue by customer
> * Gold daily trends
> * Gold weekly trends
> * Gold customer segmentation
> 
> Do NOT invent expected Gold counts.
> 
> The frozen contract deliberately did not specify exact Gold row counts.
> 
> Use the actual Databricks results as evidence.
> 
> ---
> 
> # 10. Validate daily/weekly trends
> 
> For:
> 
> `gold_daily_weekly_trends`
> 
> validate:
> 
> * only `day` and `week` values exist in `time_grain`
> * daily `period_start` matches `order_date`
> * weekly `period_start` is Monday
> * no duplicate (`time_grain`, `period_start`) rows
> * daily and weekly revenue independently reconcile to Silver
> * daily and weekly order counts independently reconcile to Silver
> 
> Do NOT compare the sum of daily + weekly revenue to Silver because they represent two views of the same data.
> 
> ---
> 
> # 11. Validate customer segmentation
> 
> Validate:
> 
> * `customer_id` uniqueness
> * `customer_segment` comes from Silver customers
> * `lifetime_value` comes from Silver customers
> * `frequency = COUNT(DISTINCT order_id)`
> * `total_spend = SUM(quantity * unit_price)`
> * no zero-order customers are present
> 
> Do not recalculate or reinterpret `customer_segment` or `lifetime_value`.
> 
> They are source attributes from Silver.
> 
> ---
> 
> # 12. Idempotency test
> 
> Run the complete Gold orchestration twice using the same Silver input.
> 
> Capture the relevant results after Run 1 and Run 2.
> 
> At minimum compare:
> 
> * row counts
> * total revenue
> * total quantity where applicable
> * order counts
> * Gold schemas
> 
> Expected result:
> 
> **Run 1 and Run 2 produce equivalent Gold results.**
> 
> Because the frozen contract uses:
> 
> `CREATE OR REPLACE TABLE`
> 
> there should be no accumulation of duplicate records between runs.
> 
> Do not switch to MERGE/upsert.
> 
> ---
> 
> # 13. Acceptance criteria
> 
> Evaluate the following explicitly:
> 
> ### AC-1
> 
> `create_gold_tables.py` runs successfully on Databricks Serverless.
> 
> ### AC-2
> 
> All four Gold analytical outputs exist.
> 
> ### AC-3
> 
> Sales-by-product contains the required product attributes, total quantity, and total revenue.
> 
> ### AC-4
> 
> Revenue-by-customer is one row per customer with total revenue.
> 
> ### AC-5
> 
> Trends contain daily and weekly grains with revenue and business order counts.
> 
> ### AC-6
> 
> Customer segmentation contains segment, lifetime value, frequency, and total spend.
> 
> ### AC-7
> 
> No helper columns are present.
> 
> ### AC-8
> 
> Gold reads Silver entity tables only.
> 
> ### AC-9
> 
> Join keys match the frozen Gold contract.
> 
> ### AC-10
> 
> Repeated execution is idempotent.
> 
> ### AC-11
> 
> Revenue and quantity reconciliation passes.
> 
> Do not mark an acceptance criterion PASS without actual evidence.
> 
> ---
> 
> # 14. Documentation
> 
> After successful validation update:
> 
> `src/gold/GOLD_LAYER_NOTES.md`
> 
> Add a final Gold Iteration 6 / validation section containing:
> 
> * orchestration implementation
> * Databricks Serverless execution result
> * actual Gold row counts
> * schema validation
> * grain validation
> * revenue reconciliation
> * quantity reconciliation
> * order-count validation
> * frequency validation
> * total-spend validation
> * idempotency result
> * acceptance criteria results
> * any issues encountered and their resolution
> 
> Also update:
> 
> `ai-prompts/gold-layer.md`
> 
> with the Iteration 6 implementation and validation history.
> 
> Update:
> 
> `tool-specific/cursor-workflow/task-breakdown.md`
> 
> to reflect the actual completion status.
> 
> If all acceptance criteria pass, mark:
> 
> **Phase 5 Gold — COMPLETE / ACCEPTED**
> 
> Do not mark it accepted if any required runtime validation remains unresolved.
> 
> ---
> 
> # 15. Final response format
> 
> Return a concise but complete report containing:
> 
> 1. Files created
> 2. Files modified
> 3. Files not modified
> 4. Orchestration approach
> 5. Databricks execution result
> 6. Actual Silver row counts
> 7. Actual Gold row counts
> 8. Schema validation
> 9. Grain validation
> 10. Revenue reconciliation
> 11. Quantity reconciliation
> 12. Order-count validation
> 13. Customer frequency validation
> 14. Customer total-spend validation
> 15. Idempotency result
> 16. Acceptance criteria AC-1 through AC-11
> 17. Issues encountered/resolved
> 18. Final decision
> 
> If everything passes:
> 
> **FINAL DECISION: ACCEPTED — Phase 5 Gold COMPLETE**
> 
> If anything fails:
> 
> **FINAL DECISION: NOT YET ACCEPTED**
> 
> Do not fabricate any runtime evidence or counts.


---


## Phase 6 — Dashboard Implementation

**Recovery key:** `dashboard-phase6-implementation`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> You are now implementing **Phase 6 — Dashboard** for the `DE_C1_Coding_Evaluation` repository.
> 
> Phase 5 Gold is COMPLETE and ACCEPTED on Databricks Serverless.
> 
> ## Frozen baseline
> 
> Do not use the pre-RI-fix numbers.
> 
> Current validated state:
> 
> * `SERVERLESS_COMPAT_VERSION = 10`
> * `silver_customers = 878`
> * `silver_products = 164`
> * `silver_orders = 3646`
> * Silver revenue = `2,708,411.08`
> * Silver quantity = `10,899`
> * Silver distinct orders = `2,052`
> 
> Gold is frozen and accepted:
> 
> * `gold_sales_by_product = 164 rows`
> * `gold_revenue_by_customer = 792 rows`
> * `gold_customer_segmentation = 792 rows`
> * `gold_daily_weekly_trends = 950 rows`
> 
>   * 818 daily
>   * 132 weekly
> * Gold revenue = `2,708,411.08`
> * Gold quantity = `10,899`
> * Gold distinct orders = `2,052`
> * Gold ↔ Silver reconciliation = PASS
> * Gold idempotency = PASS
> * AC-1 through AC-11 = PASS
> 
> ---
> 
> # IMPORTANT: Phase 6 scope
> 
> Implement only the Dashboard layer.
> 
> The Dashboard is a **consumption layer over Gold**.
> 
> Architecture:
> 
> ```text
> Bronze
>    ↓
> Silver
>    ↓
> Gold
>    ↓
> Dashboard SQL
>    ↓
> Databricks SQL visualizations
> ```
> 
> Dashboard must read **Gold only**.
> 
> Do not introduce any direct Dashboard dependency on:
> 
> * Bronze
> * Silver
> * raw CSV files
> * quarantine tables
> * DQ summary tables
> 
> Do not recreate Gold business logic.
> 
> Do not modify Gold to make Dashboard easier.
> 
> ---
> 
> # Files that are FROZEN
> 
> Do not modify anything under:
> 
> ```text
> src/bronze/
> src/silver/
> src/gold/
> data/
> src/data_generation/
> ```
> 
> In particular, do NOT modify:
> 
> ```text
> src/gold/*.sql
> src/gold/create_gold_tables.py
> src/gold/GOLD_LAYER_NOTES.md
> ```
> 
> Do not change:
> 
> * Gold grains
> * Gold metric definitions
> * Gold joins
> * Gold aggregation logic
> * Silver RI alignment
> * Gold SQL
> * Gold Python orchestration
> 
> If something appears inconsistent with Dashboard requirements, stop and report it rather than modifying the frozen layers.
> 
> ---
> 
> # Step 1 — Inspect before modifying
> 
> Before creating anything, inspect the repository.
> 
> Read:
> 
> ```text
> requirements-analysis.md
> design-notes.md
> tool-workflow.md
> data-model.md
> README.md
> src/gold/GOLD_LAYER_NOTES.md
> src/gold/01_sales_by_product.sql
> src/gold/02_revenue_by_customer.sql
> src/gold/03_daily_weekly_trends.sql
> src/gold/04_customer_segmentation.sql
> tool-specific/cursor-workflow/task-breakdown.md
> relevant repository instructions/rules
> ```
> 
> Also inspect:
> 
> ```text
> src/dashboard/
> ai-prompts/
> ```
> 
> Determine:
> 
> 1. Whether `src/dashboard/` already exists.
> 2. Whether `dashboard_queries.sql` already exists.
> 3. Whether `DASHBOARD_GUIDE.md` already exists.
> 4. Whether `ai-prompts/dashboard.md` already exists.
> 5. Whether any Dashboard implementation already exists elsewhere.
> 6. Whether repository documentation resolves the `DASHBOARD_GUIDE.md` location ambiguity.
> 
> Do not guess the location.
> 
> ---
> 
> # Step 2 — Establish the actual Gold contract
> 
> Before writing Dashboard SQL, inspect the actual Gold SQL and `GOLD_LAYER_NOTES.md`.
> 
> For each Gold table establish the exact:
> 
> * FQN
> * columns
> * data types
> * grain
> * metric semantics
> 
> The Dashboard must use the actual schema.
> 
> The four approved Gold sources are:
> 
> ```text
> de_c1_coding_evaluation.gold.gold_sales_by_product
> 
> de_c1_coding_evaluation.gold.gold_revenue_by_customer
> 
> de_c1_coding_evaluation.gold.gold_daily_weekly_trends
> 
> de_c1_coding_evaluation.gold.gold_customer_segmentation
> ```
> 
> Do not assume column names from the Phase 6 prompt if the actual Gold implementation differs.
> 
> ---
> 
> # Step 3 — Implement the Dashboard query catalog
> 
> Create:
> 
> ```text
> src/dashboard/dashboard_queries.sql
> ```
> 
> unless repository inspection proves a different required location.
> 
> Keep the query set **small and high-value**.
> 
> Organize the SQL into these four sections:
> 
> ```text
> 1. Product Performance
> 2. Customer Revenue
> 3. Revenue / Trends
> 4. Customer Segmentation
> ```
> 
> Target approximately **8–10 visualization-ready queries**, unless repository requirements justify a different number.
> 
> Do not create dozens of redundant queries.
> 
> ## Product Performance
> 
> Use:
> 
> ```text
> gold_sales_by_product
> ```
> 
> Provide useful visualization-oriented queries such as:
> 
> * Top products by revenue
> * Top products by quantity
> * Revenue by category, if `category` exists in the confirmed Gold schema
> 
> Use `ORDER BY` and a reasonable `LIMIT` only where appropriate for a visualization.
> 
> Do not introduce arbitrary business rules.
> 
> ## Customer Revenue
> 
> Use:
> 
> ```text
> gold_revenue_by_customer
> ```
> 
> Provide useful views such as:
> 
> * Top customers by revenue
> * Customer revenue distribution / ranking
> 
> Only use columns confirmed by the Gold contract.
> 
> ## Revenue / Trends
> 
> Use:
> 
> ```text
> gold_daily_weekly_trends
> ```
> 
> Provide useful views for:
> 
> * Daily revenue trend
> * Weekly revenue trend
> * Daily order trend
> * Weekly order trend
> 
> Respect the existing:
> 
> ```text
> time_grain
> period_start
> ```
> 
> semantics.
> 
> Do NOT recreate weekly boundaries.
> 
> Do NOT derive weekly periods from dates independently.
> 
> ## Customer Segmentation
> 
> Use:
> 
> ```text
> gold_customer_segmentation
> ```
> 
> Provide useful views such as:
> 
> * Customer count by segment
> * Revenue by segment
> * Average lifetime value by segment
> * Average frequency by segment
> 
> Only use the actual Gold metrics.
> 
> ---
> 
> # Step 4 — Dashboard SQL design rules
> 
> Every query must satisfy these rules.
> 
> ### Rule A — Gold only
> 
> Every source table referenced by Dashboard SQL must be one of the four approved Gold objects.
> 
> No:
> 
> ```text
> silver.*
> bronze.*
> data/*.csv
> ```
> 
> references.
> 
> ### Rule B — Consume existing Gold metrics
> 
> If Gold provides:
> 
> ```text
> total_revenue
> total_quantity
> order_count
> lifetime_value
> frequency
> total_spend
> ```
> 
> consume those metrics.
> 
> Do not rebuild them from lower layers.
> 
> Additional aggregation is allowed when it is genuinely required for visualization.
> 
> For example:
> 
> ```sql
> SELECT
>     category,
>     SUM(total_revenue) AS total_revenue
> FROM de_c1_coding_evaluation.gold.gold_sales_by_product
> GROUP BY category
> ORDER BY total_revenue DESC;
> ```
> 
> That is acceptable because it aggregates an existing Gold metric for presentation.
> 
> ### Rule C — Preserve semantics
> 
> Do not:
> 
> * redefine revenue
> * redefine order count
> * redefine frequency
> * redefine lifetime value
> * redefine customer segments
> * redefine weekly periods
> * join Gold back to Silver to recover attributes
> * reconstruct missing dimensions
> 
> ### Rule D — Visualization readiness
> 
> Queries should return clean analytical result sets.
> 
> Prefer:
> 
> * descriptive aliases
> * deterministic ordering
> * appropriate aggregation
> * no helper/debug columns
> * no unnecessary technical columns
> 
> Avoid unnecessary parameters unless the repository already has a parameterization convention.
> 
> ---
> 
> # Step 5 — Create the Dashboard guide
> 
> Create the repository-approved location for:
> 
> ```text
> DASHBOARD_GUIDE.md
> ```
> 
> The guide should contain:
> 
> ## 1. Overview
> 
> Explain:
> 
> ```text
> Bronze → Silver → Gold → Dashboard
> ```
> 
> and that Dashboard consumes Gold only.
> 
> ## 2. Prerequisites
> 
> Include:
> 
> * Databricks workspace
> * access to `de_c1_coding_evaluation.gold`
> * Databricks SQL / SQL editor
> * validated Gold tables
> 
> ## 3. Gold dependencies
> 
> Document the four exact Gold FQNs.
> 
> ## 4. Query catalog
> 
> For every Dashboard query explain:
> 
> * query name
> * source Gold table
> * purpose
> * output grain
> * important output columns
> * recommended visualization
> 
> ## 5. Running the SQL
> 
> Explain how to:
> 
> 1. Open Databricks SQL
> 2. Open/import `dashboard_queries.sql`
> 3. Execute individual queries
> 4. Use each result set to create a visualization
> 5. Add the queries to a SQL Dashboard if required by the repository
> 
> Do not invent UI instructions that depend on an unverified Databricks interface version.
> 
> ## 6. Recommended visualizations
> 
> Map the queries to appropriate visualization types.
> 
> At minimum consider:
> 
> * bar chart
> * histogram
> * line chart
> * pie/donut or bar chart for segmentation
> 
> Use the repository's original dashboard requirement as the source of truth where applicable.
> 
> ## 7. Validation baselines
> 
> Document the current validated Gold baseline:
> 
> ```text
> Gold revenue: 2,708,411.08
> Gold quantity: 10,899
> Gold distinct orders: 2,052
> 
> gold_sales_by_product: 164 rows
> gold_revenue_by_customer: 792 rows
> gold_customer_segmentation: 792 rows
> gold_daily_weekly_trends: 950 rows
>     daily: 818
>     weekly: 132
> ```
> 
> Do not substitute the old:
> 
> ```text
> 2,830,321.54
> 11,464
> 3,832
> ```
> 
> values anywhere as current validation baselines.
> 
> ## 8. Interpretation
> 
> Explain what each visualization represents without redefining Gold metrics.
> 
> ## 9. Limitations / assumptions
> 
> Document any genuine limitations discovered during implementation.
> 
> Do not invent limitations.
> 
> ---
> 
> # Step 6 — Create AI prompt history
> 
> Create:
> 
> ```text
> ai-prompts/dashboard.md
> ```
> 
> unless it already exists.
> 
> Follow the repository's established AI prompt documentation convention.
> 
> Record:
> 
> * Phase 6 implementation prompt
> * important repository findings
> * decisions made
> * what was accepted
> * what was rejected
> * why
> * validation performed
> 
> Do not fabricate Cursor responses or Databricks results.
> 
> Only document actual actions/results.
> 
> ---
> 
> # Step 7 — Documentation status updates
> 
> Inspect whether the repository expects Phase 6 status updates in:
> 
> ```text
> README.md
> requirements-analysis.md
> design-notes.md
> tool-specific/cursor-workflow/task-breakdown.md
> ```
> 
> Do not modify these automatically.
> 
> Only update them if the repository's established workflow clearly requires it.
> 
> If you modify any of them, report exactly what changed and why.
> 
> Do NOT modify frozen Silver/Gold documentation merely to make it appear current.
> 
> ---
> 
> # Step 8 — Local validation
> 
> After implementation:
> 
> ### SQL/static validation
> 
> Check:
> 
> * SQL syntax where a local validator is available
> * all four FQNs are valid strings
> * every query reads Gold only
> * no Silver references
> * no Bronze references
> * no CSV references
> * no accidental lower-layer joins
> * no duplicate query sections
> * no unnecessary helper columns
> 
> ### Repository validation
> 
> Check:
> 
> * expected files exist
> * Markdown is readable
> * SQL sections correspond to the guide
> * every documented query actually exists
> * every query's documented source matches the SQL
> * no secrets were introduced
> 
> Do not modify frozen layers to make validation pass.
> 
> ---
> 
> # Step 9 — Databricks Serverless validation
> 
> Run the Dashboard SQL against the already validated Gold tables in Databricks Serverless.
> 
> Validate in this order:
> 
> ## A. Gold source availability
> 
> Confirm all four tables exist and are queryable.
> 
> ## B. Gold row counts
> 
> Confirm:
> 
> ```text
> gold_sales_by_product = 164
> gold_revenue_by_customer = 792
> gold_customer_segmentation = 792
> gold_daily_weekly_trends = 950
> ```
> 
> And:
> 
> ```text
> daily trend rows = 818
> weekly trend rows = 132
> ```
> 
> ## C. Gold baseline reconciliation
> 
> Where applicable, confirm:
> 
> ```text
> Gold revenue = 2,708,411.08
> Gold quantity = 10,899
> Gold distinct orders = 2,052
> ```
> 
> Use existing Gold semantics.
> 
> Do not recreate these from Silver.
> 
> ## D. Execute every Dashboard query
> 
> Every query in `dashboard_queries.sql` must execute successfully.
> 
> Record:
> 
> * success/failure
> * returned schema
> * row-count sanity
> * relevant observations
> 
> Do not invent results.
> 
> ## E. Source dependency validation
> 
> Confirm every Dashboard query references only:
> 
> ```text
> de_c1_coding_evaluation.gold.*
> ```
> 
> and specifically the approved four Gold objects.
> 
> ---
> 
> # Step 10 — Dashboard acceptance
> 
> Use two categories.
> 
> ## Explicit requirements
> 
> Validate only requirements actually supported by repository documentation, including:
> 
> * Dashboard artifacts exist
> * Dashboard queries consume Gold
> * required analytical themes are covered
> * SQL is visualization-ready
> * Dashboard guide exists at the repository-approved location
> * prompt history exists if required by the workflow
> * required visualizations are supported if the original requirement explicitly requires them
> 
> ## Recommended validation checks
> 
> Additionally verify:
> 
> * all queries execute successfully on Serverless
> * no Bronze/Silver dependencies
> * Gold baseline remains unchanged
> * query output grains are correct
> * documented query behavior matches actual SQL
> * no Gold business logic has been duplicated
> 
> Do not label inferred checks as formal project acceptance criteria.
> 
> ---
> 
> # Step 11 — Do not prematurely mark Phase 6 complete
> 
> Implementation and validation are separate.
> 
> Do not claim:
> 
> ```text
> PHASE 6 COMPLETE
> ```
> 
> until:
> 
> 1. files are implemented,
> 2. local/static validation passes,
> 3. Databricks Serverless validation is performed,
> 4. actual evidence is recorded,
> 5. documentation is updated as required.
> 
> If Databricks validation cannot be performed from Cursor, explicitly report:
> 
> ```text
> Implementation complete; Databricks validation pending.
> ```
> 
> Do not fabricate Databricks evidence.
> 
> ---
> 
> # Final response required
> 
> After implementation, report exactly:
> 
> ## 1. Files created
> 
> List every created file.
> 
> ## 2. Files modified
> 
> List every modified existing file and why.
> 
> ## 3. Files intentionally untouched
> 
> Confirm:
> 
> ```text
> src/bronze/
> src/silver/
> src/gold/
> data/
> src/data_generation/
> ```
> 
> remain untouched.
> 
> ## 4. Dashboard query catalog
> 
> Give the final query names grouped by:
> 
> ```text
> Product Performance
> Customer Revenue
> Revenue / Trends
> Customer Segmentation
> ```
> 
> ## 5. Validation
> 
> Separate:
> 
> ```text
> Local/static validation
> Databricks Serverless validation
> ```
> 
> Report actual results only.
> 
> ## 6. Issues / ambiguities
> 
> Report any unresolved repository inconsistencies.
> 
> ## 7. Final decision
> 
> Use exactly one of:
> 
> ```text
> PHASE 6 IMPLEMENTATION COMPLETE — VALIDATION COMPLETE
> 
> ```
> 
> or
> 
> ```text
> PHASE 6 IMPLEMENTATION COMPLETE — DATABRICKS VALIDATION PENDING
> 
> ```
> 
> or
> 
> ```text
> PHASE 6 BLOCKED — <reason>
> ```
> 
> Do not make changes outside the Dashboard scope.


---


## Dashboard Evaluation Completion (Iteration 3)

**Recovery key:** `dashboard-evaluation-completion`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> We are completing the Databricks coding/evaluation project.
> 
> I need you to review the existing project code, especially:
> 
> 1. dashboard_queries.sql
> 2. all Gold-layer SQL/models/tables
> 3. the evaluation/requirements document available in the project
> 4. any existing dashboard-related code or documentation
> 
> IMPORTANT:
> Do not blindly rewrite existing SQL. First understand what has already been implemented and reuse existing Gold-layer tables and queries wherever possible.
> 
> ====================================================
> DASHBOARD REQUIREMENTS
> ====================================================
> 
> The dashboard needs at least 3 meaningful SQL-based visualizations/tiles and must include the required business views from the evaluation:
> 
> 1. Top 10 products by revenue
>    - Recommended visualization: horizontal bar chart
>    - Product on Y-axis
>    - Revenue on X-axis
>    - Sort descending
>    - Show top 10 only
> 
> 2. Customer revenue distribution
>    - Recommended visualization: histogram
>    - Customer-level total revenue/spend on X-axis
>    - Number of customers on Y-axis
>    - Use appropriate bins
> 
> 3. Customer segmentation
>    - Recommended visualization: pie/donut chart
>    - Required behavioral segmentation should be represented as:
>        High-Value
>        Repeat
>        One-Time
>        Inactive
>    - Show customer count or appropriate revenue metric according to the Gold-layer requirement
> 
> Additionally, we already have useful dashboard queries/results for:
> 
> 4. Daily order trend
> 
> 5. Weekly order trend
> 
> 6. Overall customer KPIs:
>    - total_customers
>    - total_spend
>    - avg_customer_spend
>    - avg_frequency
>    - avg_lifetime_value
>    - and total orders where available
> 
> 7. Existing customer segment analysis:
>    - Standard
>    - Basic
>    - Premium
>    - customer_count
>    - total_spend
>    - avg_total_spend
>    - avg_frequency
>    - avg_lifetime_value
>    - percentage of total spend
> 
> ====================================================
> EXISTING QUERIES
> ====================================================
> 
> The existing dashboard_queries.sql contains queries similar to:
> 
> -- Daily trend
> SELECT
>     period_start,
>     order_count
> FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
> WHERE time_grain = 'day'
> ORDER BY period_start;
> 
> -- Weekly trend
> SELECT
>     period_start AS week_start,
>     order_count AS weekly_order_count
> FROM de_c1_coding_evaluation.gold.gold_daily_weekly_trends
> WHERE time_grain = 'week'
> ORDER BY week_start;
> 
> -- Customer segment
> SELECT
>     customer_segment,
>     COUNT(*) AS customer_count,
>     SUM(total_spend) AS total_spend,
>     AVG(total_spend) AS avg_total_spend,
>     AVG(frequency) AS avg_frequency,
>     AVG(lifetime_value) AS avg_lifetime_value
> FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
> GROUP BY customer_segment
> ORDER BY total_spend DESC;
> 
> -- Customer segment percentage
> SELECT
>     customer_segment,
>     SUM(total_spend) AS total_spend,
>     ROUND(
>         100.0 * SUM(total_spend) / SUM(SUM(total_spend)) OVER (),
>         2
>     ) AS pct_of_total_spend
> FROM de_c1_coding_evaluation.gold.gold_customer_segmentation
> GROUP BY customer_segment
> ORDER BY total_spend DESC;
> 
> There is also an overall KPI query/result producing approximately:
> 
> total_customers = 792
> total_spend = 2708411.08
> avg_customer_spend = 3419.710960
> avg_frequency = 2.590909090909091
> avg_lifetime_value = 7548.671136
> 
> ====================================================
> IMPORTANT OBSERVATION
> ====================================================
> 
> Do NOT confuse:
> 
> Basic / Standard / Premium
> 
> with the required behavioral segmentation:
> 
> High-Value / Repeat / One-Time / Inactive.
> 
> First inspect the Gold-layer implementation and determine whether the required behavioral segmentation already exists in a Gold table.
> 
> If it exists:
>     reuse it.
> 
> If it does not exist:
>     determine which existing Gold tables contain the required customer/order information and implement the smallest appropriate SQL/model needed.
> 
> Do NOT unnecessarily modify upstream Silver/Gold transformations if the required information already exists.
> 
> ====================================================
> TASK 1 — AUDIT EXISTING DASHBOARD QUERIES
> ====================================================
> 
> Review dashboard_queries.sql and classify every existing query as:
> 
> A. Required dashboard visualization
> B. Useful additional visualization
> C. KPI/card query
> D. Validation/query that should not become a dashboard tile
> E. Duplicate/redundant query
> 
> For example, the query that calculates weekly totals from daily data may be useful for validation, but if the Gold table already contains weekly aggregation, don't create two identical dashboard visualizations.
> 
> Preserve working queries unless there is a concrete reason to change them.
> 
> ====================================================
> TASK 2 — IMPLEMENT MISSING REQUIRED QUERIES
> ====================================================
> 
> Add the missing dashboard SQL queries for:
> 
> A. Top 10 products by revenue
> 
> B. Customer revenue distribution
> 
> C. Required behavioral customer segmentation:
>    High-Value / Repeat / One-Time / Inactive
> 
> Use existing Gold-layer tables wherever possible.
> 
> Before writing SQL, inspect the actual schemas and column names.
> 
> Do not invent column names.
> 
> Use the project's existing naming conventions.
> 
> Each query should be independently executable in Databricks SQL.
> 
> ====================================================
> TASK 3 — LOOK FOR REUSABLE VISUALIZATIONS
> ====================================================
> 
> After implementing the required queries, identify additional visualizations that can be built directly from our existing queries without unnecessary new ETL.
> 
> Consider:
> 
> 1. Daily order trend
>    - Line chart
> 
> 2. Weekly order trend
>    - Line chart
>    - Prefer this as the main trend visualization because it is less noisy
> 
> 3. Standard/Basic/Premium revenue contribution
>    - Donut/pie chart using pct_of_total_spend
> 
> 4. Standard/Basic/Premium customer count
>    - Bar chart
> 
> 5. Standard/Basic/Premium average customer spend
>    - Bar chart
> 
> 6. Standard/Basic/Premium average frequency
>    - Bar chart
> 
> 7. Standard/Basic/Premium average lifetime value
>    - Bar chart
> 
> 8. Overall KPI cards
>    - Total customers
>    - Total spend/revenue
>    - Average customer spend
>    - Average frequency
>    - Average lifetime value
>    - Total orders
> 
> 9. Top products by revenue
>    - Required horizontal bar chart
> 
> 10. Customer revenue distribution
>    - Required histogram
> 
> 11. Behavioral segmentation
>    - Required pie/donut chart
> 
> Do not create all of these automatically if that would make the dashboard cluttered.
> 
> Instead, recommend the strongest set of visualizations for a professional business dashboard.
> 
> ====================================================
> TASK 4 — RECOMMEND FINAL DASHBOARD LAYOUT
> ====================================================
> 
> Design a recommended dashboard layout.
> 
> Prefer something like:
> 
> ROW 1 — KPI CARDS
> - Total Customers
> - Total Revenue/Spend
> - Total Orders
> - Avg Customer Spend
> - Avg Frequency
> - Avg Lifetime Value
> 
> ROW 2 — BUSINESS TREND
> - Weekly Order Trend
> - Daily Order Trend or a secondary trend if useful
> 
> ROW 3 — PRODUCT PERFORMANCE
> - Top 10 Products by Revenue
> 
> ROW 4 — CUSTOMER ANALYSIS
> - Customer Revenue Distribution
> - Behavioral Customer Segmentation
> 
> ROW 5 — OPTIONAL SEGMENT ANALYSIS
> - Basic / Standard / Premium Revenue Contribution
> - OR segment-level customer count/revenue/frequency
> 
> Explain which optional visualization is most useful and why.
> 
> ====================================================
> TASK 5 — CHECK DATA CONSISTENCY
> ====================================================
> 
> Validate that:
> 
> 1. Weekly aggregation calculated from daily data agrees with the existing Gold weekly aggregation.
> 
> 2. Customer segment revenue percentages sum to approximately 100%.
> 
> 3. Overall customer spend agrees with the sum of segment spend.
> 
> 4. Counts are logically consistent.
> 
> 5. No duplicate aggregation is being introduced.
> 
> 6. Top-10 revenue query is actually sorted descending and limited to 10.
> 
> 7. Histogram query operates at CUSTOMER level, not order level.
> 
> 8. Behavioral segmentation is based on the correct Gold-layer/customer behavior definition from the evaluation requirements.
> 
> If any inconsistency exists, report it instead of silently changing data.
> 
> ====================================================
> TASK 6 — SQL FILE ORGANIZATION
> ====================================================
> 
> Cleanly organize dashboard_queries.sql into sections:
> 
> ----------------------------------------------------
> -- 1. KPI CARDS
> ----------------------------------------------------
> 
> ----------------------------------------------------
> -- 2. ORDER TRENDS
> ----------------------------------------------------
> 
> ----------------------------------------------------
> -- 3. TOP PRODUCTS
> ----------------------------------------------------
> 
> ----------------------------------------------------
> -- 4. CUSTOMER REVENUE DISTRIBUTION
> ----------------------------------------------------
> 
> ----------------------------------------------------
> -- 5. CUSTOMER BEHAVIORAL SEGMENTATION
> ----------------------------------------------------
> 
> ----------------------------------------------------
> -- 6. CUSTOMER SEGMENT ANALYSIS
> ----------------------------------------------------
> 
> ----------------------------------------------------
> -- 7. VALIDATION QUERIES
> ----------------------------------------------------
> 
> For each dashboard query, add a short SQL comment explaining:
> 
> - What business question it answers
> - Recommended visualization
> - Important field(s) for X/Y/category
> 
> Do not add excessive comments.
> 
> ====================================================
> TASK 7 — DO NOT OVERENGINEER
> ====================================================
> 
> This is a coding/evaluation project.
> 
> Do NOT:
> 
> - introduce unnecessary frameworks
> - create unnecessary Gold tables
> - duplicate existing aggregations
> - modify working ETL just for dashboard purposes
> - invent data
> - hardcode result values
> - hardcode dates unless the requirement explicitly calls for it
> - use Python/Pandas when Databricks SQL is sufficient
> - create duplicate visualizations showing the same metric
> 
> Prefer simple, readable Databricks SQL.
> 
> ====================================================
> FINAL RESPONSE FROM YOU
> ====================================================
> 
> After making the changes, give me:
> 
> 1. Files inspected
> 2. Existing dashboard queries that can be reused
> 3. Queries that were added
> 4. Any queries that were redundant
> 5. Final recommended dashboard tiles
> 6. Recommended visualization type for every tile
> 7. Any schema/data issues discovered
> 8. Exact files changed
> 
> Do not claim that a query works unless you have verified the relevant table/column names against the project.
> 
> Most importantly:
> PRESERVE EXISTING WORK WHERE IT IS ALREADY CORRECT AND BUILD THE MISSING DASHBOARD REQUIREMENTS AROUND IT.


---


## Final Validation Review

**Recovery key:** `final-validation-review`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> We have completed the Databricks implementation and dashboard for the DE_C1_Coding_Evaluation project.
> 
> Before making any changes, inspect the existing repository thoroughly and understand its current structure and implementation. Do NOT create arbitrary files or change working pipeline/dashboard logic unnecessarily.
> 
> The Databricks dashboard is already implemented with these pages:
> 1. Executive Overview
> 2. Product Performance
> 3. Customer Insights
> 
> The dashboard consumes the existing Gold tables only:
> - de_c1_coding_evaluation.gold.gold_sales_by_product
> - de_c1_coding_evaluation.gold.gold_revenue_by_customer
> - de_c1_coding_evaluation.gold.gold_daily_weekly_trends
> - de_c1_coding_evaluation.gold.gold_customer_segmentation
> 
> The dashboard has already been validated visually in Databricks. Do NOT redesign or add dashboard pages unless the repository requirements explicitly require it.
> 
> TASK:
> Perform a FINAL VALIDATION REVIEW of the complete project.
> 
> First inspect:
> - README.md
> - requirements-analysis.md
> - design-notes.md
> - tool-workflow.md
> - data-model.md
> - data-quality-strategy.md
> - GOLD_LAYER_NOTES.md
> - existing source code
> - existing tests
> - existing dashboard files
> - relevant repository instructions/rules
> - any existing documentation related to the evaluation
> 
> Also inspect the actual Bronze/Silver/Gold SQL/code so that validation is based on the implemented project rather than assumptions.
> 
> Then determine:
> 
> 1. What validation/test artifacts already exist.
> 2. What required validation artifacts are missing.
> 3. Whether existing tests adequately cover:
>    - completeness
>    - uniqueness
>    - referential integrity
>    - business-rule validation
>    - Gold-layer aggregation correctness
>    - reconciliation between Gold tables
> 4. Whether the intentional data-quality issues introduced during data generation are actually tested and caught.
> 5. Whether the dashboard SQL uses Gold tables only.
> 6. Whether dashboard queries reimplement any Gold business logic incorrectly.
> 7. Whether all required project artifacts from the evaluation specification exist.
> 8. Whether README/setup instructions are sufficient to reproduce the project.
> 9. Whether there are inconsistencies between documentation and implementation.
> 
> IMPORTANT ARCHITECTURAL RULES:
> - Dashboard must consume Gold only.
> - Do not introduce Bronze/Silver dependencies into dashboard SQL.
> - Do not recreate Gold business metrics in the dashboard.
> - Additional aggregation of existing Gold metrics for visualization is acceptable.
> - Do not modify working Bronze/Silver/Gold logic merely for cosmetic reasons.
> - Do not invent columns, metrics, tables, or requirements.
> - Use the actual repository implementation and documentation as the source of truth.
> 
> Known Gold tables:
> 
> de_c1_coding_evaluation.gold.gold_sales_by_product
> 
> de_c1_coding_evaluation.gold.gold_revenue_by_customer
> 
> de_c1_coding_evaluation.gold.gold_daily_weekly_trends
> 
> de_c1_coding_evaluation.gold.gold_customer_segmentation
> 
> Known validation results from Databricks that should be considered when checking reconciliation:
> 
> Total Gold segmentation spend:
> 2708411.08
> 
> Total Gold revenue by customer:
> 2708411.08
> 
> Customer-segment spend percentages:
> Standard = 47.80%
> Basic = 30.55%
> Premium = 21.65%
> Total = 100.00%
> 
> Behavioral segmentation:
> Repeat = 386 customers, 1094641.95 spend, 40.42%
> One-Time = 207 customers, 264634.54 spend, 9.77%
> High-Value = 199 customers, 1349134.59 spend, 49.81%
> 
> Total revenue:
> 2708411.08
> 
> Dashboard currently contains:
> - Executive Overview
> - Product Performance
> - Customer Insights
> 
> Required dashboard concepts include:
> - Top products by revenue
> - Customer revenue distribution
> - Customer segmentation
> - Product/category analysis
> - Customer behavior analysis
> 
> Do NOT blindly assume these are the only requirements; verify against the repository/evaluation documentation.
> 
> AFTER REVIEW:
> 
> Create/update only the necessary validation artifacts in the repository.
> 
> Prefer reusing the repository's existing structure and conventions.
> 
> For validation SQL, create a clearly organized validation script if one does not already exist. It should contain executable checks for:
> 
> A. BRONZE VALIDATION
> - expected source tables/data exist
> - row counts are non-zero
> - required columns exist where practical
> 
> B. SILVER DATA QUALITY
> - null/completeness checks
> - duplicate/uniqueness checks
> - referential integrity checks
> - business-rule checks
> - intentional bad records are detected
> 
> C. GOLD VALIDATION
> - gold_sales_by_product aggregation checks
> - gold_revenue_by_customer aggregation checks
> - gold_daily_weekly_trends consistency checks
> - gold_customer_segmentation consistency checks
> 
> D. RECONCILIATION
> Verify that equivalent revenue totals reconcile across Gold outputs.
> 
> For example, validate the relationship between:
> gold_revenue_by_customer
> gold_customer_segmentation
> gold_sales_by_product
> 
> Do not assume the exact relationship if the schema/grain does not support it; inspect the implementation first.
> 
> E. DASHBOARD VALIDATION
> Verify dashboard SQL references only the approved Gold objects.
> 
> Also verify:
> - Top 10 revenue query sorts correctly by total_revenue DESC
> - Top 10 quantity query sorts correctly by total_quantity DESC
> - customer behavioral segmentation follows the documented logic
> - customer revenue distribution uses the intended Gold customer-revenue data
> - no unnecessary Silver/Bronze dependency exists
> 
> IMPORTANT:
> Do not just write tests. For every important validation, document:
> - what is being tested
> - expected result
> - actual result if it can be determined from existing repository evidence
> - PASS/FAIL
> - explanation of any known discrepancy
> 
> If a validation requires Databricks execution and cannot be executed from Cursor, clearly mark it as:
> "REQUIRES DATABRICKS EXECUTION"
> rather than pretending it passed.
> 
> Do not fabricate test results.
> 
> Finally produce a concise final validation report containing:
> 
> 1. Repository structure reviewed
> 2. Tests already present
> 3. Tests added
> 4. Tests requiring Databricks execution
> 5. Dashboard validation status
> 6. Gold reconciliation status
> 7. Documentation gaps
> 8. Missing evaluation artifacts
> 9. Recommended next actions
> 
> Do not modify unrelated files.
> Do not modify the existing working dashboard unless a concrete requirement violation is discovered.
> Do not change business logic without explaining why first.
> 
> Start by inspecting the repository and report your findings BEFORE making modifications.


---


## README / requirements-analysis Update (post 26/26)

**Recovery key:** `readme-requirements-update`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> We have now completed Databricks validation of the entire pipeline.
> 
> IMPORTANT VALIDATION RESULT:
> - src/validation/pipeline_validation.sql: 26/26 PASS
> - Executed successfully on Databricks Serverless
> - Bronze, Silver/DQ, Gold, reconciliation, and dashboard validation all passed
> - No pipeline or dashboard implementation changes are required.
> 
> Now update ONLY:
> 1. README.md
> 2. requirements-analysis.md
> 
> Use the current repository implementation and VALIDATION_REPORT.md as the source of truth.
> 
> Requirements:
> 
> 1. Inspect the actual implementation before editing.
> 2. Remove or update stale statements saying that Bronze, Silver, Gold, Dashboard, validation, etc. are "not started", if those statements are no longer accurate.
> 3. Accurately describe the implemented medallion architecture:
>    - data generation
>    - Bronze
>    - Silver
>    - data quality/quarantine
>    - Gold
>    - dashboard
>    - validation
> 4. Accurately reflect that the Databricks validation suite is COMPLETE with 26/26 PASS.
> 5. Preserve the existing structure, terminology, and intent of the documents wherever possible.
> 6. Do not invent functionality.
> 7. Do not change Python/SQL pipeline code.
> 8. Do not change dashboard SQL.
> 9. Do not change dashboard pages.
> 10. Do not alter validation logic.
> 11. Do not remove useful existing documentation.
> 12. If a requirement is genuinely not implemented, leave it clearly marked as incomplete rather than falsely marking it complete.
> 
> After editing, provide:
> - files modified
> - sections modified
> - stale statements corrected
> - requirements now confirmed complete
> - any remaining gaps


---


## Submission Closure — Prompt History & Provenance (Step 4)

**Recovery key:** `submission-closure-step4`  
**Source:** development session record (user message)

**PROMPT SENT — VERBATIM (recovered):**


> # Step 4 — Finalize AI Prompt History, Dataset Provenance & Submission Closure Artifacts
> 
> You are working on the DE_C1_Coding_Evaluation repository.
> 
> The pipeline implementation, dashboard, and end-to-end validation are already complete.
> 
> IMPORTANT CURRENT STATUS:
> - Pipeline validation is COMPLETE: 26 / 26 checks PASS on Databricks Serverless.
> - Dashboard validation is PASS.
> - Gold reconciliation is PASS.
> - Bronze/Silver/Gold implementation is complete.
> - Dashboard consists of 3 implemented pages.
> - Generated datasets are present under data/.
> - ai-prompts/ already contains substantial phase-by-phase prompt history.
> - Do NOT modify working Bronze/Silver/Gold/Dashboard implementation unless you discover an actual validation failure.
> - This task is primarily about FINAL SUBMISSION DOCUMENTATION, PROVENANCE, TRACEABILITY, and CLOSURE.
> 
> ## PRIMARY REQUIREMENT
> 
> The final repository must preserve an auditable record of:
> 
> 1. The AI prompts used to create/develop the project.
> 2. The generated datasets used by the project.
> 3. The relationship between prompts → generated artifacts → validation → final accepted implementation.
> 4. AI-assisted debugging and validation activities.
> 5. Human/developer review and final decisions.
> 6. Any prompt-history gaps that cannot be established from the repository.
> 
> The evaluator specifically requires an artefact containing the prompt history used during project creation together with the generated datasets.
> 
> Therefore, treat `ai-prompts/` + `data/` + provenance documentation as a formal submission artifact, not merely informal documentation.
> 
> ---
> 
> # PART A — AUDIT EXISTING AI PROMPT HISTORY
> 
> First inspect the entire repository, especially:
> 
> - ai-prompts/
> - data/
> - src/
> - DATA_GENERATION_NOTES.md
> - BRONZE_LAYER_NOTES.md
> - SILVER_LAYER_NOTES.md
> - GOLD_LAYER_NOTES.md
> - DASHBOARD_GUIDE.md
> - VALIDATION_REPORT.md
> - README.md
> - requirements-analysis.md
> - data-model.md
> - data-quality-strategy.md
> - reflection.md
> - final-ai-usage-summary.md (if present)
> - debugging-notes.md (if present)
> - tool-specific/cursor-workflow/
> - git history if available
> 
> Do NOT assume that an existing summary is equivalent to a historical prompt.
> 
> For every existing `ai-prompts/*.md` file, determine:
> 
> - phase
> - prompt number/iteration
> - whether PROMPT SENT is verbatim or a faithful summary
> - AI RESPONSE SUMMARY
> - YOUR EVALUATION
> - FINAL DECISION
> - generated/modified artifacts
> - validation evidence
> - whether developer review is documented
> 
> Preserve existing accurate history.
> 
> Do not rewrite existing prompt history unnecessarily.
> 
> ---
> 
> # PART B — PRESERVE PROMPT HISTORY
> 
> The `ai-prompts/` directory is the PRIMARY detailed prompt provenance artifact.
> 
> Ensure it covers the major development phases:
> 
> 1. Foundation / requirements
> 2. Data generation
> 3. Bronze
> 4. Silver
> 5. Gold
> 6. Dashboard
> 7. Debugging
> 8. Validation
> 9. Final documentation / closure
> 
> For every prompt that is actually available in repository history or provided source material:
> 
> Use this structure:
> 
> ## Prompt N — <short description>
> 
> **TYPE:** Original / Iteration / Debugging / Validation / Correction
> 
> **PROMPT SENT:**
> 
> > <exact original prompt where available>
> 
> If exact wording is NOT available:
> 
> **PROMPT SENT — FAITHFUL SUMMARY:**
> 
> > <clearly labeled faithful summary>
> 
> Do NOT present reconstructed wording as an original prompt.
> 
> **AI RESPONSE SUMMARY:**
> - ...
> 
> **ARTIFACTS CREATED/MODIFIED:**
> - ...
> 
> **VALIDATION / TESTING:**
> - ...
> 
> **YOUR EVALUATION:**
> - ...
> 
> **FINAL DECISION:**
> - ACCEPTED / MODIFIED / REJECTED / DEFERRED
> 
> ---
> 
> # PART C — CLOSE THE KNOWN PROMPT-HISTORY GAPS
> 
> Audit specifically for these known gaps:
> 
> 1. ai-prompts/debugging.md
> 2. validation-phase prompt history
> 3. Silver RI alignment prompt
> 4. Gold Iteration 6 prompt
> 5. Dashboard Iteration 1 prompt
> 6. Dashboard Iteration 3 prompt
> 7. Data-generation original prompt
> 8. Original project kickoff prompt
> 9. Recent README/requirements documentation prompts
> 10. Any closure/reflection/final-summary prompts
> 
> For each gap:
> 
> - Search repository/git history/conversation-accessible material for the actual prompt.
> - If actual wording is available, preserve it.
> - If only a faithful summary is available, explicitly label it as a summary.
> - If it cannot be established, DO NOT invent it.
> 
> For example:
> 
> **PROMPT SENT — NOT AVAILABLE IN REPOSITORY**
> 
> The original prompt text could not be established from repository evidence. Related implementation and validation evidence is documented here...
> 
> This is preferable to fabricated historical text.
> 
> ---
> 
> # PART D — CREATE / COMPLETE ai-prompts/debugging.md
> 
> Create:
> 
> `ai-prompts/debugging.md`
> 
> if it does not already exist.
> 
> Consolidate debugging history from:
> 
> - Bronze Spark/session issues
> - Databricks `!python` / Spark Connect issues
> - Silver Serverless compatibility issues
> - Silver RI alignment issue
> - Quarantine/DQ-summary issues
> - Dashboard `order_count` issue
> - Validation SQL issues
> - Any other documented debugging iterations
> 
> IMPORTANT:
> 
> This file is a CROSS-REFERENCE/CONSOLIDATION artifact.
> 
> Do not falsely claim that every consolidated item came from a standalone debugging prompt.
> 
> Where the original debugging prompt exists, preserve it.
> 
> Where debugging was documented only inside another phase file, reference that file.
> 
> ---
> 
> # PART E — CREATE / COMPLETE VALIDATION PROMPT HISTORY
> 
> Create:
> 
> `ai-prompts/validation.md`
> 
> if appropriate.
> 
> Document the AI-assisted work that resulted in:
> 
> - src/validation/pipeline_validation.sql
> - VALIDATION_REPORT.md
> 
> Include:
> 
> - prompt history where available
> - AI response summary
> - changes made to validation SQL
> - the three validation-query corrections
> - final Databricks execution
> - final result: 26 / 26 PASS
> 
> If the original validation prompt is unavailable, clearly state:
> 
> "Original validation prompt text was not preserved in the repository; this entry documents the resulting artifact and available implementation evidence only."
> 
> Do not fabricate a prompt.
> 
> ---
> 
> # PART F — DATASET PROVENANCE MUST BE EXPLICIT
> 
> The generated datasets are part of the required provenance artifact.
> 
> Document the relationship:
> 
> AI prompt
>     ↓
> generate_sample_data.py
>     ↓
> generated CSV datasets
>     ↓
> Bronze ingestion
>     ↓
> Silver DQ / quarantine
>     ↓
> Gold aggregation
>     ↓
> Dashboard
> 
> Explicitly document:
> 
> ### Generated datasets
> 
> - data/customers.csv
> - data/products.csv
> - data/orders.csv
> 
> For each dataset record:
> 
> - purpose
> - schema
> - row count
> - generator script
> - generation seed
> - generation parameters
> - intentional defects
> - defect IDs
> - downstream usage
> 
> Current known committed dataset counts:
> 
> - customers.csv — 1,006 data rows
> - products.csv — 206 data rows
> - orders.csv — 5,163 data rows
> 
> Generation:
> 
> - default seed = 42
> - generation script = src/data_generation/generate_sample_data.py
> - Python standard library only
> - clean generation followed by intentional defect injection
> 
> Document the D01–D17 defect matrix using the existing
> DATA_GENERATION_NOTES.md and generator implementation.
> 
> Do not invent additional defects or statistics.
> 
> ---
> 
> # PART G — DATASET → PROMPT TRACEABILITY
> 
> Create a clear traceability table showing:
> 
> | Prompt / Phase | AI-assisted activity | Dataset/artifact produced | Validation |
> |---|---|---|---|
> | Data generation | Sample-data generation | data/*.csv | row counts / defect checks / reproducibility |
> | Bronze | Ingestion | Bronze tables | ingestion + defect preservation |
> | Silver | DQ + cleansing | Silver curated/quarantine | DQ validation |
> | Gold | Aggregations | Gold tables | reconciliation |
> | Dashboard | Gold-only analytics | dashboard SQL/pages | dashboard validation |
> | Validation | End-to-end checks | pipeline_validation.sql | 26/26 PASS |
> 
> This table should make it obvious to an evaluator that the generated datasets are not orphaned files: they are the actual source data used throughout the pipeline.
> 
> ---
> 
> # PART H — CREATE final-ai-usage-summary.md
> 
> Create:
> 
> `final-ai-usage-summary.md`
> 
> This is an INDEX and EXECUTIVE SUMMARY.
> 
> Do NOT duplicate all prompt history into this file.
> 
> It should point the evaluator to the detailed `ai-prompts/` files.
> 
> Include:
> 
> ## 1. AI tools used
> 
> Only state tools that can be established from repository evidence.
> 
> Do not guess.
> 
> ## 2. Purpose of AI usage
> 
> Summarize use of AI for:
> 
> - requirements/design
> - data generation
> - pipeline implementation
> - debugging
> - dashboard SQL/design
> - validation
> - documentation
> 
> ## 3. Prompt history index
> 
> Table:
> 
> | Phase | Detailed prompt file | Main artifacts | Status |
> |---|---|---|---|
> 
> Include all `ai-prompts/*.md`.
> 
> ## 4. Iterative development
> 
> Summarize the documented iterations:
> 
> - Data generation
> - Bronze
> - Silver
> - Gold
> - Dashboard
> - Debugging
> - Validation
> 
> ## 5. AI-generated / AI-assisted artifacts
> 
> Map prompts to:
> 
> - src/data_generation/
> - src/bronze/
> - src/silver/
> - src/gold/
> - src/dashboard/
> - src/validation/
> - documentation
> 
> ## 6. Human review
> 
> Explain that AI output was reviewed, modified where necessary, tested, and accepted/rejected based on validation.
> 
> Link/reference the `YOUR EVALUATION` and `FINAL DECISION` sections.
> 
> ## 7. Validation
> 
> Reference:
> 
> - VALIDATION_REPORT.md
> - src/validation/pipeline_validation.sql
> - layer notes
> - final 26/26 PASS result
> 
> ## 8. Debugging
> 
> Reference:
> 
> - ai-prompts/debugging.md
> - bronze-layer.md
> - silver-layer.md
> - dashboard.md
> 
> Clearly distinguish original prompt evidence from consolidated summaries.
> 
> ## 9. Dataset provenance
> 
> Explicitly reference:
> 
> - data/customers.csv
> - data/products.csv
> - data/orders.csv
> - src/data_generation/generate_sample_data.py
> - src/data_generation/DATA_GENERATION_NOTES.md
> - seed 42
> - intentional defect matrix D01–D17
> 
> ## 10. Known provenance limitations
> 
> Clearly list any prompts whose exact original wording could not be recovered.
> 
> Do NOT hide these gaps.
> 
> Do NOT reconstruct them and label them as original.
> 
> ---
> 
> # PART I — COMPLETE debugging-notes.md
> 
> If required by the submission structure, create:
> 
> `debugging-notes.md`
> 
> This should be a concise chronological debugging log.
> 
> Include:
> 
> - issue
> - symptom/error
> - investigation
> - resolution
> - affected files
> - validation after fix
> 
> Cross-reference the detailed prompt history rather than duplicating large prompts.
> 
> ---
> 
> # PART J — REFLECTION
> 
> Complete `reflection.md` if it is currently only a placeholder.
> 
> Base it strictly on the actual project evidence.
> 
> Include:
> 
> - what was learned
> - where AI was useful
> - where human review was required
> - important debugging lessons
> - data-quality lessons
> - Databricks implementation lessons
> - what would be improved in a future implementation
> 
> Do not fabricate experiences that are not supported by the repository history.
> 
> ---
> 
> # PART K — README / DOCUMENTATION STATUS
> 
> Inspect:
> 
> - README.md
> - requirements-analysis.md
> - data-quality-strategy.md
> - tool-specific/cursor-workflow/spec.md
> - tool-specific/cursor-workflow/project-context.md
> - tool-specific/cursor-workflow/task-breakdown.md
> 
> Update stale "not started" status statements ONLY where the current implementation evidence clearly establishes completion.
> 
> Do not redesign documentation unnecessarily.
> 
> Do not change implementation code.
> 
> ---
> 
> # PART L — FINAL PROVENANCE CHECK
> 
> At the end, verify that an evaluator can answer all of these questions from the repository:
> 
> 1. What AI tools were used?
> 2. What prompts were used?
> 3. Where is the detailed prompt history?
> 4. Which prompts generated the datasets?
> 5. Where are the generated datasets?
> 6. What seed generated them?
> 7. What defects were intentionally injected?
> 8. Which pipeline artifacts were created from those datasets?
> 9. Which AI iterations were used for Bronze/Silver/Gold/Dashboard?
> 10. What debugging occurred?
> 11. What validation work was AI-assisted?
> 12. What was human-reviewed?
> 13. What was accepted/rejected/modified?
> 14. What is the final validation result?
> 15. Which historical prompt details could not be recovered?
> 
> The evaluator should be able to trace:
> 
> PROMPT HISTORY
>       ↓
> DATASET GENERATION
>       ↓
> BRONZE
>       ↓
> SILVER + DQ
>       ↓
> GOLD
>       ↓
> DASHBOARD
>       ↓
> VALIDATION
>       ↓
> FINAL SUBMISSION
> 
> ---
> 
> # IMPORTANT SAFETY / ACCURACY RULES
> 
> 1. Do NOT fabricate historical prompts.
> 2. Do NOT turn a reconstructed prompt into a verbatim prompt.
> 3. Clearly distinguish:
>    - VERBATIM PROMPT
>    - FAITHFUL SUMMARY
>    - REPOSITORY-DERIVED CONTEXT
>    - UNKNOWN / NOT RECOVERABLE
> 4. Do not alter working pipeline logic.
> 5. Do not alter dashboard logic merely for documentation.
> 6. Do not change generated datasets.
> 7. Do not regenerate the datasets unless required for validation.
> 8. Preserve existing correct prompt history.
> 9. Do not invent AI tools or models.
> 10. Do not invent developer decisions.
> 11. Use the existing validation evidence.
> 12. Final validation remains 26/26 PASS.
> 13. The generated datasets under data/ must remain committed and traceable to the generation script.
> 14. `ai-prompts/` is the detailed historical record; `final-ai-usage-summary.md` is only the evaluator-facing index/summary.
> 
> ---
> 
> # FINAL OUTPUT
> 
> After making the documentation changes, provide:
> 
> 1. Files created
> 2. Files modified
> 3. Prompt-history coverage
> 4. Dataset-provenance coverage
> 5. Remaining historical gaps, if any
> 6. Confirmation that no pipeline/dashboard implementation was changed
> 7. Final validation status: 26/26 PASS


---

