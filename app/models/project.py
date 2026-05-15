import uuid
from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Uuid
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")