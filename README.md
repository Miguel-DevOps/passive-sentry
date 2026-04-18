<div align="center">
<img src="docs/assets/passive-sentry.png" width="150" alt="Passive Sentry logo" />

# PassiveSentry

PassiveSentry is a passive (OSINT-only) security auditing framework aligned to OWASP Top 10:2025 (A01-A10), with deterministic reporting for executive and technical audiences.

</div>

## Current Status

- Runtime baseline: Python 3.14+
- Package manager: uv with deterministic lockfile (uv.lock)
- Security model: 100% passive-only collection
- OWASP scope: A01-A10 mapped with passive heuristics
- Latest verification: 2026-04-06
- Test result: 40/40 passed

Validated command:

```bash
uv run --python 3.14 pytest -q
```

## Core Features

- Single-domain audit via CLI
- Multi-domain batch processing
- Canonical OWASP A01-A10 module orchestration
- Deterministic risk scoring and finding normalization
- JSON report generation
- PDF report generation (lazy-loaded, native dependencies required at generation time)
- Streamlit dashboard for result exploration
- Docker and Docker Compose workflows

## Logging and Output Behavior

PassiveSentry runs cleanly with minimal noise:

- **Expected 404s (suppressed)**: HTTP 404 responses for optional resources (robots.txt, sitemap.xml, security.txt, etc.) are logged at DEBUG level to avoid warning spam.
- **External library logs suppressed**: Third-party libraries (fontTools, Pillow, urllib3, etc.) are silenced to keep output focused on PassiveSentry results.
- **Verbose mode** (`--verbose`): Pass the flag to enable DEBUG logging if needed for troubleshooting.

## Passive-Only Enforcement

PassiveSentry is intentionally non-intrusive:

- No exploitation
- No brute force
- No fuzzing
- No active payload injection
- No authenticated internal app testing

HTTP collection is constrained to safe methods (GET/HEAD/OPTIONS). Results are based on publicly observable artifacts.

## OWASP Coverage (Top 10:2025)

Implemented in [src/passivesentry/modules/owasp_top10_2025.py](src/passivesentry/modules/owasp_top10_2025.py):

- A01 Broken Access Control
- A02 Security Misconfiguration
- A03 Software Supply Chain Failures
- A04 Cryptographic Failures
- A05 Injection
- A06 Insecure Design
- A07 Authentication Failures
- A08 Software or Data Integrity Failures
- A09 Security Logging and Alerting Failures
- A10 Mishandling of Exceptional Conditions

Coverage notes:

- All categories are represented and executed in full audits.
- Depth is intentionally passive; some categories provide indicator-level confidence only.
- A09 is modeled from externally visible DNS and related telemetry, so it should be treated as indirect evidence.

## Deterministic Reporting Model

Canonical source of truth:

- Field: risk_analysis.normalized_findings
- Producer: [src/passivesentry/reporting/risk_scoring.py](src/passivesentry/reporting/risk_scoring.py)

Normalization guarantees:

- Deduplication by category + text
- Highest-severity-wins for duplicates
- Stable sort order for reproducible outputs
- Normalized English phrasing for legacy finding variants

## Output Paths and Domain Processing Guarantees

Default output directory for both single and batch workflows is now results.

Single-domain audit output:

- JSON report in results
- Optional summary text
- Optional PDFs

Batch output:

- One subdirectory per input domain
- Per-domain audit_results.json
- Optional per-domain technical and executive PDFs
- Batch summary JSON and execution log in root output directory

Domain processing guarantee:

- Every non-empty, non-comment line in the input file is processed.
- Batch summary includes total_domains, succeeded, failed, and per-domain status.
- Invalid domains are counted as processed failures (not silently skipped).

## Requirements

- Python >= 3.14
- uv as the supported resolver and runner
- uv.lock committed for reproducible installs
- Docker optional

### Native requirements for PDF generation

PDF output depends on WeasyPrint native libraries. On Debian/Ubuntu environments, install:

```bash
sudo apt-get update
sudo apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi8 shared-mime-info fonts-dejavu
```

If these libraries are unavailable, run batch mode without PDF artifacts:

```bash
uv run --python 3.14 passivesentry batch --input domains.txt --no-pdf --no-summary
```

Batch runtime behavior:

- On startup, batch mode checks PDF runtime capability.
- The check is silent and does not import WeasyPrint directly (to avoid startup noise).
- If dependencies are missing, the warning includes exact missing components.
- If WeasyPrint native dependencies are missing, PDF artifacts are automatically disabled.
- Domain processing continues in JSON-only mode instead of failing the batch.
- A warning is logged so operators can enable PDF support later without losing execution coverage.

