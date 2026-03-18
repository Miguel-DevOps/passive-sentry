from passivesentry.modules.owasp_top10_2025 import (
    OwaspA01BrokenAccessControl,
    OwaspA02SecurityMisconfiguration,
    OwaspA03SoftwareSupplyChainFailures,
    OwaspA04CryptographicFailures,
    OwaspA05Injection,
    OwaspA06InsecureDesign,
    OwaspA07AuthenticationFailures,
    OwaspA08SoftwareOrDataIntegrityFailures,
    OwaspA09SecurityLoggingAndAlertingFailures,
    OwaspA10MishandlingOfExceptionalConditions,
)


class FakeDelegate:
    def __init__(self, payload):
        self.payload = payload

    def analyze(self, url):
        out = dict(self.payload)
        out["url"] = url
        return out


def test_a01_detects_exposed_indicators_from_public_artifacts():
    analyzer = OwaspA01BrokenAccessControl()
    analyzer._fetch_public_artifacts = lambda url: {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        },
        "html": "<html><body>Index of / backup</body></html>",
        "soup": None,
        "robots_txt": "Disallow: /admin",
        "sitemap_xml": "",
        "errors": [],
    }

    result = analyzer.analyze("https://example.com")

    assert result["risk_level"] in {"MEDIUM", "HIGH", "CRITICAL"}
    assert result["findings"]
    assert result["coverage_scope"] == "partial"


def test_a02_wrapper_includes_owasp_metadata_and_limits():
    analyzer = OwaspA02SecurityMisconfiguration()
    analyzer._delegate = FakeDelegate({"risk_level": "LOW", "miswithoutg_headers": []})

    result = analyzer.analyze("https://example.com")

    assert result["owasp"]["id"] == "A02:2025"
    assert result["analysis_mode"] == "passive_only"
    assert result["limitations"]


def test_a03_wrapper_includes_owasp_metadata_and_limits():
    analyzer = OwaspA03SoftwareSupplyChainFailures()
    analyzer._delegate = FakeDelegate({"risk_level": "LOW", "vulnerable_libs_found": []})

    result = analyzer.analyze("https://example.com")

    assert result["owasp"]["id"] == "A03:2025"
    assert result["limitations"]


def test_a04_wrapper_includes_owasp_metadata_and_limits():
    analyzer = OwaspA04CryptographicFailures()
    analyzer._delegate = FakeDelegate({"risk_level": "LOW", "certificate_valid": True})

    result = analyzer.analyze("https://example.com")

    assert result["owasp"]["id"] == "A04:2025"
    assert result["coverage_scope"] == "partial"


def test_a05_detects_injection_risk_signals_in_public_html():
    analyzer = OwaspA05Injection()
    analyzer._fetch_public_artifacts = lambda url: {
        "headers": {},
        "html": "<html><script>eval('x')</script><form method='get'><input name='sql'></form></html>",
        "soup": __import__("bs4").BeautifulSoup(
            "<html><script>eval('x')</script><form method='get'><input name='sql'></form></html>",
            "html.parser",
        ),
        "robots_txt": "",
        "sitemap_xml": "",
        "errors": [],
    }

    result = analyzer.analyze("https://example.com")

    assert result["findings"]
    assert result["risk_level"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    assert "No executes payloads" in " ".join(result["limitations"])


def test_a06_detects_design_risk_signals_from_public_flows():
    analyzer = OwaspA06InsecureDesign()
    analyzer._fetch_public_artifacts = lambda url: {
        "headers": {},
        "html": "<a href='/checkout'>Checkout</a>",
        "soup": __import__("bs4").BeautifulSoup("<a href='/checkout'>Checkout</a>", "html.parser"),
        "robots_txt": "",
        "sitemap_xml": "",
        "errors": [],
    }

    result = analyzer.analyze("https://example.com")

    assert result["public_buwithoutess_flow_indicators"]
    assert result["owasp"]["id"] == "A06:2025"


def test_a07_detects_login_form_signals_and_cookie_flags():
    analyzer = OwaspA07AuthenticationFailures()
    analyzer._fetch_public_artifacts = lambda url: {
        "headers": {"Set-Cookie": "sessionid=abc"},
        "html": "<form method='get'><input type='password' name='password'></form>",
        "soup": __import__("bs4").BeautifulSoup(
            "<form method='get'><input type='password' name='password'></form>",
            "html.parser",
        ),
        "robots_txt": "",
        "sitemap_xml": "",
        "errors": [],
    }

    result = analyzer.analyze("https://example.com")

    assert result["password_forms"] == 1
    assert result["get_login_forms"] == 1
    assert result["cookie_flags"]["secure"] is False


def test_a08_detects_external_scripts_without_sri():
    analyzer = OwaspA08SoftwareOrDataIntegrityFailures()
    analyzer._fetch_public_artifacts = lambda url: {
        "headers": {},
        "html": "<script src='https://cdn.example.org/lib.js'></script>",
        "soup": __import__("bs4").BeautifulSoup(
            "<script src='https://cdn.example.org/lib.js'></script>",
            "html.parser",
        ),
        "robots_txt": "",
        "sitemap_xml": "",
        "errors": [],
    }

    result = analyzer.analyze("https://example.com")

    assert result["scripts_without_sri"]
    assert result["owasp"]["id"] == "A08:2025"


def test_a09_wrapper_includes_owasp_metadata_and_limits():
    analyzer = OwaspA09SecurityLoggingAndAlertingFailures()
    analyzer._delegate = FakeDelegate({"risk_level": "LOW", "miswithoutg_spf": False, "miswithoutg_dmarc": False})

    result = analyzer.analyze("https://example.com")

    assert result["owasp"]["id"] == "A09:2025"
    assert result["coverage_scope"] == "very_limited"


def test_a10_detects_exception_handling_indicators():
    analyzer = OwaspA10MishandlingOfExceptionalConditions()
    analyzer._fetch_public_artifacts = lambda url: {
        "headers": {"X-Debug-Token": "debug"},
        "html": "Traceback (most recent call last)",
        "soup": __import__("bs4").BeautifulSoup("<a href='/error'>error</a>", "html.parser"),
        "robots_txt": "",
        "sitemap_xml": "",
        "errors": [],
    }

    result = analyzer.analyze("https://example.com")

    assert result["error_pattern_indicators"]
    assert result["debug_headers_exposed"]
    assert result["owasp"]["id"] == "A10:2025"
