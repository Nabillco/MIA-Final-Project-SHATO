from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import json
import re

app = FastAPI()

model_path = r"C:\Users\esraa\Desktop\AI training\MIA-Final-Project-SHATO\llama-3.2-3b-instruct-q4_k_m.gguf"

llm = Llama(model_path=model_path, n_ctx=1024,n_batch=512 , n_threads=16, n_gpu_layers=32)

class instruction(BaseModel):
    instruction : str

#end point
@app.post("/llm")
def generate_text(input : instruction):
  prompt = f"""
You are a command generator. 
Convert the given instruction into a JSON object following the schema below.

STRICT RULES:
- Output ONLY one valid JSON object.
- No explanations, notes, or labels.
- No text before or after the JSON.
- Always include all keys from the schema.
- If a parameter is missing or cannot be inferred, assign null (literal).
- The "message" key must always be the last key.
-Do NOT wrap output in ```json or any code fences.
-Do Not add any notes 

Schema:
- Move: {{ "command": "move_to", "x": float|null, "y": float|null, "message": str }}
- Rotate: {{ "command": "rotate", "angle": float|null, "direction": "clockwise|counterclockwise|null", "message": str }}
- Start Patrol: {{ "command": "start_patrol", "route_id": "first_floor|bedrooms|second_floor|null", "speed": "slow|medium|fast|null", "repeat_count": -1 or integer >=1|null, "message": str }}

- The "command" value must be exactly one of: "move_to", "rotate", or "start_patrol". Never use synonyms like "go", "turn", or "spin".
- The "direction" value must be exactly "clockwise", "counterclockwise", or null. Never use "left", "right", "cw", or "ccw".
- Always normalize synonyms:
  - "turn", "spin" → "rotate"
  - "right" → "clockwise"
  - "left" → "counterclockwise"
- Do not invent or alter keys. Only use keys from the schema.

Additional mapping rules:
- If speed is described as "turtle", "snail", or "very slow" → use "slow".
- If speed is described as "cheetah", "rabbit", "very fast" → use "fast".
- Never invent new route_id or speed values outside the schema.

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
 
  output = llm(prompt, max_tokens=200, temperature=0.0, top_p=1.0)
  raw_text = output["choices"][0]["text"]

  match = re.search(r"\{.*?\}", raw_text, re.DOTALL)
  if not match:
        raise ValueError(f"No JSON found in output: {raw_text}")

  try:
        parsed = json.loads(match.group(0))
  except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}\nRaw: {raw_text}")

  return parsed
