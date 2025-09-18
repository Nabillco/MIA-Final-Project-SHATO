# orchestrator/orchestrator.py
from fastapi import FastAPI, UploadFile, File
import requests
import tempfile
import os
import json
from fastapi.responses import JSONResponse, StreamingResponse
import io

app = FastAPI(title="Orchestrator API")

STT_URL = "http://stt-service:8000/stt"
LLM_URL = "http://llm-service:8001/llm"
VALIDATOR_URL = "http://validator-service:8002/execute_command"
TTS_URL = "http://tts-service:8003/speak"

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        tmpfile.write(await file.read())
        audio_path = tmpfile.name

    # 1) STT
    try:
        with open(audio_path, "rb") as f:
            stt_response = requests.post(STT_URL, files={"file": f}, timeout=30)
            stt_response.raise_for_status()
            text = stt_response.json().get("text", "")
    except Exception as e:
        try:
            os.remove(audio_path)
        except:
            pass
        return JSONResponse(content={"error": f"STT failed: {str(e)}"})

    # 2) LLM
    try:
        llm_data = {"instruction": text}
        llm_response = requests.post(LLM_URL, json=llm_data, timeout=30)
        llm_response.raise_for_status()
        llm_output = llm_response.json()
    except Exception as e:
        try:
            os.remove(audio_path)
        except:
            pass
        return JSONResponse(content={"error": f"LLM failed: {str(e)}", "transcribed_text": text})

    # 3) Validator
    message_for_tts = "No valid command"
    validator_result = None
    try:
        validator_payload = {k: llm_output.get(k) for k in ["command", "angle", "direction", "x", "y", "route_id", "speed", "repeat_count", "message"] if k in llm_output}
        validator_response = requests.post(VALIDATOR_URL, json=validator_payload, timeout=15)
        if validator_response.status_code == 200:
            validator_result = validator_response.json()
            if isinstance(validator_result, dict) and validator_result.get("command") and validator_result["command"].get("message"):
                message_for_tts = validator_result["command"]["message"]
            else:
                message_for_tts = llm_output.get("message", "No valid command")
        else:
            message_for_tts = llm_output.get("message", "No valid command")
    except Exception:
        message_for_tts = llm_output.get("message", "No valid command")

    tts_audio_data = None
    try:
        if message_for_tts and message_for_tts != "No valid command":
            tts_payload = {"message": message_for_tts, "lang": "en"}
            tts_response = requests.post(TTS_URL, json=tts_payload, timeout=30)
            tts_response.raise_for_status()
            tts_audio_data = tts_response.content
    except Exception as e:
        print(f"TTS failed: {str(e)}")

    try:
        os.remove(audio_path)
    except:
        pass

    response_data = {
        "transcribed_text": text,
        "llm_output": llm_output,
        "validator_message": message_for_tts,
        "validator_result": validator_result,
        "tts_audio": tts_audio_data.hex() if tts_audio_data else None
    }

    return JSONResponse(content=response_data)