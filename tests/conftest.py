"""
Pytest configuration for PassiveSentry.
Adds src to sys.path so package imports resolve correctly.
Defines common fixtures for tests.
"""

import sys
import os
import pytest

# Add src to path so the package can be imported
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)


@pytest.fixture
def domain():
    """Fixture that provides a test domain."""
    return "example.com"


@pytest.fixture
def url():
    """Fixture that provides a test URL."""
    return "https://example.com"


def pytest_collection_modifyitems(items):
    """Automatically marks tests based on their folder."""
    for item in items:
        node_id = item.nodeid
        if "/tests/unit/" in node_id or "tests/unit/" in node_id:
            item.add_marker(pytest.mark.unit)
        if "/tests/e2e/" in node_id or "tests/e2e/" in node_id:
            item.add_marker(pytest.mark.e2e)
