from __future__ import annotations

import csv
import io
from typing import Any, Dict, List, MutableMapping

from analyzers.stats_analyzer import StatsAnalyzer
from models import (
    CRM_SCHEMA,
    CUSTOMER_SCHEMA,
    EMPLOYEE_SCHEMA,
    FINANCE_SCHEMA,
    INVENTORY_SCHEMA,
    PROCUREMENT_SCHEMA,
    PRODUCT_SCHEMA,
    SALES_SCHEMA,
    SHIPMENT_SCHEMA,
    SUPPLIER_SCHEMA,
)
from utils import enrich_date_fields, parse_csv_dict_rows, top_groups_from_records, validate_batch


class PipelineService:
    """ERP-style pipelines; each workflow decomposed into small steps (vs. monolith)."""

    PASSES = 5

    def __init__(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        self._data = data
        self._cache: Dict[str, Any] = {}
        self._exec_report: List[Dict[str, Any]] = []
        self._analyzer = StatsAnalyzer()

    def full_cache(self) -> Dict[str, Any]:
        return self._cache

    def _csv_roundtrip(self, rows: List[Dict[str, Any]]) -> List[MutableMapping[str, Any]]:
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow(row)
        return parse_csv_dict_rows(buf.getvalue())

    def process_all_sales_data(self) -> None:
        rows = self._data["sales"]
        parsed = self._csv_roundtrip(rows)
        vs, _ = validate_batch(parsed, SALES_SCHEMA)
        for rec in vs:
            enrich_date_fields(rec, "sale_date")
        out: List[Dict[str, Any]] = []
        for pass_idx in range(self.PASSES):
            region_totals = {"EU": 0.0, "NA": 0.0, "LATAM": 0.0, "APAC": 0.0}
            amounts: List[float] = []
            for rec in vs:
                q = float(rec["quantity"])
                p = float(rec["price"])
                amounts.append(q * p)
                region_totals[rec["region"]] = region_totals.get(rec["region"], 0.0) + q * p
            st = self._analyzer.summarize(amounts)
            top_regions_qty = top_groups_from_records(vs, "region", "quantity", 4)
            out.append(
                {
                    "pass": pass_idx,
                    "stats": st,
                    "region_totals": region_totals,
                    "top_regions_qty": top_regions_qty,
                }
            )
        self._cache["sales"] = out

    def process_all_finance_data(self) -> None:
        rows = self._data["finance"]
        parsed = self._csv_roundtrip(rows)
        vf, _ = validate_batch(parsed, FINANCE_SCHEMA)
        out: List[Dict[str, Any]] = []
        for pass_idx in range(self.PASSES):
            vals = [float(r["amount"]) for r in vf]
            st = self._analyzer.summarize(vals)
            by_type = top_groups_from_records(vf, "type", "amount", 5)
            out.append({"pass": pass_idx, "stats": st, "by_type": by_type})
        self._cache["finance"] = out

    def generate_executive_report(self) -> None:
        sections: List[Dict[str, Any]] = []
        plan = [
            ("customers", CUSTOMER_SCHEMA, "lifetime_value"),
            ("products", PRODUCT_SCHEMA, "unit_cost"),
            ("suppliers", SUPPLIER_SCHEMA, "rating"),
            ("employees", EMPLOYEE_SCHEMA, "salary"),
        ]
        for ent, schema, metric_key in plan:
            rows = self._data[ent]
            parsed = self._csv_roundtrip(rows)
            valid, _ = validate_batch(parsed, schema)
            vals = [float(r[metric_key]) for r in valid]
            st = self._analyzer.summarize(vals)
            sections.append({"entity": ent, "stats": st, "n": len(valid)})
        self._exec_report = sections

    def run_full_inventory_analysis(self) -> None:
        rows = self._data["inventory"]
        parsed = self._csv_roundtrip(rows)
        vi, _ = validate_batch(parsed, INVENTORY_SCHEMA)
        out: List[Dict[str, Any]] = []
        for pass_idx in range(self.PASSES):
            wh = top_groups_from_records(vi, "warehouse", "stock", 5)
            st = self._analyzer.summarize([float(r["stock"]) for r in vi])
            out.append({"pass": pass_idx, "stats": st, "top_wh": wh})
        self._cache["inventory"] = out

    def run_hr_payroll_analysis(self) -> None:
        rows = self._data["employees"]
        parsed = self._csv_roundtrip(rows)
        ve, _ = validate_batch(parsed, EMPLOYEE_SCHEMA)
        out: List[Dict[str, Any]] = []
        for pass_idx in range(self.PASSES):
            by_dept = top_groups_from_records(ve, "department", "salary", 4)
            st = self._analyzer.summarize([float(r["salary"]) for r in ve])
            out.append({"pass": pass_idx, "stats": st, "by_dept": by_dept})
        self._cache["hr"] = out

    def run_procurement_logistics_analysis(self) -> None:
        out: List[Dict[str, Any]] = []
        for pass_idx in range(self.PASSES):
            pr = self._data["procurement"]
            sh = self._data["shipments"]
            vp, _ = validate_batch(self._csv_roundtrip(pr), PROCUREMENT_SCHEMA)
            vsh, _ = validate_batch(self._csv_roundtrip(sh), SHIPMENT_SCHEMA)
            stp = self._analyzer.summarize([float(r["value"]) for r in vp])
            sts = self._analyzer.summarize([float(r["weight"]) for r in vsh])
            top_carriers = top_groups_from_records(vsh, "carrier", "weight", 4)
            out.append(
                {
                    "pass": pass_idx,
                    "procurement": stp,
                    "shipments": sts,
                    "top_carriers": top_carriers,
                }
            )
        self._cache["proclog"] = out

    def run_crm_analysis(self) -> None:
        rows = self._data["crm"]
        parsed = self._csv_roundtrip(rows)
        vc, _ = validate_batch(parsed, CRM_SCHEMA)
        out: List[Dict[str, Any]] = []
        for pass_idx in range(self.PASSES):
            ch = top_groups_from_records(vc, "channel", "score", 3)
            st = self._analyzer.summarize([float(r["score"]) for r in vc])
            out.append({"pass": pass_idx, "stats": st, "channels": ch})
        self._cache["crm"] = out
