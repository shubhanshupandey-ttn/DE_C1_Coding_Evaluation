#!/usr/bin/env python3
"""
Orchestrate Bronze ingestion for all three source entities.

Execution order: customers → products → orders (dimensions before facts).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bronze_common import (  # noqa: E402
    build_arg_parser,
    config_from_args,
    dry_run_all,
    get_spark,
    ingest_entity,
    require_pyspark,
)

INGEST_ORDER = ("customers", "products", "orders")


def main() -> None:
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
    spark = get_spark()

    print("=" * 60)
    print("Bronze ingestion — starting")
    print("=" * 60)
    counts: dict[str, int] = {}
    for entity_key in INGEST_ORDER:
        counts[entity_key] = ingest_entity(spark, config, entity_key)

    print("=" * 60)
    print("Bronze ingestion — complete")
    for entity_key, count in counts.items():
        print(f"  {entity_key}: {count} rows")
    print("=" * 60)


if __name__ == "__main__":
    main()
