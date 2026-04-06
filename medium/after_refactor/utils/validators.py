from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Mapping, MutableMapping, Tuple


def validate_batch(
    records: List[MutableMapping[str, Any]],
    schema: Mapping[str, str],
) -> Tuple[List[MutableMapping[str, Any]], int]:
    valid: List[MutableMapping[str, Any]] = []
    rejected = 0
    for rec in records:
        ok = True
        for field, kind in schema.items():
            if kind == "required":
                val = rec.get(field)
                if val is None or val == "":
                    ok = False
                    break
            elif kind == "nonneg":
                try:
                    if float(rec.get(field, -1) or 0) < 0:
                        ok = False
                        break
                except (TypeError, ValueError):
                    ok = False
                    break
        if ok:
            valid.append(rec)
        else:
            rejected += 1
    return valid, rejected


def enrich_date_fields(record: MutableMapping[str, Any], date_field: str) -> None:
    raw = record.get(date_field)
    if not raw:
        return
    try:
        record[f"{date_field}_dt"] = datetime.strptime(str(raw), "%Y-%m-%d")
    except ValueError:
        record[f"{date_field}_dt"] = None
