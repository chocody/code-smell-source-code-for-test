"""Sales-related validation schema (shared contract for pipelines)."""

SALES_SCHEMA = {
    "sale_id": "required",
    "quantity": "nonneg",
    "price": "nonneg",
    "region": "required",
}
