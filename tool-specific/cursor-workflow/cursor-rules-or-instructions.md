# Cursor Rules & Instructions

Project instructions applied during Cursor-assisted development of `DE_C1_Coding_Evaluation`.

## Architecture & Scope

1. **Repository root is the project root** — no nested `databricks-medallion-pipeline/` directory.
2. **Medallion architecture** — Raw → Bronze → Silver (+ DQ) → Gold → Dashboard.
3. **Implement incrementally** — one phase per prompt; do not build future layers early.
4. **Respect Phase 1 foundation docs** as authoritative baseline unless the phase prompt explicitly overrides.

## Development Rules

| Rule | Application |
|------|-------------|
| Do not invent requirements | Schema and defects defined in phase prompt + existing docs only |
| No secrets | No credentials, tokens, or connection strings in code or docs |
| Documentation accompanies implementation | Same task delivers code + notes + doc updates |
| Prompt artifacts required | Record in `ai-prompts/<phase>.md` using PROMPT SENT / AI RESPONSE / EVALUATION / DECISION |
| Validate generated code | Run generator, check outputs, verify reproducibility |
| Preserve evidence | Cursor workflow files under `tool-specific/cursor-workflow/` |
| Do not claim unimplemented work | README and status tables must reflect actual progress |

## Phase 2 Specific Instructions

- Resolve order granularity → **line-item model**
- Finalize physical schemas in `data-model.md`
- Seed **documented** intentional defects (no random undocumented corruption)
- Stdlib Python only for generator
- Update `data-quality-strategy.md` with concrete fields/rules

## AI Evaluation Convention

For each significant prompt iteration:

```
PROMPT SENT → AI RESPONSE SUMMARY → YOUR EVALUATION → FINAL DECISION
```

Developer completes **YOUR EVALUATION** and **FINAL DECISION** after review. Do not fabricate human approval.

## Quality Bar for Cursor Output

- Readable, modular code with docstrings
- Consistent terminology: `customer_id`, `product_id`, `order_line_id`, `order_id`
- Defect counts in code (`DEFECT_COUNTS`) must match documentation
- Git status reviewed at end of phase; no commit unless user requests

## References

- `tool-workflow.md` — Part A AI workflow foundation
- `ai-prompts/documentation.md` — Prompt artifact template
- Submission templates — minimum doc structure (candidate info, requirements, design, DQ, reflection)
