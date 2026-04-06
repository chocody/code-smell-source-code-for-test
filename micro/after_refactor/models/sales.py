from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any, Dict, List

SALES_TARGET_COUNT = 500
INVENTORY_TARGET_COUNT = 200
CUSTOMER_TARGET_COUNT = 100
PRODUCT_TARGET_COUNT = 50


def build_dataset() -> Dict[str, List[Dict[str, Any]]]:
    random.seed(42)
    regions = ["EU", "NA", "LATAM", "APAC"]
    base = datetime(2023, 1, 1)
    products: List[Dict[str, Any]] = []
    for i in range(PRODUCT_TARGET_COUNT):
        products.append(
            {
                "product_id": f"P{i:04d}",
                "category": random.choice(["A", "B", "C"]),
                "unit_cost": round(random.uniform(5, 80), 2),
            }
        )
    customers: List[Dict[str, Any]] = []
    for i in range(CUSTOMER_TARGET_COUNT):
        customers.append(
            {
                "customer_id": f"C{i:04d}",
                "region": random.choice(regions),
                "lifetime_value": round(random.uniform(100, 5000), 2),
            }
        )
    inventory: List[Dict[str, Any]] = []
    for i in range(INVENTORY_TARGET_COUNT):
        inventory.append(
            {
                "item_id": f"I{i:04d}",
                "stock": random.randint(0, 500),
                "reorder_level": random.randint(10, 100),
                "warehouse": random.choice(["W1", "W2", "W3"]),
            }
        )
    sales: List[Dict[str, Any]] = []
    for i in range(SALES_TARGET_COUNT):
        p = random.choice(products)
        c = random.choice(customers)
        qty = random.randint(1, 20)
        price = round(random.uniform(10, 200), 2)
        sales.append(
            {
                "sale_id": f"S{i:05d}",
                "customer_id": c["customer_id"],
                "product_id": p["product_id"],
                "quantity": qty,
                "price": price,
                "region": c["region"],
                "sale_date": (base + timedelta(days=random.randint(0, 400))).strftime(
                    "%Y-%m-%d"
                ),
            }
        )
    return {
        "sales": sales,
        "inventory": inventory,
        "customers": customers,
        "products": products,
    }
