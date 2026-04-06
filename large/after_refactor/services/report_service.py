from __future__ import annotations

from typing import Any, Dict, List

from utils.formatters import format_currency_line


class ReportService:
    def headline_revenue(self, total: float) -> str:
        return format_currency_line("total_revenue_last_pass", total)
