from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from typing import Union, Literal, Optional
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

class Move(BaseModel):
    command: Literal["move_to"]
    x: float
    y: float
    message: str

class Rotate(BaseModel):
    command: Literal["rotate"]
    angle: float
    direction: Literal["clockwise", "counter-clockwise"]
    message: str

class StartPatrol(BaseModel):
    command: Literal["start_patrol"]
    route_id: Literal["first_floor", "bedrooms", "second_floor"]
    speed: Optional[Literal["slow", "medium", "fast"]] = "medium"
    repeat_count: Optional[Union[Literal[-1], conint(ge=1)]] = 1
    message: str

CommandRequest = Union[Move, Rotate, StartPatrol]

app = FastAPI(title="Robot Validator API", version="1.0")

def normalize_rotate_direction(direction: str) -> str:
    dir_map = {
        "right": "clockwise",
        "cw": "clockwise",
        "left": "counter-clockwise",
        "ccw": "counter-clockwise",
        "clockwise": "clockwise",
        "counterclockwise": "counter-clockwise",
        "counter-clockwise": "counter-clockwise"
    }
    normalized = dir_map.get(direction.lower())
    if not normalized:
        raise ValueError(f"Invalid rotate direction: {direction}")
    return normalized

@app.post("/execute_command")
def execute_command(cmd: CommandRequest):
    """
    Validate and normalize incoming robot command.
    """
    try:
        if isinstance(cmd, Rotate):
            cmd.direction = normalize_rotate_direction(cmd.direction)
        
        logger.info(f"[ROBOT-VALIDATOR-SUCCESS] Validated command: {cmd}")
        return {"status": "success", "command": cmd}
    except Exception as e:
        logger.error(f"[ROBOT-VALIDATOR-ERROR] {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid command: {str(e)}")
