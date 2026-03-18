from pathlib import Path
import importlib

from click.testing import CliRunner


def test_batch_command_uses_domains_file_and_returns_success(monkeypatch, tmp_path):
    cli_module = importlib.import_module("passivesentry.cli")

    input_file = tmp_path / "domains.txt"
    input_file.write_text("example.com\n", encoding="utf-8")

    captured = {}

    class FakeBatchProcessor:
        def __init__(self, config):
            captured["config"] = config

        def process_domains_file(self, domains_file_path, parallel=True):
            captured["domains_file_path"] = domains_file_path
            captured["parallel"] = parallel
            return [{"domain": "example.com", "success": True}]

    monkeypatch.setattr(cli_module, "BatchProcessor", FakeBatchProcessor)

    runner = CliRunner()
    result = runner.invoke(
        cli_module.cli,
        [
            "batch",
            "--input",
            str(input_file),
            "--output",
            str(tmp_path / "out"),
            "--workers",
            "2",
        ],
    )

    assert result.exit_code == 0
    assert Path(captured["domains_file_path"]).name == "domains.txt"
    assert captured["parallel"] is True
    assert captured["config"].max_workers == 2
