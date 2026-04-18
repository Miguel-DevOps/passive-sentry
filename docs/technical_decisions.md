# PassiveSentry Technical Decisions

Date: 2026-04-06

This document records architectural and implementation decisions that shape the current release-ready state.

## 1) Single Source of Truth for Findings

Decision:

- Use risk_analysis.normalized_findings as the canonical finding source for all report consumers.

Why:

- Prevent executive/technical report drift
- Enforce deterministic severity and ordering
- Centralize language and text normalization

Implementation:

- Producer: [src/passivesentry/reporting/risk_scoring.py](../src/passivesentry/reporting/risk_scoring.py)
- Main consumers: [src/passivesentry/reporting/pdf_reporter.py](../src/passivesentry/reporting/pdf_reporter.py), [src/passivesentry/reporting/json_reporter.py](../src/passivesentry/reporting/json_reporter.py)

Behavioral guarantees:

- Deduplicate by category+text
- Keep highest severity when duplicates conflict
- Sort findings deterministically
- Derive severity arrays from canonical findings

## 2) PDF Rendering Stack

Decision:

- Standardize PDF generation on Jinja2 + WeasyPrint.

Why:

- Maintainable HTML-based report templates
- Clear separation between data context and rendering
- Easier style iteration for executive and technical outputs

Assets:

- [src/passivesentry/reporting/templates/executive_summary.html](../src/passivesentry/reporting/templates/executive_summary.html)
- [src/passivesentry/reporting/templates/full_technical_report.html](../src/passivesentry/reporting/templates/full_technical_report.html)
- [src/passivesentry/reporting/pdf_reporter.py](../src/passivesentry/reporting/pdf_reporter.py)

## 3) Fallback Strategy for Technical Reports

Decision:

- Prefer canonical normalized findings; if unavailable, apply robust module fallback extraction.

Why:

- Preserve technical report completeness for legacy or partial execution paths
- Avoid missing critical derived findings in fallback mode

Fallback now captures:

- Missing security headers
- Vulnerable libraries
- HTTP form transport issues
- SPF/DMARC missing/weak signals
- DNS error counts

## 4) Risk Scoring and Severity Consistency

Decision:

- Keep weighted scoring and finding classification in one component (RiskScorer).

Why:

- One place for scoring logic and severity derivation
- Better testability and reduced duplicate heuristics

## 5) Dashboard Data Model

Decision:

- Keep Streamlit + Pandas + Plotly for current scale.

Why:

- Existing workload is moderate
- Integration is straightforward and stable
- Migration cost to Polars is not justified without measured bottlenecks

Future trigger for reevaluation:

- Persistent memory/latency bottlenecks from large batch datasets

## 6) CLI and Batch Execution Model

Decision:

- Keep a canonical CLI surface centered on `audit` and module selectors (`-m`).
- Keep batch processor as first-class path for domain lists and deterministic outputs.

Why:

- Reduces command-surface ambiguity and operational drift
- Ensures one consistent invocation model for automation and analysts
- Supports both quick checks and scaled external posture runs

## 7) Containerized Reproducibility

Decision:

- Maintain Docker and Compose workflows including PDF dependencies.

Why:

- Reproducible runtime for CLI, batch, and dashboard
- Reduces environment drift in report generation

## 8) Verification Standard

Decision:

- Use uv-managed pytest execution as the baseline verification command.

Current status:

- Full suite passing: 40/40
- Command: uv run --python 3.14 pytest -q

## 9) Known Non-Blocking Gaps

Current non-blocking improvements (not release blockers):

- CI workflow files are not yet present in repository automation
- Dedicated lint/type gates are not yet enforced in automated pipeline

Recommended next hardening step:

- Add CI pipeline for tests, lint, and packaging checks

Last updated: 2026-04-06
