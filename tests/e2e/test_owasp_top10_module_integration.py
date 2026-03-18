from passivesentry.core import PassiveSentryAuditor


class FakeAnalyzer:
    def __init__(self, payload):
        self.payload = payload

    def analyze(self, url):
        result = dict(self.payload)
        result["url"] = url
        return result


def test_each_owasp2025_module_runs_in_core_without_network(tmp_path):
    auditor = PassiveSentryAuditor(verbose=False, output_dir=str(tmp_path))

    fake_payloads = {
        "broken_access_control": {"risk_level": "LOW", "findings": []},
        "security_misconfiguration": {"risk_level": "LOW", "missing_headers": []},
        "software_supply_chain_failures": {
            "risk_level": "LOW",
            "vulnerable_libs_found": [],
            "forms_with_http_action": [],
        },
        "cryptographic_failures": {
            "risk_level": "LOW",
            "certificate_expired": False,
            "tls_version_insecure": False,
            "weak_ciphers_count": 0,
        },
        "injection": {"risk_level": "LOW", "findings": []},
        "insecure_design": {"risk_level": "LOW", "findings": []},
        "authentication_failures": {"risk_level": "LOW", "findings": []},
        "software_or_data_integrity_failures": {"risk_level": "LOW", "findings": []},
        "security_logging_and_alerting_failures": {
            "risk_level": "LOW",
            "missing_spf": False,
            "missing_dmarc": False,
        },
        "mishandling_exceptional_conditions": {"risk_level": "LOW", "findings": []},
    }

    for module_id, payload in fake_payloads.items():
        auditor.modules[module_id]["analyzer"] = FakeAnalyzer(payload)

    result = auditor.audit(
        "example.com",
        parallel=False,
        generate_json=True,
        generate_pdf=False,
    )

    assert result["url"].startswith("https://")
    assert len(result["module_results"]) == 10
    assert set(result["module_results"].keys()) == set(fake_payloads.keys())
    assert "json" in result["report_paths"]
