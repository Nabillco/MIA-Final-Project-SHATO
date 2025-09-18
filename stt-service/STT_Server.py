from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel

model = WhisperModel("small.en", device="cpu")
app = FastAPI(title="Speech-to-Text API")

def transcribe_audio(file_path: str) -> str:
    segments, _ = model.transcribe(file_path)
    return "".join([s.text for s in segments])

@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    text = transcribe_audio(temp_path)
    return {"text": text}
