# Final AI Usage Summary

**Project:** `DE_C1_Coding_Evaluation` — Databricks medallion pipeline (customers, orders, products)  
**Purpose of this document:** Evaluator-facing **index and executive summary**. Detailed prompt history lives in `ai-prompts/`; generated datasets live in `data/`.

**Final validation:** `src/validation/pipeline_validation.sql` — **26 / 26 PASS** on Databricks Serverless (2026-08-30).

---

## 1. AI tools used

| Evidence | Finding |
|----------|---------|
| `tool-workflow.md`, `tool-specific/cursor-workflow/` | AI-assisted development workflow documented for **Cursor** |
| `ai-prompts/*.md` | Cursor-assisted implementation prompts per phase |
| `candidate-info.md` | **Cursor** (Shubhanshu Pandey, SSE); assessment 20/08/2026–31/08/2026 |

**Established from repository:** Cursor was the AI-assisted development environment (workflow artifacts, `ai-prompts/`, cursor-workflow folder). **Not established:** specific Cursor model names or versions.

---

## 2. Purpose of AI usage

AI (Cursor) was used across:

| Area | Role |
|------|------|
| Requirements / design | Foundation docs, template alignment, Silver/Gold design iterations |
| Data generation | `generate_sample_data.py`, defect matrix, CSV generation |
| Pipeline implementation | Bronze, Silver (5 DQ categories + orchestration), Gold SQL + orchestrator |
| Debugging | Serverless compatibility, Spark session patterns, RI alignment, validation SQL fixes |
| Dashboard | Gold-only SQL, guide, evaluation visualizations |
| Validation | Unified `pipeline_validation.sql`, `VALIDATION_REPORT.md` |
| Documentation | Layer notes, README, requirements, workflow evidence |

Human/developer review is recorded in `YOUR EVALUATION` / `FINAL DECISION` sections within each `ai-prompts/<phase>.md` file.

---

## 3. Prompt history index

| Phase | Detailed prompt file | Main artifacts | Status |
|-------|---------------------|----------------|--------|
| Foundation / docs | `ai-prompts/documentation.md` | Root foundation docs | Complete |
| Data generation | `ai-prompts/data-generation.md` | `generate_sample_data.py`, `data/*.csv` | Complete |
| Bronze | `ai-prompts/bronze-layer.md` | `src/bronze/*` | Complete — ACCEPTED |
| Silver | `ai-prompts/silver-layer.md` | `src/silver/*`, DQ/quarantine | Complete — ACCEPTED |
| Gold | `ai-prompts/gold-layer.md` | `src/gold/*` | Complete — ACCEPTED |
| Dashboard | `ai-prompts/dashboard.md` | `src/dashboard/*` | Complete — ACCEPTED |
| Debugging (consolidated) | `ai-prompts/debugging.md` | Cross-ref to layer files | Complete |
| Validation | `ai-prompts/validation.md` | `pipeline_validation.sql`, `VALIDATION_REPORT.md` | Complete — 26/26 PASS |
| Verbatim recoveries (supplement) | `ai-prompts/verbatim-recoveries.md` | Long-form prompts recovered at closure | Supplement only |

---

## 4. Iterative development (documented)

| Phase | Iterations |
|-------|------------|
| Data generation | 1 primary prompt + validation fixes |
| Bronze | 1 implementation + 1 Databricks debugging prompt |
| Silver | 5 planned iterations + RI alignment fix (`SERVERLESS_COMPAT_VERSION` 7→10) |
| Gold | Design (1/1b) + 4 SQL files + orchestration/validation (Iteration 6) |
| Dashboard | 3 iterations (initial SQL, `order_count` clarification, evaluation completion) |
| Debugging | 14 consolidated items (`debugging.md`) |
| Validation | Review prompt + operator re-run corrections |

---

## 5. AI-generated / AI-assisted artifacts

| Path | Prompt source |
|------|---------------|
| `src/data_generation/` | `data-generation.md` |
| `data/*.csv` | `data-generation.md` + `generate_sample_data.py` |
| `src/bronze/` | `bronze-layer.md` |
| `src/silver/` | `silver-layer.md` |
| `src/gold/` | `gold-layer.md` |
| `src/dashboard/` | `dashboard.md` |
| `src/validation/` | `validation.md` |
| Foundation + layer docs | `documentation.md` + phase files |
| `tool-specific/cursor-workflow/` | Phase 2+ workflow evidence |

---

## 6. Human review

AI output was reviewed against:

- `requirements-analysis.md`, `design-notes.md`, `data-model.md`, `data-quality-strategy.md`
- Phase-specific layer notes and frozen contracts (especially Gold)
- Local validation (`py_compile`, `--dry-run`, `test_silver_helpers.py`)
- Databricks Serverless execution evidence

