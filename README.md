# PassiveSentry

PassiveSentry is a passive (OSINT-only) security auditing framework aligned to OWASP Top 10 (A01-A10), with deterministic reporting for both executive and technical audiences.

## Current Project Status

- Status: production-ready for passive security posture assessments
- Scope: external/public attack surface only (no intrusive testing)
- Core validation: full automated test suite passing
- Last verified: 2026-03-17
- Test result: 33/33 passed

Validated test command:

```bash
uv run pytest -q
```

## What Is Included

- Single-domain auditing via CLI
- Massive multi-domain batch processing
- OWASP A01-A10 passive module orchestration
- Centralized risk scoring and normalized findings
- Canonical severity and finding deduplication
- JSON report generation
- PDF report generation
- Streamlit dashboard for result exploration
- Docker and Docker Compose workflows

## Reporting Consistency Model

The project uses a single source of truth for findings:

- Canonical field: `risk_analysis.normalized_findings`
- Producer: `RiskScorer` in [src/passivesentry/reporting/risk_scoring.py](src/passivesentry/reporting/risk_scoring.py)
- Consumers:
  - Executive summary calculations
  - Technical PDF OWASP sections
  - Minimal JSON (high-priority extract)

This prevents the classic split-brain issue where executive and technical reports diverge.

### Canonical finding structure

Each normalized finding includes:

- `category` (OWASP bucket: `A01` ... `A10`)
- `severity` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
- `text` (normalized human-readable finding)
- `recommendation` (action-oriented remediation)

### Normalization guarantees

- Same findings feed executive and technical outputs
- Duplicates are merged by category+text
- Highest severity wins on duplicates
- Findings are sorted deterministically by severity, category, then text
- Common legacy Spanish phrases are normalized for report consistency

## OWASP Coverage

Implemented OWASP 2025 passive modules in [src/passivesentry/modules/owasp_top10_2025.py](src/passivesentry/modules/owasp_top10_2025.py):

- A01: Broken Access Control
- A02: Security Misconfiguration
- A03: Software Supply Chain Failures
- A04: Cryptographic Failures
- A05: Injection
- A06: Insecure Design
- A07: Authentication Failures
- A08: Software or Data Integrity Failures
- A09: Security Logging and Alerting Failures
- A10: Mishandling of Exceptional Conditions

## Repository Layout

```text
src/passivesentry/
  core.py
  cli.py
  batch.py
  modules/
    owasp_top10_2025.py
    security_misconfiguration.py
    software_supply_chain.py
    cryptographic_failures.py
    security_logging.py
  reporting/
    risk_scoring.py
    json_reporter.py
    pdf_reporter.py
    templates/
      executive_summary.html
      full_technical_report.html
scripts/
  streamlit_dashboard.py
tests/
  unit/
  e2e/
docs/
```

## Requirements

- Python >= 3.10
- `uv` recommended for reproducible local execution
- Docker optional

## Installation

### Local editable install

```bash
pip install -e .
```

### Using uv environment

```bash
uv sync
```

## CLI Usage

Main command group:

```bash
passivesentry --help
```

### Full audit (all OWASP modules)

```bash
passivesentry audit example.com
```

### Audit with specific modules

```bash
passivesentry audit example.com -m security_misconfiguration -m cryptographic_failures
```

### Batch mode

```bash
passivesentry batch --input domains.txt --output results_massive
```

### Legacy single-purpose commands (still available)

```bash
passivesentry security example.com
passivesentry frontend example.com
passivesentry crypto example.com
passivesentry dns example.com
```

## Output Artifacts

### Single domain

- Full JSON report
- Optional executive summary text file (CLI flag)
- Optional PDF report(s)

### Batch execution

For each domain directory:

- Domain JSON report(s)
- Optional technical PDF
- Optional executive PDF
- `audit_results.json` (full serialized run)

For batch root directory:

- `batch_report_*.json` (execution summary)
- `batch_execution_*.log` (runtime log)

## Streamlit Dashboard

Run:

```bash
streamlit run scripts/streamlit_dashboard.py
```

The dashboard loads:

- Per-scan JSON outputs
- Batch execution summary JSON outputs

Main capabilities:

- Global KPIs
- Risk distribution charts
- Domain filtering
- Drill-down to module-level payloads
- Parse/load error visibility

## Docker

### Build image

```bash
docker build -t passivesentry:latest .
```

### Run full audit in container

```bash
docker run --rm passivesentry:latest passivesentry audit example.com
```

### Run batch and persist results

```bash
docker run --rm \
  -v $(pwd)/results_massive:/app/results_massive \
  -v $(pwd)/domains.txt:/app/domains.txt:ro \
  passivesentry:latest \
  passivesentry batch --input domains.txt --output results_massive
```

### Run dashboard

```bash
docker run --rm -p 8501:8501 \
  -v $(pwd)/results_massive:/app/results_massive \
  passivesentry:latest \
  streamlit run scripts/streamlit_dashboard.py --server.address=0.0.0.0 --server.port=8501
```

### Compose

```bash
docker compose up --build
```

## Testing

### Full suite

```bash
uv run pytest -q
```

### Unit only

```bash
uv run pytest -m unit -q
```

### E2E only

```bash
uv run pytest -m e2e -q
```

## Non-Goals and Boundaries

PassiveSentry is intentionally non-intrusive:

- No exploitation
- No brute force
- No fuzzing or active payload injection
- No authenticated internal app testing

Use active testing tools in controlled environments to complement this framework.

## Security and Quality Notes

- Canonical findings are centrally normalized to reduce language/format drift
- Risk and finding calculations are deterministic and test-covered
- Reporting templates are English-guarded by automated tests
- Batch and domain-level outputs are traceable via JSON and logs

## Documentation

Additional design notes:

- [docs/architecture.md](docs/architecture.md)
- [docs/technical_decisions.md](docs/technical_decisions.md)
- [docs/owasp_coverage.md](docs/owasp_coverage.md)

## Ownership and Contact

The core and modules of PassiveSentry are proprietary. If you want commercial access, contact me at miguel@developmi.com.

Author: Miguel Lozano | Developmi

- GitHub: https://github.com/Miguel-DevOps
- Website: https://developmi.com/
- LinkedIn: https://www.linkedin.com/in/miguel-dev-ops/
