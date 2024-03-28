from unittest.mock import call

import pytest
import snap_http

from src.aspects import get_aspect, set_aspect, unset_aspect

# get_aspect


def test_get_aspect():
    snap_http.http._make_request.return_value = {
        "type": "sync",
        "status_code": 200,
        "status": "OK",
        "result": {
            "follower": {"domain": "staging.example.com"},
            "follower_4": {"telemetry": True},
        },
        "sources": None,
        "change": None,
        "warning_timestamp": None,
        "warning_count": None,
    }

    result = get_aspect("snap-config")

    assert result == {
        "follower": {"domain": "staging.example.com"},
        "follower_4": {"telemetry": True},
    }
    snap_http.http._make_request.assert_called_once_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
        "GET",
        query_params={},
    )


def test_get_aspect_specific_field():
    snap_http.http._make_request.return_value = {
        "type": "sync",
        "status_code": 200,
        "status": "OK",
        "result": {
            "follower": {"domain": "staging.example.com"},
        },
        "sources": None,
        "change": None,
        "warning_timestamp": None,
        "warning_count": None,
    }

    result = get_aspect("snap-config", fields=["follower"])

    assert result == {
        "follower": {"domain": "staging.example.com"},
    }
    snap_http.http._make_request.assert_called_once_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
        "GET",
        query_params={"fields": "follower"},
    )


def test_get_aspect_exception():
    snap_http.http._make_request.side_effect = snap_http.SnapdHttpException(
        (
            '{"type":"error","status-code":404,"status":"Not Found",'
            '"result":{"message":"cannot get "followed" in aspect '
            "f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config: "
            "matching rules don't map to any values\"}}"
        )
    )

    result = get_aspect("snap-config", fields=["followed"])

    assert result == {}
    snap_http.http._make_request.assert_called_once_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
        "GET",
        query_params={"fields": "followed"},
    )


# set_aspect


def test_set_aspect():
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

    set_aspect(
        "snap-config",
        {
            "follower": {"domain": "staging.example.com"},
            "follower_4": {"telemetry": True},
        },
    )

    snap_http.http._make_request.assert_called_once_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
        "PUT",
        body={
            "follower": {"domain": "staging.example.com"},
            "follower_4": {"telemetry": True},
        },
    )


def test_set_aspect_exception():
    snap_http.http._make_request.side_effect = snap_http.SnapdHttpException(
        (
            '{"type":"error","status-code":404,"status":"Not Found",'
            '"result":{"message":"cannot set "uid", "ip-address", '
            '"public-rsa-key", "private-rsa-key", "registered", '
            '"architecture" in aspect f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN'
            '/aspects-poc/devices: aspect not found"}}'
        )
    )

    with pytest.raises(snap_http.SnapdHttpException):
        set_aspect(
            "devices",
            {
                "uid": "952a4099-f85d-4116-9542-46465e105670",
                "ip-address": "127.0.0.1",
                "public-rsa-key": "public_key",
                "private-rsa-key": "private_key",
                "registered": 1,
                "architecture": "amd64",
            },
        )

    snap_http.http._make_request.assert_called_once_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/devices",
        "PUT",
        body={
            "uid": "952a4099-f85d-4116-9542-46465e105670",
            "ip-address": "127.0.0.1",
            "public-rsa-key": "public_key",
            "private-rsa-key": "private_key",
            "registered": 1,
            "architecture": "amd64",
        },
    )


# unset_aspect


def test_unset_aspect():
    def _mock_snap_response(path, method, **kwargs):
        if "GET" == method:
            # get all the fields
            return {
                "type": "sync",
                "status_code": 200,
                "status": "OK",
                "result": {
                    "follower": {"domain": "staging.example.com"},
                    "follower_4": {"telemetry": True},
                },
                "sources": None,
                "change": None,
                "warning_timestamp": None,
                "warning_count": None,
            }
        else:
            # set the new aspect values
            return {
                "type": "async",
                "status_code": 202,
                "status": "Accepted",
                "result": None,
                "sources": None,
                "change": "1496",
                "warning_timestamp": None,
                "warning_count": None,
            }

    snap_http.http._make_request.side_effect = _mock_snap_response

    unset_aspect("snap-config")

    snap_http.http._make_request.assert_has_calls(
        [
            call(
                "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
                "GET",
                query_params={},
            ),
            call(
                "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
                "PUT",
                body={"follower": None, "follower_4": None},
            ),
        ]
    )


def test_unset_aspect_specific_fields():
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

    unset_aspect("snap-config", fields=["follower"])

    snap_http.http._make_request.assert_called_once_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
        "PUT",
        body={"follower": None},
    )


def test_unset_aspect_exception():
    snap_http.http._make_request.side_effect = snap_http.SnapdHttpException(
        (
            '{"type":"error","status-code":404,"status":"Not Found",'
            '"result":{"message":"cannot get "followed" in aspect '
            "f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config: "
            "matching rules don't map to any values\"}}"
        )
    )

    unset_aspect("snap-config", fields=["followed"])

    snap_http.http._make_request.assert_called_once_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
        "PUT",
        body={"followed": None},
    )
