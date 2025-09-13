from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io
from typing import Optional
from gtts import gTTS

app = FastAPI()

class CommandRequest(BaseModel):
    message: Optional[str] = None
    text: Optional[str] = None
    lang: str = "en"

def get_text(req: CommandRequest) -> str:
    return req.message or req.text or ""

@app.post("/speak")
async def speak(req: CommandRequest):
    speech_text = get_text(req)

    if not speech_text:
        return {"error": "You must provide either 'message' or 'text'."}

    tts = gTTS(text=speech_text, lang=req.lang)

    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer, 
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=speech.mp3"}
    )
