FROM python:3.11.9-bullseye

WORKDIR /app

COPY requirements.txt .
COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libopenblas-dev \
    libssl-dev \
    libffi-dev \
    wget \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip --default-timeout=2000 install --no-cache-dir llama-cpp-python

RUN pip --default-timeout=2000 install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/app/docker-entrypoint.sh"]
