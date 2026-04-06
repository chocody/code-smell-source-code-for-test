from dataclasses import dataclass
from typing import Dict


@dataclass
class SalesModel:
    sale_id: int
    customer_id: int
    product_id: int
    quantity: int
    price: float
    region: str
    sale_date: str

    @classmethod
    def from_record(cls, record: Dict[str, object]) -> "SalesModel":
        return cls(
            sale_id=int(record["sale_id"]),
            customer_id=int(record["customer_id"]),
            product_id=int(record["product_id"]),
            quantity=int(record["quantity"]),
            price=float(record["price"]),
            region=str(record["region"]),
            sale_date=str(record["sale_date"]),
        )
