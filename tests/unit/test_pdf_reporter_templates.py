from pathlib import Path

from passivesentry.reporting.pdf_reporter import PDFReporter


def test_pdf_reporter_renders_executive_template(tmp_path):
    reporter = PDFReporter(output_dir=str(tmp_path))

    html = reporter.render_html(
        "executive_summary.html",
        {
            "domains": ["example.com"],
            "owasp_findings": {"example.com": {f"A{i:02d}": [] for i in range(1, 11)}},
            "risk_scores": {"example.com": 12},
            "executive_summary": "One medium-severity finding was detected.",
            "recommendations": ["Add missing security headers."],
            "audit_date": "2026-03-17 10:00:00",
            "company_name": "Miguel Lozano | Developmi",
            "analyst_name": "Security Analyst",
            "severity_table": {"critical": 0, "high": 0, "medium": 1, "low": 0},
            "key_findings": [{"severity": "MEDIUM", "text": "Missing CSP header", "recommendation": "Add CSP"}],
        },
    )

    assert "PassiveSentry Executive Summary" in html
    assert "example.com" in html
    assert "Missing CSP header" in html


def test_pdf_reporter_generates_pdf_with_weasyprint(monkeypatch, tmp_path):
    reporter = PDFReporter(output_dir=str(tmp_path))

    captured = {"path": None}

    def fake_write_pdf(self, target, *args, **kwargs):
        captured["path"] = target
        Path(target).write_bytes(b"%PDF-1.4\n%fake")

    monkeypatch.setattr("passivesentry.reporting.pdf_reporter.HTML.write_pdf", fake_write_pdf)

    path = reporter.generate_executive_summary_pdf(
        url="https://example.com",
        risk_analysis={
            "risk_level": "HIGH",
            "risk_score": 42,
            "critical_findings": [],
            "high_findings": ["[A02] Missing security headers"],
            "medium_findings": [],
            "low_findings": [],
            "recommendations": ["Deploy strict security headers"],
        },
        company_name="Miguel Lozano | Developmi",
        analyst_name="Auditor",
    )

    assert captured["path"] is not None
    assert Path(path).exists()
    assert Path(path).suffix.lower() == ".pdf"
