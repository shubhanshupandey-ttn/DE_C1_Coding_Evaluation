#!/usr/bin/env python3
"""
Silver data quality — referential integrity checks (Iteration 3).

Validates orders.customer_id and orders.product_id against canonical valid parent keys.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _load_silver_common import load_silver_common  # noqa: E402

sc = load_silver_common()

CHECK_REFERENTIAL_INTEGRITY = sc.CHECK_REFERENTIAL_INTEGRITY
SilverConfig = sc.SilverConfig
build_failures_from_rules = sc.build_failures_from_rules
canonical_parent_keys_df = sc.canonical_parent_keys_df
col_is_blank = sc.col_is_blank
notebook_spark_if_defined = sc.notebook_spark_if_defined
prepare_canonical_entity_df = sc.prepare_canonical_entity_df
prepare_entity_dataframe = sc.prepare_entity_dataframe
read_bronze_table = sc.read_bronze_table
require_pyspark = sc.require_pyspark
resolve_spark = sc.resolve_spark

# Phase 2 defect mapping: D11 (orphan customer_id), D12 (orphan product_id)


def check_referential_integrity(
    orders_df,
    canonical_customers_df,
    canonical_products_df,
    config: SilverConfig,
    spark,
):
    """
    Flag order rows whose customer_id / product_id do not resolve to canonical parents.

    Returns (orders_df_with_join_markers, failures_df).
    """
    from pyspark.sql import functions as F

    customer_keys = canonical_parent_keys_df(canonical_customers_df, "customers").withColumn(
        "_customer_parent_ok", F.lit(True)
    )
    product_keys = canonical_parent_keys_df(canonical_products_df, "products").withColumn(
        "_product_parent_ok", F.lit(True)
    )

    orders_marked = (
        orders_df.join(customer_keys, on="customer_id", how="left")
        .join(product_keys, on="product_id", how="left")
    )

    orphan_customer = ~col_is_blank("customer_id") & F.col("_customer_parent_ok").isNull()
    orphan_product = ~col_is_blank("product_id") & F.col("_product_parent_ok").isNull()

    failures = build_failures_from_rules(
        orders_marked,
        "orders",
        config,
        CHECK_REFERENTIAL_INTEGRITY,
        [
            (
                orphan_customer,
                "Foreign key 'customer_id' does not resolve to a valid customer",
                "customer_id",
            ),
            (
                orphan_product,
                "Foreign key 'product_id' does not resolve to a valid product",
                "product_id",
            ),
        ],
        spark=spark,
    )
    return orders_marked, failures


def run_referential_integrity_all(spark, config: SilverConfig | None = None) -> dict:
    """Build canonical parents and validate order foreign keys."""
    config = config or SilverConfig()

    _, canonical_customers = prepare_canonical_entity_df(spark, config, "customers")
    _, canonical_products = prepare_canonical_entity_df(spark, config, "products")

    orders_bronze = read_bronze_table(spark, config, "orders")
    orders_prepared = prepare_entity_dataframe(orders_bronze, "orders")

    orders_marked, failures = check_referential_integrity(
        orders_prepared,
        canonical_customers,
        canonical_products,
        config,
        spark,
    )

    return {
        "orders": {
            "prepared_df": orders_marked,
            "failures_df": failures,
        }
    }


def main() -> None:
    require_pyspark()
    spark = resolve_spark(notebook_spark_if_defined())
    config = SilverConfig()

    print("=" * 60)
    print("Silver Iteration 3 — Referential integrity checks")
    print(f"Serverless compat version: {sc.SERVERLESS_COMPAT_VERSION}")
    print("=" * 60)

    results = run_referential_integrity_all(spark, config)
    failures = results["orders"]["failures_df"]
    count = failures.count()
    print(f"[referential_integrity] orders: {count} failure record(s)")
    if count > 0 and count <= 30:
        failures.groupBy("failed_column").count().show(truncate=False)
        failures.select("business_key", "failed_column", "failure_reason").show(
            truncate=False
        )

    print("=" * 60)


if __name__ == "__main__":
    main()
