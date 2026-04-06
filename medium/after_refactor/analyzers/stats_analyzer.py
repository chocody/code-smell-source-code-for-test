from __future__ import annotations

from typing import List

from utils.stats import describe


class StatsAnalyzer:
    """Thin wrapper over shared statistics utilities."""

    def describe(self, values: List[float]) -> dict:
        return describe(values)
