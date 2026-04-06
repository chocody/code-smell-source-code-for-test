from __future__ import annotations

from typing import List


class TrendAnalyzer:
    def net_direction(self, series: List[float]) -> str:
        if len(series) < 2:
            return "flat"
        head = sum(series[: len(series) // 2])
        tail = sum(series[len(series) // 2 :])
        if tail > head:
            return "up"
        if tail < head:
            return "down"
        return "flat"
