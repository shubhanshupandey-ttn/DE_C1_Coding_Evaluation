# AI Prompts — Database (Step 7)

**Prompts in this file:** 36  
**Implementation order:** Source schema/setup artifacts (`database/`)

---

## Prompt 36 — Step 7 — Database implementation (schema + seed/setup notes)

**TYPE:** Original (contemporaneous Step 7 implementation prompt)

**PROMPT SENT:**

```text
# STEP 7 — DATABASE IMPLEMENTATION
## DE_C1_Coding_Evaluation

We are now implementing the remaining Database requirement for the
DE_C1_Coding_Evaluation project.

IMPORTANT:
This is a DATABASE-ARTIFACT implementation task.

The repository's original requirements explicitly require:

    database/
    ├── schema.sql
    ├── seed-data-notes.md
    └── setup-notes.md

The requirements also explicitly state that every submission must include
a "Database schema or setup script".

Therefore, unlike the earlier documentation-only decision, the database/
requirement should now be implemented.

However, this implementation MUST be based on the CURRENT repository state,
not blindly copied from the original assignment template.

[Protection rules: do not modify src/bronze|silver|gold|dashboard|validation,
data/*.csv, dashboard/validation SQL, screenshots, or medallion logic.]

[Inspect repository; establish current source contract from CSVs, generator,
DATA_GENERATION_NOTES.md, data-model.md, Bronze contracts.]

[Create database/schema.sql, seed-data-notes.md, setup-notes.md documenting
source model — order line-item grain, seed 42, D01–D17 defects, no full
CSV INSERTs, no external RDBMS deployment claimed unless evidenced.]

[Update only obsolete current-status documentation; record prompt in
ai-prompts/database.md; validate; git safety check; implementation report.]
```

*(Full Step 7 specification: inspect → source contract → three database files →
narrow doc updates → validation → git diff → report. See session transcript
for complete protection rules and validation checklist.)*

**AI RESPONSE SUMMARY:**

- Inspected committed CSVs, `generate_sample_data.py`, `DATA_GENERATION_NOTES.md`,
  `data-model.md`, Bronze contracts, and existing docs for stale `database/` status
- Created `database/schema.sql` — portable PostgreSQL-compatible DDL for
  `source.customers`, `source.products`, `source.orders` (line-item grain;
  PKs on `customer_id`, `product_id`, `order_line_id`; logical FKs documented
  but not enforced due to intentional D11/D12 orphans)
- Created `database/seed-data-notes.md` — seed 42, row counts 1,006 / 206 / 5,163,
  generator reference, D01–D17 link, pipeline relationship
- Created `database/setup-notes.md` — reviewer flow; distinguishes schema artifact
  vs Databricks execution vs optional external RDBMS load
- Updated current-status lines in `README.md`, `requirements-analysis.md`,
  `candidate-info.md`, `final-ai-usage-summary.md`, `reflection.md`, `VALIDATION_REPORT.md`
- Did **not** modify Bronze/Silver/Gold/Dashboard/validation code, CSVs, or SQL

**YOUR EVALUATION:**

- ✓ Schema matches authoritative CSV headers and generator column lists
- ✓ Order grain correctly modeled as line items (`order_line_id` PK)
- ✓ No invented columns from original assignment template
- ✓ Defect strategy documented; source data not implied clean
- ✓ External database deployment honestly **not claimed**
- △ `COMMENT ON` syntax is PostgreSQL-oriented; noted in setup-notes for adaptation

**FINAL DECISION:** **ACCEPTED** — Database schema/setup artifacts implemented per
current repository contract. Medallion pipeline unchanged. External RDBMS runtime
not deployed or claimed.

---

## Validation Log (Step 7)

| Check | Result |
|-------|--------|
| `database/schema.sql` exists | Pass |
| `database/seed-data-notes.md` exists | Pass |
| `database/setup-notes.md` exists | Pass |
| CSV headers vs schema columns | Pass |
| Row counts: 1006 / 206 / 5163 | Pass |
| PKs: customer_id, product_id, order_line_id | Pass |
| Logical FKs documented | Pass |
| Protected paths unchanged | Pass (git diff verified) |
| External DB deployment | Not executed / not claimed |
