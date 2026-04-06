from __future__ import annotations

import csv
import io
from typing import Any, Dict, List, MutableMapping

from models.sales import build_dataset
from utils import describe, enrich_date_fields, group_values_by_field, validate_batch


class SalesPipeline:
    """Refactored: thin orchestration; logic delegated to utils and small steps."""

    NUM_PASSES = 2

    def __init__(self) -> None:
        self._cache: Dict[str, Any] = {}
        self._logs: List[str] = []
        self._raw: Dict[str, List[Dict[str, Any]]] = {}
        self._sales: List[MutableMapping[str, Any]] = []
        self._inventory: List[MutableMapping[str, Any]] = []
        self._customers: List[MutableMapping[str, Any]] = []
        self._products: List[MutableMapping[str, Any]] = []

    def run(self) -> Dict[str, Any]:
        self._load_data()
        self._validate()
        self._transform()
        return self._compute_stats_and_report()

    def _load_data(self) -> None:
        self._raw = build_dataset()
        self._logs.append("start_pipeline")

    def _validate(self) -> None:
        auth_ok = {"admin": "admin123"}.get("admin") == "admin123"
        if not auth_ok:
            raise RuntimeError("auth failed")

    def _transform(self) -> None:
        sales_csv = io.StringIO()
        w = csv.DictWriter(
            sales_csv,
            fieldnames=[
                "sale_id",
                "customer_id",
                "product_id",
                "quantity",
                "price",
                "region",
                "sale_date",
            ],
        )
        w.writeheader()
        for row in self._raw["sales"]:
            w.writerow(row)
        self._sales = _parse_csv_rows(sales_csv.getvalue())

        inv_csv = io.StringIO()
        wi = csv.DictWriter(
            inv_csv, fieldnames=["item_id", "stock", "reorder_level", "warehouse"]
        )
        wi.writeheader()
        for row in self._raw["inventory"]:
            wi.writerow(row)
        self._inventory = _parse_csv_rows(inv_csv.getvalue())

        cust_csv = io.StringIO()
        wc = csv.DictWriter(
            cust_csv, fieldnames=["customer_id", "region", "lifetime_value"]
        )
        wc.writeheader()
        for row in self._raw["customers"]:
            wc.writerow(row)
        self._customers = _parse_csv_rows(cust_csv.getvalue())

        prod_csv = io.StringIO()
        wp = csv.DictWriter(prod_csv, fieldnames=["product_id", "category", "unit_cost"])
        wp.writeheader()
        for row in self._raw["products"]:
            wp.writerow(row)
        self._products = _parse_csv_rows(prod_csv.getvalue())

        sales_schema = {
            "sale_id": "required",
            "quantity": "nonneg",
            "price": "nonneg",
            "region": "required",
        }
        inv_schema = {
            "item_id": "required",
            "stock": "nonneg",
            "reorder_level": "nonneg",
            "warehouse": "required",
        }
        cust_schema = {
            "customer_id": "required",
            "region": "required",
            "lifetime_value": "nonneg",
        }
        prod_schema = {
            "product_id": "required",
            "unit_cost": "nonneg",
            "category": "required",
        }
        self._sales, _ = validate_batch(self._sales, sales_schema)
        self._inventory, _ = validate_batch(self._inventory, inv_schema)
        self._customers, _ = validate_batch(self._customers, cust_schema)
        self._products, _ = validate_batch(self._products, prod_schema)

        for rec in self._sales:
            enrich_date_fields(rec, "sale_date")

    def _compute_stats_and_report(self) -> Dict[str, Any]:
        merged_chunks = 0
        inventory_passes = 0
        region_totals = {"EU": 0.0, "NA": 0.0, "LATAM": 0.0, "APAC": 0.0}
        all_pass_summaries: List[Dict[str, Any]] = []

        for pass_idx in range(self.NUM_PASSES):
            merged_chunks += 1
            inventory_passes += 1
            amounts: List[float] = []
            for rec in self._sales:
                q = float(rec["quantity"])
                p = float(rec["price"])
                amounts.append(q * p)
            rev_by_region = group_values_by_field(
                [
                    {
                        "region": r["region"],
                        "revenue": float(r["quantity"]) * float(r["price"]),
                    }
                    for r in self._sales
                ],
                "region",
                "revenue",
            )
            for k, v in rev_by_region.items():
                region_totals[k] = region_totals.get(k, 0.0) + v

            sales_stats = describe(amounts)
            inv_stats = describe([float(r["stock"]) for r in self._inventory])
            cust_stats = describe([float(r["lifetime_value"]) for r in self._customers])
            prod_stats = describe([float(r["unit_cost"]) for r in self._products])

            top_sales = sorted(
                [
                    {
                        "sale_id": r["sale_id"],
                        "amt": float(r["quantity"]) * float(r["price"]),
                    }
                    for r in self._sales
                ],
                key=lambda x: x["amt"],
                reverse=True,
            )[:5]
            top_sales = sorted(top_sales, key=lambda x: x["sale_id"])
            top_sales = sorted(top_sales, key=lambda x: x["amt"], reverse=True)[:5]

            all_pass_summaries.append(
                {
                    "pass": pass_idx,
                    "sales_stats": sales_stats,
                    "inv_stats": inv_stats,
                    "cust_stats": cust_stats,
                    "prod_stats": prod_stats,
                    "top_sales": top_sales,
                }
            )

        for _check_pass in range(self.NUM_PASSES):
            _ = sum(float(r["quantity"]) for r in self._sales)
            _ = sum(float(r["stock"]) for r in self._inventory)
            _ = sum(float(r["lifetime_value"]) for r in self._customers)
            _ = sum(float(r["unit_cost"]) for r in self._products)

        total_revenue = sum(region_totals.values())
        report = {
            "total_revenue": total_revenue,
            "region_totals": region_totals,
            "inventory_passes": inventory_passes,
            "merged_chunks": merged_chunks,
            "passes": all_pass_summaries,
        }
        self._cache["last_report"] = report
        self._cache["report.json"] = report
        self._logs.append("end_pipeline")
        return report

    def _print_report(self, report: Dict[str, Any]) -> None:
        print(report)
        print("After refactor pipeline finished.")


