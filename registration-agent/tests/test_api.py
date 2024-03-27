from dataclasses import dataclass
from typing import Optional
from unittest.mock import call, DEFAULT, Mock, patch

import pytest
import requests
import snap_http.http

from src.api import _map_snap_config, HttpException, poll, register


@dataclass
class TestResponse:
    status_code: int
    data: Optional[dict] = None
    text: Optional[str] = None

    __test__ = False

    def json(self):
        return self.data


# _map_snap_config


def test_map_snap_config():
    config = {
        "follower_1": {"telemetry": True},
        "follower": {"port": 80},
        "follower-3": {"domain": "example.com"},
    }
    expected = {
        "follower-1": {"telemetry": True},
        "follower": {"port": 80},
        "follower-3": {"domain": "example.com"},
    }
    assert _map_snap_config(config) == expected


# register


@patch("src.api.get_architecture", return_value="amd64")
@patch("src.api.get_ip_address", return_value="192.168.0.106")
@patch(
    "src.api.generate_keys",
    return_value=("some private rsa key", "some public rsa key"),
)
def test_register_success(mock_gen_keys, mock_get_ip, mock_get_arch):
    requests.request.return_value = TestResponse(
        200,
        {
            "uuid": "b6b53f82-b892-43a7-9d90-09b7479c7a5d",
            "ip-address": "192.168.0.106",
            "public-rsa-key": "some public rsa key",
            "private-rsa-key": "some private rsa key",
            "registered": 1711613131,
            "architecture": "amd64",
        },
    )
    snap_http.http._make_request.return_value = {
        "type": "async",
        "status_code": 202,
        "status": "Accepted",
        "result": None,
        "sources": None,
        "change": "1496",
        "warning_timestamp": None,
        "warning_count": None,
    }

    register("http://localhost:8000")

    requests.request.assert_called_once_with(
        "post",
        "http://localhost:8000/register/",
        json={
            "ip-address": "192.168.0.106",
            "arch": "amd64",
            "public-key-rsa": "some public rsa key",
        },
    )
    snap_http.http._make_request.assert_has_calls(
        [
            call(
                "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/device",
                "PUT",
                body={
                    "uid": "b6b53f82-b892-43a7-9d90-09b7479c7a5d",
                    "ip-address": "192.168.0.106",
                    "public-rsa-key": "some public rsa key",
                    "private-rsa-key": "some private rsa key",
                    "registered": 1711613131,
                    "architecture": "amd64",
                },
            ),
            call(
                "/snaps/aspects-registration-agent/conf",
                "PUT",
                body={"is-registered": True},
            ),
        ]
    )


@patch.multiple(
    "src.api",
    get_architecture=DEFAULT,
    get_ip_address=DEFAULT,
    generate_keys=Mock(
        return_value=("some private rsa key", "some public rsa key"),
    ),
)
def test_register_failure(*args, **kwargs):
    requests.request.return_value = TestResponse(404, text="Not Found")

    with pytest.raises(HttpException):
        register("http://localhost:8000")


# poll


def test_poll_config_does_not_match():
    def _mock_snap_response(path, method, **kwargs):
        if "device" in path:
            result = {
                "architecture": "amd64",
                "ip-address": "192.168.0.106",
                "public-rsa-key": "some public rsa key",
                "registered": 1711613131,
                "uid": "b6b53f82-b892-43a7-9d90-09b7479c7a5d",
            }
        else:
            # snap-config
            result = {}
        return {
            "type": "sync",
            "status_code": 200,
            "status": "OK",
            "result": result,
            "sources": None,
            "change": None,
            "warning_timestamp": None,
            "warning_count": None,
        }

    snap_http.http._make_request.side_effect = _mock_snap_response

    requests.request.return_value = TestResponse(
        200,
        {
            "config": {
                "follower": {"domain": "staging.example.com"},
                "follower_4": {"telemetry": False},
            }
        },
    )

    poll("http://localhost:8000")

    requests.request.assert_called_once_with(
        "post",
        "http://localhost:8000/poll/",
        json={"uuid": "b6b53f82-b892-43a7-9d90-09b7479c7a5d", "config": {}},
    )
    snap_http.http._make_request.assert_called_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
        "PUT",
        body={
            "follower": {"domain": "staging.example.com"},
            "follower-4": {"telemetry": False},
        },
    )
