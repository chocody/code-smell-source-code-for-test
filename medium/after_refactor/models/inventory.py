"""Inventory validation schema."""

INVENTORY_SCHEMA = {
    "item_id": "required",
    "stock": "nonneg",
    "warehouse": "required",
}
