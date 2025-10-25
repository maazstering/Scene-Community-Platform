from sqlalchemy.orm import Session
from app.backend.models.activity import Activity, ActivityRequest
from app.backend.schemas.activity import (
    ActivityCreate,
    ActivityRequestCreate,
    ActivityRequestUpdate,
)
from app.backend.models.user import User


def create_activity(
    db: Session, *, obj_in: ActivityCreate, host_user_id: str
) -> Activity:
    db_obj = Activity(**obj_in.dict(), host_user_id=host_user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> list[Activity]:
    return db.query(Activity).offset(skip).limit(limit).all()


def get(db: Session, id: str) -> Activity | None:
    return db.query(Activity).filter(Activity.id == id).first()


activity = {"create": create_activity, "get_multi": get_multi, "get": get}