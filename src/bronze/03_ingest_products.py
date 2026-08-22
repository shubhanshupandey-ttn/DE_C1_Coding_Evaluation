#!/usr/bin/env python3
"""
Ingest data/products.csv into the bronze_products Delta table.

Bronze preserves all source values (including intentional Phase 2 defects).
No cleansing or data-quality filtering is applied.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bronze_common import (  # noqa: E402
    build_arg_parser,
    config_from_args,
    dry_run_validate,
    get_spark,
    ingest_entity,
    require_pyspark,
)

ENTITY_KEY = "products"


def main() -> None:
    parser = build_arg_parser("Bronze ingest: products.csv → bronze_products")
    args = parser.parse_args()
    config = config_from_args(args)

    if config.dry_run:
        dry_run_validate(config, ENTITY_KEY)
        return

    require_pyspark()
    spark = get_spark()
    ingest_entity(spark, config, ENTITY_KEY)


if __name__ == "__main__":
    main()
