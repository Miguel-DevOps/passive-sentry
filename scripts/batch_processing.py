"""Compatibility wrapper for package-level batch processing."""

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from passivesentry.batch import BatchConfig, BatchProcessor


def main():
    """Entry point to process domains from a text file."""
    parser = argparse.ArgumentParser(
        description="Batch processing for PassiveSentry - large-scale domain auditing"
    )
    parser.add_argument("-i", "--input", default="domains.txt")
    parser.add_argument("-o", "--output", default="results_massive")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--sequential", action="store_true")
    parser.add_argument("--no-json", action="store_true")
    parser.add_argument("--no-pdf", action="store_true")
    parser.add_argument("--no-summary", action="store_true")
    parser.add_argument("--company", default="Miguel Lozano | Developmi")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    config = BatchConfig(
        output_base_dir=args.output,
        verbose=args.verbose,
        max_workers=args.workers,
        generate_json=not args.no_json,
        generate_pdf=not args.no_pdf,
        generate_executive_summary=not args.no_summary,
        company_name=args.company,
    )
    processor = BatchProcessor(config=config)
    processor.process_domains_file(str(Path(args.input)), parallel=not args.sequential)


if __name__ == "__main__":
    main()
