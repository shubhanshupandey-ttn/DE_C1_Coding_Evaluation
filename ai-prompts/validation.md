# AI Prompts — Validation (index)

**Primary location:** Prompt **24** in `ai-prompts/documentation.md` (full prompt text + results).

Validation is documented in the documentation phase file because it is a **closure** activity spanning all layers, not a separate implementation phase.

---

## Numbered prompts

| # | Title | File | Notes |
|---|-------|------|-------|
| **24** | Final validation review | `documentation.md` | Full **PROMPT SENT** + `pipeline_validation.sql` + **26/26 PASS** |

---

## Follow-up (not a separate numbered prompt)

| Activity | Evidence | Notes |
|----------|----------|-------|
| Validation SQL corrections | `debugging.md` Debug 12–13; git `1965d50` | Operator re-run after first Databricks execution; exact follow-up prompt **not preserved** |
| Post-validation README update | git history | Smaller doc update; not numbered separately |

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
