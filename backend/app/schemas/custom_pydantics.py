
from pydantic import BaseModel, UUID4

class UUIDModelMixin(BaseModel):
    id: UUID4

    class Config:
        orm_mode = True
