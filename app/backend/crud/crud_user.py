from sqlalchemy.orm import Session
from app.backend.models.user import User
from app.backend.schemas.user import UserCreate, UserUpdate
from app.backend.core.security import hash_password


def get_user_by_email(db: Session, *, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, *, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        name=obj_in.name,
        phone=obj_in.phone,
        city=obj_in.city,
        bio=obj_in.bio,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get(db: Session, id: str) -> User | None:
    return db.query(User).filter(User.id == id).first()


user = {
    "get_by_email": get_user_by_email,
    "create": create_user,
    "get_multi": get_multi,
    "get": get,
}