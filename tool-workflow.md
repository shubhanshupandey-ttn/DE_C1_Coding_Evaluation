# Tool Workflow — Part A: AI Workflow Foundation

This document describes how **AI-assisted development** is incorporated into the Databricks Medallion Pipeline project. It defines the intended workflow for this repository; it does not claim that all steps have already been executed for every phase.

## Goals

- Use AI tools productively for drafting, exploration, and implementation support
- Maintain **developer ownership** of requirements, design decisions, and final code
- Preserve an auditable trail of prompts and outcomes
- Keep **documentation synchronized** with implementation—no documentation debt at the end

## Intended Workflow

### 1. Requirements & Design

| Activity | Human role | AI role |
|----------|------------|---------|
| Define scope and constraints | Lead; approve requirements | Assist with structuring and clarifying documents |
| Architecture and data model | Decide and document trade-offs | Suggest patterns consistent with medallion architecture |
| Quality rules | Define business and technical expectations | Help articulate check categories and examples |

**Outputs:** `requirements-analysis.md`, `design-notes.md`, `data-model.md`, `data-quality-strategy.md`

**Rule:** Do not treat AI-generated requirements as confirmed until reviewed. Items not yet decided are marked *"To be finalized during implementation."*

### 2. AI-Assisted Implementation

For each implementation phase (data generation, Bronze, Silver, Gold, dashboard):

1. Provide a **focused prompt** with context from existing docs and prior layers
2. Generate or refine code/SQL in the appropriate `src/` directory
3. **Record the prompt** (and meaningful follow-ups) in the matching `ai-prompts/` file

| Phase | Code location | Prompt artifact |
|-------|---------------|-----------------|
| Data generation | `src/data_generation/` | `ai-prompts/data-generation.md` |
| Bronze | `src/bronze/` | `ai-prompts/bronze-layer.md` |
| Silver | `src/silver/` | `ai-prompts/silver-layer.md` |
| Gold | `src/gold/` | `ai-prompts/gold-layer.md` |
| Dashboard | `src/dashboard/` | `ai-prompts/dashboard.md` |
| Debugging | (as needed) | `ai-prompts/debugging.md` |
| Documentation | (root and layer docs) | `ai-prompts/documentation.md` |

For each prompt iteration, use the submission template structure:

| Section | Content |
|---------|---------|
| **PROMPT SENT** | Full prompt or faithful summary |
| **AI RESPONSE SUMMARY** | What the AI generated |
| **YOUR EVALUATION** | ✓ Accepted / △ Changed / ✗ Rejected — with reasons |
| **FINAL DECISION** | Which version was kept |

**Rule:** Implementation + documentation + prompt artifact = **one unit of work** per phase. Do not defer docs or prompt recording to the end of the project.

### 3. Developer Review

Before considering a phase complete, the developer reviews:

- Correctness and alignment with `requirements-analysis.md` and `design-notes.md`
- Consistency with `data-model.md` and `data-quality-strategy.md`
- Naming, structure, and conventions across layers
- Security (no hardcoded secrets; no credential leakage)
- Whether AI output invents requirements or schema not yet approved

Review outcomes (changes made, rejections, rationale) may be noted in phase-specific notes or `debugging-notes.md` when relevant.

### 4. Validation & Testing

Validation approach **to be finalized during implementation**, but the intended minimum includes:

- Running generation and ingestion scripts in the target Databricks (or local dev) environment
- Verifying row counts, schemas, and sample outputs at each layer
- Confirming data quality checks detect known issues in sample data (where intentionally introduced)
- Validating Gold SQL produces expected aggregates on clean Silver data

Test evidence (commands run, results, limitations) should be documented in the relevant phase notes—not fabricated.

### 5. Debugging

When issues arise:

1. Reproduce the problem with concrete inputs or job output
2. Use AI for hypothesis generation and fix suggestions **after** sharing actual errors/logs (redacted)
3. Record significant debugging prompts in `ai-prompts/debugging.md`
4. Document root cause and resolution in `debugging-notes.md` when non-trivial

### 6. Documentation

Documentation is **continuous**, not a final cleanup task.

| When | Update |
|------|--------|
| Foundation (Phase 1) | README, requirements, design, model, quality strategy |
| Data generation | `DATA_GENERATION_NOTES.md`, data files context |
| Bronze | `BRONZE_LAYER_NOTES.md` |
| Silver / Gold | Design notes, quality strategy, layer-specific notes as needed |
| Dashboard | `DASHBOARD_GUIDE.md` |
| Project close | `reflection.md`, `final-ai-usage-summary.md`, `debugging-notes.md`, `ai-prompts/debugging.md`, `ai-prompts/validation.md` |

Docs must describe **actual implementation**. If behavior changes, update docs in the same change set.

### 7. Git & Version Control

| Practice | Intent |
|----------|--------|
| Meaningful commits per milestone | Each phase or logical chunk is reviewable |
| Include docs and `ai-prompts/` in commits | Preserve the full artifact trail |
| Branch for feature work | Avoid unreviewed direct changes to `main` when using shared workflows |
| No push unless instructed | Remote updates are explicit |

After each milestone: inspect `git status`, ensure prompt and doc files are included, and use a concise commit message describing *why* the change was made.

## AI Usage Principles

1. **Transparency** — Prompts and major follow-ups are preserved, not reconstructed from memory.
2. **No fabrication** — Do not claim tests, reviews, or debugging that did not occur.
3. **Human decisions** — Architecture, business rules, and schema details require explicit approval.
4. **Incremental scope** — Do not implement future phases prematurely; wait for phase-specific instructions.
5. **Consistency** — All layers must align with the same entities: customers, orders, products.

## Current Status of This Workflow

| Item | Status |
|------|--------|
| Workflow documented (this file) | Complete |
| Prompt artifact convention established | Complete (`ai-prompts/documentation.md`) |
| Implementation phases using this workflow | Phases 2–6 complete; validation **26/26 PASS**; closure docs complete |
