from dataclasses import dataclass
from typing import Dict


@dataclass
class InventoryModel:
    item_id: int
    product_id: int
    stock: int
    reorder_level: int
    warehouse: str

    @classmethod
    def from_record(cls, record: Dict[str, object]) -> "InventoryModel":
        return cls(
            item_id=int(record["item_id"]),
            product_id=int(record["product_id"]),
            stock=int(record["stock"]),
            reorder_level=int(record["reorder_level"]),
            warehouse=str(record["warehouse"]),
        )
