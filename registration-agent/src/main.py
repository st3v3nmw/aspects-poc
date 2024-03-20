import snap_http

from src.api import poll, register


def main() -> None:
    config = snap_http.get_conf("aspects-registration-agent").result
    is_registered = config["is-registered"]
    server_url = config["server-url"]

    if is_registered:
        poll(server_url)
    else:
        register(server_url)
