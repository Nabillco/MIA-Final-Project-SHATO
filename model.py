from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

model_path = r"C:\Users\esraa\Desktop\AI training\MIA-Final-Project-SHATO\models\mistral-7b-instruct-v0.2.Q4_K_M.gguf"

llm = Llama(model_path=model_path)

class instruction(BaseModel):
    instruction : str

#end point
@app.post("/llm")
def generate_text(input : instruction):
    prompt = f"""
You are a command generator. 
Convert the given instruction into a JSON object following the schema below.

Do not output arrays, lists, or multiple objects.
Do not include explanations, extra text, or labels like "Instruction:" or "Output:".
Respond with ONLY one valid JSON object.
Always produce a single valid JSON object with opening and closing.
Do not stop until the JSON is complete.

Important: 
The "message" field must be a **clear, human-friendly sentence** suitable for text-to-speech. 
It should fully describe what the robot is doing.

Schema:
- Move: {{ "command": "move_to", "x": float, "y": float, "message": str }}
- Rotate: {{ "command": "rotate", "angle": float, "direction": "clockwise|counterclockwise", "message": str }}
- Start Patrol: {{ "command": "start_patrol", "route_id": "first_floor|bedrooms|second_floor", "speed": "slow|medium|fast", "repeat_count": -1 or integer >=1, "message": str }}

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
    output = llm(prompt, max_tokens=300)
    raw_text = output["choices"][0]["text"]

    return {raw_text}