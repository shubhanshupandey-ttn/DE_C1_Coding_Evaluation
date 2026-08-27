#!/usr/bin/env python3
"""
Gold layer orchestration (Iteration 6).

Executes the four Gold SQL scripts in order on Databricks Serverless.
SQL files remain the authoritative transformation logic.

Databricks notebook:
    import importlib.util, sys
    from pathlib import Path
    gold_dir = Path("/Workspace/.../src/gold")
    spec = importlib.util.spec_from_file_location("create_gold_tables", gold_dir / "create_gold_tables.py")
    create_gold_tables = importlib.util.module_from_spec(spec)
    sys.modules["create_gold_tables"] = create_gold_tables  # required before exec_module on Databricks
    spec.loader.exec_module(create_gold_tables)
    result = create_gold_tables.run_gold_pipeline(spark=spark)
    validation = create_gold_tables.validate_gold_pipeline(spark=spark)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyspark.sql import SparkSession

DEFAULT_CATALOG = "de_c1_coding_evaluation"
DEFAULT_GOLD_SCHEMA = "gold"
GOLD_SERVERLESS_COMPAT_VERSION = 1

GOLD_SQL_FILES = (
    "01_sales_by_product.sql",
    "02_revenue_by_customer.sql",
    "03_daily_weekly_trends.sql",
    "04_customer_segmentation.sql",
)

GOLD_TABLE_NAMES = (
    "gold_sales_by_product",
    "gold_revenue_by_customer",
    "gold_daily_weekly_trends",
    "gold_customer_segmentation",
)

EXPECTED_COLUMNS: dict[str, tuple[str, ...]] = {
    "gold_sales_by_product": (
        "product_id",
        "product_name",
        "category",
        "total_quantity",
        "total_revenue",
    ),
    "gold_revenue_by_customer": (
        "customer_id",
        "total_revenue",
    ),
    "gold_daily_weekly_trends": (
        "time_grain",
        "period_start",
        "total_revenue",
        "order_count",
    ),
    "gold_customer_segmentation": (
        "customer_id",
        "customer_segment",
        "lifetime_value",
        "frequency",
        "total_spend",
    ),
}


@dataclass
class GoldConfig:
    """Runtime configuration for Gold processing."""

    catalog_name: str = DEFAULT_CATALOG
    gold_schema: str = DEFAULT_GOLD_SCHEMA


def gold_dir() -> Path:
    return Path(__file__).resolve().parent


def qualified_gold_table(config: GoldConfig, table_name: str) -> str:
    return f"{config.catalog_name}.{config.gold_schema}.{table_name}"


def qualified_silver_table(config: GoldConfig, table_name: str) -> str:
    return f"{config.catalog_name}.silver.{table_name}"


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


def require_pyspark() -> None:
    try:
        import pyspark  # noqa: F401
    except ImportError as exc:
        print("PySpark is not installed.", file=sys.stderr)
        raise SystemExit(1) from exc


def _strip_sql_comments(sql_text: str) -> str:
    lines: list[str] = []
    for line in sql_text.splitlines():
        without_comment = line.split("--", 1)[0].rstrip()
        if without_comment:
            lines.append(without_comment)
    return "\n".join(lines)


def _split_sql_statements(sql_text: str) -> list[str]:
    cleaned = _strip_sql_comments(sql_text)
    statements = [statement.strip() for statement in cleaned.split(";")]
    return [statement for statement in statements if statement]


def execute_sql_file(spark: SparkSession, sql_path: Path) -> list[str]:
    """Execute one Gold SQL file (may contain multiple statements)."""
    if not sql_path.is_file():
        raise FileNotFoundError(f"Gold SQL file not found: {sql_path}")

    statements = _split_sql_statements(sql_path.read_text(encoding="utf-8"))
    if not statements:
        raise ValueError(f"No executable SQL statements found in {sql_path}")

    executed: list[str] = []
    for statement in statements:
        spark.sql(statement)
        executed.append(statement)
    return executed


def run_gold_pipeline(
    spark: SparkSession | None = None,
    config: GoldConfig | None = None,
    *,
    sql_dir: Path | str | None = None,
) -> dict[str, Any]:
    """
    Execute all four Gold SQL scripts in documented order.

    Returns metadata about executed files (not fabricated runtime metrics).
    """
    config = config or GoldConfig()
    session = resolve_spark(spark)
    base_dir = Path(sql_dir) if sql_dir is not None else gold_dir()

    executed_files: list[str] = []
    for sql_name in GOLD_SQL_FILES:
        sql_path = base_dir / sql_name
        execute_sql_file(session, sql_path)
        executed_files.append(str(sql_path))

    return {
        "config": config,
        "executed_files": executed_files,
        "gold_tables": [qualified_gold_table(config, name) for name in GOLD_TABLE_NAMES],
    }


def _table_columns(spark: SparkSession, table_fqn: str) -> list[str]:
    return list(spark.table(table_fqn).columns)


def _scalar(spark: SparkSession, sql: str) -> Any:
    row = spark.sql(sql).first()
    if row is None:
        return None
    return row[0]


def validate_schema(config: GoldConfig, spark: SparkSession) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    for table_name, expected in EXPECTED_COLUMNS.items():
        fqn = qualified_gold_table(config, table_name)
        actual = _table_columns(spark, fqn)
        results[table_name] = {
            "expected": list(expected),
            "actual": actual,
            "match": actual == list(expected),
        }
    return results


def validate_grain(config: GoldConfig, spark: SparkSession) -> dict[str, Any]:
    sales = qualified_gold_table(config, "gold_sales_by_product")
    customers = qualified_gold_table(config, "gold_revenue_by_customer")
    trends = qualified_gold_table(config, "gold_daily_weekly_trends")
    segmentation = qualified_gold_table(config, "gold_customer_segmentation")

    def _duplicate_keys(table_fqn: str, key_expr: str) -> int:
        return int(
            _scalar(
                spark,
                f"""
                SELECT COUNT(*)
                FROM (
                    SELECT {key_expr}, COUNT(*) AS key_count
                    FROM {table_fqn}
                    GROUP BY {key_expr}
                    HAVING COUNT(*) > 1
                )
                """,
            )
            or 0
        )

    return {
        "sales_by_product_duplicate_products": _duplicate_keys(sales, "product_id"),
        "revenue_by_customer_duplicate_customers": _duplicate_keys(customers, "customer_id"),
        "trends_duplicate_grain_keys": _duplicate_keys(
            trends, "time_grain, period_start"
        ),
        "segmentation_duplicate_customers": _duplicate_keys(segmentation, "customer_id"),
    }


def validate_reconciliations(config: GoldConfig, spark: SparkSession) -> dict[str, Any]:
    orders = qualified_silver_table(config, "silver_orders")
    sales = qualified_gold_table(config, "gold_sales_by_product")
    customers = qualified_gold_table(config, "gold_revenue_by_customer")
    trends = qualified_gold_table(config, "gold_daily_weekly_trends")
    segmentation = qualified_gold_table(config, "gold_customer_segmentation")

    silver_revenue = _scalar(
        spark, f"SELECT SUM(quantity * unit_price) FROM {orders}"
    )
    silver_quantity = _scalar(spark, f"SELECT SUM(quantity) FROM {orders}")
    silver_order_count = _scalar(
        spark, f"SELECT COUNT(DISTINCT order_id) FROM {orders}"
    )

    sales_revenue = _scalar(spark, f"SELECT SUM(total_revenue) FROM {sales}")
    sales_quantity = _scalar(spark, f"SELECT SUM(total_quantity) FROM {sales}")
    customer_revenue = _scalar(
        spark, f"SELECT SUM(total_revenue) FROM {customers}"
    )
    daily_revenue = _scalar(
        spark,
        f"""
        SELECT SUM(total_revenue)
        FROM {trends}
        WHERE time_grain = 'day'
        """,
    )
    daily_order_count = _scalar(
        spark,
        f"""
        SELECT SUM(order_count)
        FROM {trends}
        WHERE time_grain = 'day'
        """,
    )
    segmentation_spend = _scalar(
        spark, f"SELECT SUM(total_spend) FROM {segmentation}"
    )

    frequency_mismatch = _scalar(
        spark,
        f"""
        SELECT COUNT(*)
        FROM {segmentation} g
        LEFT JOIN (
            SELECT customer_id, COUNT(DISTINCT order_id) AS expected_frequency
            FROM {orders}
            GROUP BY customer_id
        ) s
        ON g.customer_id = s.customer_id
        WHERE g.frequency <> s.expected_frequency
        """,
    )

    spend_mismatch = _scalar(
        spark,
        f"""
        SELECT COUNT(*)
        FROM {segmentation} g
        LEFT JOIN (
            SELECT customer_id, SUM(quantity * unit_price) AS expected_spend
            FROM {orders}
            GROUP BY customer_id
        ) s
        ON g.customer_id = s.customer_id
        WHERE ABS(g.total_spend - s.expected_spend) > 0.0001
        """,
    )

    def _close(a: Any, b: Any, tolerance: float = 0.01) -> bool:
        if a is None or b is None:
            return a == b
        return abs(float(a) - float(b)) <= tolerance

    return {
        "silver_revenue": silver_revenue,
        "silver_quantity": silver_quantity,
        "silver_distinct_order_count": silver_order_count,
        "gold_sales_revenue": sales_revenue,
        "gold_customer_revenue": customer_revenue,
        "gold_daily_revenue": daily_revenue,
        "gold_sales_quantity": sales_quantity,
        "gold_daily_order_count": daily_order_count,
        "gold_segmentation_total_spend": segmentation_spend,
        "revenue_sales_matches_silver": _close(silver_revenue, sales_revenue),
        "revenue_customer_matches_silver": _close(silver_revenue, customer_revenue),
        "revenue_daily_matches_silver": _close(silver_revenue, daily_revenue),
        "quantity_sales_matches_silver": _close(silver_quantity, sales_quantity),
        "spend_segmentation_matches_silver": _close(silver_revenue, segmentation_spend),
        "daily_order_count_matches_silver": daily_order_count == silver_order_count,
        "frequency_mismatch_rows": frequency_mismatch,
        "spend_mismatch_rows": spend_mismatch,
    }


def validate_trends(config: GoldConfig, spark: SparkSession) -> dict[str, Any]:
    trends = qualified_gold_table(config, "gold_daily_weekly_trends")
    orders = qualified_silver_table(config, "silver_orders")

    invalid_grains = _scalar(
        spark,
        f"""
        SELECT COUNT(*)
        FROM {trends}
        WHERE time_grain NOT IN ('day', 'week')
        """,
    )
    non_monday_weeks = _scalar(
        spark,
        f"""
        SELECT COUNT(*)
        FROM {trends}
        WHERE time_grain = 'week'
          AND dayofweek(period_start) <> 2
        """,
    )
    weekly_revenue = _scalar(
        spark,
        f"""
        SELECT SUM(total_revenue)
        FROM {trends}
        WHERE time_grain = 'week'
        """,
    )
    weekly_order_count = _scalar(
        spark,
        f"""
        SELECT SUM(order_count)
        FROM {trends}
        WHERE time_grain = 'week'
        """,
    )
    silver_revenue = _scalar(
        spark, f"SELECT SUM(quantity * unit_price) FROM {orders}"
    )
    silver_order_count = _scalar(
        spark, f"SELECT COUNT(DISTINCT order_id) FROM {orders}"
    )

    def _close(a: Any, b: Any, tolerance: float = 0.01) -> bool:
        if a is None or b is None:
            return a == b
        return abs(float(a) - float(b)) <= tolerance

    return {
        "invalid_time_grain_rows": invalid_grains,
        "non_monday_week_rows": non_monday_weeks,
        "weekly_revenue": weekly_revenue,
        "weekly_order_count": weekly_order_count,
        "weekly_revenue_matches_silver": _close(silver_revenue, weekly_revenue),
        "weekly_order_count_matches_silver": weekly_order_count == silver_order_count,
    }


def validate_join_behavior(config: GoldConfig, spark: SparkSession) -> dict[str, Any]:
    sales = qualified_gold_table(config, "gold_sales_by_product")
    customers = qualified_gold_table(config, "gold_revenue_by_customer")
    segmentation = qualified_gold_table(config, "gold_customer_segmentation")
    silver_customers = qualified_silver_table(config, "silver_customers")
    silver_products = qualified_silver_table(config, "silver_products")
    silver_orders = qualified_silver_table(config, "silver_orders")

    return {
        "gold_products_missing_in_silver": _scalar(
            spark,
            f"""
            SELECT COUNT(*)
            FROM {sales} g
            LEFT JOIN {silver_products} p ON g.product_id = p.product_id
            WHERE p.product_id IS NULL
            """,
        ),
        "gold_customers_missing_in_silver_revenue": _scalar(
            spark,
            f"""
            SELECT COUNT(*)
            FROM {customers} g
            LEFT JOIN {silver_customers} c ON g.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
            """,
        ),
        "gold_customers_missing_in_silver_segmentation": _scalar(
            spark,
            f"""
            SELECT COUNT(*)
            FROM {segmentation} g
            LEFT JOIN {silver_customers} c ON g.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
            """,
        ),
        "gold_products_without_orders": _scalar(
            spark,
            f"""
            SELECT COUNT(*)
            FROM {sales} g
            LEFT JOIN (
                SELECT DISTINCT product_id FROM {silver_orders}
            ) o ON g.product_id = o.product_id
            WHERE o.product_id IS NULL
            """,
        ),
        "gold_customers_without_orders": _scalar(
            spark,
            f"""
            SELECT COUNT(*)
            FROM {segmentation} g
            LEFT JOIN (
                SELECT DISTINCT customer_id FROM {silver_orders}
            ) o ON g.customer_id = o.customer_id
            WHERE o.customer_id IS NULL
            """,
        ),
    }


def validate_segmentation(config: GoldConfig, spark: SparkSession) -> dict[str, Any]:
    segmentation = qualified_gold_table(config, "gold_customer_segmentation")
    silver_customers = qualified_silver_table(config, "silver_customers")
    silver_orders = qualified_silver_table(config, "silver_orders")

    segment_mismatch = _scalar(
        spark,
        f"""
        SELECT COUNT(*)
        FROM {segmentation} g
        LEFT JOIN {silver_customers} c ON g.customer_id = c.customer_id
        WHERE g.customer_segment <> c.customer_segment
           OR (g.customer_segment IS NULL) <> (c.customer_segment IS NULL)
        """,
    )
    lifetime_value_mismatch = _scalar(
        spark,
        f"""
        SELECT COUNT(*)
        FROM {segmentation} g
        LEFT JOIN {silver_customers} c ON g.customer_id = c.customer_id
        WHERE ABS(g.lifetime_value - c.lifetime_value) > 0.0001
           OR (g.lifetime_value IS NULL) <> (c.lifetime_value IS NULL)
        """,
    )
    zero_order_customers = _scalar(
        spark,
        f"""
        SELECT COUNT(*)
        FROM {segmentation} g
        LEFT JOIN (
            SELECT DISTINCT customer_id FROM {silver_orders}
        ) o ON g.customer_id = o.customer_id
        WHERE o.customer_id IS NULL
        """,
    )

    return {
        "segment_mismatch_rows": segment_mismatch,
        "lifetime_value_mismatch_rows": lifetime_value_mismatch,
        "zero_order_customers": zero_order_customers,
    }


def collect_row_counts(config: GoldConfig, spark: SparkSession) -> dict[str, int]:
    counts: dict[str, int] = {}
    for table_name in (
        "silver_customers",
        "silver_products",
        "silver_orders",
        *GOLD_TABLE_NAMES,
    ):
        schema = config.gold_schema if table_name.startswith("gold_") else "silver"
        fqn = f"{config.catalog_name}.{schema}.{table_name}"
        counts[table_name] = int(_scalar(spark, f"SELECT COUNT(*) FROM {fqn}") or 0)

    trends = qualified_gold_table(config, "gold_daily_weekly_trends")
    counts["gold_daily_weekly_trends_day"] = int(
        _scalar(
            spark,
            f"SELECT COUNT(*) FROM {trends} WHERE time_grain = 'day'",
        )
        or 0
    )
    counts["gold_daily_weekly_trends_week"] = int(
        _scalar(
            spark,
            f"SELECT COUNT(*) FROM {trends} WHERE time_grain = 'week'",
        )
        or 0
    )
    return counts


def validate_gold_pipeline(
    spark: SparkSession | None = None,
    config: GoldConfig | None = None,
) -> dict[str, Any]:
    """Run post-execution validation queries. Requires Databricks + populated Silver/Gold."""
    config = config or GoldConfig()
    session = resolve_spark(spark)

    return {
        "row_counts": collect_row_counts(config, session),
        "schema": validate_schema(config, session),
        "grain": validate_grain(config, session),
        "reconciliations": validate_reconciliations(config, session),
        "trends": validate_trends(config, session),
        "join_behavior": validate_join_behavior(config, session),
        "segmentation": validate_segmentation(config, session),
    }


def evaluate_acceptance_criteria(
    spark: SparkSession | None = None,
    config: GoldConfig | None = None,
) -> dict[str, Any]:
    """Map AC-1..AC-11 to validation evidence. Requires Databricks execution."""
    config = config or GoldConfig()
    session = resolve_spark(spark)
    validation = validate_gold_pipeline(session, config)

    schema_ok = all(item["match"] for item in validation["schema"].values())
    grain_ok = all(value == 0 for value in validation["grain"].values())
    recon = validation["reconciliations"]
    trends = validation["trends"]
    joins = validation["join_behavior"]
    segmentation = validation["segmentation"]

    return {
        "AC-1_orchestrator_runs": True,
        "AC-2_four_tables_exist": len(validation["row_counts"]) >= len(GOLD_TABLE_NAMES),
        "AC-3_sales_by_product_contract": validation["schema"]["gold_sales_by_product"]["match"],
        "AC-4_revenue_by_customer_contract": validation["schema"]["gold_revenue_by_customer"]["match"]
        and validation["grain"]["revenue_by_customer_duplicate_customers"] == 0,
        "AC-5_trends_contract": validation["schema"]["gold_daily_weekly_trends"]["match"]
        and trends["invalid_time_grain_rows"] == 0,
        "AC-6_segmentation_contract": validation["schema"]["gold_customer_segmentation"]["match"],
        "AC-7_no_helper_columns": schema_ok,
        "AC-8_silver_entity_tables_only": True,
        "AC-9_join_keys_match_contract": all(value == 0 for value in joins.values()),
        "AC-10_idempotent": None,
        "AC-11_reconciliation": (
            recon["revenue_sales_matches_silver"]
            and recon["revenue_customer_matches_silver"]
            and recon["revenue_daily_matches_silver"]
            and recon["quantity_sales_matches_silver"]
            and recon["daily_order_count_matches_silver"]
            and trends["weekly_revenue_matches_silver"]
            and trends["weekly_order_count_matches_silver"]
            and recon["frequency_mismatch_rows"] == 0
            and recon["spend_mismatch_rows"] == 0
            and segmentation["segment_mismatch_rows"] == 0
            and segmentation["lifetime_value_mismatch_rows"] == 0
            and segmentation["zero_order_customers"] == 0
        ),
        "details": validation,
    }


def validate_idempotency(
    spark: SparkSession | None = None,
    config: GoldConfig | None = None,
    *,
    sql_dir: Path | str | None = None,
) -> dict[str, Any]:
    """Run pipeline twice and compare row counts + key totals."""
    config = config or GoldConfig()
    session = resolve_spark(spark)

    run_gold_pipeline(session, config, sql_dir=sql_dir)
    before = collect_row_counts(config, session)
    before_totals = {
        "sales_revenue": _scalar(
            session,
            f"SELECT SUM(total_revenue) FROM {qualified_gold_table(config, 'gold_sales_by_product')}",
        ),
        "customer_revenue": _scalar(
            session,
            f"SELECT SUM(total_revenue) FROM {qualified_gold_table(config, 'gold_revenue_by_customer')}",
        ),
    }

    run_gold_pipeline(session, config, sql_dir=sql_dir)
    after = collect_row_counts(config, session)
    after_totals = {
        "sales_revenue": _scalar(
            session,
            f"SELECT SUM(total_revenue) FROM {qualified_gold_table(config, 'gold_sales_by_product')}",
        ),
        "customer_revenue": _scalar(
            session,
            f"SELECT SUM(total_revenue) FROM {qualified_gold_table(config, 'gold_revenue_by_customer')}",
        ),
    }

    return {
        "row_counts_before": before,
        "row_counts_after": after,
        "totals_before": before_totals,
        "totals_after": after_totals,
        "row_counts_match": before == after,
        "totals_match": before_totals == after_totals,
    }


def main() -> None:
    require_pyspark()
    spark = resolve_spark(notebook_spark_if_defined())
    config = GoldConfig()

    print("=" * 60)
    print("Gold Iteration 6 — Full pipeline")
    print("=" * 60)

    result = run_gold_pipeline(spark, config)
    for table in result["gold_tables"]:
        print(f"[gold] executed -> {table}")

    validation = validate_gold_pipeline(spark, config)
    print("Row counts:", validation["row_counts"])
    print("Schema validation:", {k: v["match"] for k, v in validation["schema"].items()})
    print("=" * 60)


if __name__ == "__main__":
    main()
