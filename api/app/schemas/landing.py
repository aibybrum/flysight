from typing import List
from uuid import UUID
from pydantic import BaseModel


class Data(BaseModel):
    top_of_turn: int
    max_horz_speed: int
    stop: int
    dataframe: List[dict]


class Landing(BaseModel):
    id: UUID
    name: str
    user_id: UUID
    data: Data
