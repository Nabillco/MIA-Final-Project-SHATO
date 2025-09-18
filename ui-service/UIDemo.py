# ui.py
import gradio as gr
import requests
import io
import numpy as np
from scipy.io import wavfile
import tempfile
import base64

ORCHESTRATOR_URL = "http://orchestrator-service:8004/process-audio"

def process_audio(audio_path):
    if audio_path is None:
        return None, "No Recording Found", "No LLM Output", "No Validator Message", None

    try:
        with open(audio_path, "rb") as f:
            response = requests.post(ORCHESTRATOR_URL, files={"file": f})
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        return audio_path, f"Error: {str(e)}", "No LLM Output", "No Validator Message", None

    tts_audio_path = None
    if data.get("tts_audio"):
        try:
            audio_bytes = bytes.fromhex(data["tts_audio"])
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(audio_bytes)
                tts_audio_path = tmp.name
        except Exception as e:
            print(f"Error processing TTS audio: {e}")

    return (
        audio_path,                          
        data.get("transcribed_text", ""),    
        str(data.get("llm_output", "")),     
        data.get("validator_message", ""),  
        tts_audio_path                     
    )

with gr.Blocks() as demo:
    gr.Markdown("## 🎤 SHATO Voice Control Demo")

    with gr.Row():
        audio_input = gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="🎙️ Record or Upload Audio",
        )

    with gr.Row():
        process_button = gr.Button("🚀 Process")
        play_original_button = gr.Button("▶ Play Original")
        play_tts_button = gr.Button("🔊 Play TTS Response")

    with gr.Row():
        audio_output = gr.Audio(label="Original Audio", type="filepath")
        tts_output = gr.Audio(label="TTS Response", type="filepath")
    
    with gr.Row():
        text_output = gr.Textbox(label="Transcribed Text (STT)")
        llm_output_box = gr.Textbox(label="LLM Output (JSON)")
        validator_output_box = gr.Textbox(label="Validator Message")

    process_button.click(
        fn=process_audio,
        inputs=audio_input,
        outputs=[
            audio_output,
            text_output,
            llm_output_box,
            validator_output_box,
            tts_output
        ],
    )

    play_original_button.click(
        fn=lambda path: path if path else None,
        inputs=audio_input,
        outputs=audio_output,
    )

    play_tts_button.click(
        fn=lambda path: path if path else None,
        inputs=tts_output,
        outputs=tts_output,
    )

demo.launch(server_name="0.0.0.0", server_port=7860, )