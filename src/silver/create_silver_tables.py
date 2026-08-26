#!/usr/bin/env python3
"""
Silver layer orchestration (Iteration 5).

Runs the full Bronze → DQ → quarantine/summary → curated Silver pipeline.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _load_silver_common import load_silver_common  # noqa: E402

sc = load_silver_common()

ENTITY_CONFIG = sc.ENTITY_CONFIG
ENTITY_KEYS = sc.ENTITY_KEYS
filter_valid_rows = sc.filter_valid_rows
SILVER_CUSTOMERS_TABLE_NAME = sc.SILVER_CUSTOMERS_TABLE_NAME
SILVER_ORDERS_TABLE_NAME = sc.SILVER_ORDERS_TABLE_NAME
SILVER_PRODUCTS_TABLE_NAME = sc.SILVER_PRODUCTS_TABLE_NAME
SilverConfig = sc.SilverConfig
ensure_silver_schema_exists = sc.ensure_silver_schema_exists
notebook_spark_if_defined = sc.notebook_spark_if_defined
require_pyspark = sc.require_pyspark
resolve_spark = sc.resolve_spark
silver_table_name = sc.silver_table_name
write_delta_table = sc.write_delta_table

CURATED_CUSTOMER_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "country",
    "signup_date",
    "customer_segment",
    "lifetime_value",
]

CURATED_PRODUCT_COLUMNS = [
    "product_id",
    "product_name",
    "category",
    "unit_price",
]

CURATED_ORDER_COLUMNS = [
    "order_line_id",
    "order_id",
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "unit_price",
]


def _load_module(stem: str) -> ModuleType:
    module_path = Path(__file__).resolve().parent / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(stem, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def select_curated_customers(df):
    from pyspark.sql import functions as F

    return df.select(
        F.col("customer_id"),
        F.col("customer_name"),
        F.col("email"),
        F.col("country"),
        F.col("signup_date_typed").alias("signup_date"),
        F.col("customer_segment"),
        F.col("lifetime_value_typed").alias("lifetime_value"),
    )


def select_curated_products(df):
    from pyspark.sql import functions as F

    return df.select(
        F.col("product_id"),
        F.col("product_name"),
        F.col("category"),
        F.col("unit_price_typed").alias("unit_price"),
    )


def select_curated_orders(df):
    from pyspark.sql import functions as F

    return df.select(
        F.col("order_line_id"),
        F.col("order_id"),
        F.col("customer_id"),
        F.col("product_id"),
        F.col("order_date_typed").alias("order_date"),
        F.col("quantity_typed").alias("quantity"),
        F.col("unit_price_typed").alias("unit_price"),
    )


def build_curated_entity_df(entity_key: str, dq_results: dict):
    """Build curated Silver output for one entity from precomputed DQ results."""
    prepared_df = dq_results["business_logic"][entity_key]["prepared_df"]
    valid_df = filter_valid_rows(prepared_df, entity_key, dq_results)

    if entity_key == "customers":
        return select_curated_customers(valid_df)
    if entity_key == "products":
        return select_curated_products(valid_df)
    if entity_key == "orders":
        return select_curated_orders(valid_df)
    raise ValueError(f"Unsupported entity_key: {entity_key}")


def write_curated_silver_table(
    df,
    config: SilverConfig,
    table_name: str,
    columns: list[str],
) -> str:
    """Overwrite one curated Silver entity table."""
    target = silver_table_name(config, table_name)
    write_delta_table(df, target, columns=columns)
    return target


def run_silver_pipeline(spark, config: SilverConfig | None = None) -> dict:
    """
    Execute the full Silver pipeline:

    Bronze → DQ (01–05) → quarantine + DQ summary (06) → curated Silver tables.
    """
    config = config or SilverConfig()
    ensure_silver_schema_exists(spark, config)

    write_dq = _load_module("06_write_dq_results")
    dq_results = write_dq.run_all_dq_checks(spark, config)
    persistence = write_dq.run_dq_persistence(spark, config, dq_results=dq_results)

    curated = {}
    tables = {}
    for entity_key, table_name, columns in (
        ("customers", SILVER_CUSTOMERS_TABLE_NAME, CURATED_CUSTOMER_COLUMNS),
        ("products", SILVER_PRODUCTS_TABLE_NAME, CURATED_PRODUCT_COLUMNS),
        ("orders", SILVER_ORDERS_TABLE_NAME, CURATED_ORDER_COLUMNS),
    ):
        curated_df = build_curated_entity_df(entity_key, dq_results)
        tables[entity_key] = write_curated_silver_table(
            curated_df, config, table_name, columns
        )
        curated[entity_key] = curated_df

    return {
        "config": config,
        "dq_results": dq_results,
        "persistence": persistence,
        "curated": curated,
        "curated_tables": tables,
        "quarantine_table": persistence["quarantine_table"],
        "summary_table": persistence["summary_table"],
    }


def main() -> None:
    require_pyspark()
    spark = resolve_spark(notebook_spark_if_defined())
    config = SilverConfig()

    print("=" * 60)
    print("Silver Iteration 5 — Full pipeline")
    print(f"Serverless compat version: {sc.SERVERLESS_COMPAT_VERSION}")
    print("=" * 60)

    result = run_silver_pipeline(spark, config)

    for entity_key in ENTITY_KEYS:
        count = result["curated"][entity_key].count()
        print(f"[silver_{entity_key}] wrote {count} row(s) to {result['curated_tables'][entity_key]}")

    print(
        f"[quarantine] {result['persistence']['quarantine_df'].count()} failure record(s) "
        f"-> {result['quarantine_table']}"
    )
    print(
        f"[dq_summary] {result['persistence']['summary_df'].count()} summary row(s) "
        f"-> {result['summary_table']}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
