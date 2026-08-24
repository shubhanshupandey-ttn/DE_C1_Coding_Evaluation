#!/usr/bin/env python3
"""
Silver data quality — business logic checks (Iteration 3).

Validates domain rules per data-quality-strategy.md and SILVER_LAYER_NOTES.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _load_silver_common import load_silver_common  # noqa: E402

sc = load_silver_common()

CHECK_BUSINESS_LOGIC = sc.CHECK_BUSINESS_LOGIC
SilverConfig = sc.SilverConfig
build_failures_from_rules = sc.build_failures_from_rules
col_is_blank = sc.col_is_blank
col_is_valid_customer_segment = sc.col_is_valid_customer_segment
notebook_spark_if_defined = sc.notebook_spark_if_defined
prepare_canonical_entity_df = sc.prepare_canonical_entity_df
prepare_entity_dataframe = sc.prepare_entity_dataframe
read_bronze_table = sc.read_bronze_table
require_pyspark = sc.require_pyspark
resolve_spark = sc.resolve_spark

# Phase 2 defect mapping: D06, D10, D14, D15, D17 + invalid customer_segment


def check_customer_business_logic(df, config: SilverConfig, spark):
    """Customer business rules. Returns (input_df, failures_df)."""
    from pyspark.sql import functions as F

    rules = [
        (
            F.col("signup_date_typed").isNotNull()
            & (F.col("signup_date_typed") > F.current_date()),
            "Signup date is in the future",
            "signup_date",
        ),
        (
            ~col_is_blank("customer_segment") & ~col_is_valid_customer_segment("customer_segment"),
            "Customer segment is not one of Premium, Standard, Basic",
            "customer_segment",
        ),
    ]
    failures = build_failures_from_rules(
        df, "customers", config, CHECK_BUSINESS_LOGIC, rules, spark=spark
    )
    return df, failures


def check_product_business_logic(df, config: SilverConfig, spark):
    """Product business rules. Returns (input_df, failures_df)."""
    from pyspark.sql import functions as F

    rules = [
        (
            F.col("unit_price_typed").isNotNull() & (F.col("unit_price_typed") < F.lit(0)),
            "Product unit price must be non-negative",
            "unit_price",
        ),
    ]
    failures = build_failures_from_rules(
        df, "products", config, CHECK_BUSINESS_LOGIC, rules, spark=spark
    )
    return df, failures


def check_order_business_logic(df, canonical_products_df, config: SilverConfig, spark):
    """Order business rules. Returns (input_df, failures_df)."""
    from pyspark.sql import functions as F

    catalog_prices = canonical_products_df.select(
        F.col("product_id"),
        F.col("unit_price_typed").alias("_catalog_unit_price_typed"),
    )
    orders_marked = df.join(catalog_prices, on="product_id", how="left")

    rules = [
        (
            F.col("quantity_typed").isNotNull() & (F.col("quantity_typed") <= F.lit(0)),
            "Order quantity must be greater than zero",
            "quantity",
        ),
        (
            F.col("order_date_typed").isNotNull()
            & (F.col("order_date_typed") > F.current_date()),
            "Order date is in the future",
            "order_date",
        ),
        (
            F.col("unit_price_typed").isNotNull()
            & F.col("_catalog_unit_price_typed").isNotNull()
            & (F.col("unit_price_typed") != F.col("_catalog_unit_price_typed")),
            "Order unit price does not match product catalog price",
            "unit_price",
        ),
    ]
    failures = build_failures_from_rules(
        orders_marked, "orders", config, CHECK_BUSINESS_LOGIC, rules, spark=spark
    )
    return orders_marked, failures


def run_business_logic_for_entity(
    spark, entity_key: str, config: SilverConfig | None = None, canonical_products_df=None
):
    config = config or SilverConfig()
    bronze_df = read_bronze_table(spark, config, entity_key)
    prepared = prepare_entity_dataframe(bronze_df, entity_key)

    if entity_key == "customers":
        return check_customer_business_logic(prepared, config, spark)
    if entity_key == "products":
        return check_product_business_logic(prepared, config, spark)
    if entity_key == "orders":
        if canonical_products_df is None:
            _, canonical_products_df = prepare_canonical_entity_df(spark, config, "products")
        return check_order_business_logic(prepared, canonical_products_df, config, spark)
    raise ValueError(f"Unsupported entity_key: {entity_key}")


def run_business_logic_all(spark, config: SilverConfig | None = None) -> dict:
    """Run business-logic checks for customers, products, and orders."""
    config = config or SilverConfig()
    _, canonical_products = prepare_canonical_entity_df(spark, config, "products")

    results = {}
    for entity_key in ("customers", "products", "orders"):
        if entity_key == "orders":
            prepared, failures = run_business_logic_for_entity(
                spark, entity_key, config, canonical_products_df=canonical_products
            )
        else:
            prepared, failures = run_business_logic_for_entity(spark, entity_key, config)
        results[entity_key] = {"prepared_df": prepared, "failures_df": failures}
    return results


def main() -> None:
    require_pyspark()
    spark = resolve_spark(notebook_spark_if_defined())
    config = SilverConfig()

    print("=" * 60)
    print("Silver Iteration 3 — Business logic checks")
    print(f"Serverless compat version: {sc.SERVERLESS_COMPAT_VERSION}")
    print("=" * 60)

    results = run_business_logic_all(spark, config)
    for entity_key in ("customers", "products", "orders"):
        failures = results[entity_key]["failures_df"]
        count = failures.count()
        print(f"[business_logic] {entity_key}: {count} failure record(s)")
        if count > 0 and count <= 30:
            failures.groupBy("failed_column").count().show(truncate=False)

    print("=" * 60)


if __name__ == "__main__":
    main()
