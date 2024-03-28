from unittest.mock import patch

import snap_http

from src.main import main

# main


@patch("src.main.poll")
@patch("src.main.register")
def test_starting_daemon_device_not_registered(mock_register, mock_poll):
    snap_http.http._make_request.return_value = {
        "type": "sync",
        "status_code": 200,
        "status": "OK",
        "result": {"is-registered": False, "server-url": "http://localhost:8000"},
        "sources": None,
        "change": None,
        "warning_timestamp": None,
        "warning_count": None,
    }

    main()

    mock_poll.assert_not_called()
    mock_register.assert_called_once_with("http://localhost:8000")


@patch("src.main.poll")
@patch("src.main.register")
def test_starting_daemon_device_registered(mock_register, mock_poll):
    snap_http.http._make_request.return_value = {
        "type": "sync",
        "status_code": 200,
        "status": "OK",
        "result": {"is-registered": True, "server-url": "http://localhost:8000"},
        "sources": None,
        "change": None,
        "warning_timestamp": None,
        "warning_count": None,
    }

    main()

    mock_poll.assert_called_once_with("http://localhost:8000")
    mock_register.assert_not_called()
