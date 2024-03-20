import os
from typing import Any, Optional

from snap_http.http import get, put


def get_aspect(
    name: str,
    *,
    fields: Optional[list[str]] = None,
) -> dict:
    """Get the aspect values."""
    query_params = {}
    if fields:
        query_params["fields"] = ",".join(fields)

    account_id = os.environ["ACCOUNT_ID"]
    response = get(
        f"/aspects/{account_id}/aspects-poc/{name}",
        query_params=query_params,
    )
    return response.result


def set_aspect(
    name: str,
    value: dict[str, Any],
) -> None:
    """Set the aspect values."""
    account_id = os.environ["ACCOUNT_ID"]
    put(
        f"/aspects/{account_id}/aspects-poc/{name}",
        value,
    )
