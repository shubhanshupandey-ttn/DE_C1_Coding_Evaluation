#!/usr/bin/env python3
"""
Silver data quality — type validation (Iteration 2).

Validates numeric identifier parseability, dates, decimals, integers, and email format.
Identifiers remain STRING in Silver; malformed values produce explicit failures.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from silver_common import (  # noqa: E402
    CHECK_TYPE_VALIDATION,
    ENTITY_CONFIG,
    SilverConfig,
    build_failure_df,
    col_is_blank,
    col_is_numeric_identifier,
    col_is_valid_email,
    col_is_valid_iso_date,
    notebook_spark_if_defined,
    prepare_entity_dataframe,
    read_bronze_table,
    require_pyspark,
    resolve_spark,
    union_failures,
)

# Phase 2 defect mapping: D04, D05, D09, D13 + invalid numeric values


def _non_empty_source(column_name: str):
    from pyspark.sql import functions as F

    return ~col_is_blank(column_name)


def check_type_validation(df, entity_key: str, config: SilverConfig):
    """
    Validate types and formats. Returns (input_df, failures_df).
    """
    from pyspark.sql import functions as F

    entity = ENTITY_CONFIG[entity_key]
    spark = df.sparkSession
    failures = []

    for column in entity["id_columns"]:
        condition = _non_empty_source(column) & ~col_is_numeric_identifier(column)
        failures.append(
            build_failure_df(
                spark,
                df,
                entity_key,
                config,
                CHECK_TYPE_VALIDATION,
                condition,
                f"Identifier '{column}' is not numerically parseable",
                column,
            )
        )

    for column in entity["email_columns"]:
        condition = _non_empty_source(column) & ~col_is_valid_email(column)
        failures.append(
            build_failure_df(
                spark,
                df,
                entity_key,
                config,
                CHECK_TYPE_VALIDATION,
                condition,
                f"Email '{column}' has invalid format",
                column,
            )
        )

    for column in entity["date_columns"]:
        typed_col = f"{column}_typed"
        condition = _non_empty_source(column) & (
            ~col_is_valid_iso_date(column) | F.col(typed_col).isNull()
        )
        failures.append(
            build_failure_df(
                spark,
                df,
                entity_key,
                config,
                CHECK_TYPE_VALIDATION,
                condition,
                f"Date '{column}' is not a valid ISO date (YYYY-MM-DD)",
                column,
            )
        )

    for column in entity["int_columns"]:
        typed_col = f"{column}_typed"
        condition = _non_empty_source(column) & F.col(typed_col).isNull()
        failures.append(
            build_failure_df(
                spark,
                df,
                entity_key,
                config,
                CHECK_TYPE_VALIDATION,
                condition,
                f"Integer '{column}' is not parseable",
                column,
            )
        )

    for column, _precision, _scale in entity["decimal_columns"]:
        typed_col = f"{column}_typed"
        trimmed = F.trim(F.col(column))
        non_empty = _non_empty_source(column)
        # INVALID literal and other non-numeric strings
        condition = non_empty & F.col(typed_col).isNull()
        failures.append(
            build_failure_df(
                spark,
                df,
                entity_key,
                config,
                CHECK_TYPE_VALIDATION,
                condition,
                f"Decimal '{column}' is not parseable",
                column,
            )
        )

    return df, union_failures(spark, *failures)


def run_type_validation_for_entity(
    spark, entity_key: str, config: SilverConfig | None = None
):
    config = config or SilverConfig()
    bronze_df = read_bronze_table(spark, config, entity_key)
    prepared = prepare_entity_dataframe(bronze_df, entity_key)
    return check_type_validation(prepared, entity_key, config)


def run_type_validation_all(spark, config: SilverConfig | None = None) -> dict:
    config = config or SilverConfig()
    results = {}
    for entity_key in ("customers", "products", "orders"):
        prepared, failures = run_type_validation_for_entity(spark, entity_key, config)
        results[entity_key] = {"prepared_df": prepared, "failures_df": failures}
    return results


def main() -> None:
    require_pyspark()
    spark = resolve_spark(notebook_spark_if_defined())
    config = SilverConfig()

    print("=" * 60)
    print("Silver Iteration 2 — Type validation checks")
    print("=" * 60)

    for entity_key in ("customers", "products", "orders"):
        _, failures = run_type_validation_for_entity(spark, entity_key, config)
        count = failures.count()
        print(f"[type_validation] {entity_key}: {count} failure record(s)")
        if count > 0 and count <= 20:
            failures.select("business_key", "failed_column", "failure_reason").show(
                truncate=False
            )

    print("=" * 60)


if __name__ == "__main__":
    main()
