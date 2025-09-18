from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import json
import re
import os

app = FastAPI(title="LLM API")

model_path = os.environ.get("MODEL_PATH", "/app/models/llama-3.2-3b-instruct-q4_k_m.gguf")
llm = Llama(model_path=model_path, n_ctx=1024)

class instruction(BaseModel):
    instruction : str

@app.post("/llm")
def generate_text(input : instruction):
  prompt = f"""
You are a command generator. 
Convert the given instruction into a JSON object following the schema below.

STRICT RULES:
- Output ONLY one valid JSON object.
- No explanations, notes, or labels.
- No text before or after the JSON.
- Do NOT wrap output in ```json or any code fences.
- Always include all keys from the schema. 
- If a parameter is missing or cannot be inferred, assign null (literal).
- The "message" key must always be the last key.
- If a parameter is missing or cannot be inferred, assign null (literal).

Schema:
- Move: {{ "command": "move_to", "x": float|null, "y": float|null, "message": str }}
- Rotate: {{ "command": "rotate", "angle": float|null, "direction": "clockwise|counterclockwise|null", "message": str }}
- Start Patrol: {{ "command": "start_patrol", "route_id": "first_floor|bedrooms|second_floor|null if not specified in instruction", "speed": "slow|medium|fast|null", "repeat_count": -1 or integer >=1|null, "message": str }}

Additional mapping rules:
- The "command" value must be exactly one of: "move_to", "rotate", or "start_patrol". Always normalize synonyms like "go", "turn", or "spin" to the correct command.
- The "direction" value must be exactly "clockwise", "counterclockwise", or null. 
- Always normalize synonyms like "right", "cw", "left", or "ccw".
- Do not invent or alter keys. Only use keys from the schema.
- Do not invent new route_id or speed values outside the schema.
- If speed is described as "turtle", "snail", or "very slow" → use "slow".
- If speed is described as "cheetah", "rabbit", "very fast" → use "fast".


Examples:
Input: Move to x=9
{{
  "command": "move_to",
  "x": 9,
  "y": null,
  "message": "Moving forward to coordinates (9, 0)."
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
 
  output = llm(prompt, max_tokens=100)
  raw_text = output["choices"][0]["text"]

  match = re.search(r"\{.*?\}", raw_text, re.DOTALL)
  parsed = json.loads(match.group(0))
  return parsed