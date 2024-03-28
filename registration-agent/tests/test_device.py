import re

from src.device import generate_keys, get_architecture, get_ip_address


# generate_keys


def test_generate_keys():
    private_key, public_key = generate_keys()
    assert private_key.startswith("-----BEGIN PRIVATE KEY-----\n")
    assert private_key.endswith("-----END PRIVATE KEY-----\n")
    assert public_key.startswith("ssh-rsa")


# get_architecture


def test_get_architecture():
    arch = get_architecture()
    assert arch in [
        "amd64",
        "arm64",
        "armhf",
        "ppc64el",
        "s390x",
        "i386",
    ]


# get_ip_address


def test_get_ip_address():
    ip = get_ip_address()
    pattern = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"
    assert re.search(pattern, ip) is not None
