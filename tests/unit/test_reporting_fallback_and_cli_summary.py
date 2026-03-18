from pathlib import Path
import importlib

from click.testing import CliRunner

from passivesentry.reporting.pdf_reporter import PDFReporter


class _FakeAuditor:
    def __init__(self, verbose, output_dir):
        self.verbose = verbose
        self.output_dir = output_dir

    def audit(self, url, modules, parallel, generate_json, generate_pdf):
        return {
            "module_results": {
                "security_misconfiguration": {"risk_level": "HIGH", "missing_headers": ["CSP"]}
            },
            "risk_analysis": {
                "risk_level": "HIGH",
                "risk_score": 42,
                "executive_summary": "Critical: 0 | High: 1 | Medium: 0 | Low: 0 | Overall risk level: HIGH",
                "critical_findings": [],
                "high_findings": ["[A02] 5 missing security headers"],
                "medium_findings": [],
                "low_findings": [],
            },
            "report_paths": {"json": str(Path(self.output_dir) / "audit.json")},
        }


def test_audit_summary_file_includes_executive_and_key_findings(monkeypatch, tmp_path):
    cli_module = importlib.import_module("passivesentry.cli")
    monkeypatch.setattr(cli_module, "PassiveSentryAuditor", _FakeAuditor)

    summary_path = tmp_path / "summary.txt"
    runner = CliRunner()
    result = runner.invoke(
        cli_module.cli,
        [
            "audit",
            "example.com",
            "--output-summary",
            str(summary_path),
        ],
    )

    assert result.exit_code == 0
    assert summary_path.exists()

    content = summary_path.read_text(encoding="utf-8")
    assert "EXECUTIVE SUMMARY:" in content
    assert "Critical: 0 | High: 1" in content
    assert "KEY FINDINGS:" in content
    assert "[A02] 5 missing security headers" in content


def test_pdf_extract_module_findings_covers_common_fallback_fields(tmp_path):
    reporter = PDFReporter(output_dir=str(tmp_path))

    entries = reporter._extract_module_findings(
        {
            "risk_level": "LOW",
            "missing_headers": [
                "Content-Security-Policy",
                "Strict-Transport-Security",
                "X-Frame-Options",
                "X-Content-Type-Options",
                "Referrer-Policy",
            ],
            "missing_spf": True,
            "missing_dmarc": True,
            "forms_with_http_action": [{"action": "http://example.com/login"}],
        }
    )

    texts = [entry["text"] for entry in entries]
    assert "5 missing security headers" in texts
    assert "Missing SPF record" in texts
    assert "Missing DMARC record" in texts
    assert any("Form action uses HTTP transport" in text for text in texts)
