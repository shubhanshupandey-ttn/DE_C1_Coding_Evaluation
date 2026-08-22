# Bronze Layer Notes

Phase 3 implementation: ingest Phase 2 CSVs into Delta Bronze tables on Databricks.

## Purpose

Land raw source data with **minimal transformation**. Bronze does **not** cleanse, deduplicate, or filter intentional Phase 2 defects.

## Target Tables

| Source CSV | Bronze Delta table (default) |
|------------|------------------------------|
| `data/customers.csv` | `bronze.bronze_customers` |
| `data/products.csv` | `bronze.bronze_products` |
| `data/orders.csv` | `bronze.bronze_orders` |

Optional Unity Catalog: `--catalog <catalog>` → `<catalog>.bronze.bronze_<entity>`

## Design Decisions (Phase 3)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Column types in Bronze | **All source columns as STRING** | Preserves invalid dates (`NOT-A-DATE`), bad prices (`INVALID`), empty strings |
| Write mode | `overwrite` (default) | Simple full reload for assessment/dev |
| Metadata columns | `_ingestion_timestamp`, `_source_file` | Audit trail without altering business columns |
| Quality filtering | **None** | Silver owns DQ per architecture |
| Schema creation | `CREATE SCHEMA IF NOT EXISTS bronze` | Minimal setup; no external locations |

## Bronze Table Schema

Source columns (STRING) plus metadata:

| Column | Type | Source |
|--------|------|--------|
| *(entity columns)* | STRING | CSV — see `data-model.md` |
| `_ingestion_timestamp` | TIMESTAMP | Added at ingest |
| `_source_file` | STRING | Absolute path of source CSV |

## Execution

### Local CSV validation (no PySpark required)

From repository root:

```bash
python3 src/bronze/ingest_all.py --dry-run
```

Validates headers, row counts, and spot-checks known Phase 2 defects.

### Databricks cluster / notebook

1. Ensure repo or `data/` CSVs are available to the cluster (Repos, workspace upload, or DBFS).
2. Install/sync `src/bronze/` on the cluster Python path.
3. Run:

```bash
python src/bronze/ingest_all.py --data-dir /path/to/data
```

Or in a Databricks notebook:

```python
%run ./src/bronze/ingest_all
```

With CLI args in notebook:

```python
dbutils.notebook.run("ingest_all", 600, {"dry_run": "false"})
```

### Per-entity scripts

```bash
python src/bronze/01_ingest_customers.py --data-dir data
python src/bronze/03_ingest_products.py --data-dir data
python src/bronze/02_ingest_orders.py --data-dir data
```

### CLI parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--data-dir` | `<repo>/data` | CSV source directory |
| `--schema` | `bronze` | Target schema |
| `--catalog` | *(none)* | Optional Unity Catalog |
| `--write-mode` | `overwrite` | Delta write mode |
| `--dry-run` | off | Local CSV validation only |

## Row Count Expectations (seed 42 defaults)

| Entity | Expected rows |
|--------|---------------|
| customers | 1,006 |
| products | 206 |
| orders (line items) | 5,163 |

Bronze row counts must match CSV row counts (no rows dropped).

## Validation Status

| Check | Environment | Status |
|-------|-------------|--------|
| Python syntax (`py_compile`) | Local | Performed |
| `--dry-run` CSV validation | Local | Performed |
| Delta write + table read | Databricks | **Not performed** (PySpark unavailable locally) |

## Related Files

- `bronze_common.py` — shared ingest logic
- `data-model.md` — source schemas
- `ai-prompts/bronze-layer.md` — Cursor prompt history
