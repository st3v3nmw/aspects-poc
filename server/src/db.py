import json
import os
import uuid

from src import schemas
from src.constants import JSON_INDENT
from src.types import ConfigDict

DB = os.getenv("DATABASE", "db")


def update_target_config(config: ConfigDict) -> None:
    with open(f"{DB}/target_config.json", "w") as f:
        json.dump(config, f, indent=JSON_INDENT)


def get_target_config() -> schemas.Config:
    with open(f"{DB}/target_config.json", "r") as f:
        return schemas.Config(config=json.load(f))


def create_state(registration_uuid: uuid.UUID, state: schemas.State) -> None:
    _create_or_update_state(registration_uuid, state)


def update_state(registration_uuid: uuid.UUID, state: schemas.State) -> None:
    _create_or_update_state(registration_uuid, state)


def _create_or_update_state(registration_uuid: uuid.UUID, state: schemas.State) -> None:
    with open(f"{DB}/state_{registration_uuid}.json", "w") as f:
        json.dump(state.model_dump(), f, indent=JSON_INDENT)


def get_state(registration_uuid: uuid.UUID) -> schemas.State:
    with open(f"{DB}/state_{registration_uuid}.json", "r") as f:
        return schemas.State(**json.load(f))


def is_registered(registration_uuid: uuid.UUID) -> bool:
    return os.path.exists(f"{DB}/state_{registration_uuid}.json")
