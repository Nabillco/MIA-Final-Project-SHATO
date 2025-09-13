from faster_whisper import WhisperModel

model = WhisperModel("small.en", device="cuda")

segments, info = model.transcribe("test.wav")
text = "".join([segment.text for segment in segments])
print(text)
