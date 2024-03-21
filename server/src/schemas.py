from pydantic import BaseModel, UUID4, Field

from src.types import ConfigDict


class Config(BaseModel):
    config: ConfigDict


class State(BaseModel):
    registered: int
    ip_address: str = Field(serialization_alias="ip-address")
    public_key_rsa: str = Field(serialization_alias="public-key-rsa")
    arch: str
    config: ConfigDict


class RegisterRequest(BaseModel):
    ip_address: str = Field(validation_alias="ip-address")
    public_key_rsa: str = Field(validation_alias="public-key-rsa")
    arch: str


class RegisterResponse(RegisterRequest):
    uuid: UUID4
    registered: int
    ip_address: str = Field(serialization_alias="ip-address")
    public_key_rsa: str = Field(serialization_alias="public-key-rsa")
    arch: str


class PollRequest(BaseModel):
    uuid: UUID4
    config: ConfigDict


class PollResponse(BaseModel):
    config: ConfigDict
