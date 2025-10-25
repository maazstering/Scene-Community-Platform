from sqlalchemy.orm import Session
from app.backend.models.event import Event
from app.backend.schemas.event import EventCreate


def create_event(db: Session, *, obj_in: EventCreate, host_user_id: str) -> Event:
    db_obj = Event(**obj_in.dict(), host_user_id=host_user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> list[Event]:
    return db.query(Event).offset(skip).limit(limit).all()


def get(db: Session, id: str) -> Event | None:
    return db.query(Event).filter(Event.id == id).first()


event = {"create": create_event, "get_multi": get_multi, "get": get}