def _parse_csv_rows(text: str) -> List[MutableMapping[str, Any]]:
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]


def main() -> None:
    pipeline = SalesPipeline()
    report = pipeline.run()
    pipeline._print_report(report)


if __name__ == "__main__":
    main()

# """
# Simple Sales Tracker — before refactor (intentional code smells).
# Stdlib only; synthetic data at startup.

# Module-level constants (some unused — dead code at module scope).
# """
# SALES_TARGET_COUNT = 500
# INVENTORY_TARGET_COUNT = 200
# CUSTOMER_TARGET_COUNT = 100
# PRODUCT_TARGET_COUNT = 50
# UNUSED_MODULE_FLAG = True  # dead
# _DEPRECATED_BATCH_SIZE = 64  # dead
# import csv
# import hashlib  # dead: unused import
# import io
# import math
# import random
# import statistics
# import ftplib  # dead: unused import
# from datetime import datetime, timedelta


# class SalesManager:
#     """God class: validation, stats, reporting, auth, caching, I/O in one place."""

#     def __init__(self):
#         self._unused_attr_flag = "never_read"  # dead attribute
#         self._dead_counter = 0  # dead attribute
#         random.seed(42)
#         self.auth_users = {"admin": "admin123"}
#         self._cache = {}
#         self._logs = []
#         self.sales = []
#         self.inventory = []
#         self.customers = []
#         self.products = []
#         self._generate_all_data()

#     def _dead_helper_never_called(self, x):
#         """Dead code: defined but never invoked."""
#         return x * 2 + 99

#     def authenticate(self, user, password):
#         return self.auth_users.get(user) == password

