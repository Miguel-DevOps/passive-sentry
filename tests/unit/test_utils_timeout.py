from unittest.mock import Mock

import requests

from passivesentry.utils import create_http_session, safe_request


def test_safe_request_timeout_sets_friendly_error(monkeypatch):
    session = create_http_session(timeout=7, max_retries=1)

    def fake_request(*args, **kwargs):
        raise requests.exceptions.Timeout("connect timeout")

    monkeypatch.setattr(session, "request", fake_request)

    response = safe_request(session, "https://guatt.com", "GET")

    assert response is None
    error_msg = getattr(session, "_passivesentry_last_error", "")
    assert "Timeout de 7s" in error_msg
    assert "guatt.com" in error_msg


def test_safe_request_clears_previous_error_on_success(monkeypatch):
    session = create_http_session(timeout=5, max_retries=0)
    setattr(session, "_passivesentry_last_error", "old error")

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None

    def fake_request(*args, **kwargs):
        return mock_response

    monkeypatch.setattr(session, "request", fake_request)

    response = safe_request(session, "https://example.com", "GET")

    assert response is mock_response
    assert getattr(session, "_passivesentry_last_error", None) is None
