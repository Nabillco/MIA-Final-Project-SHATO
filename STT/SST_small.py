import whisper
import soundfile as sf
import whisper
import torch
import librosa
import numpy as np
MODEL_PATH = "model/small.en.pt"
AUDIO_FILE = "test.wav"

model = whisper.load_model(MODEL_PATH)
# Load WAV file
audio_file = "test.wav"
audio, sr = sf.read(audio_file, dtype="float32")

# Convert stereo to mono if needed
if len(audio.shape) > 1:
    audio = np.mean(audio, axis=1)

# Resample to 16kHz if needed
if sr != 16000:
    import librosa
    audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

# Transcribe from numpy array directly
result = model.transcribe(audio, fp16=False, language="en")
print("Transcription:", result["text"])