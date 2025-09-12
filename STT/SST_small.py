import torch
import whisper
import os
import soundfile as sf
import librosa
import numpy as np


loaded_model = whisper.load_model("tiny.en")  

#Transcribe a WAV file
audio_file = "test.wav"
audio, sr = sf.read(audio_file, dtype="float32")

# Convert stereo to mono if needed
if len(audio.shape) > 1:
    audio = np.mean(audio, axis=1)

# Resample to 16kHz if needed
if sr != 16000:
    audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

# Transcribe
result = loaded_model.transcribe(audio, fp16=False, language="en")
print("Transcription:", result["text"])
