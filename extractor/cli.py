import argparse
import json
from pathlib import Path
from extractor.extraction import extract
from extractor.transformation import normalize
from extractor.validation import validate
from extractor.export import export

def process_directory(source: Path) -> tuple[list[dict], dict]:
    if not source.is_dir():
        raise ValueError("Input directory does not exist")
    records, seen = [], set()
    for path in sorted(source.glob("*.txt")):
        try:
            values, errors = extract(path.read_text(encoding="utf-8"))
            record = normalize(values)
            errors.extend(validate(record))
            if record["document_id"] in seen:
                errors.append("document_id: duplicate")
            seen.add(record["document_id"])
        except (OSError, UnicodeError) as error:
            record = dict(document_id="", company="", issue_date="", amount=None)
            errors = [f"read_error: {type(error).__name__}"]
        records.append(record | {"source": path.name, "valid": not errors, "errors": errors})
    report = {"total": len(records), "valid": sum(row["valid"] for row in records),
              "invalid": sum(not row["valid"] for row in records), "error_count": sum(len(row["errors"]) for row in records)}
    return records, report

def main():
    parser = argparse.ArgumentParser(description="Extract fictional text documents")
    parser.add_argument("--input", type=Path, default=Path("samples"))
    parser.add_argument("--output", type=Path, default=Path("output"))
    args = parser.parse_args()
    try:
        records, report = process_directory(args.input)
    except ValueError as error:
        parser.error(str(error))
    export(records, report, args.output)
    print(json.dumps(report))

if __name__ == "__main__":
    main()
