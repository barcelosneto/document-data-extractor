from datetime import date
from decimal import Decimal
import re

def validate(record: dict) -> list[str]:
    errors = []
    if not re.fullmatch(r"DEMO-\d{4}", record["document_id"]):
        errors.append("document_id: expected DEMO-0000 format")
    if not record["company"].startswith("FICTITIOUS"):
        errors.append("company: demonstration must use FICTITIOUS prefix")
    try:
        date.fromisoformat(record["issue_date"])
    except ValueError:
        errors.append("issue_date: invalid ISO date")
    amount = record["amount"]
    if amount is None or not Decimal(amount).is_finite() or Decimal(amount) <= 0:
        errors.append("amount: expected positive finite number")
    elif Decimal(amount).as_tuple().exponent < -2:
        errors.append("amount: maximum two decimal places")
    return errors
