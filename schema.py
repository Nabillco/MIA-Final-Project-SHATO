from pydantic import BaseModel, conint 
from typing import Union, Literal, Optional


class Move(BaseModel):
    command : Literal["move_to"]
    x : float
    y : float
    message : str

class Rotate(BaseModel):
    command : Literal["rotate"]
    angle : float
    direction : Literal["clockwise", "counterclockwise"]
    message : str

class Startpatrol(BaseModel):
    command :Literal["start_patrol"]
    route_id : Literal["first_floor", "bedrooms", "second_floor"]
    speed : Optional[Literal["slow", "medium", "fast"]] = "medium"
    repeat_count : Optional[Union[Literal[-1], conint(ge=1)]] = 1
    message : str

CommandResponse = Union[Move, Rotate, Startpatrol]