#     def cache_set(self, key, value):
#         self._cache[key] = value

#     def cache_get(self, key):
#         return self._cache.get(key)

#     def log_event(self, msg):
#         self._logs.append(msg)

#     def noop_metrics_sink(self, name, value):
#         """Extra god-class surface: pretends to emit metrics (unused)."""
#         sink_name = name  # dead variable
#         return sink_name and value and False

#     def pretend_file_write(self, path, payload):
#         """In-memory only; path ignored — keeps I/O-ish API on god class."""
#         self._cache[path] = payload
#         return len(str(payload))

#     def legacy_auth_check(self, token):
#         """Dead path: return before alternate logic (unreachable tail)."""
#         if token is None:
#             return False
#         return True
#         return token == "legacy"  # unreachable

#     # --- Smell: mutable default arguments ---
#     def add_record(self, data, records=[]):
#         records.append(data)
#         return records

#     def build_report(self, sections=[], config={}):
#         sections.append("footer")
#         return {"sections": list(sections), "config": dict(config)}

#     def update_cache(self, key, value, cache={}):
#         cache[key] = value
#         return cache

#     def merge_meta(self, meta={}, tags=[]):
#         meta["tags"] = tags
#         return meta

#     # --- Duplicated: sales validation (copy 1) ---
#     def _validate_sales_records(self, records):
#         valid = []
#         for rec in records:
#             if not rec.get("sale_id"):
#                 continue
#             try:
#                 if float(rec.get("quantity", 0) or 0) < 0:
#                     continue
#                 if float(rec.get("price", 0) or 0) < 0:
#                     continue
#             except (TypeError, ValueError):
#                 continue
#             if not rec.get("region"):
#                 continue
#             valid.append(rec)
#         return valid

#     # --- Duplicated: inline stats block (copy 1 — sales amounts) ---
#     def _stats_block_sales(self, amounts):
#         if not amounts:
#             return {"mean": 0.0, "std": 0.0, "median": 0.0, "min": 0.0, "max": 0.0}
#         mean_v = sum(amounts) / len(amounts)
#         var = sum((x - mean_v) ** 2 for x in amounts) / len(amounts)
#         std_v = math.sqrt(var)
#         sorted_a = sorted(amounts)
#         mid = len(sorted_a) // 2
#         if len(sorted_a) % 2:
#             med = sorted_a[mid]
#         else:
#             med = (sorted_a[mid - 1] + sorted_a[mid]) / 2
#         return {
#             "mean": mean_v,
#             "std": std_v,
#             "median": med,
#             "min": min(amounts),
#             "max": max(amounts),
#         }

#     # --- Duplicated: CSV parse (copy 1) ---
#     def _parse_csv_sales(self, text):
#         out = []
#         reader = csv.DictReader(io.StringIO(text))
#         for row in reader:
#             out.append(dict(row))
#         return out

#     # --- Duplicated: inventory validation (copy 2) ---
#     def _validate_inventory_records(self, records):
#         valid = []
#         for rec in records:
#             if not rec.get("item_id"):
#                 continue
#             try:
#                 if float(rec.get("stock", 0) or 0) < 0:
#                     continue
#                 if float(rec.get("reorder_level", 0) or 0) < 0:
#                     continue
#             except (TypeError, ValueError):
#                 continue
#             if not rec.get("warehouse"):
#                 continue
#             valid.append(rec)
#         return valid

#     # --- Duplicated: inline stats (copy 2 — stock levels) ---
#     def _stats_block_inventory(self, values):
#         if not values:
#             return {"mean": 0.0, "std": 0.0, "median": 0.0, "min": 0.0, "max": 0.0}
#         mean_v = sum(values) / len(values)
#         var = sum((x - mean_v) ** 2 for x in values) / len(values)
#         std_v = math.sqrt(var)
#         sorted_a = sorted(values)
#         mid = len(sorted_a) // 2
#         if len(sorted_a) % 2:
#             med = sorted_a[mid]
#         else:
#             med = (sorted_a[mid - 1] + sorted_a[mid]) / 2
#         return {
#             "mean": mean_v,
#             "std": std_v,
#             "median": med,
#             "min": min(values),
#             "max": max(values),
#         }

