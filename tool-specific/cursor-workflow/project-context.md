# Project Context — Cursor Workflow

How project context is supplied to Cursor for the Databricks Medallion Pipeline (`DE_C1_Coding_Evaluation`).

## Persistent Baseline (Phase 1)

Phase 1 foundation documents are the **authoritative project context**. Cursor is instructed to read these before each implementation phase:

| Document | Context provided |
|----------|------------------|
| `README.md` | Project purpose, architecture, status, repo layout |
| `requirements-analysis.md` | Functional/non-functional requirements, assumptions, open items |
| `design-notes.md` | Medallion layer responsibilities, data flow |
| `data-model.md` | Entities, relationships, schemas (updated in Phase 2) |
| `data-quality-strategy.md` | Five DQ categories and field-level rules |
| `tool-workflow.md` | AI-assisted development process and prompt artifact rules |
| `ai-prompts/documentation.md` | Prompt recording convention |

## Phase-Specific Context (Phase 2)

For data generation, Cursor received:

1. Explicit Phase 2 scope boundary (no Bronze/Silver/Gold)
2. Instruction to resolve order granularity (line-item model)
3. Requirement for intentional, documented defects mapped to Silver checks
4. Reference to submission templates and Cursor evidence artifacts

## How Context Is Provided in Cursor

| Method | Usage in this project |
|--------|----------------------|
| **Chat prompt** | Primary vehicle — full phase instructions pasted with references to existing docs |
| **@ file references** | User can attach foundation docs; agent reads them via workspace tools |
| **Workspace rules** | Team rules (incremental delivery, no secrets, doc + prompt artifacts per phase) |
| **Open files** | Developer may keep `data-model.md`, `requirements-analysis.md` open for review |

## Context Hierarchy

```
Team / user rules (global)
    ↓
Phase 1 foundation docs (persistent)
    ↓
Phase-specific prompt (e.g., Phase 2 data generation)
    ↓
tool-specific/cursor-workflow/spec.md (phase spec artifact)
    ↓
Implementation output + DATA_GENERATION_NOTES.md + ai-prompts/data-generation.md
```

## What Cursor Must Not Assume

- Databricks workspace credentials or catalog names
- Business requirements not in foundation docs or phase prompt
- That prior phases beyond documented status are complete

## Current State

| Phase | Context status |
|-------|----------------|
| Phase 1 foundation | Complete and accepted |
| Phase 2 data generation | Spec in `spec.md`; implementation complete |
| Phase 3+ | Awaiting phase prompts |
