# OWASP Top 10 2025 Passive Coverage

This document summarizes how PassiveSentry currently maps passive analysis to OWASP Top 10 2025.

Primary reference: https://owasp.org/Top10/2025/

## Coverage Model and Constraints

- Scope: public-facing observation only (HTTP headers, HTML/JS resources, DNS, TLS)
- No authenticated testing
- No exploit payload execution
- No fuzzing or brute-force activity
- Findings are indicators of exposure, not exploit confirmation

## Coverage Summary

- OWASP modules implemented: 10/10
- Practical passive coverage estimate: 30-40% overall
- Main reason for partial coverage: many OWASP risks require internal context, authenticated workflows, and active validation

## Risk-by-Risk Mapping

### A01:2025 - Broken Access Control

- Module: OwaspA01BrokenAccessControl
- Official: https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/
- Passive signals used:
  - Public CORS policy checks
  - Sensitive route indicators in robots.txt, sitemap.xml, and public HTML
  - Directory listing patterns
- Limits:
  - No role-based authorization validation
  - No authenticated IDOR verification
- Estimated passive coverage: 25-35%

### A02:2025 - Security Misconfiguration

- Module: OwaspA02SecurityMisconfiguration (wrapper over SecurityHeadersAnalyzer)
- Official: https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/
- Passive signals used:
  - Missing/weak security headers
  - Informative headers and server fingerprint hints
  - Banner and version-risk heuristics
- Limits:
  - No internal infrastructure configuration inspection
  - No active misconfiguration exploitation
- Estimated passive coverage: 45-60% for web edge configuration

### A03:2025 - Software Supply Chain Failures

- Module: OwaspA03SoftwareSupplyChainFailures (wrapper over FrontendAnalyzer)
- Official: https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
- Passive signals used:
  - Frontend dependency exposure and version patterns
  - Insecure form transport indicators
  - Third-party script exposure checks
- Limits:
  - No internal SBOM visibility
  - No CI/CD provenance or signing validation
- Estimated passive coverage: 30-45%

### A04:2025 - Cryptographic Failures

- Module: OwaspA04CryptographicFailures (wrapper over CryptographicAnalyzer)
- Official: https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/
- Passive signals used:
  - Certificate validity and expiration
  - Negotiated TLS version checks
  - Weak cipher indicators
- Limits:
  - No at-rest encryption verification
  - No key-management architecture validation
- Estimated passive coverage: 40-55% for in-transit crypto posture

### A05:2025 - Injection

- Module: OwaspA05Injection
- Official: https://owasp.org/Top10/2025/A05_2025-Injection/
- Passive signals used:
  - Public form method patterns
  - Frontend sink heuristics (eval, innerHTML, and similar)
  - Suspicious parameter naming indicators
- Limits:
  - No payload execution
  - No backend SQL/NoSQL/command injection confirmation
- Estimated passive coverage: 20-35%

### A06:2025 - Insecure Design

- Module: OwaspA06InsecureDesign
- Official: https://owasp.org/Top10/2025/A06_2025-Insecure_Design/
- Passive signals used:
  - Public critical-flow exposure hints
  - Surface-level anti-automation signal checks
  - Header hygiene correlation
- Limits:
  - No threat modeling replacement
  - No internal design-control review
- Estimated passive coverage: 15-25%

### A07:2025 - Authentication Failures

- Module: OwaspA07AuthenticationFailures
- Official: https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/
- Passive signals used:
  - Login form method and structure checks
  - Session cookie flag visibility checks
  - Public MFA indicator checks
- Limits:
  - No real authentication attempts
  - No session lifecycle verification across user contexts
- Estimated passive coverage: 25-40%

### A08:2025 - Software or Data Integrity Failures

- Module: OwaspA08SoftwareOrDataIntegrityFailures
- Official: https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/
- Passive signals used:
  - Missing SRI on external scripts
  - Insecure script transport checks
  - CSP-related integrity hints
- Limits:
  - No release-signature verification
  - No backend deserialization integrity validation
- Estimated passive coverage: 25-40%

### A09:2025 - Security Logging and Alerting Failures

- Module: OwaspA09SecurityLoggingAndAlertingFailures (wrapper over DNSAnalyzer)
- Official: https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/
- Passive signals used:
  - DNS hygiene indicators (SPF/DMARC/MX/NS)
- Limits:
  - No direct observability into SIEM/SOC telemetry pipelines
  - Coverage is indirect by design
- Estimated passive coverage: 10-20%

### A10:2025 - Mishandling of Exceptional Conditions

- Module: OwaspA10MishandlingOfExceptionalConditions
- Official: https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/
- Passive signals used:
  - Exposed stack traces and error patterns
  - Debug header exposure checks
  - Public error/debug route indicators
- Limits:
  - No forced exception testing
  - No fail-open/fail-closed transactional validation
- Estimated passive coverage: 20-35%

## Interpretation Guidance

Use PassiveSentry as an external visibility baseline, then layer active, authenticated testing for high-assurance validation.

Recommended complementary controls:

1. Authenticated role-based test plans (A01, A06, A07)
2. Active DAST/fuzzing for injection paths (A05)
3. Internal SBOM + provenance controls (A03, A08)
4. Operational telemetry validation (A09)
5. Internal crypto and key-management assessments (A04)

Last updated: 2026-04-06
