from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any, Dict, List


def build_medium_dataset() -> Dict[str, List[Dict[str, Any]]]:
    random.seed(42)
    regions = ["EU", "NA", "LATAM", "APAC"]
    base = datetime(2023, 1, 1)
    products: List[Dict[str, Any]] = []
    for i in range(2000):
        products.append(
            {
                "product_id": f"P{i:05d}",
                "category": random.choice(["A", "B", "C", "D"]),
                "unit_cost": round(random.uniform(2, 120), 2),
            }
        )
    customers: List[Dict[str, Any]] = []
    for i in range(3000):
        customers.append(
            {
                "customer_id": f"C{i:05d}",
                "region": random.choice(regions),
                "lifetime_value": round(random.uniform(50, 8000), 2),
            }
        )
    suppliers: List[Dict[str, Any]] = []
    for i in range(500):
        suppliers.append(
            {
                "supplier_id": f"U{i:04d}",
                "region": random.choice(regions),
                "rating": round(random.uniform(1, 5), 2),
            }
        )
    inventory: List[Dict[str, Any]] = []
    for i in range(5000):
        inventory.append(
            {
                "item_id": f"I{i:05d}",
                "stock": random.randint(0, 800),
                "warehouse": random.choice(["W1", "W2", "W3", "W4"]),
            }
        )
    sales: List[Dict[str, Any]] = []
    for i in range(10000):
        p = random.choice(products)
        c = random.choice(customers)
        sales.append(
            {
                "sale_id": f"S{i:05d}",
                "customer_id": c["customer_id"],
                "product_id": p["product_id"],
                "quantity": random.randint(1, 25),
                "price": round(random.uniform(5, 250), 2),
                "region": c["region"],
                "sale_date": (base + timedelta(days=random.randint(0, 500))).strftime(
                    "%Y-%m-%d"
                ),
            }
        )
    returns: List[Dict[str, Any]] = []
    for i in range(1500):
        returns.append(
            {
                "return_id": f"R{i:05d}",
                "amount": round(random.uniform(10, 500), 2),
                "reason": random.choice(["defect", "changed_mind", "other"]),
            }
        )
    orders: List[Dict[str, Any]] = []
    for i in range(4000):
        orders.append(
            {
                "order_id": f"O{i:05d}",
                "total": round(random.uniform(20, 2000), 2),
                "status": random.choice(["open", "shipped", "closed"]),
            }
        )
    shipments: List[Dict[str, Any]] = []
    for i in range(3000):
        shipments.append(
            {
                "shipment_id": f"H{i:05d}",
                "weight": round(random.uniform(0.5, 200), 2),
                "carrier": random.choice(["ACME", "FAST", "GLOBAL"]),
            }
        )
    return {
        "products": products,
        "customers": customers,
        "suppliers": suppliers,
        "inventory": inventory,
        "sales": sales,
        "returns": returns,
        "orders": orders,
        "shipments": shipments,
    }