## Site Quality Indicators

In addition to OWASP Top 10:2025 vulnerability assessment, PassiveSentry evaluates **Site Quality Indicators** that reflect operational maturity and security-conscious practices:

- `robots.txt` - Crawler directives (SEO, public/private content handling)
- `sitemap.xml` - Site structure declaration (crawlability)
- `security.txt` - Vulnerability disclosure policy (RFC 9110 compliant)
- `llms.txt` - LLM/AI training directives (data governance)
- `ai.json` - AI bot behavior configuration (emerging standard)
- `dnt-policy.txt` - Do Not Track policy (privacy)

### How They Appear in Reports

**Executive Summary PDF:**
- Concise presence/absence listing
- High-level recommendations for each indicator

**Full Technical Report PDF:**
- Detailed per-domain assessment
- For each **present** indicator: URL, size, and targeted guidance
- For each **absent** indicator: purpose, implementation steps, and priority ranking
- Priority focus list to guide remediation order

**JSON Output (`audit_results.json`):**
```json
"site_quality_indicators": {
  "present": {
    "sitemap.xml (site structure)": {
      "url": "https://example.com/sitemap.xml",
      "status_code": 200,
      "size_bytes": 1524
    }
  },
  "absent": [
    "robots.txt (crawler directives)",
    "security.txt (security policy)"
  ]
}
```

### Customization

Site Quality Indicators are **fully customizable** for your organization's standards:
- Add/remove resources to check (e.g., industry compliance files, custom endpoints)
- Modify recommendation text per indicator
- Adjust priority rankings
- Add compliance framework mappings

See [`docs/customizing_reports.md`](docs/customizing_reports.md) for detailed instructions on:
- Where to edit templates
- How to add custom resources or fields
- Mapping to your org's compliance standards
- Automation and CI/CD integration examples

## Installation

Install locked runtime dependencies:

```bash
uv sync --frozen
```

Install dev dependencies:

```bash
uv sync --dev
```

Refresh lockfile after dependency changes:

```bash
uv lock --python 3.14
```

## CLI Usage

Help:

```bash
uv run --python 3.14 passivesentry --help
```

Full audit (A01-A10):

```bash
uv run --python 3.14 passivesentry audit example.com
```

Scoped audit:

```bash
uv run --python 3.14 passivesentry audit example.com -m security_misconfiguration -m cryptographic_failures
```

Batch (default output is results):

```bash
uv run --python 3.14 passivesentry batch --input domains.txt
```

Batch with explicit output:

```bash
uv run --python 3.14 passivesentry batch --input domains.txt --output results
```

## Streamlit Dashboard

Run:

```bash
streamlit run scripts/streamlit_dashboard.py
```

Default dashboard input directory is results.

## Docker

Build image:

```bash
docker build -t passivesentry:latest .
```

Run single audit:

```bash
docker run --rm passivesentry:latest passivesentry audit example.com
```

Run batch and persist output in results:

```bash
docker run --rm \
  -v $(pwd)/results:/app/results \
  -v $(pwd)/domains.txt:/app/domains.txt:ro \
  passivesentry:latest \
  passivesentry batch --input domains.txt --output results
```

Run dashboard:

```bash
docker run --rm -p 8501:8501 \
  -v $(pwd)/results:/app/results \
  passivesentry:latest \
  streamlit run scripts/streamlit_dashboard.py --server.address=0.0.0.0 --server.port=8501
```

Compose:

```bash
docker compose up --build
```

## Testing

Full suite:

```bash
uv run --python 3.14 pytest -q
```

Batch and output behavior checks:

```bash
uv run --python 3.14 pytest -q tests/e2e/test_batch_cli.py tests/unit/test_batch_processing.py
```

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
  batch_processing.py
  streamlit_dashboard.py
tests/
  unit/
  e2e/
docs/
```

## Documentation

- [docs/architecture.md](docs/architecture.md)
- [docs/technical_decisions.md](docs/technical_decisions.md)
- [docs/owasp_coverage.md](docs/owasp_coverage.md)

## Ownership and Contact

The core and modules of PassiveSentry are proprietary. For commercial access, contact [miguel@developmi.com](mailto:miguel@developmi.com).

Author: Miguel Lozano | Developmi

- GitHub: [Miguel-DevOps](https://github.com/Miguel-DevOps)
- Website: [developmi.com](https://developmi.com/)
- LinkedIn: [Miguel DevOps](https://www.linkedin.com/in/miguel-dev-ops/)
