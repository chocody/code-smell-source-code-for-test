from __future__ import annotations


def format_currency_line(label: str, amount: float) -> str:
    return f"{label}={amount:.2f}"
