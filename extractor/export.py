import json
from pathlib import Path
import pandas as pd

def safe_csv(value):
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value

def export(records: list[dict], report: dict, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "records.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    columns = ["document_id", "company", "issue_date", "amount", "source", "valid", "errors"]
    frame = pd.DataFrame(records, columns=columns)
    frame["errors"] = frame["errors"].map(lambda errors: "; ".join(errors))
    frame = frame.map(safe_csv)
    frame.to_csv(destination / "records.csv", index=False, encoding="utf-8")
    (destination / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
