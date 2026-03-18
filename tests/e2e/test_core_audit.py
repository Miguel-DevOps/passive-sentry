from pathlib import Path

from passivesentry.core import PassiveSentryAuditor


class FakeAnalyzer:
    def __init__(self, payload):
        self.payload = payload

    def analyze(self, url):
        return dict(self.payload)


def test_core_audit_runs_enabled_modules_without_network(tmp_path):
    auditor = PassiveSentryAuditor(verbose=False, output_dir=str(tmp_path))

    auditor.modules["broken_access_control"]["analyzer"] = FakeAnalyzer(
        {"risk_level": "LOW", "findings": []}
    )
    auditor.modules["security_misconfiguration"]["analyzer"] = FakeAnalyzer(
        {"risk_level": "LOW", "missing_headers": [], "vulnerability_hints": []}
    )
    auditor.modules["software_supply_chain_failures"]["analyzer"] = FakeAnalyzer(
        {"risk_level": "LOW", "vulnerable_libs_found": [], "forms_with_http_action": []}
    )
    auditor.modules["cryptographic_failures"]["analyzer"] = FakeAnalyzer(
        {
            "risk_level": "LOW",
            "certificate_expired": False,
            "tls_version_insecure": False,
            "weak_ciphers_count": 0,
        }
    )
    auditor.modules["injection"]["analyzer"] = FakeAnalyzer(
        {"risk_level": "LOW", "findings": []}
    )
    auditor.modules["insecure_design"]["analyzer"] = FakeAnalyzer(
        {"risk_level": "LOW", "findings": []}
    )
    auditor.modules["authentication_failures"]["analyzer"] = FakeAnalyzer(
        {"risk_level": "LOW", "findings": []}
    )
    auditor.modules["software_or_data_integrity_failures"]["analyzer"] = FakeAnalyzer(
        {"risk_level": "LOW", "findings": []}
    )
    auditor.modules["security_logging_and_alerting_failures"]["analyzer"] = FakeAnalyzer(
        {"risk_level": "LOW", "missing_spf": False, "missing_dmarc": False}
    )
    auditor.modules["mishandling_exceptional_conditions"]["analyzer"] = FakeAnalyzer(
        {"risk_level": "LOW", "findings": []}
    )

    result = auditor.audit("example.com", parallel=False, generate_json=True, generate_pdf=False)

    assert result["url"].startswith("https://")
    assert "module_results" in result
    assert len(result["module_results"]) == 10
    assert "json" in result["report_paths"]
    assert Path(result["report_paths"]["json"]).exists()
