from typing import Optional

from pydantic import BaseModel, UUID4

from app.schemas.custom_pydantics import UUIDModelMixin


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase, UUIDModelMixin):
    title: str
    owner_id: Optional[UUID4] = None

# Properties to return to client
class Item(ItemInDBBase):
    pass

# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
