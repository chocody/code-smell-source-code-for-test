from __future__ import annotations

import math
from typing import Any, Dict, List, Mapping, MutableMapping


def describe(values: List[float]) -> Dict[str, float]:
    """Mean, population std dev, median, min, max — single implementation used everywhere."""
    if not values:
        return {"mean": 0.0, "std": 0.0, "median": 0.0, "min": 0.0, "max": 0.0}
    mean_v = sum(values) / len(values)
    var = sum((x - mean_v) ** 2 for x in values) / len(values)
    std_v = math.sqrt(var)
    sorted_a = sorted(values)
    mid = len(sorted_a) // 2
    if len(sorted_a) % 2:
        med = sorted_a[mid]
    else:
        med = (sorted_a[mid - 1] + sorted_a[mid]) / 2
    return {
        "mean": mean_v,
        "std": std_v,
        "median": med,
        "min": min(values),
        "max": max(values),
    }


def group_values_by_field(
    records: List[Mapping[str, Any]],
    group_field: str,
    value_field: str,
) -> Dict[str, float]:
    """Sum numeric value_field grouped by group_field (missing groups skipped)."""
    buckets: Dict[str, float] = {}
    for rec in records:
        g = rec.get(group_field)
        if g is None:
            continue
        try:
            v = float(rec[value_field])
        except (KeyError, TypeError, ValueError):
            continue
        key = str(g)
        buckets[key] = buckets.get(key, 0.0) + v
    return buckets
