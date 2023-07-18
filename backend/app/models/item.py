from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship

from app.database.base import Base

class Item(Base):
    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))

    owner = relationship("User", back_populates="items")
