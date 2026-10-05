from decimal import Decimal, InvalidOperation

def normalize(values: dict[str, str]) -> dict:
    result = {key: value.strip() for key, value in values.items()}
    result["document_id"] = result["document_id"].upper()
    result["company"] = " ".join(result["company"].split())
    raw_amount = result["amount"]
    if "," in raw_amount:
        raw_amount = raw_amount.replace(".", "").replace(",", ".")
    try:
        result["amount"] = str(Decimal(raw_amount))
    except InvalidOperation:
        result["amount"] = None
    return result
