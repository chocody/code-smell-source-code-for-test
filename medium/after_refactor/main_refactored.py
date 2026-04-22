from __future__ import annotations

from typing import Any, Dict, List

from services.pipeline_service import PipelineService
from services.report_service import ReportService
from utils.data_generator import build_medium_dataset


class DataManager:
    """Thin facade: delegates to focused services (not a god class)."""

    def __init__(self) -> None:
        self._data = build_medium_dataset()
        self._pipeline = PipelineService(self._data)
        self._reports = ReportService()
        self._report_chunks: List[Dict[str, Any]] = []

    def process_all_sales_data(self) -> None:
        self._pipeline.process_all_sales_data()

    def generate_complete_report(self) -> None:
        entities = [
            (
                "customers",
                {
                    "customer_id": "required",
                    "region": "required",
                    "lifetime_value": "nonneg",
                },
                lambda r: float(r["lifetime_value"]),
            ),
            (
                "products",
                {
                    "product_id": "required",
                    "unit_cost": "nonneg",
                    "category": "required",
                },
                lambda r: float(r["unit_cost"]),
            ),
            (
                "suppliers",
                {
                    "supplier_id": "required",
                    "rating": "nonneg",
                    "region": "required",
                },
                lambda r: float(r["rating"]),
            ),
            (
                "returns",
                {
                    "return_id": "required",
                    "amount": "nonneg",
                    "reason": "required",
                },
                lambda r: float(r["amount"]),
            ),
            (
                "orders",
                {
                    "order_id": "required",
                    "total": "nonneg",
                    "status": "required",
                },
                lambda r: float(r["total"]),
            ),
            (
                "shipments",
                {
                    "shipment_id": "required",
                    "weight": "nonneg",
                    "carrier": "required",
                },
                lambda r: float(r["weight"]),
            ),
        ]
        self._report_chunks = self._reports.build_entity_chunks(self._data, entities)

    def run_full_inventory_analysis(self) -> None:
        self._pipeline.run_full_inventory_analysis()

    def run_all_analyses(self) -> Dict[str, Any]:
        sales = self._pipeline.sales_cache().get("sales", [])
        inv = self._pipeline.inventory_analysis()
        total_rev = 0.0
        if sales:
            rt = sales[-1].get("region_totals", {})
            total_rev = sum(rt.values())
        summary = {
            "total_revenue_last_pass": total_rev,
            "inventory_passes": len(inv),
            "report_entities": len(self._report_chunks),
        }
        print(summary)
        print("After refactor pipeline finished.")
        return summary


def main() -> None:
    manager = DataManager()
    manager.process_all_sales_data()
    manager.generate_complete_report()
    manager.run_full_inventory_analysis()
    manager.run_all_analyses()


if __name__ == "__main__":
    main()