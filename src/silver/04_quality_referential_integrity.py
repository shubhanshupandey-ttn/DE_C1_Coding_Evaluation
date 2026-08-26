#!/usr/bin/env python3
"""
Silver data quality — referential integrity checks (Iteration 3).

Validates orders.customer_id and orders.product_id against curated-eligible
parent keys (same population written to silver_customers / silver_products).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _load_silver_common import load_silver_common  # noqa: E402

sc = load_silver_common()

CHECK_REFERENTIAL_INTEGRITY = sc.CHECK_REFERENTIAL_INTEGRITY
SilverConfig = sc.SilverConfig
build_failures_from_rules = sc.build_failures_from_rules
col_is_blank = sc.col_is_blank
curated_eligible_parent_keys_df = sc.curated_eligible_parent_keys_df
notebook_spark_if_defined = sc.notebook_spark_if_defined
prepare_entity_dataframe = sc.prepare_entity_dataframe
read_bronze_table = sc.read_bronze_table
require_pyspark = sc.require_pyspark
resolve_spark = sc.resolve_spark

# Phase 2 defect mapping: D11 (orphan customer_id), D12 (orphan product_id)


def _load_module(stem: str) -> ModuleType:
    module_path = Path(__file__).resolve().parent / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(stem, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _prerequisite_dq_results(spark, config: SilverConfig) -> dict:
    """Run DQ modules required before RI when dq_results is not supplied."""
    completeness = _load_module("01_quality_completeness").run_completeness_all(spark, config)
    uniqueness = _load_module("02_quality_uniqueness").run_uniqueness_all(spark, config)
    type_validation = _load_module("03_quality_type_validation").run_type_validation_all(
        spark, config
    )
    business_logic = _load_module("05_quality_business_logic").run_business_logic_all(
        spark, config
    )
    return {
        "completeness": completeness,
        "uniqueness": uniqueness,
        "type_validation": type_validation,
        "business_logic": business_logic,
    }


def check_referential_integrity(
    orders_df,
    customer_parent_keys_df,
    product_parent_keys_df,
    config: SilverConfig,
    spark,
):
    """
    Flag order rows whose customer_id / product_id do not resolve to curated parents.

    Returns (orders_df_with_join_markers, failures_df).
    """
    from pyspark.sql import functions as F

    customer_keys = customer_parent_keys_df.withColumn("_customer_parent_ok", F.lit(True))
    product_keys = product_parent_keys_df.withColumn("_product_parent_ok", F.lit(True))

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


def run_referential_integrity_all(
    spark,
    config: SilverConfig | None = None,
    dq_results: dict | None = None,
) -> dict:
    """
    Validate order foreign keys against curated-eligible parent keys.

    When ``dq_results`` is omitted (standalone execution), prerequisite DQ modules
    (01, 02, 03, 05) are run first so business_logic results are available.
    """
    config = config or SilverConfig()
    if dq_results is None:
        dq_results = _prerequisite_dq_results(spark, config)

    customer_parent_keys = curated_eligible_parent_keys_df(
        dq_results["business_logic"]["customers"]["prepared_df"],
        "customers",
        dq_results,
    )
    product_parent_keys = curated_eligible_parent_keys_df(
        dq_results["business_logic"]["products"]["prepared_df"],
        "products",
        dq_results,
    )

    orders_bronze = read_bronze_table(spark, config, "orders")
    orders_prepared = prepare_entity_dataframe(orders_bronze, "orders")

    orders_marked, failures = check_referential_integrity(
        orders_prepared,
        customer_parent_keys,
        product_parent_keys,
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