**Review locations:** `YOUR EVALUATION` and `FINAL DECISION` in each `ai-prompts/<phase>.md`. Several early entries were marked pending at implementation time; closure review accepts documented validation evidence as basis for acceptance.

**Rejected / modified AI suggestions (documented):** Dashboard — no Silver joins, no Gold metric reimplementation (`dashboard.md` § Rejected). Silver — Serverless API replacements (`silver-layer.md`). Validation — SQL schema fixes only (`validation.md`).

---

## 7. Validation

| Evidence | Result |
|----------|--------|
| `VALIDATION_REPORT.md` | End-to-end review |
| `src/validation/pipeline_validation.sql` | **26/26 PASS** Databricks Serverless |
| `BRONZE_LAYER_NOTES.md` | 1,006 / 206 / 5,163; defects preserved |
| `SILVER_LAYER_NOTES.md` | DQ categories, quarantine, curated 878/164/3646 |
| `GOLD_LAYER_NOTES.md` | Reconciliation 2,708,411.08; idempotency PASS |
| `DASHBOARD_GUIDE.md` + operator evidence | 3 pages validated |

---

## 8. Debugging

**Consolidated index:** `ai-prompts/debugging.md`  
**Chronological log:** `debugging-notes.md`  
**Original prompts where preserved:** `bronze-layer.md` Prompt 2, `dashboard.md` Iteration 2  
**Recovered verbatim:** `verbatim-recoveries.md` (RI alignment, validation review, etc.)

---

## 9. Dataset provenance

### Generated datasets (committed)

| File | Rows | Purpose |
|------|------|---------|
| `data/customers.csv` | **1,006** | Customer dimension |
| `data/products.csv` | **206** | Product dimension |
| `data/orders.csv` | **5,163** | Order line items (fact) |

### Generation

| Item | Value |
|------|-------|
| Script | `src/data_generation/generate_sample_data.py` |
| Default seed | **42** |
| Defaults | 1,000 customers + 6 dup; 200 products + 6 dup; 5,000 valid lines + 163 defective |
| Dependencies | Python stdlib only |
| Method | Clean generation → intentional defect injection (`DEFECT_COUNTS`) → CSV export |

### Defect matrix

17 defect types (D01–D17), **328 injections** — full matrix in `src/data_generation/DATA_GENERATION_NOTES.md` and `DEFECT_COUNTS` in generator.

### Downstream flow

```
AI prompt (Phase 2) → generate_sample_data.py → data/*.csv
    → Bronze (preserve defects) → Silver (DQ/quarantine) → Gold → Dashboard → validation (26/26)
```

---

## 10. Prompt → artifact traceability

| Prompt / Phase | AI-assisted activity | Dataset / artifact | Validation |
|----------------|---------------------|-------------------|------------|
| Data generation | Sample data + defects | `data/*.csv` | Row counts, defect spot checks, seed-42 reproducibility |
| Bronze | CSV → Delta ingest | `bronze_*` tables | dry-run + Databricks 1,006/206/5,163 |
| Silver | DQ + quarantine + curated | `silver_*`, quarantine, DQ summary | Databricks DQ evidence; 0 orphan FKs post–RI |
| Gold | Aggregations | 4 Gold tables | Reconciliation + idempotency |
| Dashboard | Gold-only analytics SQL | `dashboard_queries.sql`, 3 UI pages | Static review + checks 22–26 |
| Validation | End-to-end SQL suite | `pipeline_validation.sql` | **26/26 PASS** |

---

## 11. Known provenance limitations

| Gap | Status |
|-----|--------|
| Phase 2–6 long-form prompts originally filed as **faithful summaries** in phase files | **Supplemented** by `verbatim-recoveries.md` (recovered 2026-08-30) |
| `ai-prompts/debugging.md` did not exist during implementation | **Created at closure** as consolidation (cross-references originals) |
| Validation operator re-run prompt (3 SQL fixes) | **Not preserved** — fixes documented in `validation.md` + git `1965d50` |
| `candidate-info.md` personal fields | **Complete** |
| `database/` setup | **Not implemented** |
| Original kickoff (Aug 21) | Recovered in `verbatim-recoveries.md`; Phase 1 prompts also in `documentation.md` |

**Rule applied:** No reconstructed prompts are labeled as verbatim unless sourced from recovery file or existing `PROMPT SENT` blocks.

---

## Related documents

- **Detailed prompts:** `ai-prompts/` (all `*.md`)
- **Datasets:** `data/`, `DATA_GENERATION_NOTES.md`
- **Reflection:** `reflection.md`
- **Debugging log:** `debugging-notes.md`
