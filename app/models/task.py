import uuid
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Uuid
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)

    project_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")