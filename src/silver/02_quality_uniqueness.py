#!/usr/bin/env python3
"""
Silver data quality — uniqueness checks (Iteration 2).

Validates primary business keys. order_line_id for orders (NOT order_id).
Deterministic duplicate handling: first occurrence canonical; duplicates flagged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _load_silver_common import load_silver_common  # noqa: E402

sc = load_silver_common()

CHECK_UNIQUENESS = sc.CHECK_UNIQUENESS
ENTITY_CONFIG = sc.ENTITY_CONFIG
SilverConfig = sc.SilverConfig
add_deterministic_row_number = sc.add_deterministic_row_number
build_failures_from_rules = sc.build_failures_from_rules
deterministic_tiebreaker_columns = sc.deterministic_tiebreaker_columns
notebook_spark_if_defined = sc.notebook_spark_if_defined
prepare_entity_dataframe = sc.prepare_entity_dataframe
read_bronze_table = sc.read_bronze_table
require_pyspark = sc.require_pyspark
resolve_spark = sc.resolve_spark

# Phase 2 defect mapping: D03 (dup customer_id), D08 (dup product_id), D16 (dup order_line_id)


def check_uniqueness(df, entity_key: str, config: SilverConfig, spark):
    """
    Flag duplicate business keys. Retain first canonical row deterministically.

    Ranking order: business key partition, tiebreaker columns ascending nulls last,
    then _row_num (stable input order).

    Returns (df_with_dup_rank, failures_df).
    """
    from pyspark.sql import functions as F
    from pyspark.sql.window import Window

    entity = ENTITY_CONFIG[entity_key]
    business_key = entity["business_key"]

    df_numbered = add_deterministic_row_number(df)
    tiebreakers = deterministic_tiebreaker_columns(df_numbered, entity_key, business_key)
    order_cols = [F.col(c).asc_nulls_last() for c in tiebreakers]
    order_cols.append(F.col("_row_num").asc())

    window = Window.partitionBy(F.col(business_key)).orderBy(*order_cols)
    ranked = df_numbered.withColumn("_dup_rank", F.row_number().over(window))

    duplicate_condition = F.col("_dup_rank") > F.lit(1)
    failures = build_failures_from_rules(
        ranked,
        entity_key,
        config,
        CHECK_UNIQUENESS,
        [
            (
                duplicate_condition,
                f"Duplicate business key '{business_key}' (non-canonical occurrence)",
                business_key,
            )
        ],
        spark=spark,
    )

    return ranked, failures


def run_uniqueness_for_entity(spark, entity_key: str, config: SilverConfig | None = None):
    config = config or SilverConfig()
    bronze_df = read_bronze_table(spark, config, entity_key)
    prepared = prepare_entity_dataframe(bronze_df, entity_key)
    return check_uniqueness(prepared, entity_key, config, spark)


def run_uniqueness_all(spark, config: SilverConfig | None = None) -> dict:
    config = config or SilverConfig()
    results = {}
    for entity_key in ("customers", "products", "orders"):
        ranked, failures = run_uniqueness_for_entity(spark, entity_key, config)
        results[entity_key] = {"ranked_df": ranked, "failures_df": failures}
    return results


def main() -> None:
    require_pyspark()
    spark = resolve_spark(notebook_spark_if_defined())
    config = SilverConfig()

    print("=" * 60)
    print("Silver Iteration 2 — Uniqueness checks")
    print(f"Serverless compat version: {sc.SERVERLESS_COMPAT_VERSION}")
    print("=" * 60)

    for entity_key in ("customers", "products", "orders"):
        _, failures = run_uniqueness_for_entity(spark, entity_key, config)
        count = failures.count()
        print(f"[uniqueness] {entity_key}: {count} failure record(s)")
        if count > 0 and count <= 20:
            failures.select("business_key", "failure_reason").show(truncate=False)

    print("=" * 60)


if __name__ == "__main__":
    main()
