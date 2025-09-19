# 🤖 SHATO: MIA Final Project

**SHATO** is a modular, containerized pipeline that enables speech-based interactions, using multiple services including speech-to-text, a large language model (LLM), validation of outputs, text-to-speech, and a user interface. This README describes the project structure, how to set it up, and how the parts interact.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Services](#services)
4. [project Structure](#project-structure)
5. [Requirements](#requirements)
6. [Setup & Run](#setup--run)
7. [Usage](#usage)
8. [Design Decisions](#design-decisions)
---

## Overview

SHATO is intended to process spoken input, convert it to text, feed the text into a language model to formulate structured commands or responses, validate those responses, convert them back to speech, and deliver them via a simple UI. The goal is reliability, clarity in output (e.g. valid JSON for robot control or structured outcomes), and modularity so different components can be replaced or tuned independently.

---

## Architecture

Below is a high-level view of how the system works:

```
[ User / UI ] → [ Orchestrator ] → { STT → LLM → Validator → TTS } → [ UI / Robot / Output ]
```

* 💻**UI-Service**: Interface for user input/output (likely via web).
* 🎙 **STT-Service**: Converts speech to text.
* 🧠**LLM-Service**: Processes textual instruction via a quantized language model, produces structured text (JSON).
* ✅**Validator-Service**: Checks the output of LLM for correctness / format (e.g., JSON, schema).
* 🔊**TTS-Service**: Converts validated responses to speech.
* 💻 **Orchestrator-Service**: Coordinates the flow among the services.

All services are containerized, and run together via Docker Compose. Each listens on its own port. Volumes are used for shared data where needed (e.g. model files).

---

## Services

Here’s what each service does, roughly:

| Service                | Main Role                                                                                                                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `llm-service`          | Hosts a quantized language model (e.g. LLaMA-3 3B instruct, GGUF Q4) using `llama.cpp` + FastAPI. Takes text input → outputs structured JSON. |
| `stt-service`          | Speech-to-text (turning audio into text).                                                                                                     |
| `validator-service`    | Validates LLM outputs (ensures they follow expected format / schema).                                                                         |
| `tts-service`          | Turns text responses into speech audio.                                                                                                       |
| `orchestrator-service` | Manages the entire flow: accepts requests, routes them through the services, collates responses.                                              |
| `ui-service`           | Front-end interface (likely web) for users to interact with the system.                                                                       |

---

## 📂 Project Structure
├── docker-compose.yml
├── llm-service/
│ ├── Dockerfile
│ ├── LLM.py
│ ├── requirements.txt
│ ├── docker-entrypoint.sh
│ └── models/
├── orchestrator/
│ ├── Dockerfile
│ ├── orchestrator.py
│ └── requirements.txt
├── robot-validator/
│ ├── Dockerfile
│ ├── validator.py
│ └── requirements.txt
├── stt-service/
│ ├── Dockerfile
│ ├── STT_Server.py
│ └── requirements.txt
├── tts-service/
│ ├── Dockerfile
│ ├── TTS.py
│ └── requirements.txt
└── ui-service/
├── Dockerfile
├── UIDemo.py
└── requirements.txt

```markdown
- **llm-service/** → Runs LLaMA-3 inference (llama.cpp + FastAPI).  
- **orchestrator/** → Coordinates between all services.  
- **robot-validator/** → Validates JSON commands (FastAPI + rule-based).  
- **stt-service/** → Speech-to-text (Whisper + FastAPI).  
- **tts-service/** → Text-to-speech (Coqui TTS / pyttsx3 + FastAPI).  
- **ui-service/** → User interface (Gradio).  
```
--- 

## Requirements

To run everything, you’ll need:

* Docker & Docker Compose installed on your machine.
* Enough disk space for the model(s).
* A system with some CPU performance (for running quantized LLM + speech components).

Optional:

* GPU if you plan to use it, but current setup appears CPU-oriented.
* Internet access (for pulling container images, downloading models, etc.).

---

## Setup & Run

1. Clone this repository:

   ```bash
   git clone https://github.com/Nabillco/MIA-Final-Project-SHATO.git
   cd MIA-Final-Project-SHATO
   ```

2. Build and start all services with Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. Wait for all containers to start. Key ports:

   * `llm-service`: port **8001** (FastAPI)
   * `ui-service`: port **7860** (UI)
   * Other services work internally via orchestrator or exposed ports (e.g. STT on 8000, Validator on 8002, TTS on 8003, etc.)

4. Visit the UI in your browser:

   ```
   http://localhost:7860
   ```

5. Make sure the `models` folder is populated (for `llm-service`). If not, the `docker-entrypoint.sh` script in `llm-service` will download the model automatically.

---

## Usage

* Interact via UI: speak or type an instruction.
* The system will convert speech → text (if voice input), feed text to LLM, validate the output, possibly convert to speech, and respond.
* For robotics or structured command-type use, ensure that the LLM’s JSON output adheres to expected schema so the validator passes, and downstream systems can consume it reliably.

---

## Design Decisions

Some of the key rationales:

* **Model choice**: A quantized LLaMA model (GGUF Q4) was chosen for a balance between reasoning/capability and resource efficiency.
* **Dockerized pipeline**: Each service is containerized to isolate concerns, simplify development/deployment, and make replacement easier.
* **Prompt engineering & validation**: To reduce hallucinations, ensure consistency, and make JSON output reliable, the system uses prompt engineering and a validator service.
* **SSH debugging in LLM service**: To allow developers to access the LLM container for troubleshooting without rebuilding image each time.

---
