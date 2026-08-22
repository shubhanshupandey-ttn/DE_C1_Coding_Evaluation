#!/usr/bin/env python3
"""
Ingest data/orders.csv into the bronze_orders Delta table.

orders.csv contains ORDER LINE ITEMS (one row per line).
Bronze preserves all source values; Silver performs quality checks later.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bronze_common import (  # noqa: E402
    build_arg_parser,
    config_from_args,
    dry_run_validate,
    ingest_entity,
    notebook_spark_if_defined,
    require_pyspark,
    resolve_spark,
)

ENTITY_KEY = "orders"


def main(spark=None) -> None:
    parser = build_arg_parser("Bronze ingest: orders.csv → bronze_orders")
    args = parser.parse_args()
    config = config_from_args(args)

    if config.dry_run:
        dry_run_validate(config, ENTITY_KEY)
        return

    require_pyspark()
    session = resolve_spark(spark or notebook_spark_if_defined())
    ingest_entity(session, config, ENTITY_KEY)


if __name__ == "__main__":
    main(spark=notebook_spark_if_defined())
