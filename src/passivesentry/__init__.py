"""
PassiveSentry - Passive security auditing (OSINT-only) mapped to OWASP Top 10 2025
"""

__version__ = "0.1.0"
__author__ = "Miguel Lozano | Developmi"

# Utilities
from .utils import PassiveSentryLogger, create_http_session, safe_request

# Analysis modules
from .modules.security_misconfiguration import SecurityHeadersAnalyzer
from .modules.software_supply_chain import FrontendAnalyzer
from .modules.cryptographic_failures import CryptographicAnalyzer
from .modules.owasp_top10_2025 import (
    OwaspA01BrokenAccessControl,
    OwaspA02SecurityMisconfiguration,
    OwaspA03SoftwareSupplyChainFailures,
    OwaspA04CryptographicFailures,
    OwaspA05Injection,
    OwaspA06InsecureDesign,
    OwaspA07AuthenticationFailures,
    OwaspA08SoftwareOrDataIntegrityFailures,
    OwaspA09SecurityLoggingAndAlertingFailures,
    OwaspA10MishandlingOfExceptionalConditions,
)

# Reporting
from .reporting.risk_scoring import RiskScorer
from .reporting.json_reporter import JSONReporter
from .reporting.pdf_reporter import PDFReporter
from .batch import BatchConfig, BatchProcessor, load_domains_from_file

# Core
from .core import PassiveSentryAuditor

# CLI (available if installed with scripts)
try:
    from .cli import cli, main
except ImportError:
    pass  # Click may not be available in all environments
