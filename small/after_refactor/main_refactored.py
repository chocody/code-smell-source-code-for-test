from pathlib import Path
from typing import Dict, List

from analyzers import StatsAnalyzer
from models import InventoryModel, SalesModel
from services import CSVService, ReportService
from utils import validate_required_fields


def _validate_sales(records: List[Dict[str, object]]) -> List[Dict[str, object]]:
    required = [
        "sale_id",
        "customer_id",
        "product_id",
        "quantity",
        "price",
        "region",
        "sale_date",
    ]
    valid, _ = validate_required_fields(records, required)
    return valid


def _to_sales_models(records: List[Dict[str, object]]) -> List[SalesModel]:
    return [SalesModel.from_record(rec) for rec in records]


def _to_inventory_models(records: List[Dict[str, object]]) -> List[InventoryModel]:
    return [InventoryModel.from_record(rec) for rec in records]


def _run_sales_pipeline(
    records: List[SalesModel], analyzer: StatsAnalyzer
) -> List[Dict[str, object]]:
    outputs: List[Dict[str, object]] = []
    for pass_idx in range(3):
        sorted_records = sorted(records, key=lambda item: item.sale_id)
        payload = [
            {"quantity": rec.quantity, "price": rec.price, "region": rec.region}
            for rec in sorted_records
        ]
        analysis = analyzer.analyze_sales(payload)
        total_revenue = sum(float(rec.quantity) * float(rec.price) for rec in sorted_records)
        top_entries = sorted(
            [
                {
                    "sale_id": rec.sale_id,
                    "amount": float(rec.quantity) * float(rec.price),
                    "region": rec.region,
                }
                for rec in sorted_records
            ],
            key=lambda row: row["amount"],
            reverse=True,
        )[:10]
        outputs.append(
            {
                "pass_idx": pass_idx,
                "total_revenue": total_revenue,
                "regional": analysis["by_region"],
                "stats": analysis["stats"],
                "top_entries": top_entries,
            }
        )
    return outputs


def _run_inventory_pipeline(records: List[InventoryModel]) -> List[Dict[str, object]]:
    outputs: List[Dict[str, object]] = []
    for pass_idx in range(3):
        low_stock = [item for item in records if item.stock < item.reorder_level]
        low_stock.sort(key=lambda item: item.stock)
        sample = [
            {
                "item_id": item.item_id,
                "stock": item.stock,
                "reorder_level": item.reorder_level,
                "warehouse": item.warehouse,
            }
            for item in low_stock[:10]
        ]
        outputs.append(
            {"pass_idx": pass_idx, "low_stock_count": len(low_stock), "sample": sample}
        )
    return outputs


def run() -> Dict[str, object]:
    csv_service = CSVService()
    report_service = ReportService()
    analyzer = StatsAnalyzer()

    data = csv_service.generate_data()
    valid_sales = _validate_sales(data["sales"])
    sales_models = _to_sales_models(valid_sales)
    inventory_models = _to_inventory_models(data["inventory"])

    sales_chunks = _run_sales_pipeline(sales_models, analyzer)
    inventory_chunks = _run_inventory_pipeline(inventory_models)
    summary = report_service.summarize(sales_chunks, inventory_chunks)

    output_path = Path(__file__).resolve().parent / "after_output_report.txt"
    report_service.write_report(output_path, summary)
    return summary


def main() -> None:
    summary = run()
    print("After refactor pipeline finished.")
    print(summary)


if __name__ == "__main__":
    main()