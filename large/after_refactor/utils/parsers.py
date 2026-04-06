from __future__ import annotations

import csv
import io
from typing import Any, Dict, List, MutableMapping


def parse_csv_dict_rows(text: str) -> List[MutableMapping[str, Any]]:
    return [dict(row) for row in csv.DictReader(io.StringIO(text))]
