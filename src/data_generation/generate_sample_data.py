#!/usr/bin/env python3
"""
Generate sample e-commerce CSV datasets for the Databricks medallion pipeline.

Produces customers.csv, products.csv, and orders.csv (order line items) under data/.
Valid records preserve referential integrity; intentional defects are injected per
DEFECT_SPEC and documented in DATA_GENERATION_NOTES.md.
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Schema column definitions (CSV header order)
# ---------------------------------------------------------------------------

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

SEGMENTS = ("Premium", "Standard", "Basic")
COUNTRIES = (
    "United States",
    "Canada",
    "United Kingdom",
    "Germany",
    "India",
    "Australia",
    "France",
    "Japan",
)
CATEGORIES = (
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Sports",
    "Books",
    "Beauty",
    "Toys",
    "Grocery",
)
FIRST_NAMES = (
    "Alex",
    "Jordan",
    "Taylor",
    "Morgan",
    "Casey",
    "Riley",
    "Avery",
    "Quinn",
    "Sam",
    "Jamie",
)
LAST_NAMES = (
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Wilson",
    "Moore",
)

# Orphan FK sentinel — outside generated ID ranges
ORPHAN_CUSTOMER_ID = 9_999_991
ORPHAN_PRODUCT_ID = 9_999_992

# Fixed defect counts (must match DATA_GENERATION_NOTES.md defect matrix)
DEFECT_COUNTS = {
    "customers_null_email": 50,
    "customers_null_name": 10,
    "customers_duplicate_id_rows": 6,
    "customers_invalid_signup_date": 20,
    "customers_invalid_email_format": 30,
    "customers_future_signup_date": 10,
    "products_null_name": 8,
    "products_duplicate_id_rows": 6,
    "products_invalid_unit_price_type": 15,
    "products_negative_unit_price": 10,
    "orders_orphan_customer_id": 25,
    "orders_orphan_product_id": 25,
    "orders_invalid_order_date": 30,
    "orders_future_order_date": 15,
    "orders_non_positive_quantity": 40,
    "orders_duplicate_line_id_rows": 8,
    "orders_unit_price_catalog_mismatch": 20,
}


@dataclass
class GenerationConfig:
    """Configurable dataset sizes and reproducibility settings."""

    seed: int = 42
    num_customers: int = 1_000
    num_products: int = 200
    num_order_lines: int = 5_000
    output_dir: Path = Path("data")

    @property
    def num_orders(self) -> int:
        """Approximate distinct order headers (1–3 lines per order)."""
        return max(1, self.num_order_lines // 2)


@dataclass
class GenerationStats:
    customers: int = 0
    products: int = 0
    order_lines: int = 0
    distinct_order_ids: int = 0
    defects_applied: dict[str, int] | None = None


def repo_root() -> Path:
    """Repository root (two levels above this file: src/data_generation/)."""
    return Path(__file__).resolve().parents[2]


def parse_args() -> GenerationConfig:
    parser = argparse.ArgumentParser(
        description="Generate sample customers, products, and order line-item CSVs."
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument(
        "--customers", type=int, default=1_000, help="Number of valid customers (default: 1000)"
    )
    parser.add_argument(
        "--products", type=int, default=200, help="Number of valid products (default: 200)"
    )
    parser.add_argument(
        "--order-lines",
        type=int,
        default=5_000,
        dest="order_lines",
        help="Number of valid order line items (default: 5000)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for CSV files (default: <repo>/data)",
    )
    args = parser.parse_args()
    output = args.output_dir if args.output_dir else repo_root() / "data"
    return GenerationConfig(
        seed=args.seed,
        num_customers=args.customers,
        num_products=args.products,
        num_order_lines=args.order_lines,
        output_dir=output,
    )


def random_date(rng: random.Random, start: date, end: date) -> date:
    span = (end - start).days
    return start + timedelta(days=rng.randint(0, span))


def format_money(value: float) -> str:
    return f"{value:.2f}"


def generate_clean_customers(cfg: GenerationConfig, rng: random.Random) -> list[dict[str, Any]]:
    """Build valid customer rows with unique customer_id values 1..num_customers."""
    rows: list[dict[str, Any]] = []
    signup_start = date(2020, 1, 1)
    signup_end = date(2024, 12, 31)

    for cid in range(1, cfg.num_customers + 1):
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}{cid}@example.com"
        segment = rng.choices(SEGMENTS, weights=[2, 5, 3], k=1)[0]
        ltv = round(rng.uniform(100, 15_000), 2)
        rows.append(
            {
                "customer_id": str(cid),
                "customer_name": name,
                "email": email,
                "country": rng.choice(COUNTRIES),
                "signup_date": random_date(rng, signup_start, signup_end).isoformat(),
                "customer_segment": segment,
                "lifetime_value": format_money(ltv),
            }
        )
    return rows


def generate_clean_products(cfg: GenerationConfig, rng: random.Random) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pid in range(1, cfg.num_products + 1):
        category = rng.choice(CATEGORIES)
        price = round(rng.uniform(4.99, 499.99), 2)
        rows.append(
            {
                "product_id": str(pid),
                "product_name": f"{category} Item {pid}",
                "category": category,
                "unit_price": format_money(price),
            }
        )
    return rows


def generate_clean_order_lines(
    cfg: GenerationConfig,
    rng: random.Random,
    customers: list[dict[str, Any]],
    products: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    """
    Generate order line items. Multiple lines may share the same order_id.
    Returns (rows, distinct_order_id_count).
    """
    valid_customer_ids = [int(r["customer_id"]) for r in customers[: cfg.num_customers]]
    product_price = {int(r["product_id"]): float(r["unit_price"]) for r in products[: cfg.num_products]}

    rows: list[dict[str, Any]] = []
    order_start = date(2023, 1, 1)
    order_end = date(2025, 6, 30)
    next_line_id = 1
    next_order_id = 1
    order_ids_used: set[int] = set()

    while len(rows) < cfg.num_order_lines:
        lines_in_order = rng.randint(1, 3)
        order_id = next_order_id
        next_order_id += 1
        order_ids_used.add(order_id)
        customer_id = rng.choice(valid_customer_ids)
        order_date = random_date(rng, order_start, order_end).isoformat()

        for _ in range(lines_in_order):
            if len(rows) >= cfg.num_order_lines:
                break
            product_id = rng.randint(1, cfg.num_products)
            quantity = rng.randint(1, 5)
            unit_price = product_price[product_id]
            rows.append(
                {
                    "order_line_id": str(next_line_id),
                    "order_id": str(order_id),
                    "customer_id": str(customer_id),
                    "product_id": str(product_id),
                    "order_date": order_date,
                    "quantity": str(quantity),
                    "unit_price": format_money(unit_price),
                }
            )
            next_line_id += 1

    return rows, len(order_ids_used)


def _pick_indices(rng: random.Random, population: int, count: int) -> list[int]:
    count = min(count, population)
    return rng.sample(range(population), count)


def inject_customer_defects(
    rows: list[dict[str, Any]], rng: random.Random, defects: dict[str, int]
) -> None:
    """Mutate or append customer rows with documented defects."""
    n = len(rows)

    for idx in _pick_indices(rng, n, DEFECT_COUNTS["customers_null_email"]):
        rows[idx]["email"] = ""
        defects["customers_null_email"] += 1

    for idx in _pick_indices(rng, n, DEFECT_COUNTS["customers_null_name"]):
        rows[idx]["customer_name"] = ""
        defects["customers_null_name"] += 1

    for idx in _pick_indices(rng, n, DEFECT_COUNTS["customers_invalid_signup_date"]):
        rows[idx]["signup_date"] = "NOT-A-DATE"
        defects["customers_invalid_signup_date"] += 1

    for idx in _pick_indices(rng, n, DEFECT_COUNTS["customers_invalid_email_format"]):
        rows[idx]["email"] = "invalid-email-format"
        defects["customers_invalid_email_format"] += 1

    for idx in _pick_indices(rng, n, DEFECT_COUNTS["customers_future_signup_date"]):
        future = date.today() + timedelta(days=rng.randint(30, 400))
        rows[idx]["signup_date"] = future.isoformat()
        defects["customers_future_signup_date"] += 1

    # Duplicate customer_id: copy 3 existing rows with same ids (6 rows = 3 pairs)
    dup_sources = _pick_indices(rng, n, DEFECT_COUNTS["customers_duplicate_id_rows"])
    for src in dup_sources:
        rows.append(dict(rows[src]))
        defects["customers_duplicate_id_rows"] += 1


def inject_product_defects(
    rows: list[dict[str, Any]], rng: random.Random, defects: dict[str, int]
) -> None:
    n = len(rows)

    for idx in _pick_indices(rng, n, DEFECT_COUNTS["products_null_name"]):
        rows[idx]["product_name"] = ""
        defects["products_null_name"] += 1

    for idx in _pick_indices(rng, n, DEFECT_COUNTS["products_invalid_unit_price_type"]):
        rows[idx]["unit_price"] = "INVALID"
        defects["products_invalid_unit_price_type"] += 1

    for idx in _pick_indices(rng, n, DEFECT_COUNTS["products_negative_unit_price"]):
        rows[idx]["unit_price"] = format_money(-1 * rng.uniform(1, 50))
        defects["products_negative_unit_price"] += 1

    dup_sources = _pick_indices(rng, n, DEFECT_COUNTS["products_duplicate_id_rows"])
    for src in dup_sources:
        rows.append(dict(rows[src]))
        defects["products_duplicate_id_rows"] += 1


def inject_order_defects(
    rows: list[dict[str, Any]],
    rng: random.Random,
    defects: dict[str, int],
    products: list[dict[str, Any]],
) -> None:
    """Append defective order lines (valid lines already generated)."""
    product_price = {int(r["product_id"]): float(r["unit_price"]) for r in products if r["unit_price"].replace(".", "", 1).isdigit()}
    max_line_id = max(int(r["order_line_id"]) for r in rows)
    next_line_id = max_line_id + 1
    next_order_id = max(int(r["order_id"]) for r in rows) + 1

    def append_line(**kwargs: Any) -> None:
        nonlocal next_line_id, next_order_id
        row = {
            "order_line_id": str(kwargs.get("order_line_id", next_line_id)),
            "order_id": str(kwargs.get("order_id", next_order_id)),
            "customer_id": str(kwargs["customer_id"]),
            "product_id": str(kwargs["product_id"]),
            "order_date": kwargs["order_date"],
            "quantity": str(kwargs["quantity"]),
            "unit_price": kwargs["unit_price"],
        }
        rows.append(row)
        if "order_line_id" not in kwargs:
            next_line_id += 1
        next_order_id += 1

    valid_cid = 1
    valid_pid = 1
    valid_price = format_money(product_price.get(valid_pid, 19.99))

    for _ in range(DEFECT_COUNTS["orders_orphan_customer_id"]):
        append_line(
            customer_id=ORPHAN_CUSTOMER_ID,
            product_id=valid_pid,
            order_date="2024-05-01",
            quantity=1,
            unit_price=valid_price,
        )
        defects["orders_orphan_customer_id"] += 1

    for _ in range(DEFECT_COUNTS["orders_orphan_product_id"]):
        append_line(
            customer_id=valid_cid,
            product_id=ORPHAN_PRODUCT_ID,
            order_date="2024-05-02",
            quantity=1,
            unit_price=valid_price,
        )
        defects["orders_orphan_product_id"] += 1

    for _ in range(DEFECT_COUNTS["orders_invalid_order_date"]):
        append_line(
            customer_id=valid_cid,
            product_id=valid_pid,
            order_date="31/13/2024",
            quantity=2,
            unit_price=valid_price,
        )
        defects["orders_invalid_order_date"] += 1

    for _ in range(DEFECT_COUNTS["orders_future_order_date"]):
        future = date.today() + timedelta(days=rng.randint(10, 120))
        append_line(
            customer_id=valid_cid,
            product_id=valid_pid,
            order_date=future.isoformat(),
            quantity=1,
            unit_price=valid_price,
        )
        defects["orders_future_order_date"] += 1

    for _ in range(DEFECT_COUNTS["orders_non_positive_quantity"]):
        qty = rng.choice([0, -1, -3, -10])
        append_line(
            customer_id=valid_cid,
            product_id=valid_pid,
            order_date="2024-03-15",
            quantity=qty,
            unit_price=valid_price,
        )
        defects["orders_non_positive_quantity"] += 1

    # Duplicate order_line_id: reuse an existing line id on new rows
    existing_ids = [int(r["order_line_id"]) for r in rows[:100]]
    dup_ids = rng.sample(existing_ids, DEFECT_COUNTS["orders_duplicate_line_id_rows"] // 2)
    for dup_id in dup_ids:
        for _ in range(2):
            append_line(
                order_line_id=dup_id,
                customer_id=valid_cid,
                product_id=valid_pid,
                order_date="2024-04-01",
                quantity=1,
                unit_price=valid_price,
            )
            defects["orders_duplicate_line_id_rows"] += 1

    for _ in range(DEFECT_COUNTS["orders_unit_price_catalog_mismatch"]):
        pid = rng.randint(1, min(len(products), 200))
        catalog_price = product_price.get(pid, 25.0)
        wrong_price = format_money(catalog_price + rng.uniform(5, 50))
        append_line(
            customer_id=valid_cid,
            product_id=pid,
            order_date="2024-06-01",
            quantity=rng.randint(1, 3),
            unit_price=wrong_price,
        )
        defects["orders_unit_price_catalog_mismatch"] += 1


def write_csv(path: Path, columns: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def generate_datasets(cfg: GenerationConfig) -> GenerationStats:
    rng = random.Random(cfg.seed)
    defects: dict[str, int] = {key: 0 for key in DEFECT_COUNTS}

    customers = generate_clean_customers(cfg, rng)
    products = generate_clean_products(cfg, rng)
    orders, distinct_orders = generate_clean_order_lines(cfg, rng, customers, products)

    inject_customer_defects(customers, rng, defects)
    inject_product_defects(products, rng, defects)
    inject_order_defects(orders, rng, defects, products)

    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(cfg.output_dir / "customers.csv", CUSTOMER_COLUMNS, customers)
    write_csv(cfg.output_dir / "products.csv", PRODUCT_COLUMNS, products)
    write_csv(cfg.output_dir / "orders.csv", ORDER_COLUMNS, orders)

    return GenerationStats(
        customers=len(customers),
        products=len(products),
        order_lines=len(orders),
        distinct_order_ids=distinct_orders,
        defects_applied=defects,
    )


def print_stats(cfg: GenerationConfig, stats: GenerationStats) -> None:
    print("=" * 60)
    print("Sample data generation complete")
    print("=" * 60)
    print(f"Seed:              {cfg.seed}")
    print(f"Output directory:  {cfg.output_dir.resolve()}")
    print(f"Customers:         {stats.customers} rows")
    print(f"Products:          {stats.products} rows")
    print(f"Order lines:       {stats.order_lines} rows")
    print(f"Distinct order_id: {stats.distinct_order_ids} (valid lines only)")
    print("-" * 60)
    print("Intentional defects applied:")
    total = 0
    if stats.defects_applied:
        for name, count in sorted(stats.defects_applied.items()):
            print(f"  {name}: {count}")
            total += count
    print(f"  TOTAL defect injections: {total}")
    print("=" * 60)


def main() -> None:
    cfg = parse_args()
    stats = generate_datasets(cfg)
    print_stats(cfg, stats)


if __name__ == "__main__":
    main()
