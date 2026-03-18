from passivesentry.reporting.risk_scoring import RiskScorer


def test_risk_scorer_severity_counts_match_summary_text():
    scorer = RiskScorer()
    analysis = scorer.calculate_overall_risk(
        {
            "security_misconfiguration": {
                "risk_level": "HIGH",
                "missing_headers": ["Content-Security-Policy", "X-Frame-Options"],
                "vulnerability_hints": ["HIGH: Missing HSTS", "MEDIUM: Verbose server header"],
                "informative_headers_found": {},
            },
            "cryptographic_failures": {
                "risk_level": "HIGH",
                "certificate_expired": False,
                "certificate_valid": True,
                "tls_version_insecure": True,
                "tls_version_used": "TLSv1.0",
                "weak_ciphers_count": 1,
            },
        }
    )

    summary = analysis["executive_summary"]

    assert f"Critical: {len(analysis['critical_findings'])}" in summary
    assert f"High: {len(analysis['high_findings'])}" in summary
    assert f"Medium: {len(analysis['medium_findings'])}" in summary
    assert f"Low: {len(analysis['low_findings'])}" in summary


def test_risk_scorer_recommendations_are_english():
    scorer = RiskScorer()
    recommendations = scorer.generate_recommendations(
        {
            "risk_level": "HIGH",
            "critical_findings": ["[A04] TLS certificate is expired"],
            "high_findings": ["[A02] Missing security headers"],
            "medium_findings": [],
            "low_findings": [],
        }
    )

    assert recommendations
    assert all("correg" not in item.lower() for item in recommendations)
    assert all("auditor" not in item.lower() for item in recommendations)
