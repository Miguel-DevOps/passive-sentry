import json
from pathlib import Path

from scripts.streamlit_dashboard import load_results


def test_load_results_parses_scan_and_batch_json(tmp_path):
    results_dir = tmp_path / "results_massive"
    results_dir.mkdir(parents=True)

    scan_payload = {
        "metadata": {"url": "https://example.com", "scan_date": "2026-03-17T10:00:00"},
        "summary": {
            "risk_level": "HIGH",
            "risk_score": 35,
            "overall_status": "COMPLETED",
            "modules_with_errors": [],
            "modules_executed": ["security_misconfiguration"],
            "findings_count": {"critical": 0, "high": 2, "medium": 1, "low": 0, "info": 0},
        },
        "detailed_results": {},
    }
    (results_dir / "scan.json").write_text(json.dumps(scan_payload), encoding="utf-8")

    batch_payload = {
        "execution_summary": {
            "start_time": "2026-03-17T10:00:00",
            "end_time": "2026-03-17T10:05:00",
            "total_time_seconds": 300,
            "total_domains": 1,
            "succeeded": 1,
            "failed": 0,
            "success_rate": 100.0,
        },
        "results_by_domain": [{"domain": "example.com", "success": True}],
    }
    (results_dir / "batch.json").write_text(json.dumps(batch_payload), encoding="utf-8")

    scans_df, batch_df, parse_errors = load_results(str(results_dir))

    assert parse_errors == []
    assert len(scans_df) == 1
    assert len(batch_df) == 1
    assert scans_df.iloc[0]["domain"] == "example.com"
    assert batch_df.iloc[0]["total_domains"] == 1


def test_load_results_returns_error_for_missing_directory(tmp_path):
    scans_df, batch_df, parse_errors = load_results(str(tmp_path / "missing"))

    assert scans_df.empty
    assert batch_df.empty
    assert parse_errors
    assert "Path does not exist" in parse_errors[0]["error"]
