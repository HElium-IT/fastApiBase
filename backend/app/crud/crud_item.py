from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_by_title(self, db: Session, *, title: str) -> Item:
        return db.query(Item).filter(Item.title == title).first()

    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: UUID
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Item(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(Item)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


item = CRUDItem(Item)
