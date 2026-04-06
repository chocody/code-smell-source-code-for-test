from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any, Dict, List


def build_large_dataset() -> Dict[str, List[Dict[str, Any]]]:
    random.seed(42)
    regions = ["EU", "NA", "LATAM", "APAC"]
    depts = ["SALES", "OPS", "HR", "FIN"]
    base = datetime(2023, 1, 1)
    products = [
        {
            "product_id": f"P{i:05d}",
            "category": random.choice(["A", "B", "C", "D", "E"]),
            "unit_cost": round(random.uniform(1, 150), 2),
        }
        for i in range(5000)
    ]
    customers = [
        {
            "customer_id": f"C{i:05d}",
            "region": random.choice(regions),
            "lifetime_value": round(random.uniform(20, 12000), 2),
        }
        for i in range(8000)
    ]
    suppliers = [
        {
            "supplier_id": f"U{i:04d}",
            "region": random.choice(regions),
            "rating": round(random.uniform(1, 5), 2),
        }
        for i in range(2000)
    ]
    employees = [
        {
            "employee_id": f"E{i:05d}",
            "department": random.choice(depts),
            "salary": round(random.uniform(30000, 150000), 2),
        }
        for i in range(3000)
    ]
    inventory = [
        {
            "item_id": f"I{i:05d}",
            "stock": random.randint(0, 1200),
            "warehouse": random.choice(["W1", "W2", "W3", "W4", "W5"]),
        }
        for i in range(15000)
    ]
    sales: List[Dict[str, Any]] = []
    for i in range(30000):
        p = random.choice(products)
        c = random.choice(customers)
        sales.append(
            {
                "sale_id": f"S{i:05d}",
                "customer_id": c["customer_id"],
                "product_id": p["product_id"],
                "quantity": random.randint(1, 30),
                "price": round(random.uniform(4, 320), 2),
                "region": c["region"],
                "sale_date": (base + timedelta(days=random.randint(0, 700))).strftime(
                    "%Y-%m-%d"
                ),
            }
        )
    finance = [
        {
            "txn_id": f"F{i:06d}",
            "amount": round(random.uniform(-5000, 5000), 2),
            "type": random.choice(["credit", "debit", "fee"]),
        }
        for i in range(10000)
    ]
    procurement = [
        {
            "po_id": f"Q{i:05d}",
            "value": round(random.uniform(100, 50000), 2),
            "status": random.choice(["draft", "approved", "closed"]),
        }
        for i in range(5000)
    ]
    shipments = [
        {
            "shipment_id": f"H{i:05d}",
            "weight": round(random.uniform(0.2, 500), 2),
            "carrier": random.choice(["ACME", "FAST", "GLOBAL", "NIMBLE"]),
        }
        for i in range(8000)
    ]
    returns = [
        {
            "return_id": f"R{i:05d}",
            "amount": round(random.uniform(5, 900), 2),
            "reason": random.choice(["defect", "changed_mind", "other", "late"]),
        }
        for i in range(4000)
    ]
    crm = [
        {
            "interaction_id": f"X{i:05d}",
            "score": random.randint(1, 10),
            "channel": random.choice(["email", "phone", "chat"]),
        }
        for i in range(6000)
    ]
    return {
        "products": products,
        "customers": customers,
        "suppliers": suppliers,
        "employees": employees,
        "inventory": inventory,
        "sales": sales,
        "finance": finance,
        "procurement": procurement,
        "shipments": shipments,
        "returns": returns,
        "crm": crm,
    }