#     # --- Duplicated: CSV parse (copy 2) ---
#     def _parse_csv_inventory(self, text):
#         out = []
#         reader = csv.DictReader(io.StringIO(text))
#         for row in reader:
#             out.append(dict(row))
#         return out

#     # --- Duplicated: customers validation (copy 3) ---
#     def _validate_customer_records(self, records):
#         valid = []
#         for rec in records:
#             if not rec.get("customer_id"):
#                 continue
#             if not rec.get("region"):
#                 continue
#             try:
#                 if float(rec.get("lifetime_value", 0) or 0) < 0:
#                     continue
#             except (TypeError, ValueError):
#                 continue
#             valid.append(rec)
#         return valid

#     # --- Duplicated: inline stats (copy 3) ---
#     def _stats_block_customers(self, values):
#         if not values:
#             return {"mean": 0.0, "std": 0.0, "median": 0.0, "min": 0.0, "max": 0.0}
#         mean_v = sum(values) / len(values)
#         var = sum((x - mean_v) ** 2 for x in values) / len(values)
#         std_v = math.sqrt(var)
#         sorted_a = sorted(values)
#         mid = len(sorted_a) // 2
#         if len(sorted_a) % 2:
#             med = sorted_a[mid]
#         else:
#             med = (sorted_a[mid - 1] + sorted_a[mid]) / 2
#         return {
#             "mean": mean_v,
#             "std": std_v,
#             "median": med,
#             "min": min(values),
#             "max": max(values),
#         }

#     # --- Duplicated: CSV parse (copy 3) ---
#     def _parse_csv_customers(self, text):
#         out = []
#         reader = csv.DictReader(io.StringIO(text))
#         for row in reader:
#             out.append(dict(row))
#         return out

#     # --- Duplicated: products validation (copy 4) ---
#     def _validate_product_records(self, records):
#         valid = []
#         for rec in records:
#             if not rec.get("product_id"):
#                 continue
#             try:
#                 if float(rec.get("unit_cost", 0) or 0) < 0:
#                     continue
#             except (TypeError, ValueError):
#                 continue
#             if not rec.get("category"):
#                 continue
#             valid.append(rec)
#         return valid

#     # --- Duplicated: inline stats (copy 4) ---
#     def _stats_block_products(self, values):
#         if not values:
#             return {"mean": 0.0, "std": 0.0, "median": 0.0, "min": 0.0, "max": 0.0}
#         mean_v = sum(values) / len(values)
#         var = sum((x - mean_v) ** 2 for x in values) / len(values)
#         std_v = math.sqrt(var)
#         sorted_a = sorted(values)
#         mid = len(sorted_a) // 2
#         if len(sorted_a) % 2:
#             med = sorted_a[mid]
#         else:
#             med = (sorted_a[mid - 1] + sorted_a[mid]) / 2
#         return {
#             "mean": mean_v,
#             "std": std_v,
#             "median": med,
#             "min": min(values),
#             "max": max(values),
#         }

#     # --- Duplicated: CSV parse (copy 4) ---
#     def _parse_csv_products(self, text):
#         out = []
#         reader = csv.DictReader(io.StringIO(text))
#         for row in reader:
#             out.append(dict(row))
#         return out

#     def _unreachable_demo(self):
#         x = 1
#         return x
#         y = 2  # dead: unreachable
#         return y  # dead: unreachable

