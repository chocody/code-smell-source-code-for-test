from __future__ import annotations

import csv
import io
from typing import Any, Dict, List, MutableMapping

from analyzers.stats_analyzer import StatsAnalyzer
from models.inventory import INVENTORY_SCHEMA
from models.sales import SALES_SCHEMA
from utils import enrich_date_fields, parse_csv_dict_rows, validate_batch


class PipelineService:
    """Sales and inventory pipelines (mirrors before_refactor passes)."""

    SALES_PASSES = 3
    INVENTORY_PASSES = 3

    def __init__(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        self._data = data
        self._logs: List[str] = []
        self._cache: Dict[str, Any] = {}
        self._sales_pass_outputs: List[Dict[str, Any]] = []
        self._inventory_analysis: List[Dict[str, Any]] = []
        self._analyzer = StatsAnalyzer()

    def process_all_sales_data(self) -> List[Dict[str, Any]]:
        self._logs.append("sales_start")
        rows = self._data["sales"]
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow(row)
        parsed: List[MutableMapping[str, Any]] = parse_csv_dict_rows(buf.getvalue())
        vs, _ = validate_batch(parsed, SALES_SCHEMA)
        for rec in vs:
            enrich_date_fields(rec, "sale_date")
        outputs: List[Dict[str, Any]] = []
        for pass_idx in range(self.SALES_PASSES):
            region_totals = {"EU": 0.0, "NA": 0.0, "LATAM": 0.0, "APAC": 0.0}
            amounts: List[float] = []
            for rec in vs:
                q = float(rec["quantity"])
                p = float(rec["price"])
                amounts.append(q * p)
                region_totals[rec["region"]] = region_totals.get(rec["region"], 0.0) + q * p
            st = self._analyzer.describe(amounts)
            top = sorted(
                [
                    {
                        "sale_id": r["sale_id"],
                        "amt": float(r["quantity"]) * float(r["price"]),
                    }
                    for r in vs
                ],
                key=lambda x: x["amt"],
                reverse=True,
            )[:15]
            outputs.append(
                {
                    "pass": pass_idx,
                    "stats": st,
                    "region_totals": region_totals,
                    "top": top,
                }
            )
        self._sales_pass_outputs = outputs
        self._cache["sales"] = outputs
        self._logs.append("sales_end")
        return outputs

    def run_full_inventory_analysis(self) -> List[Dict[str, Any]]:
        rows = self._data["inventory"]
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow(row)
        parsed = parse_csv_dict_rows(buf.getvalue())
        vi, _ = validate_batch(parsed, INVENTORY_SCHEMA)
        out: List[Dict[str, Any]] = []
        for pass_idx in range(self.INVENTORY_PASSES):
            low = [r for r in vi if float(r["stock"]) < 50]
            st = self._analyzer.describe([float(r["stock"]) for r in vi])
            out.append({"pass": pass_idx, "low_stock": len(low), "stats": st})
        self._inventory_analysis = out
        return out

    def sales_cache(self) -> Dict[str, Any]:
        return self._cache

    def inventory_analysis(self) -> List[Dict[str, Any]]:
        return self._inventory_analysis
