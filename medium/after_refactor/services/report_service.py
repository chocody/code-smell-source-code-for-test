from __future__ import annotations

import csv
import io
from typing import Any, Callable, Dict, List, MutableMapping, Tuple

from utils import parse_csv_dict_rows, validate_batch
from utils.stats import describe


class ReportService:
    """Cross-entity reporting using shared validate/parse/stats."""

    def __init__(self) -> None:
        self._chunks: List[Dict[str, Any]] = []

    def build_entity_chunks(
        self,
        data: Dict[str, List[Dict[str, Any]]],
        entities: List[Tuple[str, Dict[str, str], Callable[[Dict[str, Any]], float]]],
    ) -> List[Dict[str, Any]]:
        chunks: List[Dict[str, Any]] = []
        for ent, schema, metric_fn in entities:
            rows = data.get(ent, [])
            if not rows:
                continue
            buf = io.StringIO()
            w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for row in rows:
                w.writerow(row)
            parsed: List[MutableMapping[str, Any]] = parse_csv_dict_rows(buf.getvalue())
            valid, _ = validate_batch(parsed, schema)
            vals = [metric_fn(dict(r)) for r in valid]
            st = describe(vals)
            chunks.append({"entity": ent, "count": len(valid), "stats": st})
        self._chunks = chunks
        return chunks
