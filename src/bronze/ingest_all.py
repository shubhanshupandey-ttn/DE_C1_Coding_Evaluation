#!/usr/bin/env python3
"""
Orchestrate Bronze ingestion for all three source entities.

Execution order: customers → products → orders (dimensions before facts).

Databricks: import and call run_ingestion(config, spark=spark) in a notebook cell.
Do NOT use ``!python ingest_all.py`` — that subprocess lacks the notebook Spark session.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bronze_common import (  # noqa: E402
    BronzeConfig,
    build_arg_parser,
    config_from_args,
    dry_run_all,
    ingest_entity,
    notebook_spark_if_defined,
    require_pyspark,
    resolve_spark,
)

if TYPE_CHECKING:
    from pyspark.sql import SparkSession

INGEST_ORDER = ("customers", "products", "orders")


def run_ingestion(config: BronzeConfig, spark: SparkSession | None = None) -> dict[str, int]:
    """Run Bronze ingest for all entities. Pass notebook ``spark`` on Databricks."""
    session = resolve_spark(spark or notebook_spark_if_defined())

    print("=" * 60)
    print("Bronze ingestion — starting")
    print("=" * 60)
    counts: dict[str, int] = {}
    for entity_key in INGEST_ORDER:
        counts[entity_key] = ingest_entity(session, config, entity_key)

    print("=" * 60)
    print("Bronze ingestion — complete")
    for entity_key, count in counts.items():
        print(f"  {entity_key}: {count} rows")
    print("=" * 60)
    return counts


def main(spark: SparkSession | None = None) -> None:
    parser = build_arg_parser("Bronze ingest: all CSV sources → Delta tables")
    args = parser.parse_args()
    config = config_from_args(args)

    if config.dry_run:
        print("=" * 60)
        print("Bronze dry-run — CSV validation only (no Spark/Delta write)")
        print("=" * 60)
        results = dry_run_all(config)
        total = sum(item["row_count"] for item in results)
        print("=" * 60)
        print(f"Total source rows across entities: {total}")
        print("=" * 60)
        return

    require_pyspark()
    run_ingestion(config, spark=spark or notebook_spark_if_defined())


if __name__ == "__main__":
    main(spark=notebook_spark_if_defined())
