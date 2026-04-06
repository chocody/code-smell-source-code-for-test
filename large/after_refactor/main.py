from __future__ import annotations

from typing import Any, Dict

from analyzers.risk_analyzer import RiskAnalyzer
from services import (
    AuditService,
    ForecastService,
    PipelineService,
    ReportService,
)
from utils.data_generator import build_large_dataset


class ERPManager:
    """Thin orchestrator: domain logic lives in services and utils."""

    def __init__(self) -> None:
        self._data = build_large_dataset()
        self._pipeline = PipelineService(self._data)
        self._forecast = ForecastService()
        self._audit = AuditService()
        self._report = ReportService()
        self._risk = RiskAnalyzer()

    def process_all_sales_data(self) -> None:
        self._pipeline.process_all_sales_data()

    def process_all_finance_data(self) -> None:
        self._pipeline.process_all_finance_data()

    def generate_executive_report(self) -> None:
        self._pipeline.generate_executive_report()

    def run_full_inventory_analysis(self) -> None:
        self._pipeline.run_full_inventory_analysis()

    def run_hr_payroll_analysis(self) -> None:
        self._pipeline.run_hr_payroll_analysis()

    def run_procurement_logistics_analysis(self) -> None:
        self._pipeline.run_procurement_logistics_analysis()

    def run_crm_analysis(self) -> None:
        self._pipeline.run_crm_analysis()

    def run_all_supplementary_analyses(self) -> Dict[str, Any]:
        cache = self._pipeline.full_cache()
        fin = cache.get("finance", [])
        self._forecast.preview_from_finance_cache(fin)
        self._audit.snapshot_cache(cache)
        sales = cache.get("sales", [])
        if sales:
            last_amts = []
            for rec in self._data["sales"][:500]:
                last_amts.append(float(rec["quantity"]) * float(rec["price"]))
            _ = self._risk.volatility_score(last_amts)
        total_rev = 0.0
        if sales:
            total_rev = sum(sales[-1]["region_totals"].values())
        summary = {
            "total_revenue_last_pass": total_rev,
            "finance_passes": len(fin),
        }
        _ = self._report.headline_revenue(total_rev)
        print(summary)
        print("After refactor pipeline finished.")
        return summary


def main() -> None:
    manager = ERPManager()
    manager.process_all_sales_data()
    manager.process_all_finance_data()
    manager.generate_executive_report()
    manager.run_full_inventory_analysis()
    manager.run_hr_payroll_analysis()
    manager.run_procurement_logistics_analysis()
    manager.run_crm_analysis()
    manager.run_all_supplementary_analyses()


if __name__ == "__main__":
    main()
