from unittest.mock import call, patch

from src.main import main

# main


@patch("src.main.print")
@patch("src.main.get_config")
def test_log_config_to_stdout(mock_get_conf, mock_print):
    mock_get_conf.return_value = {
        "follower": {"domain": "staging.example.com"},
    }

    main()

    mock_print.assert_has_calls(
        [
            call("The current config is:"),
            call("\t{'follower': {'domain': 'staging.example.com'}}"),
        ]
    )
