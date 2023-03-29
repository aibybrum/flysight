from typing import List, Dict
from pydantic import BaseModel


class Speed(BaseModel):
    horizontal: Dict[str, List[float]]
    vertical: Dict[str, List[float]]


class Location(BaseModel):
    lat: List[float]
    lon: List[float]


class Distance(BaseModel):
    horizontal: Dict[str, List[float]]
    x_axis: Dict[str, List[float]]
    y_axis: Dict[str, List[float]]


class LandingParams(BaseModel):
    top_of_turn: int
    max_horz_speed: int
    stop: int


class Data(BaseModel):
    params: LandingParams
    time: List[float]
    location: Location
    elevation: List[float]
    distance: Distance
    speed: Speed
    dive_angle: List[float]
    heading: List[float]


class Landing(BaseModel):
    name: str
    data: Data
