from pprint import pformat
from textwrap import indent

from src.aspects import get_config


def main() -> None:
    config = get_config()
    print("The current config is:")
    pretty = pformat(config)
    print(indent(pretty, prefix="\t"))
