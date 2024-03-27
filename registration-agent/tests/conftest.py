from unittest.mock import Mock

import pytest
import requests
import snap_http.http


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Prevent external requests from going out."""
    monkeypatch.setattr(requests, "request", Mock())
    monkeypatch.setattr(snap_http.http, "_make_request", Mock())


@pytest.fixture(autouse=True)
def test_env(monkeypatch):
    monkeypatch.setenv("ACCOUNT_ID", "f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN")
