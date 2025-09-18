FROM python:3.10

RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

RUN pip install --no-cache-dir torch==2.3.0+cpu torchaudio==2.3.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

RUN pip install --upgrade faster-whisper ctranslate2

COPY . .

CMD ["uvicorn", "STT_Server:app", "--host", "0.0.0.0", "--port", "8000"]
