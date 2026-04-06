SALES_SCHEMA = {
    "sale_id": "required",
    "quantity": "nonneg",
    "price": "nonneg",
    "region": "required",
}

PRODUCT_SCHEMA = {
    "product_id": "required",
    "unit_cost": "nonneg",
    "category": "required",
}

CRM_SCHEMA = {
    "interaction_id": "required",
    "score": "nonneg",
    "channel": "required",
}
