import json
from pathlib import Path
from src.reporting.report import RunReport, SourceResult

def test_report_lifecycle():
    report = RunReport(run_id="test-run")
    assert report.start_time > 0
    assert report.end_time is None
    
    result = SourceResult(id="s1", status="success", duration=1.5)
    report.record_result(result)
    
    assert report.summary["success"] == 1
    assert report.results["s1"] == result
    
    report.finalize()
    assert report.end_time >= report.start_time

def test_atomic_write(tmp_path):
    report_file = tmp_path / "report.json"
    report = RunReport(run_id="test-run")
    report.record_result(SourceResult(id="s1", status="success", duration=1.0))
    report.finalize()
    
    report.to_json(str(report_file))
    
    assert report_file.exists()
    content = json.loads(report_file.read_text())
    assert content["run_id"] == "test-run"
    assert content["summary"]["success"] == 1
