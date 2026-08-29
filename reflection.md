# Reflection

Evidence-based reflection for the Databricks medallion pipeline project (`DE_C1_Coding_Evaluation`). Sources: `ai-prompts/`, `VALIDATION_REPORT.md`, layer notes, and validation results (**26/26 PASS**).

---

## What I Built

An end-to-end **medallion analytics pipeline** on Databricks Unity Catalog (`de_c1_coding_evaluation`):

1. **Data generation** — reproducible CSVs (`customers`, `products`, order line items) with **17 intentional defect types** (D01–D17) for Silver DQ testing.
2. **Bronze** — faithful CSV ingestion to Delta with STRING schema preserving defects.
3. **Silver** — five DQ categories, `silver_quarantine_records`, `silver_dq_summary`, curated tables (878 / 164 / 3,646 orders post–RI alignment).
4. **Gold** — four analytical tables (sales by product, revenue by customer, daily/weekly trends, customer segmentation) with documented reconciliation (revenue **2,708,411.08**).
5. **Dashboard** — Gold-only SQL (`dashboard_queries.sql`) and a **3-page** Databricks SQL dashboard (Executive Overview, Product Performance, Customer Insights).
6. **Validation** — unified `pipeline_validation.sql` with **26/26 PASS** on Databricks Serverless.

Prompt and dataset provenance: `ai-prompts/`, `data/`, `final-ai-usage-summary.md`.

---

## How I Used AI (Across the Lifecycle)

AI assistance (documented as **Cursor** in workflow artifacts) followed an incremental phase model (`tool-workflow.md`):

- **Foundation:** requirements, design, data model, DQ strategy (`ai-prompts/documentation.md`).
- **Implementation:** one phase per prompt with matching `ai-prompts/<phase>.md` artifact.
- **Iteration:** Silver (5 iterations + RI fix), Gold (6 iterations), Dashboard (3 iterations).
- **Debugging:** recorded in phase files and consolidated in `ai-prompts/debugging.md`.
- **Validation:** AI-assisted creation of unified validation SQL and report (`ai-prompts/validation.md`).

Each significant prompt used: **PROMPT SENT → AI RESPONSE → YOUR EVALUATION → FINAL DECISION**.

---

## What AI Helped With Most

Based on repository evidence (not subjective ranking):

- **Boilerplate and structure** — modular Bronze/Silver Python, Gold SQL files, orchestrators, layer notes.
- **Silver DQ implementation** — five check modules, Serverless compatibility iterations, quarantine/DQ summary design (`silver-layer.md` is the largest prompt artifact).
- **Design extraction** — Gold contract freeze in `GOLD_LAYER_NOTES.md` before SQL implementation.
- **Validation suite** — `pipeline_validation.sql` covering Bronze through dashboard logic in one script.
- **Documentation sync** — README, requirements, defect matrix, workflow evidence.

Areas requiring **human judgment** (documented in evaluations): defect matrix acceptance, Gold contract freeze, rejecting Dashboard changes that would modify Gold or join Silver.

---

## What AI Got Wrong

Documented corrections (see `ai-prompts/debugging.md`):

| Area | Issue | Outcome |
|------|-------|---------|
| Data generation | Wrong duplicate defect count; argparse typo | Fixed before acceptance |
| Bronze | Top-level PySpark imports; `!python` subprocess on Databricks | Lazy imports; `resolve_spark()` pattern |
| Silver | `rdd.isEmpty()`, array+explode inflation, ANSI `to_date`, `F.try_cast` | Serverless-safe DataFrame patterns |
| Silver RI | Parent keys for RI ≠ curated dimension eligibility | RI alignment fix (`SERVERLESS_COMPAT_VERSION = 10`) |
| Dashboard | Operator `order_count` error on wrong table | Repo SQL already correct; docs hardened |
| Validation SQL | `DESCRIBE` subquery; wrong DQ summary column name | Fixed in validation script only |

No evidence that AI invented requirements outside foundation docs without later correction.

---

## How I Validated AI Output

| Layer | Method |
|-------|--------|
| Data generation | `py_compile`, row counts, defect spot checks, seed-42 reproducibility |
| Bronze | `--dry-run`; Databricks row counts + defect-preservation SQL |
| Silver | `test_silver_helpers.py`; Databricks per-module and full-pipeline runs; DQ summary vs defect matrix |
| Gold | SQL contract review; `validate_gold_pipeline()`; reconciliation; idempotency |
| Dashboard | Gold-only grep; operator visual validation; validation checks 22–26 |
| End-to-end | `pipeline_validation.sql` — **26/26 PASS** |

Validation evidence is archived in `VALIDATION_REPORT.md` and `*_LAYER_NOTES.md`.

---

## What I Would Improve Next

From documented gaps (not speculative):

- **`database/`** setup notes still missing if required by evaluator.
- **Automated Spark integration tests** for Silver DQ modules (only helper unit tests exist locally).
- **Databricks Jobs/bundles** orchestration (currently per-layer notebook/Python entry points).
- **Earlier closure documentation** — root status docs lagged implementation until final pass.
- **Consolidate debugging prompts at time of fix** rather than at project close.

---

## Reusable Workflow

From `tool-workflow.md` and demonstrated practice:

1. **Freeze foundation docs** before implementation phases.
2. **One phase per prompt** — scope boundary explicit (no future layers).
3. **Record prompts immediately** in `ai-prompts/<phase>.md` with evaluation/decision.
4. **Validate on target platform** (Databricks Serverless) before accepting a layer.
5. **Preserve datasets and defects** as first-class test fixtures (`data/` + `DEFECT_COUNTS`).
6. **Freeze downstream contracts** (Gold) before consumption layers (Dashboard).
7. **Unified validation script** at end for evaluator reproducibility.

See `final-ai-usage-summary.md` for the full prompt index and provenance map.
