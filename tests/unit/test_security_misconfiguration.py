from passivesentry.modules.security_misconfiguration import SecurityHeadersAnalyzer


def test_validate_hsts_header_detects_weak_configuration():
    analyzer = SecurityHeadersAnalyzer()

    validation = analyzer._validate_security_header(
        "Strict-Transport-Security",
        "max-age=300",
    )

    assert validation["is_valid"] is False
    assert validation["score"] < 10
    assert any("includeSubDomains" in issue for issue in validation["issues"])


def test_analyze_etag_identifies_weak_etag_format():
    analyzer = SecurityHeadersAnalyzer()

    result = analyzer._analyze_etag('W/"abc-123"')

    assert result["is_weak"] is True
    assert result["format"] in ["weak_etag", "unknown"]


def test_banner_vulnerability_detection_finds_known_versions():
    analyzer = SecurityHeadersAnalyzer()

    vulnerabilities = analyzer._check_banner_vulnerabilities("Apache/2.4.49")

    assert vulnerabilities
    assert any("Apache" in vuln for vuln in vulnerabilities)
