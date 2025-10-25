from fastapi import APIRouter, Depends, HTTPException
from app.backend.api.deps import get_current_active_user
from app.backend.schemas.circle import CircleCreate
from app.backend.models.user import User
from app.backend.data.memory_store import memory_store

router = APIRouter()


@router.get("", response_model=list[dict])
async def get_circles():
    return memory_store.get_circles()


@router.post("", response_model=dict, status_code=201)
async def create_circle(
    circle_in: CircleCreate, current_user: dict = Depends(get_current_active_user)
):
    circle = memory_store.create_circle(
        circle_in=circle_in, owner_id=current_user["id"]
    )
    return circle


@router.get("/{circle_id}", response_model=dict)
async def get_circle_details(circle_id: str):
    circle = memory_store.get_circle_by_id(circle_id)
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")
    return circle


@router.post("/{circle_id}/members", response_model=dict)
async def add_circle_member(circle_id: str):
    return {"message": "Not implemented"}