"""
Shared configuration and utilities for the Silver layer.

Iteration 2: type standardization helpers, completeness/uniqueness/type-validation
support, and structured failure records for later quarantine (Iterations 4–5).
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    from pyspark.sql import Column, DataFrame, SparkSession

# ---------------------------------------------------------------------------
# Catalog / entity configuration (aligned with data-model.md)
# ---------------------------------------------------------------------------

DEFAULT_CATALOG = "de_c1_coding_evaluation"
DEFAULT_BRONZE_SCHEMA = "bronze"
DEFAULT_SILVER_SCHEMA = "silver"

BRONZE_METADATA_COLUMNS = ("_ingestion_timestamp", "_source_file")

CUSTOMER_STRING_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "country",
    "signup_date",
    "customer_segment",
    "lifetime_value",
]

PRODUCT_STRING_COLUMNS = [
    "product_id",
    "product_name",
    "category",
    "unit_price",
]

ORDER_STRING_COLUMNS = [
    "order_line_id",
    "order_id",
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "unit_price",
]

ENTITY_CONFIG: dict[str, dict[str, Any]] = {
    "customers": {
        "bronze_table": "bronze_customers",
        "business_key": "customer_id",
        "string_columns": CUSTOMER_STRING_COLUMNS,
        "required_fields": CUSTOMER_STRING_COLUMNS,
        "id_columns": ["customer_id"],
        "date_columns": ["signup_date"],
        "decimal_columns": [("lifetime_value", 12, 2)],
        "int_columns": [],
        "email_columns": ["email"],
    },
    "products": {
        "bronze_table": "bronze_products",
        "business_key": "product_id",
        "string_columns": PRODUCT_STRING_COLUMNS,
        "required_fields": PRODUCT_STRING_COLUMNS,
        "id_columns": ["product_id"],
        "date_columns": [],
        "decimal_columns": [("unit_price", 10, 2)],
        "int_columns": [],
        "email_columns": [],
    },
    "orders": {
        "bronze_table": "bronze_orders",
        "business_key": "order_line_id",
        "string_columns": ORDER_STRING_COLUMNS,
        "required_fields": ORDER_STRING_COLUMNS,
        "id_columns": ["order_line_id", "order_id", "customer_id", "product_id"],
        "date_columns": ["order_date"],
        "decimal_columns": [("unit_price", 10, 2)],
        "int_columns": ["quantity"],
        "email_columns": [],
    },
}

CHECK_COMPLETENESS = "completeness"
CHECK_UNIQUENESS = "uniqueness"
CHECK_TYPE_VALIDATION = "type_validation"

QUARANTINE_COLUMNS = [
    "entity_name",
    "business_key",
    "check_category",
    "failure_reason",
    "failed_column",
    "bronze_source_values",
    "quarantine_timestamp",
    "run_timestamp",
]


@dataclass
class SilverConfig:
    """Runtime configuration for Silver processing."""

    catalog_name: str = DEFAULT_CATALOG
    bronze_schema: str = DEFAULT_BRONZE_SCHEMA
    silver_schema: str = DEFAULT_SILVER_SCHEMA
    run_timestamp: datetime = field(default_factory=datetime.utcnow)


def qualified_table(config: SilverConfig, schema: str, table: str) -> str:
    return f"{config.catalog_name}.{schema}.{table}"


def bronze_table_name(config: SilverConfig, entity_key: str) -> str:
    table = ENTITY_CONFIG[entity_key]["bronze_table"]
    return qualified_table(config, config.bronze_schema, table)


def resolve_spark(explicit: SparkSession | None = None) -> SparkSession:
    if explicit is not None:
        return explicit

    from pyspark.sql import SparkSession

    active = SparkSession.getActiveSession()
    if active is not None:
        return active

    import __main__ as main_module

    notebook_spark = getattr(main_module, "spark", None)
    if notebook_spark is not None and hasattr(notebook_spark, "read"):
        return notebook_spark

    import os

    if os.environ.get("DATABRICKS_RUNTIME_VERSION"):
        raise RuntimeError(
            "No active Spark session on Databricks. Pass spark=spark from the notebook."
        )

    return SparkSession.builder.getOrCreate()


def notebook_spark_if_defined() -> SparkSession | None:
    try:
        candidate = spark  # type: ignore[name-defined]  # noqa: F821
    except NameError:
        return None
    if candidate is not None and hasattr(candidate, "read"):
        return candidate
    return None


def read_bronze_table(spark: SparkSession, config: SilverConfig, entity_key: str) -> DataFrame:
    table = bronze_table_name(config, entity_key)
    return spark.table(table)


def require_pyspark() -> None:
    try:
        import pyspark  # noqa: F401
    except ImportError as exc:
        print("PySpark is not installed.", file=sys.stderr)
        raise SystemExit(1) from exc


# ---------------------------------------------------------------------------
# Pure-Python validation helpers (testable without Spark)
# ---------------------------------------------------------------------------

_NUMERIC_ID_PATTERN = re.compile(r"^-?\d+$")
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_blank(value: str | None) -> bool:
    return value is None or str(value).strip() == ""


def is_numeric_identifier(value: str | None) -> bool:
    if is_blank(value):
        return False
    return _NUMERIC_ID_PATTERN.match(str(value).strip()) is not None


def is_valid_email_format(value: str | None) -> bool:
    if is_blank(value):
        return False
    return _EMAIL_PATTERN.match(str(value).strip()) is not None


def is_valid_iso_date_string(value: str | None) -> bool:
    if is_blank(value):
        return False
    text = str(value).strip()
    if not _ISO_DATE_PATTERN.match(text):
        return False
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def parse_decimal_string(value: str | None) -> float | None:
    if is_blank(value):
        return None
    text = str(value).strip()
    if text.upper() == "INVALID":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_int_string(value: str | None) -> int | None:
    if is_blank(value):
        return None
    text = str(value).strip()
    try:
        return int(text)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Spark column helpers
# ---------------------------------------------------------------------------


def trim_string_columns(df: DataFrame, columns: Sequence[str]) -> DataFrame:
    from pyspark.sql import functions as F

    result = df
    for column in columns:
        if column in result.columns:
            result = result.withColumn(column, F.trim(F.col(column)))
    return result


def col_is_blank(column_name: str) -> Column:
    from pyspark.sql import functions as F

    return F.col(column_name).isNull() | (F.trim(F.col(column_name)) == F.lit(""))


def col_is_numeric_identifier(column_name: str) -> Column:
    from pyspark.sql import functions as F

    trimmed = F.trim(F.col(column_name))
    return trimmed.rlike(r"^-?\d+$")


def col_is_valid_email(column_name: str) -> Column:
    from pyspark.sql import functions as F

    trimmed = F.trim(F.col(column_name))
    return trimmed.rlike(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def col_is_valid_iso_date(column_name: str) -> Column:
    from pyspark.sql import functions as F

    trimmed = F.trim(F.col(column_name))
    parsed = F.to_date(trimmed, "yyyy-MM-dd")
    return parsed.isNotNull() & trimmed.rlike(r"^\d{4}-\d{2}-\d{2}$")


def add_typed_columns(df: DataFrame, entity_key: str) -> DataFrame:
    """
    Add safely parsed typed columns (NULL when parse fails).

    Identifier columns remain STRING; typed companions use `_typed` suffix except
    identifiers which keep STRING names after trim.
    """
    from pyspark.sql import functions as F

    config = ENTITY_CONFIG[entity_key]
    result = trim_string_columns(df, config["string_columns"])

    for column in config["date_columns"]:
        trimmed = F.trim(F.col(column))
        result = result.withColumn(f"{column}_typed", F.to_date(trimmed, "yyyy-MM-dd"))

    for column in config["int_columns"]:
        trimmed = F.trim(F.col(column))
        result = result.withColumn(
            f"{column}_typed",
            F.when(trimmed.rlike(r"^-?\d+$"), trimmed.cast("int")).otherwise(F.lit(None)),
        )

    for column, precision, scale in config["decimal_columns"]:
        trimmed = F.trim(F.col(column))
        result = result.withColumn(
            f"{column}_typed",
            F.when(trimmed.rlike(r"^-?\d+(\.\d+)?$"), trimmed.cast(f"decimal({precision},{scale})")).otherwise(
                F.lit(None)
            ),
        )

    return result


def business_columns(entity_key: str) -> list[str]:
    """Bronze business columns used for failure traceability (excludes metadata)."""
    return list(ENTITY_CONFIG[entity_key]["string_columns"])


def bronze_source_json_expr(entity_key: str) -> Column:
    from pyspark.sql import functions as F

    fields = business_columns(entity_key)
    map_cols = []
    for name in fields:
        map_cols.extend([F.lit(name), F.col(name)])
    return F.to_json(F.create_map(*map_cols))


def empty_failures_df(spark: SparkSession):
    """Return an empty failures DataFrame with the quarantine schema (serverless-safe)."""
    from pyspark.sql import functions as F

    return spark.range(0).select(
        F.lit(None).cast("string").alias("entity_name"),
        F.lit(None).cast("string").alias("business_key"),
        F.lit(None).cast("string").alias("check_category"),
        F.lit(None).cast("string").alias("failure_reason"),
        F.lit(None).cast("string").alias("failed_column"),
        F.lit(None).cast("string").alias("bronze_source_values"),
        F.lit(None).cast("timestamp").alias("quarantine_timestamp"),
        F.lit(None).cast("timestamp").alias("run_timestamp"),
    )


def build_failure_df(
    spark: SparkSession,
    source_df: DataFrame,
    entity_key: str,
    config: SilverConfig,
    check_category: str,
    condition: Column,
    failure_reason: str,
    failed_column: str,
) -> DataFrame:
    """Materialize rows matching condition into the quarantine-compatible schema."""
    from pyspark.sql import functions as F

    entity = ENTITY_CONFIG[entity_key]
    business_key = entity["business_key"]
    run_ts = F.lit(config.run_timestamp)
    now_ts = F.current_timestamp()

    failing = source_df.filter(condition)
    return failing.select(
        F.lit(entity_key).alias("entity_name"),
        F.col(business_key).alias("business_key"),
        F.lit(check_category).alias("check_category"),
        F.lit(failure_reason).alias("failure_reason"),
        F.lit(failed_column).alias("failed_column"),
        bronze_source_json_expr(entity_key).alias("bronze_source_values"),
        now_ts.alias("quarantine_timestamp"),
        run_ts.alias("run_timestamp"),
    )


def union_failures(spark: SparkSession, *frames: DataFrame) -> DataFrame:
    """Union failure DataFrames; empty inputs are skipped via union (serverless-safe)."""
    result: DataFrame | None = None
    for frame in frames:
        if frame is None:
            continue
        result = frame if result is None else result.unionByName(frame)
    return result if result is not None else empty_failures_df(spark)


def deterministic_tiebreaker_columns(df: DataFrame, entity_key: str, business_key: str) -> list[str]:
    """Columns for deterministic duplicate ranking (ascending, nulls last)."""
    excluded = {business_key, "_dup_rank", "_row_num"}
    excluded.update(BRONZE_METADATA_COLUMNS)
    return sorted(c for c in df.columns if c not in excluded)


def add_deterministic_row_number(df: DataFrame) -> DataFrame:
    from pyspark.sql import functions as F
    from pyspark.sql.window import Window

    window = Window.orderBy(
        *[F.col(c).asc_nulls_last() for c in sorted(df.columns)],
    )
    return df.withColumn("_row_num", F.row_number().over(window))


def prepare_entity_dataframe(df: DataFrame, entity_key: str) -> DataFrame:
    """Trim strings and add typed columns (Iteration 2 type standardization)."""
    return add_typed_columns(df, entity_key)
