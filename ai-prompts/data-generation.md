# AI Prompts — Data Generation

## Prompt 1: Phase 2 — Data Generation (Primary)

**PROMPT SENT — FAITHFUL SUMMARY:**

> Phase 2 DATA GENERATION for `DE_C1_Coding_Evaluation`. Implement only:
> - `src/data_generation/generate_sample_data.py`
> - `src/data_generation/DATA_GENERATION_NOTES.md`
> - `data/customers.csv`, `orders.csv`, `products.csv`
>
> Read Phase 1 foundation docs first. Resolve order granularity as line-item model. Finalize physical schemas. Include intentional documented defects for all five Silver quality categories. Generator: deterministic seed, configurable sizes, stdlib only, modular functions, no secrets.
>
> Update `data-model.md`, `data-quality-strategy.md`, `requirements-analysis.md`, `README.md`.
>
> Create `tool-specific/cursor-workflow/` evidence files and `ai-prompts/data-generation.md`.
>
> Validate: run generator, verify CSVs, defects, reproducibility. Do not commit. Do not implement Bronze+.

**Verbatim recovery:** Full Phase 2 prompt text — `ai-prompts/verbatim-recoveries.md` (recovery key `phase2-data-generation`).

**AI RESPONSE SUMMARY:**

- Implemented `generate_sample_data.py` with clean generation + defect injection (`DEFECT_COUNTS`)
- Chose **order line-item** model: `order_line_id` PK, `order_id` groups lines
- Generated CSVs: 1,006 customers, 206 products, 5,163 order lines (default seed 42)
- 17 defect types, 328 injections, mapped to Silver modules
- Created `DATA_GENERATION_NOTES.md`, updated foundation docs, Cursor workflow artifacts
- Fixed duplicate-row injection counts (6 customer/product dup rows) and argparse typo during validation

**YOUR EVALUATION:**

- ✓ **What was good:**
  - Line-item order model supports multi-product orders and revenue derivation
  - Defect matrix is explicit with Silver check mapping
  - Reproducibility verified (MD5 match on re-run with seed 42)
  - Stdlib-only; no unnecessary dependencies

- △ **What may need review:**
  - Default volumes (1K/200/5K) — confirm acceptable for assessment
  - Overlapping mutations on same customer row possible (documented)
  - `lifetime_value` not derived from orders (documented limitation)

- ✗ **Issues found during validation:**
  - Initial duplicate defect count reported 3 instead of 6 — **fixed** in generator
  - Argparse indentation typo — **fixed**

**FINAL DECISION:** **ACCEPTED** — Generator, CSVs, defect matrix, and reproducibility validated (see Validation Log below). Committed datasets: `data/customers.csv` (1,006 rows), `data/products.csv` (206), `data/orders.csv` (5,163); seed **42**.

---

## Prompt 2: (Reserved for follow-up)

_Add iteration prompts here if schema volumes, defect counts, or columns are adjusted._

---

## Validation Log (actual)

| Step | Command / action | Result |
|------|------------------|--------|
| Syntax | `python3 -m py_compile src/data_generation/generate_sample_data.py` | Pass |
| Generate | `python3 src/data_generation/generate_sample_data.py` | Pass |
| Row counts | customers=1006, products=206, orders=5163 | Pass |
| NULL emails | count=50 | Pass |
| Orphan FKs | customer=25, product=25 | Pass |
| Reproducibility | Re-run seed 42, MD5 hashes match | Pass |
