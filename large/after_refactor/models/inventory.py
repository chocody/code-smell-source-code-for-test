INVENTORY_SCHEMA = {
    "item_id": "required",
    "stock": "nonneg",
    "warehouse": "required",
}

SHIPMENT_SCHEMA = {
    "shipment_id": "required",
    "weight": "nonneg",
    "carrier": "required",
}
