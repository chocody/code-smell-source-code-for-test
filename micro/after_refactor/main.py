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
