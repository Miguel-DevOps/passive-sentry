# PassiveSentry Architecture

## Overview

PassiveSentry is a modular passive security auditing framework that maps findings to OWASP Top 10 2025 (A01-A10). The design prioritizes non-intrusive assessment of public attack surface signals through HTTP and DNS observations.

The framework is intended for:

- External posture checks
- Repeatable domain audits
- Executive and technical reporting from one normalized finding model

It is not intended to replace authenticated, active, or exploit-driven testing.

## Design Principles

1. Passive-by-design
2. Deterministic reporting
3. Modular OWASP coverage
4. Clear separation between collection, scoring, and rendering
5. Automation-friendly outputs

## High-Level Components

- Audit orchestration: [src/passivesentry/core.py](../src/passivesentry/core.py)
- CLI entry points: [src/passivesentry/cli.py](../src/passivesentry/cli.py)
- Batch execution: [src/passivesentry/batch.py](../src/passivesentry/batch.py)
- OWASP module implementations: [src/passivesentry/modules/owasp_top10_2025.py](../src/passivesentry/modules/owasp_top10_2025.py)
- Shared analyzers (used by OWASP wrappers): [src/passivesentry/modules/security_misconfiguration.py](../src/passivesentry/modules/security_misconfiguration.py), [src/passivesentry/modules/software_supply_chain.py](../src/passivesentry/modules/software_supply_chain.py), [src/passivesentry/modules/cryptographic_failures.py](../src/passivesentry/modules/cryptographic_failures.py), [src/passivesentry/modules/security_logging.py](../src/passivesentry/modules/security_logging.py)
- Risk and finding normalization: [src/passivesentry/reporting/risk_scoring.py](../src/passivesentry/reporting/risk_scoring.py)
- Report renderers: [src/passivesentry/reporting/json_reporter.py](../src/passivesentry/reporting/json_reporter.py), [src/passivesentry/reporting/pdf_reporter.py](../src/passivesentry/reporting/pdf_reporter.py)
- PDF templates: [src/passivesentry/reporting/templates/executive_summary.html](../src/passivesentry/reporting/templates/executive_summary.html), [src/passivesentry/reporting/templates/full_technical_report.html](../src/passivesentry/reporting/templates/full_technical_report.html)
- Dashboard: [scripts/streamlit_dashboard.py](../scripts/streamlit_dashboard.py)

## Runtime Flow

1. Input normalization
2. Module execution
3. Score and finding aggregation
4. Canonical finding normalization
5. Output generation (JSON, PDF, batch artifacts)

### 1) Input normalization

- CLI and core normalize domains to HTTPS URLs when protocol is missing.
- Unsafe HTTP methods are prevented in shared request helpers.

### 2) Module execution

- The core orchestrator can run modules in parallel.
- Each module returns a structured dictionary with module-level signals and risk level.

### 3) Score aggregation

- Module outputs are scored with configurable weights.
- Global risk score and global risk level are produced.

### 4) Canonical finding normalization

The canonical finding collection is the single source of truth:

- Field: risk_analysis.normalized_findings
- Producer: RiskScorer
- Includes: category, severity, normalized text, recommendation

Normalization guarantees:

- Deduplication by category+text
- Highest severity retained on duplicates
- Stable deterministic sort order
- Severity arrays derived from canonical findings

### 5) Output generation

- JSON full report includes metadata, summary, detailed module results, and risk analysis.
- PDF technical report prefers canonical normalized findings and only falls back to module extraction when canonical data is unavailable.
- Batch mode creates per-domain outputs and global batch reports/logs.

## Reporting Consistency Architecture

Consistency is enforced through a single finding pipeline:

1. RiskScorer collects raw module findings and derived signals.
2. RiskScorer normalizes and deduplicates findings.
3. Executive summary and severity arrays are derived from the same normalized set.
4. PDF technical context uses the same normalized set when available.

This eliminates executive/technical desynchronization.

## Batch Architecture

Batch mode in [src/passivesentry/batch.py](../src/passivesentry/batch.py):

- Loads domains from plain text file
- Runs each domain through the same core pipeline
- Supports parallel workers
- Produces per-domain outputs plus batch summary
- Default batch output root is `results`

Per-domain artifact example:

- audit_results.json
- JSON report
- Technical PDF (optional)
- Executive PDF (optional)

Global artifact example:

- batch_report_*.json
- batch_execution_*.log

## Dashboard Data Path

The Streamlit dashboard consumes:

- Per-domain JSON scan reports
- Batch summary JSON reports

It provides:

- Global metrics
- Risk distribution views
- Domain filtering and drill-down
- JSON parse error visibility

## Quality Gates and Verification

Current automated status (last verified 2026-04-06):

- Full test suite passing: 40/40
- Command used: uv run --python 3.14 pytest -q

Test layout:

- Unit: [tests/unit](../tests/unit)
- E2E: [tests/e2e](../tests/e2e)

## Security Boundaries

PassiveSentry does not perform:

- Active exploitation
- Brute force attempts
- Credential stuffing
- Authenticated backend workflow attacks

Recommended complement for mature security programs:

- Authenticated active testing
- DAST/SAST/IAST
- Threat modeling and architecture reviews

## Current Architecture Readiness

- Stable for passive posture assessment workflows
- Deterministic reporting model in place
- Canonical CLI surface standardized on `passivesentry audit` and `passivesentry batch`
- CLI, batch, reporting, and dashboard paths covered by tests
- Suitable as a baseline engine for external security visibility

Last updated: 2026-04-06
