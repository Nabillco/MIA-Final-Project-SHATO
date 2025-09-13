from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io
from gtts import gTTS

app = FastAPI()

class SpeakRequest(BaseModel):
    text: str
    lang: str = "en"

@app.post("/speak")
async def speak(req: SpeakRequest):
    tts = gTTS(text=req.text, lang=req.lang)
    
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="audio/mpeg")