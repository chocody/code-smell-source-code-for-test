from typing import Dict, Iterable


def calculate_statistics(values: Iterable[float]) -> Dict[str, float]:
    items = list(values)
    if not items:
        return {"mean": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0}
    mean = sum(items) / len(items)
    variance = sum((item - mean) ** 2 for item in items) / len(items)
    return {
        "mean": mean,
        "std_dev": variance ** 0.5,
        "min": min(items),
        "max": max(items),
    }
