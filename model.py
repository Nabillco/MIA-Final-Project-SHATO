from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import json

app = FastAPI()

model_path = r"C:\Users\esraa\Desktop\AI training\MIA-Final-Project-SHATO\models\mistral-7b-instruct-v0.2.Q4_K_M.gguf"

llm = Llama(model_path=model_path, n_ctx=4096)

class instruction(BaseModel):
    instruction : str

#end point
@app.post("/llm")
def generate_text(input : instruction):
  prompt = f"""
You are a command generator. 
Convert the given instruction into a JSON object following the schema below.

Rules:
- Do not output arrays, lists, or multiple objects.
- Do not include explanations, extra text, or labels like "Instruction:" or "Output:".
- Always output exactly ONE valid JSON object with opening {{ and closing }}.
- Every key from the schema must be present.
- If a parameter is missing or cannot be inferred, assign it the JSON literal null (not a string).
- The "message" field must always exist and be the last key.

Schema:
- Move: {{ "command": "move_to", "x": float|null, "y": float|null, "message": str }}
- Rotate: {{ "command": "rotate", "angle": float|null, "direction": "clockwise|counterclockwise|null", "message": str }}
- Start Patrol: {{ "command": "start_patrol", "route_id": "first_floor|bedrooms|second_floor|null", "speed": "slow|medium|fast|null", "repeat_count": -1 or integer >=1|null, "message": str }}

Notes:
- "right" = "clockwise"
- "left" = "counterclockwise"
- Always write null for missing values, not "N/A", "None", "", or "-".
- The "message" field must be a clear, human-friendly sentence suitable for text-to-speech, fully describing the robot's action.

Examples:

Input: Move to x=5, y=10
{{
  "command": "move_to",
  "x": 5,
  "y": 10,
  "message": "Moving to coordinates (5, 10)."
}}

Input: Rotate 90 degrees clockwise
{{
  "command": "rotate",
  "angle": 90,
  "direction": "clockwise",
  "message": "Rotating 90 degrees clockwise."
}}

Input: Start patrol the first floor slowly
{{
  "command": "start_patrol",
  "route_id": "first_floor",
  "speed": "slow",
  "repeat_count": 1,
  "message": "Starting a slow patrol of the first floor."
}}

Now convert this instruction:

Input: {input.instruction}

Output:
"""

  output = llm(prompt, max_tokens=200)
  raw_text = output["choices"][0]["text"]
  parsed = json.loads(raw_text)

  return parsed