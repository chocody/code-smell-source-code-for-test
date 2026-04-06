from typing import Dict, List, Tuple


def validate_required_fields(records: List[Dict[str, object]], required: List[str]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    valid: List[Dict[str, object]] = []
    invalid: List[Dict[str, object]] = []
    for record in records:
        is_valid = True
        for field in required:
            value = record.get(field)
            if value is None:
                is_valid = False
            elif isinstance(value, str) and not value.strip():
                is_valid = False
        if is_valid:
            valid.append(record)
        else:
            invalid.append(record)
    return valid, invalid
