from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from uuid import UUID, uuid4
from sqlalchemy.orm import relationship

from app.database.base import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(Base):
    id: str = Column(String, default=str(uuid4()), primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    
    owner_id = Column(String, ForeignKey("user.id"))
    
    owner: "User" = relationship("User", back_populates="items")
