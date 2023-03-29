from uuid import UUID
from pydantic import BaseModel


class JumpBase(BaseModel):
    id: UUID
    name: str


class JumpCreate(JumpBase):
    user_id: UUID


class Jump(JumpBase):
    pass
