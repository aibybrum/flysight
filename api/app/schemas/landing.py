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


class Data(BaseModel):
    time: List[float]
    location: Location
    elevation: List[float]
    distance: Distance
    speed: Speed
    dive_angle: List[float]
    heading: List[float]


class Features(BaseModel):
    max_horz_speed: int
    max_vert_speed: int
    stop: int
    rollout: int


class Landing(BaseModel):
    name: str
    features: Features
    data: Data
