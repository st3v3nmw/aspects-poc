import snap_http

from src.aspects import get_config

# get_config


def test_get_config():
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

    result = get_config()

    assert result == {
        "follower": {"domain": "staging.example.com"},
    }
    snap_http.http._make_request.assert_called_once_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
        "GET",
        query_params={"fields": "follower-1"},
    )


def test_get_config_exception():
    snap_http.http._make_request.side_effect = snap_http.SnapdHttpException(
        (
            '{"type":"error","status-code":404,"status":"Not Found",'
            '"result":{"message":"cannot get "follower-1" in aspect '
            "f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config: "
            "matching rules don't map to any values\"}}"
        )
    )

    result = get_config()

    assert result == {}
    snap_http.http._make_request.assert_called_once_with(
        "/aspects/f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN/aspects-poc/snap-config",
        "GET",
        query_params={"fields": "follower-1"},
    )
