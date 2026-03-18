from pathlib import Path

import pytest

from passivesentry.batch import BatchConfig, BatchProcessor, load_domains_from_file


def test_load_domains_from_file_filters_comments_and_blanks(tmp_path):
    domains_file = tmp_path / "domains.txt"
    domains_file.write_text("\n# comment\nexample.com\n\nhttps://foo.dev\n", encoding="utf-8")

    domains = load_domains_from_file(str(domains_file))

    assert domains == ["example.com", "https://foo.dev"]


def test_load_domains_from_file_raises_if_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_domains_from_file(str(tmp_path / "missing.txt"))


def test_process_domain_generates_full_results_file(tmp_path, monkeypatch):
    class FakeAuditor:
        def __init__(self, verbose, output_dir, max_workers):
            self.output_dir = output_dir

        def audit(self, domain, modules, parallel, generate_json, generate_pdf, company_name):
            return {
                "module_results": {"security_misconfiguration": {"risk_level": "LOW"}},
                "risk_analysis": {"risk_level": "LOW", "risk_score": 10},
                "report_paths": {"json": str(Path(self.output_dir) / "audit.json")},
            }

        def generate_pdf_report(self, domain, module_results, risk_analysis, company_name, executive_summary_only=False):
            name = "summary.pdf" if executive_summary_only else "report.pdf"
            path = Path(self.output_dir) / name
            path.write_text("pdf", encoding="utf-8")
            return str(path)

    monkeypatch.setattr("passivesentry.batch.PassiveSentryAuditor", FakeAuditor)

    processor = BatchProcessor(
        BatchConfig(
            output_base_dir=str(tmp_path / "out"),
            generate_json=True,
            generate_pdf=True,
            generate_executive_summary=True,
        )
    )

    result = processor.process_domain("example.com")

    assert result["success"] is True
    assert "full_results" in result["report_paths"]
    assert Path(result["report_paths"]["full_results"]).exists()


def test_process_domains_file_sequential_updates_stats(tmp_path, monkeypatch):
    domains_file = tmp_path / "domains.txt"
    domains_file.write_text("example.com\nfoo.com\n", encoding="utf-8")

    processor = BatchProcessor(BatchConfig(output_base_dir=str(tmp_path / "out"), max_workers=1))

    calls = []

    def fake_process_domain(domain):
        calls.append(domain)
        return {"domain": domain, "success": domain == "example.com", "report_paths": {}}

    monkeypatch.setattr(processor, "process_domain", fake_process_domain)

    results = processor.process_domains_file(str(domains_file), parallel=False)

    assert len(results) == 2
    assert calls == ["example.com", "foo.com"]
    assert processor.stats["total_domains"] == 2
    assert processor.stats["processed"] == 2
    assert processor.stats["succeeded"] == 1
    assert processor.stats["failed"] == 1
