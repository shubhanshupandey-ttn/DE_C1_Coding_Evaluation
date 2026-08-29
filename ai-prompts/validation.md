# AI Prompts — Validation

Evidence artifact for end-to-end pipeline validation (`src/validation/pipeline_validation.sql`, `VALIDATION_REPORT.md`).

---

## Prompt 1 — Final validation review (initial)

**TYPE:** Validation / final review

**PROMPT SENT — VERBATIM (recovered):**

> Full verbatim text: `ai-prompts/verbatim-recoveries.md` — recovery key `final-validation-review`.

**PROMPT SENT — SUMMARY (if recovery file unavailable):**

> Perform a FINAL VALIDATION REVIEW of the complete project. Inspect repository docs and implementation. Determine existing/missing validation artifacts. Add unified validation SQL if missing. Produce `VALIDATION_REPORT.md`. Do not change working pipeline/dashboard logic without concrete FAIL.

**AI RESPONSE SUMMARY:**

- Inspected Bronze → Silver → Gold → Dashboard implementation
- Created `src/validation/pipeline_validation.sql` (26 checks: Bronze A, Silver DQ B, Gold C, reconciliation D, dashboard E)
- Created `VALIDATION_REPORT.md`
- Local tests: `test_silver_helpers.py` PASS; `ingest_all.py --dry-run` PASS

**ARTIFACTS CREATED/MODIFIED:**

- `src/validation/pipeline_validation.sql` (new)
- `VALIDATION_REPORT.md` (new)
- `tool-specific/cursor-workflow/task-breakdown.md` (task 6.7 status)

**VALIDATION / TESTING:**

- Static review of dashboard Gold-only consumption — PASS
- Databricks execution deferred to operator

**YOUR EVALUATION:**

- Unified validation script fills gap identified in review
- Layer-specific validation already existed in `*_LAYER_NOTES.md` and `create_gold_tables.py`

**FINAL DECISION:** ACCEPTED — artifacts created; Databricks execution pending at time of creation

---

## Prompt 2 — Validation SQL corrections (operator re-run)

**TYPE:** Debugging / correction

**PROMPT SENT — NOT AVAILABLE IN REPOSITORY**

The operator re-ran `pipeline_validation.sql` on Databricks Serverless and reported failures. The exact follow-up prompt text was not preserved as a separate artifact. Evidence: git commit `f770ddc` (initial validation), `1965d50` (validation fix).

**OBSERVED FAILURES (first Databricks run):**

| Check | Error | Root cause |
|-------|-------|------------|
| `bronze_customers_columns` | `PARSE_SYNTAX_ERROR` | `DESCRIBE TABLE` invalid inside subquery |
| `silver_ri_orders_rows_failed` | `entity_name` not found | `silver_dq_summary` uses `table_name` |
| `silver_completeness_customers_rows_failed` | Same | Same |

**AI RESPONSE SUMMARY:**

- A2: use `system.information_schema.columns` for 7 customer business columns
- B3/B4: filter `silver_dq_summary` on `table_name` (matches `06_write_dq_results.py`)

**ARTIFACTS MODIFIED:**

- `src/validation/pipeline_validation.sql`
- `VALIDATION_REPORT.md` (§ Databricks execution results)

**VALIDATION / TESTING:**

| Run | Result |
|-----|--------|
| First operator run | 20 PASS, 3 SQL errors |
| Re-run after fixes | **26 / 26 PASS** on Databricks Serverless (2026-08-30) |

**YOUR EVALUATION:**

- Failures were validation-script issues, not pipeline logic defects
- No Bronze/Silver/Gold/Dashboard implementation changes required

**FINAL DECISION:** ACCEPTED — **26/26 PASS** final status

---

## Prompt 3 — Post-validation documentation update

**TYPE:** Documentation / closure

**PROMPT SENT — VERBATIM (recovered):**

> Full verbatim text: `ai-prompts/verbatim-recoveries.md` — recovery key `readme-requirements-update`.

**AI RESPONSE SUMMARY:**

- Updated `README.md` and `requirements-analysis.md` phase status to reflect 26/26 PASS
- No pipeline or dashboard code changes

**FINAL DECISION:** ACCEPTED

---

## Validation evidence index

| Artifact | Purpose |
|----------|---------|
| `src/validation/pipeline_validation.sql` | 26 Databricks SQL checks |
| `VALIDATION_REPORT.md` | Full validation report + operator results |
| `src/bronze/ingest_all.py --dry-run` | Local Bronze CSV validation |
| `src/silver/test_silver_helpers.py` | Local Silver helper unit tests |
| `src/gold/create_gold_tables.py` | Gold `validate_gold_pipeline()`, idempotency |
| `*_LAYER_NOTES.md` | Per-layer Databricks baselines |

**Final validation status: 26 / 26 PASS** (Databricks Serverless, 2026-08-30)
