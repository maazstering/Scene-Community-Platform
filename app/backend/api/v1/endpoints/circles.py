from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.backend.api.deps import get_db, get_current_active_user
from app.backend.crud import circle as crud_circle
from app.backend.schemas.circle import CircleCreate
from app.backend.models.user import User

router = APIRouter()


@router.get("", response_model=list[dict])
async def get_circles():
    return []


@router.post("", response_model=dict, status_code=201)
async def create_circle(
    circle_in: CircleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    circle = crud_circle.circle["create"](
        db, obj_in=circle_in, owner_id=current_user.id
    )
    return circle


@router.get("/{circle_id}", response_model=dict)
async def get_circle_details(circle_id: str, db: Session = Depends(get_db)):
    circle = crud_circle.circle["get"](db, id=circle_id)
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")
    return circle


@router.post("/{circle_id}/members", response_model=dict)
async def add_circle_member(circle_id: str):
    return {"message": "Not implemented"}