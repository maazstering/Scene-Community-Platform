from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Vouch(Base):
    __tablename__ = "vouches"
    id = Column(String, primary_key=True, default=generate_uuid)
    giver_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    receiver_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    short_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    giver = relationship(
        "User", foreign_keys=[giver_user_id], back_populates="given_vouches"
    )
    receiver = relationship(
        "User", foreign_keys=[receiver_user_id], back_populates="received_vouches"
    )
    __table_args__ = (
        UniqueConstraint("giver_user_id", "receiver_user_id", name="unique_vouch_pair"),
    )