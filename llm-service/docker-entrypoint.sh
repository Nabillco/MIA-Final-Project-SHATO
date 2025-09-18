#!/bin/bash
set -e

MODEL_URL="https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF/resolve/main/llama-3.2-3b-instruct-q4_k_m.gguf"
MODEL_NAME="llama-3.2-3b-instruct-q4_k_m.gguf"
MODEL_PATH="/app/models/${MODEL_NAME}"

echo "Checking for model at ${MODEL_PATH}..."
if [ ! -f "${MODEL_PATH}" ] || [ ! -s "${MODEL_PATH}" ]; then
    echo "Model not found or is empty. Downloading ${MODEL_NAME}..."
    wget -O "${MODEL_PATH}" "${MODEL_URL}"
    echo "Model download complete."
else
    echo "Model found at ${MODEL_PATH}. Skipping download."
fi

# SSH setup
if [ ! -f /etc/ssh/ssh_host_rsa_key ]; then
  ssh-keygen -A
fi
chmod 600 /etc/ssh/ssh_host_*_key
echo "root:$SSH_ROOT_PASSWORD" | chpasswd
/usr/sbin/sshd &

echo "Starting FastAPI application..."
exec uvicorn LLM:app --host 0.0.0.0 --port 8001
