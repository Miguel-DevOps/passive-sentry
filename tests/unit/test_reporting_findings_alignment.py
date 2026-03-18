from datetime import datetime

from passivesentry.reporting.pdf_reporter import PDFReporter
from passivesentry.reporting.risk_scoring import RiskScorer


def test_pdf_report_uses_canonical_normalized_findings(tmp_path):
    scorer = RiskScorer()
    module_results = {
        "security_misconfiguration": {
            "risk_level": "LOW",
            "findings": ["Legacy finding in Spanish: servidor inseguro"],
            "missing_headers": [
                "Content-Security-Policy",
                "Strict-Transport-Security",
                "X-Frame-Options",
                "X-Content-Type-Options",
                "Referrer-Policy",
            ],
            "vulnerability_hints": ["ALTO: Tomcat 8 sin soporte"],
        }
    }
    analysis = scorer.calculate_overall_risk(module_results)

    reporter = PDFReporter(output_dir=str(tmp_path))
    context = reporter._build_context(
        domains=["example.com"],
        module_results_by_domain={"example.com": module_results},
        risk_analysis_by_domain={"example.com": analysis},
        company_name="Miguel Lozano | Developmi",
        analyst_name="Analyst",
        audit_date=datetime.now(),
    )

    a02_findings = context["owasp_findings"]["example.com"]["A02"]
    texts = [item["text"] for item in a02_findings]

    assert any("5 missing security headers" in text for text in texts)
    assert any("Tomcat 8" in text for text in texts)
    assert all("sin soporte" not in text.lower() for text in texts)

    header_finding = next(item for item in a02_findings if "5 missing security headers" in item["text"])
    assert "OWASP-recommended security headers" in header_finding["recommendation"]


def test_risk_scorer_normalizes_common_spanish_phrases_to_english():
    scorer = RiskScorer()
    analysis = scorer.calculate_overall_risk(
        {
            "security_logging": {
                "risk_level": "HIGH",
                "missing_dmarc": True,
                "missing_spf": True,
                "weak_spf": False,
                "weak_dmarc": False,
                "dns_errors": [],
                "mx_records": ["mx.example.com"],
                "ns_records": ["ns1.example.com"],
                "findings": ["missing registro DMARC"],
            }
        }
    )

    normalized_texts = [item["text"] for item in analysis.get("normalized_findings", [])]
    assert "Missing DMARC record" in normalized_texts
    assert all("missing registro" not in text.lower() for text in normalized_texts)
