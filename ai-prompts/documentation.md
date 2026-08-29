# AI Prompts — Documentation

Prompt history for **documentation phases**. Each major activity should follow this structure:

- **PROMPT SENT** — prompt text or faithful summary
- **AI RESPONSE SUMMARY** — what the AI produced
- **YOUR EVALUATION** — what was accepted, changed, or rejected (and why)

Related files: `ai-prompts/data-generation.md`, `bronze-layer.md`, `silver-layer.md`, `gold-layer.md`, `dashboard.md`, `debugging.md`, `validation.md`, `verbatim-recoveries.md`.

---

## Prompt 1: Repository Inspection

**PROMPT SENT:**

> FIRST TASK: ONLY inspect the current repository. Do not implement. Determine current structure, existing/missing files, git status, branch, config files, work to preserve. Report findings and STOP.

**AI RESPONSE SUMMARY:**

Inspected `DE_C1_Coding_Evaluation`. Found only `.gitignore` and git metadata. No `databricks-medallion-pipeline/` subdirectory. Branch `main`, clean working tree, synced with `origin/main`. All planned pipeline artifacts missing.

**YOUR EVALUATION:**

✓ **Accepted** — Accurate baseline; no implementation performed.

---

## Prompt 2: Phase 1 — Project Foundation

**PROMPT SENT:**

> Use repository root as project root (no nested `databricks-medallion-pipeline/`). Create foundation files: README.md, candidate-info.md, tool-workflow.md, requirements-analysis.md, design-notes.md, data-model.md, data-quality-strategy.md, ai-prompts/documentation.md. Do NOT create implementation code or layer directories. Document medallion project for customers/orders/products. Mark undecided items as "To be finalized during implementation." Record prompt in ai-prompts/documentation.md. Do not commit or push.

**AI RESPONSE SUMMARY:**

Created eight foundation documents with project-specific medallion architecture, requirements, logical data model, five-category DQ framework (strategy only), and AI workflow (`tool-workflow.md`). Explicitly marked pipeline phases as not started.

**YOUR EVALUATION:**

✓ **What was good:**
- Project-specific content, not generic Databricks boilerplate
- Clear "not started" status for implementation
- Consistent entity names and layer structure
- Prompt artifact convention established

△ **To complete by developer:**
- Fill `candidate-info.md` with real name, role, dates, AI tool
- Review and adjust requirements/design before data generation phase

**FINAL DECISION:** Foundation docs accepted as Phase 1 baseline.

---

## Prompt 3: Align Docs with Submission Templates

**PROMPT SENT:**

> Submission templates provided for candidate-info, requirements-analysis, design-notes, data-quality-strategy, ai-prompts format, and reflection.md. These are a floor, not a limit. Do you wish to modify docs to align?

**AI RESPONSE SUMMARY:**

Restructured foundation docs to match submission section layouts (Problem Statement, Functional/Non-Functional Requirements, What/How/Threshold/Result for DQ checks, PROMPT SENT / AI RESPONSE / YOUR EVALUATION format). Preserved honest "not implemented" status; did not invent personal info, row counts, or ~700 quality issues.

**YOUR EVALUATION:**

- ✓ **Accept** template-aligned structure
- Foundation docs match submission template sections without claiming unimplemented work

**FINAL DECISION:** **ACCEPTED** — template alignment retained as project baseline.

---

## Prompt 4 — README / requirements update (post-validation)

**TYPE:** Documentation / closure

**PROMPT SENT — VERBATIM (recovered):**

> See `ai-prompts/verbatim-recoveries.md` — recovery key `readme-requirements-update`.

**AI RESPONSE SUMMARY:**

- Updated `README.md` and `requirements-analysis.md` to reflect Phases 2–6 complete and **26/26 PASS** validation
- No pipeline or dashboard code changes

**FINAL DECISION:** ACCEPTED

---

## Prompt 5 — Submission closure (prompt history & provenance)

**TYPE:** Closure / documentation

**PROMPT SENT — VERBATIM (recovered):**

> See `ai-prompts/verbatim-recoveries.md` — recovery key `submission-closure-step4`.

**AI RESPONSE SUMMARY:**

- Created `ai-prompts/debugging.md`, `ai-prompts/validation.md`, `ai-prompts/verbatim-recoveries.md`
- Created `final-ai-usage-summary.md`, `debugging-notes.md`; completed `reflection.md`
- Updated stale workflow/status documentation

**FINAL DECISION:** ACCEPTED (closure artifacts)

---

## Future documentation prompts

Add new sections below if post-submission documentation changes occur.
