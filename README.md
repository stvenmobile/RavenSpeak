## RavenSpeak Voice Assistant

RavenSpeak is a modular, privacy-conscious voice assistant system that runs entirely offline. It listens for commands, interprets them using natural language understanding (NLU), responds using locally generated speech, and can route certain requests to an AI backend like Ollama.

---

## 🧐 Architecture Overview

* **Wake Word** *(optional)*: Detects activation phrase (e.g., "Alexa")
* **Speech-to-Text (STT)**: Converts user speech to text
* **NLU**: Uses **Rasa** to detect user intent and extract structured information (slots)
* **Handlers**: Python modules (e.g., `weather_handler.py`) respond to specific intents
* **AI Backend**: Long-form or complex requests are routed to an LLM like Ollama
* **Text-to-Speech (TTS)**: Piper generates natural-sounding speech

---

## 🔄 Intent and AI Request Flow

### AI Preamble + Structured Capture

RavenSpeak distinguishes AI queries from local tasks using a structured pattern:

#### 🗭 Example Query
```text
Raven, I have an AI question. Use GPT-4 as a philosophy professor.
Question start: How does materialism compare to dualism and idealism? Question stop.
```

### 🧠 Rasa Flow

* **Intent**: `ai_request`
* **Slots extracted**:
  * `model`: e.g., "GPT-4"
  * `role`: e.g., "philosophy professor"
  * `temperature`: optional
* **Behavior**:
  * On `question start`, Raven buffers transcript
  * On `question stop`, Raven sends text to Ollama

If `question start/stop` is not used, the full utterance is sent.

### 💬 Response Flow

* AI responds via Ollama
* Text is converted to speech via Piper
* Response is spoken aloud to user

---

## 📃 Config File: `config.py`

Configure system defaults:
```python
DEFAULT_MODEL = "llama3"
DEFAULT_ROLE = "helpful assistant"
DEFAULT_TEMP = 0.7
OLLAMA_API_URL = "http://192.168.1.60:11435/api/generate"
```

---

## 📁 Directory Layout

```
RavenSpeak/
├── main.py                 # Main assistant logic
├── config.py              # System configuration
├── handlers/              # Intent handlers
│   └── weather_handler.py
├── stt/                   # Microphone and STT components
│   └── mic_listener.py
├── tts/                   # Piper integration
│   └── piper_interface.py
├── piper/                 # Piper model and binary
├── rasa/                  # Rasa configuration
│   ├── domain.yml
│   ├── data/
│   ├── actions.py
│   ├── config.yml
│   ├── credentials.yml
│   └── endpoints.yml
├── utilities/             # Command-line tools
│   ├── rscontrol          # Supervisor CLI
│   └── rs_net_snapshot.py # Hourly network usage snapshot
└── .venv/                 # Python virtual environment
```

---

## ✅ Setup Instructions

### 1. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Rasa
```bash
pip install rasa
rasa init --no-prompt
```

### 3. Add Piper voice model
Place `en_US-amy-medium.onnx` and config JSON into `piper/`

---

## 🔁 Running the Assistant

Use the `rscontrol` utility:

### Start all components:
```bash
./utilities/rscontrol start raven
```

### Check status:
```bash
./utilities/rscontrol status raven
```

### Stop all components:
```bash
./utilities/rscontrol stop raven
```

### Restart all components:
```bash
./utilities/rscontrol restart raven
```

### View hardware/system status:
```bash
./utilities/rscontrol status hardware
```
Includes CPU load, memory, disk, temperature, and last-hour network usage.

---

## 📆 Special Features

* Sleep Mode: Say "Raven, go to sleep" to suspend interaction
* Wake Up: Say "Raven, wake up" to resume interaction
* Ignored speech during sleep mode

---

## 📦 Future Enhancements

* Streaming STT
* Home Assistant integration
* Local RAG retrieval augmentation
* Multilingual support

---

## ✨ Credits

Created by @stvenmobile. Built with:

* Rasa NLU
* Piper TTS
* Ollama for local LLM inference
* Whisper/Vosk for STT (modular backend)
