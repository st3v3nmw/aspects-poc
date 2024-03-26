import os

from snap_http.http import get, SnapdHttpException


def get_config():
    """Get the snap's config."""
    account_id = os.environ["ACCOUNT_ID"]
    snap_instance_name = os.environ["SNAP_INSTANCE_NAME"]

    try:
        response = get(
            f"/aspects/{account_id}/aspects-poc/snap-config",
            query_params={
                "fields": snap_instance_name[8:].replace("_", "-"),
            },
        )
        return response.result
    except SnapdHttpException:
        # the aspect is empty
        return {}
