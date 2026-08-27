# AI Prompt History — Dashboard (Phase 6)

Related: `src/dashboard/dashboard_queries.sql`, `src/dashboard/DASHBOARD_GUIDE.md`, `src/gold/GOLD_LAYER_NOTES.md`

---

## Iteration 1: Dashboard query catalog + guide

> Phase 6 Dashboard — consumption layer over frozen Gold. Gold-only SQL, ~8–10 visualization-ready queries, `DASHBOARD_GUIDE.md`, local/static validation. No Bronze/Silver/Gold modifications.

**PROMPT SENT:**

Full Phase 6 implementation specification (2026-08-27):

- Inspect repository (`requirements-analysis.md`, `design-notes.md`, `tool-workflow.md`, Gold SQL/notes, `task-breakdown.md`)
- Establish Gold contract from actual `src/gold/*.sql` and `GOLD_LAYER_NOTES.md`
- Create `src/dashboard/dashboard_queries.sql` (4 sections, 8–10 queries, Gold FQNs only)
- Create `src/dashboard/DASHBOARD_GUIDE.md` (repository path: `src/dashboard/` per `requirements-analysis.md` and `tool-workflow.md`)
- Create `ai-prompts/dashboard.md`
- Local/static validation; Databricks Serverless validation if possible
- Do not modify frozen `src/bronze/`, `src/silver/`, `src/gold/`, `data/`, `src/data_generation/`
- Use post–RI-fix baselines (revenue 2,708,411.08; not pre-fix 2,830,321.54)

**Repository findings:**

| Item | Finding |
|------|---------|
| `src/dashboard/` | Did not exist before Phase 6 |
| `dashboard_queries.sql` | Did not exist |
| `DASHBOARD_GUIDE.md` | Did not exist; approved location `src/dashboard/DASHBOARD_GUIDE.md` (`requirements-analysis.md` § Dashboard, `tool-workflow.md` § Documentation) |
| `ai-prompts/dashboard.md` | Did not exist; required per `tool-workflow.md` |
| Gold contract | Four tables with columns/grains as in `GOLD_LAYER_NOTES.md` and `src/gold/01`–`04` SQL |
| `task-breakdown.md` | Phase 6 listed "Not started" |

**Decisions made:**

| Decision | Rationale |
|----------|-----------|
| 10 queries (not 12+) | Meets 8–10 target; avoids redundant overview tables |
| `customer_revenue_summary_kpis` as single-row aggregate | Supports KPI cards without duplicating top-N logic |
| Separate daily/weekly revenue and order trend queries | Clear visualization binding; respects `time_grain` filter |
| `segment_spend_share` uses window over `SUM(total_spend)` | Presentation aggregation of existing Gold metric |
| No Python orchestration for Dashboard | Phase scope is SQL + guide only; matches `requirements-analysis.md` artifacts |
| No Gold/Silver/Bronze changes | Frozen per project rules |

**Accepted:**

- Gold FQNs and column names from actual Gold implementation
- Section structure: Product Performance, Customer Revenue, Revenue/Trends, Customer Segmentation
- Post–RI-fix validation baselines in guide

**Rejected:**

- Joining Gold back to Silver for customer/product names beyond Gold columns
- Recreating weekly boundaries or segment logic in Dashboard SQL
- Modifying Gold to simplify Dashboard
- Using pre–RI-fix row counts/revenue as current baselines

### Implementation (Cursor agent — 2026-08-27)

| File | Action |
|------|--------|
| `src/dashboard/dashboard_queries.sql` | Created — 10 queries |
| `src/dashboard/DASHBOARD_GUIDE.md` | Created |
| `ai-prompts/dashboard.md` | Created (this file) |
| `tool-specific/cursor-workflow/task-breakdown.md` | Updated Phase 6 status only |

**Frozen layers:** `src/bronze/`, `src/silver/`, `src/gold/`, `data/`, `src/data_generation/` — **not modified**.

### Static / local validation

| Check | Result |
|-------|--------|
| Expected files exist | **PASS** |
| All queries reference only `de_c1_coding_evaluation.gold.*` | **PASS** (grep) |
| No `silver`, `bronze`, or `csv` references in dashboard SQL | **PASS** |
| 10 named queries in 4 sections | **PASS** |
| Guide documents all 10 queries | **PASS** |
| SQL section comments match guide query names | **PASS** |
| Secrets in artifacts | **None** |

### Databricks Serverless validation

| Check | Result |
|-------|--------|
| Gold source availability | **Not run from Cursor** |
| Gold row counts / baselines | **Not run from Cursor** |
| Execute all 10 dashboard queries | **Not run from Cursor** |

Operator checklist documented in `DASHBOARD_GUIDE.md` § Databricks validation checklist.

**FINAL DECISION:** **PHASE 6 IMPLEMENTATION COMPLETE — DATABRICKS VALIDATION PENDING**

---

## Cursor Evaluation Evidence (Phase 6)

| Requirement | Evidence |
|-------------|----------|
| Dashboard artifacts under `src/dashboard/` | `dashboard_queries.sql`, `DASHBOARD_GUIDE.md` |
| Gold-only consumption | Static grep + query review |
| Analytical themes covered | Product, customer revenue, trends, segmentation |
| Prompt history | `ai-prompts/dashboard.md` |
| Frozen layers respected | No edits under bronze/silver/gold/data/data_generation |