#     def _generate_all_data(self):
#         regions = ["EU", "NA", "LATAM", "APAC"]
#         base = datetime(2023, 1, 1)
#         products = []
#         for i in range(PRODUCT_TARGET_COUNT):
#             products.append(
#                 {
#                     "product_id": f"P{i:04d}",
#                     "category": random.choice(["A", "B", "C"]),
#                     "unit_cost": round(random.uniform(5, 80), 2),
#                 }
#             )
#         self.products = products
#         customers = []
#         for i in range(CUSTOMER_TARGET_COUNT):
#             customers.append(
#                 {
#                     "customer_id": f"C{i:04d}",
#                     "region": random.choice(regions),
#                     "lifetime_value": round(random.uniform(100, 5000), 2),
#                 }
#             )
#         self.customers = customers
#         inventory = []
#         for i in range(INVENTORY_TARGET_COUNT):
#             inventory.append(
#                 {
#                     "item_id": f"I{i:04d}",
#                     "stock": random.randint(0, 500),
#                     "reorder_level": random.randint(10, 100),
#                     "warehouse": random.choice(["W1", "W2", "W3"]),
#                 }
#             )
#         self.inventory = inventory
#         sales = []
#         for i in range(SALES_TARGET_COUNT):
#             p = random.choice(products)
#             c = random.choice(customers)
#             qty = random.randint(1, 20)
#             price = round(random.uniform(10, 200), 2)
#             sales.append(
#                 {
#                     "sale_id": f"S{i:05d}",
#                     "customer_id": c["customer_id"],
#                     "product_id": p["product_id"],
#                     "quantity": qty,
#                     "price": price,
#                     "region": c["region"],
#                     "sale_date": (base + timedelta(days=random.randint(0, 400))).strftime(
#                         "%Y-%m-%d"
#                     ),
#                 }
#             )
#         self.sales = sales

#     def process_and_report(self):
#         """Long method: load paths, validate, transform, aggregate, stats, report, I/O.

