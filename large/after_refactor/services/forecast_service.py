from __future__ import annotations

from typing import Any, Dict, List

from analyzers.trend_analyzer import TrendAnalyzer


class ForecastService:
    def __init__(self) -> None:
        self._trend = TrendAnalyzer()

    def preview_from_finance_cache(self, finance_passes: List[Dict[str, Any]]) -> str:
        if not finance_passes:
            return "flat"
        last = finance_passes[-1]
        stats = last.get("stats", {})
        mean_v = float(stats.get("mean", 0.0))
        return self._trend.net_direction([mean_v, mean_v * 1.0001])
