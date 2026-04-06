from __future__ import annotations

from typing import List

from utils.stats import describe


class RiskAnalyzer:
    """Uses dispersion of amounts as a simple risk proxy."""

    def volatility_score(self, amounts: List[float]) -> float:
        st = describe(amounts)
        return float(st["std"])
