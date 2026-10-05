import re

FIELDS = {"document_id": r"Document-ID:\s*(.*)", "company": r"Company:\s*(.*)",
          "issue_date": r"Issue-Date:\s*(.*)", "amount": r"Amount:\s*(.*)"}

def extract(text: str) -> tuple[dict[str, str], list[str]]:
    values, errors = {}, []
    for field, pattern in FIELDS.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if len(matches) != 1:
            errors.append(f"{field}: expected exactly one occurrence")
        values[field] = matches[0].strip() if matches else ""
    return values, errors
