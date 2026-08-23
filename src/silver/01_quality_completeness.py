#!/usr/bin/env python3
"""
Silver data quality — completeness checks (Iteration 2).

Validates required fields per data-quality-strategy.md.
Returns structured failure records for later quarantine (Iteration 4).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from silver_common import (  # noqa: E402
    CHECK_COMPLETENESS,
    ENTITY_CONFIG,
    SilverConfig,
    build_failure_df,
    col_is_blank,
    notebook_spark_if_defined,
    prepare_entity_dataframe,
    read_bronze_table,
    require_pyspark,
    resolve_spark,
    union_failures,
)

# Phase 2 defect mapping: D01 (null email), D02 (null name), D07 (null product name)


def check_completeness(df, entity_key: str, config: SilverConfig):
    """
    Check required fields for NULL/blank values.

    Returns (input_df, failures_df).
    """
    entity = ENTITY_CONFIG[entity_key]
    spark = df.sparkSession
    failures = []

    for column in entity["required_fields"]:
        if column not in df.columns:
            continue
        condition = col_is_blank(column)
        failure_df = build_failure_df(
            spark,
            df,
            entity_key,
            config,
            CHECK_COMPLETENESS,
            condition,
            f"Required field '{column}' is NULL or blank",
            column,
        )
        failures.append(failure_df)

    return df, union_failures(spark, *failures)


def run_completeness_for_entity(
    spark, entity_key: str, config: SilverConfig | None = None
):
    """Read Bronze, prepare types, run completeness. Returns (prepared_df, failures_df)."""
    config = config or SilverConfig()
    bronze_df = read_bronze_table(spark, config, entity_key)
    prepared = prepare_entity_dataframe(bronze_df, entity_key)
    return check_completeness(prepared, entity_key, config)


def run_completeness_all(spark, config: SilverConfig | None = None) -> dict:
    """Run completeness for customers, products, orders."""
    config = config or SilverConfig()
    results = {}
    for entity_key in ("customers", "products", "orders"):
        prepared, failures = run_completeness_for_entity(spark, entity_key, config)
        results[entity_key] = {"prepared_df": prepared, "failures_df": failures}
    return results


def main() -> None:
    require_pyspark()
    spark = resolve_spark(notebook_spark_if_defined())
    config = SilverConfig()

    print("=" * 60)
    print("Silver Iteration 2 — Completeness checks")
    print("=" * 60)

    for entity_key in ("customers", "products", "orders"):
        _, failures = run_completeness_for_entity(spark, entity_key, config)
        count = failures.count()
        print(f"[completeness] {entity_key}: {count} failure record(s)")
        if count > 0 and count <= 20:
            failures.select("business_key", "failed_column", "failure_reason").show(
                truncate=False
            )

    print("=" * 60)


if __name__ == "__main__":
    main()
