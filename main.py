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

class Startpatrol(BaseModel):
    command: Literal["start_patrol"]
    route_id: Literal["first_floor", "bedrooms", "second_floor"]
    speed: Optional[Literal["slow", "medium", "fast"]] = "medium"
    repeat_count: Optional[Union[Literal[-1], conint(ge=1)]] = 1
    message: str

# Accepts any of the three
CommandRequest = Union[Move, Rotate, Startpatrol]


app = FastAPI(title="Robot Validator API", version="1.0")

@app.post("/execute_command")
def execute_command(cmd: CommandRequest):
    """
    Validate incoming robot command against schema.
    """
    try:
        # If schema validation passes, it's automatically valid
        logger.info(f"[ROBOT-VALIDATOR-SUCCESS] Validated command: {cmd}")
        return {"status": "success", "command": cmd}
    except Exception as e:
        logger.error(f"[ROBOT-VALIDATOR-ERROR] {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid command format")
