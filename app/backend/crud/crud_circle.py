from sqlalchemy.orm import Session
from app.backend.models.circle import Circle, CircleMember
from app.backend.schemas.circle import CircleCreate
from app.backend.models.user import User


def create_circle(db: Session, *, obj_in: CircleCreate, owner_id: str) -> Circle:
    db_obj = Circle(
        name=obj_in.name, description=obj_in.description, owner_user_id=owner_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get(db: Session, id: str) -> Circle | None:
    return db.query(Circle).filter(Circle.id == id).first()


circle = {"create": create_circle, "get": get}