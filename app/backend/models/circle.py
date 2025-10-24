from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


class VisibilityScope(str, enum.Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    CIRCLES = "circles"
    INVITE_ONLY = "invite_only"


class CircleRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class Circle(Base):
    __tablename__ = "circles"
    id = Column(String, primary_key=True, default=generate_uuid)
    owner_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    visibility_scope = Column(Enum(VisibilityScope), default=VisibilityScope.FRIENDS)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner = relationship("User", back_populates="owned_circles")
    members = relationship("CircleMember", back_populates="circle")


class CircleMember(Base):
    __tablename__ = "circle_members"
    id = Column(String, primary_key=True, default=generate_uuid)
    circle_id = Column(String, ForeignKey("circles.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(CircleRole), default=CircleRole.MEMBER)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    circle = relationship("Circle", back_populates="members")
    user = relationship("User", back_populates="circle_memberships")