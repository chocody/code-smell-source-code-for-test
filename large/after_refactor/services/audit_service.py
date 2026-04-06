from __future__ import annotations

from typing import Any, Dict


class AuditService:
    def snapshot_cache(self, cache: Dict[str, Any]) -> Dict[str, int]:
        return {key: len(value) if hasattr(value, "__len__") else 1 for key, value in cache.items()}