#         This method intentionally chains: auth, CSV serialization round-trips,
#         per-entity validation using duplicated validators, repeated inline
#         statistics, multi-pass aggregation (2 passes), regional revenue rollups,
#         top-N extraction, cache/report side effects, and stdout summary.
#         """
#         unused_local_plan = "never_used"  # dead variable
#         _ghost = 123  # dead variable
#         _unused_tuple = (1, 2, 3)  # dead variable
#         self.log_event("start_pipeline")
#         if not self.authenticate("admin", "admin123"):
#             print("auth failed")
#             return
#         # Round-trip through CSV strings (duplicated parse paths exercised)
#         sales_csv = io.StringIO()
#         w = csv.DictWriter(
#             sales_csv,
#             fieldnames=[
#                 "sale_id",
#                 "customer_id",
#                 "product_id",
#                 "quantity",
#                 "price",
#                 "region",
#                 "sale_date",
#             ],
#         )
#         w.writeheader()
#         for row in self.sales:
#             w.writerow(row)
#         sales_from_csv = self._parse_csv_sales(sales_csv.getvalue())
#         inv_csv = io.StringIO()
#         wi = csv.DictWriter(
#             inv_csv, fieldnames=["item_id", "stock", "reorder_level", "warehouse"]
#         )
#         wi.writeheader()
#         for row in self.inventory:
#             wi.writerow(row)
#         inv_from_csv = self._parse_csv_inventory(inv_csv.getvalue())
#         cust_csv = io.StringIO()
#         wc = csv.DictWriter(
#             cust_csv, fieldnames=["customer_id", "region", "lifetime_value"]
#         )
#         wc.writeheader()
#         for row in self.customers:
#             wc.writerow(row)
#         cust_from_csv = self._parse_csv_customers(cust_csv.getvalue())
#         prod_csv = io.StringIO()
#         wp = csv.DictWriter(prod_csv, fieldnames=["product_id", "category", "unit_cost"])
#         wp.writeheader()
#         for row in self.products:
#             wp.writerow(row)
#         prod_from_csv = self._parse_csv_products(prod_csv.getvalue())
#         vs = self._validate_sales_records(sales_from_csv)
#         vi = self._validate_inventory_records(inv_from_csv)
#         vc = self._validate_customer_records(cust_from_csv)
#         vp = self._validate_product_records(prod_from_csv)
#         merged_chunks = 0
#         region_totals = {"EU": 0.0, "NA": 0.0, "LATAM": 0.0, "APAC": 0.0}
#         inventory_passes = 0
#         all_pass_summaries = []
#         for pass_idx in range(2):
#             # Pass loop: recompute revenue, regional splits, descriptive stats,
#             # and leaderboards so CPU work scales with pass count (spec: 2 passes).
#             merged_chunks += 1
#             inventory_passes += 1
#             amounts = []
#             for rec in vs:
#                 q = float(rec["quantity"])
#                 p = float(rec["price"])
#                 amounts.append(q * p)
#                 region_totals[rec["region"]] = region_totals.get(rec["region"], 0.0) + q * p
#             sales_stats = self._stats_block_sales(amounts)
#             stock_levels = [float(r["stock"]) for r in vi]
#             inv_stats = self._stats_block_inventory(stock_levels)
#             ltv = [float(r["lifetime_value"]) for r in vc]
#             cust_stats = self._stats_block_customers(ltv)
#             costs = [float(r["unit_cost"]) for r in vp]
#             prod_stats = self._stats_block_products(costs)
#             top_sales = sorted(
#                 [
#                     {
#                         "sale_id": r["sale_id"],
#                         "amt": float(r["quantity"]) * float(r["price"]),
#                     }
#                     for r in vs
#                 ],
#                 key=lambda x: x["amt"],
#                 reverse=True,
#             )[:5]
#             # Tie-break stability: re-sort by sale_id for deterministic ordering
#             top_sales = sorted(top_sales, key=lambda x: x["sale_id"])
#             top_sales = sorted(top_sales, key=lambda x: x["amt"], reverse=True)[:5]
#             all_pass_summaries.append(
#                 {
#                     "pass": pass_idx,
#                     "sales_stats": sales_stats,
#                     "inv_stats": inv_stats,
#                     "cust_stats": cust_stats,
#                     "prod_stats": prod_stats,
#                     "top_sales": top_sales,
#                 }
#             )
#         total_revenue = sum(region_totals.values())
#         report = {
#             "total_revenue": total_revenue,
#             "region_totals": region_totals,
#             "inventory_passes": inventory_passes,
#             "merged_chunks": merged_chunks,
#             "passes": all_pass_summaries,
#         }
#         self.cache_set("last_report", report)
#         self.pretend_file_write("report.json", report)
#         self.noop_metrics_sink("pipeline_complete", 1)
#         self.log_event("end_pipeline")
#         # Final consistency check across entity slices (inflates long method)
#         for _check_pass in range(2):
#             _ = sum(float(r["quantity"]) for r in vs)
#             _ = sum(float(r["stock"]) for r in vi)
#             _ = sum(float(r["lifetime_value"]) for r in vc)
#             _ = sum(float(r["unit_cost"]) for r in vp)
#         print(report)
#         print("Before refactor pipeline finished.")


# # ---------------------------------------------------------------------------
# # Application entry — minimal wiring so all behavior lives on SalesManager.
# # ---------------------------------------------------------------------------


# def main():
#     manager = SalesManager()
#     manager.process_and_report()


# if __name__ == "__main__":
#     main()

# # --- commented legacy blocks (dead code) ---
# # legacy_v1_export_disabled = True
# # def old_main():
# #     print("deprecated")
# #     return None
# # SALES_V0_SCHEMA = ["id", "amt"]
# # def migrate_sales_v0_to_v1(rows):
# #     return rows
# #
# # Historical note: earlier revisions inlined SQL and FTP export; both were
# # removed without deleting the scaffolding comments below.
# #
# # # conn = connect_warehouse()
# # # cursor = conn.cursor()
# # # cursor.execute("SELECT * FROM sales_fact")
# #
# # # ftp = ftplib.FTP("archive.internal")
# # # ftp.storlines("STOR dump.csv", open("dump.csv"))
