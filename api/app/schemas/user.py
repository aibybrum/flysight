from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str
    email: Optional[EmailStr]
    password: Optional[str]


class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True
