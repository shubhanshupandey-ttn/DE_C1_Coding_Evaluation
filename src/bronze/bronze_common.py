"""
Shared configuration and ingestion utilities for the Bronze layer.

Reads CSV source files as STRING columns to preserve Phase 2 intentional defects
(invalid dates, malformed values, empty strings) for Silver quality checks.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyspark.sql import DataFrame, SparkSession

# Source column definitions (match data-model.md / Phase 2 CSV headers)
CUSTOMER_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "country",
    "signup_date",
    "customer_segment",
    "lifetime_value",
]

PRODUCT_COLUMNS = [
    "product_id",
    "product_name",
    "category",
    "unit_price",
]

ORDER_COLUMNS = [
    "order_line_id",
    "order_id",
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "unit_price",
]

METADATA_COLUMNS = ("_ingestion_timestamp", "_source_file")

ENTITY_REGISTRY: dict[str, dict[str, Any]] = {
    "customers": {
        "csv_filename": "customers.csv",
        "table_name": "bronze_customers",
        "source_columns": CUSTOMER_COLUMNS,
    },
    "orders": {
        "csv_filename": "orders.csv",
        "table_name": "bronze_orders",
        "source_columns": ORDER_COLUMNS,
    },
    "products": {
        "csv_filename": "products.csv",
        "table_name": "bronze_products",
        "source_columns": PRODUCT_COLUMNS,
    },
}


@dataclass
class BronzeConfig:
    """Runtime configuration for Bronze ingestion."""

    data_dir: Path
    schema_name: str = "bronze"
    catalog_name: str | None = None
    write_mode: str = "overwrite"
    dry_run: bool = False


def repo_root() -> Path:
    """Repository root (two levels above src/bronze/)."""
    return Path(__file__).resolve().parents[2]


def default_data_dir() -> Path:
    return repo_root() / "data"


def build_arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=default_data_dir(),
        help="Directory containing source CSV files (default: <repo>/data)",
    )
    parser.add_argument(
        "--schema",
        dest="schema_name",
        default="bronze",
        help="Target schema/database name (default: bronze)",
    )
    parser.add_argument(
        "--catalog",
        dest="catalog_name",
        default=None,
        help="Optional Unity Catalog name (default: use schema only)",
    )
    parser.add_argument(
        "--write-mode",
        default="overwrite",
        choices=["overwrite", "append"],
        help="Delta write mode (default: overwrite for full reload)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate CSV inputs locally without Spark/Delta write",
    )
    return parser


def config_from_args(args: argparse.Namespace) -> BronzeConfig:
    return BronzeConfig(
        data_dir=args.data_dir,
        schema_name=args.schema_name,
        catalog_name=args.catalog_name,
        write_mode=args.write_mode,
        dry_run=args.dry_run,
    )


def qualified_table_name(config: BronzeConfig, table_name: str) -> str:
    if config.catalog_name:
        return f"{config.catalog_name}.{config.schema_name}.{table_name}"
    return f"{config.schema_name}.{table_name}"


def csv_path(config: BronzeConfig, entity_key: str) -> Path:
    filename = ENTITY_REGISTRY[entity_key]["csv_filename"]
    return config.data_dir / filename


def string_schema(columns: list[str]):
    from pyspark.sql.types import StringType, StructField, StructType

    return StructType([StructField(column, StringType(), nullable=True) for column in columns])


def get_spark() -> SparkSession:
    from pyspark.sql import SparkSession

    return SparkSession.builder.getOrCreate()


def ensure_schema_exists(spark: SparkSession, config: BronzeConfig) -> None:
    qualified = (
        f"{config.catalog_name}.{config.schema_name}"
        if config.catalog_name
        else config.schema_name
    )
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {qualified}")


def read_source_csv(spark: SparkSession, path: Path, columns: list[str]) -> DataFrame:
    """
    Read CSV with explicit STRING schema.

    No type casting, filtering, or cleansing — Bronze preserves source fidelity.
    """
    return (
        spark.read.option("header", True)
        .option("mode", "PERMISSIVE")
        .schema(string_schema(columns))
        .csv(str(path))
    )


def add_ingestion_metadata(df: DataFrame, source_file: Path) -> DataFrame:
    from pyspark.sql import functions as F

    return df.withColumn("_ingestion_timestamp", F.current_timestamp()).withColumn(
        "_source_file", F.lit(str(source_file.resolve()))
    )


def write_bronze_table(df: DataFrame, config: BronzeConfig, table_name: str) -> None:
    target = qualified_table_name(config, table_name)
    (
        df.write.format("delta")
        .mode(config.write_mode)
        .option("overwriteSchema", "true")
        .saveAsTable(target)
    )


def ingest_entity(spark: SparkSession, config: BronzeConfig, entity_key: str) -> int:
    """Ingest one entity CSV into its Bronze Delta table. Returns row count."""
    entity = ENTITY_REGISTRY[entity_key]
    path = csv_path(config, entity_key)
    if not path.is_file():
        raise FileNotFoundError(f"Source CSV not found: {path}")

    ensure_schema_exists(spark, config)
    source_df = read_source_csv(spark, path, entity["source_columns"])
    bronze_df = add_ingestion_metadata(source_df, path)
    write_bronze_table(bronze_df, config, entity["table_name"])

    row_count = bronze_df.count()
    print(
        f"[bronze] {entity_key}: wrote {row_count} rows to "
        f"{qualified_table_name(config, entity['table_name'])}"
    )
    return row_count


def count_csv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return sum(1 for _ in reader)


def dry_run_validate(config: BronzeConfig, entity_key: str) -> dict[str, Any]:
    """Local CSV validation without Spark (for dev/CI environments)."""
    entity = ENTITY_REGISTRY[entity_key]
    path = csv_path(config, entity_key)
    if not path.is_file():
        raise FileNotFoundError(f"Source CSV not found: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = list(reader)

    expected = entity["source_columns"]
    missing = [col for col in expected if col not in headers]
    extra = [col for col in headers if col not in expected]
    if missing:
        raise ValueError(f"{path.name}: missing columns {missing}")
    if extra:
        raise ValueError(f"{path.name}: unexpected columns {extra}")

    result: dict[str, Any] = {
        "entity": entity_key,
        "csv_path": str(path.resolve()),
        "target_table": qualified_table_name(config, entity["table_name"]),
        "row_count": len(rows),
        "columns": expected,
    }

    if entity_key == "customers":
        result["null_email_rows"] = sum(1 for r in rows if not r["email"].strip())
        result["duplicate_customer_id_keys"] = _duplicate_key_count(rows, "customer_id")
    elif entity_key == "products":
        result["invalid_unit_price_rows"] = sum(
            1 for r in rows if r["unit_price"].strip().upper() == "INVALID"
        )
    elif entity_key == "orders":
        result["orphan_customer_rows"] = sum(1 for r in rows if r["customer_id"] == "9999991")
        result["orphan_product_rows"] = sum(1 for r in rows if r["product_id"] == "9999992")
        result["non_positive_quantity_rows"] = sum(
            1 for r in rows if r["quantity"].lstrip("-").isdigit() and int(r["quantity"]) <= 0
        )

    print(f"[dry-run] {entity_key}: {result['row_count']} rows in {path.name}")
    print(f"          target table: {result['target_table']}")
    for key, value in result.items():
        if key.endswith("_rows") or key.endswith("_keys"):
            print(f"          {key}: {value}")
    return result


def _duplicate_key_count(rows: list[dict[str, str]], key: str) -> int:
    counts = Counter(r[key] for r in rows)
    return sum(1 for count in counts.values() if count > 1)


def dry_run_all(config: BronzeConfig) -> list[dict[str, Any]]:
    return [dry_run_validate(config, key) for key in ("customers", "products", "orders")]


def require_pyspark() -> None:
    try:
        import pyspark  # noqa: F401
    except ImportError as exc:
        print(
            "PySpark is not installed. Use --dry-run for local CSV validation, "
            "or execute on a Databricks cluster with PySpark available.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
