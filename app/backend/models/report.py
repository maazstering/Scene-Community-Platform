from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


class ReportReason(str, enum.Enum):
    INAPPROPRIATE_CONTENT = "inappropriate_content"
    HARASSMENT = "harassment"
    SPAM = "spam"
    FAKE_PROFILE = "fake_profile"
    UNSAFE_BEHAVIOR = "unsafe_behavior"
    OTHER = "other"


class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class TargetType(str, enum.Enum):
    USER = "user"
    ACTIVITY = "activity"
    EVENT = "event"
    VENUE = "venue"
    COMMENT = "comment"


class Report(Base):
    __tablename__ = "reports"
    id = Column(String, primary_key=True, default=generate_uuid)
    reporter_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    target_type = Column(Enum(TargetType), nullable=False)
    target_id = Column(String, nullable=False)
    reason = Column(Enum(ReportReason), nullable=False)
    description = Column(Text)
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    reviewed_by_user_id = Column(String, ForeignKey("users.id"))
    reviewed_at = Column(DateTime(timezone=True))
    resolution_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reporter = relationship("User", foreign_keys=[reporter_user_id])
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_user_id])