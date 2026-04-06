from __future__ import annotations

from typing import List

from utils.stats import describe


class StatsAnalyzer:
    def summarize(self, values: List[float]) -> dict:
        return describe(values)
