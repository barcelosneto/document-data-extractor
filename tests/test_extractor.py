from pathlib import Path
import json
import pandas as pd
from extractor.extraction import extract
from extractor.transformation import normalize
from extractor.validation import validate
from extractor.cli import process_directory
from extractor.export import export, safe_csv

def test_normalization_and_validation():
    values, errors = extract("Document-ID: demo-0001\nCompany: FICTITIOUS  Workshop\nIssue-Date: 2025-01-01\nAmount: 1.250,50")
    record = normalize(values)
    assert record["amount"] == "1250.50"
    assert record["company"] == "FICTITIOUS Workshop"
    assert not errors and not validate(record)

def test_missing_and_duplicate_fields():
    _, errors = extract("Document-ID: DEMO-0001\nDocument-ID: DEMO-0002")
    assert len(errors) == 4

def test_invalid_amounts():
    for value in ["NaN", "Infinity", "-1", "0", "1.234", "abc"]:
        record = normalize(dict(document_id="DEMO-0001", company="FICTITIOUS A", issue_date="2025-01-01", amount=value))
        assert validate(record)

def test_complete_pipeline(tmp_path):
    records, report = process_directory(Path("samples"))
    assert report["total"] == 3 and report["valid"] == 1
    assert "document_id: duplicate" in records[2]["errors"]
    export(records, report, tmp_path)
    assert len(json.loads((tmp_path / "records.json").read_text())) == 3
    assert len(pd.read_csv(tmp_path / "records.csv")) == 3
    assert json.loads((tmp_path / "report.json").read_text())["invalid"] == 2

def test_empty_directory(tmp_path):
    records, report = process_directory(tmp_path)
    export(records, report, tmp_path / "out")
    assert report["total"] == 0
    assert len(pd.read_csv(tmp_path / "out/records.csv")) == 0

def test_csv_formula_protection():
    assert safe_csv(" =1+1").startswith("'")
