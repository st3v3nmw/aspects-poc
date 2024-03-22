import uuid

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse, Response

from src import schemas, logic

router = APIRouter()


@router.put("/target-config/")
async def update_target_config(config: schemas.Config):
    logic.update_target_config(config.config)
    return config


@router.get("/target-config/")
async def get_target_config():
    rsp = logic.get_target_config()
    return rsp


@router.post("/register/")
async def register(register_request: schemas.RegisterRequest):
    rsp = logic.register(**register_request.dict())
    return rsp


@router.post("/poll/")
async def poll(poll_request: schemas.PollRequest):
    if not logic.is_registered(poll_request.uuid):
        raise HTTPException(status_code=400, detail=f"Not registered")
    rsp = logic.poll(poll_request.uuid, poll_request.config)
    if rsp is None:
        return Response(status_code=204)
    return rsp


@router.get("/state/{registration_uuid}/")
async def get_state(registration_uuid: uuid.UUID):
    if not logic.is_registered(registration_uuid):
        raise HTTPException(status_code=400, detail=f"Registration does not exist")
    rsp = logic.get_state(registration_uuid)
    return rsp
