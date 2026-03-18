import re
from pathlib import Path


NON_ASCII_PATTERN = re.compile(r"[^\x00-\x7F]")
REQUIRED_ENGLISH_HINTS = ["risk", "security", "report"]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8").lower()


def test_reporting_templates_use_professional_english():
    root = Path(__file__).resolve().parents[2]
    files = [
        root / "src" / "passivesentry" / "reporting" / "templates" / "executive_summary.html",
        root / "src" / "passivesentry" / "reporting" / "templates" / "full_technical_report.html",
        root / "scripts" / "streamlit_dashboard.py",
    ]

    for file_path in files:
        content = _read(file_path)
        assert NON_ASCII_PATTERN.search(content) is None, (
            f"Found non-ASCII text in {file_path}"
        )
        assert any(hint in content for hint in REQUIRED_ENGLISH_HINTS), (
            f"Expected English security-reporting terms in {file_path}"
        )
