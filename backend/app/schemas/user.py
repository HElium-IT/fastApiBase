from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.custom_pydantics import UUIDModelMixin

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None
    password: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str]
    full_name: Optional[str]


class UserInDBBase(UserBase, UUIDModelMixin):
    email: EmailStr
    is_active: bool
    is_superuser: bool


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
