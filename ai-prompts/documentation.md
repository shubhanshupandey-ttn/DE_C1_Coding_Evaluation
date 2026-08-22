# AI Prompts — Documentation

Prompt history for **documentation phases**. Each major activity should follow this structure:

- **PROMPT SENT** — prompt text or faithful summary
- **AI RESPONSE SUMMARY** — what the AI produced
- **YOUR EVALUATION** — what was accepted, changed, or rejected (and why)

Related files: `ai-prompts/data-generation.md`, `bronze-layer.md`, `silver-layer.md`, `gold-layer.md`, `dashboard.md`, `debugging.md`.

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

_To be completed by developer after review._

- ✓ **Accept** template-aligned structure
- △ **Change** — [note any edits]
- ✗ **Reject** — [note if reverting sections]

**FINAL DECISION:** _Pending developer review._

---

## Future documentation prompts

Add new sections below as docs are updated (e.g., after data generation revises `data-model.md`).
