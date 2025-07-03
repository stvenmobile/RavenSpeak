## RavenSpeak Voice Assistant

RavenSpeak is a modular, privacy-conscious voice assistant system that runs entirely offline. It listens for commands, interprets them using natural language understanding (NLU), responds using locally generated speech, and can route certain requests to an AI backend like Ollama.

---

## 🧠 Architecture Overview

* **Wake Word**: Passive listener for "Raven" using VAD and keyword spotting
* **Speech-to-Text (STT)**: Converts user speech to text
* **NLU**: Uses **Rasa** to detect user intent and extract structured information (slots)
* **Handlers**: Python modules (e.g., `weather_handler.py`) respond to specific intents
* **AI Backend**: Long-form questions or open-ended requests are routed to an LLM (Ollama) with role and model control
* **Text-to-Speech (TTS)**: Piper generates natural-sounding responses

---

## 🔄 Intent and AI Request Flow

### AI Preamble + Structured Capture

RavenSpeak distinguishes AI queries from local tasks using a structured pattern:

#### 🧭 Example Query

```
Raven, I have an AI question. Use GPT-4 as a philosophy professor.
Question start: How does materialism compare to dualism and idealism? Question stop.
```

### 🧠 Rasa Flow

* **Intent**: `ai_request`
* **Slots extracted**:

  * `model`: "GPT-4"
  * `role`: "philosophy professor"
  * `temperature`: optional, from user or `config.py`
* **Behavior**:

  * When `intent == ai_request`, Raven enters *AI input capture mode*
  * On `"question start"`, Raven begins buffering transcription
  * On `"question stop"`, Raven submits the buffered content to the AI backend

If no `question start/stop` is found, Raven sends the entire user utterance to the AI by default.

### 💬 Response Flow

* Raven receives the answer from the AI
* Converts it to speech using Piper
* Speaks the response to the user

---

## 🗃️ Config File: `config.py`

Customize system behavior:

```python
DEFAULT_MODEL = "llama3"
DEFAULT_ROLE = "helpful assistant"
DEFAULT_TEMP = 0.7
OLLAMA_API_URL = "http://192.168.1.50:11435/api/generate"
```

---

## 📁 Directory Layout

```
RavenSpeak/
├── main.py                 # Main entry point
├── config.py              # System defaults
├── handlers/
│   └── weather_handler.py # Local task handler
├── stt/
│   └── mic_listener.py    # Microphone input
├── tts/
│   └── piper_interface.py # Piper TTS integration
├── piper/                 # TTS models and binary
├── rasa/                  # Rasa NLU project (intents, stories)
│   ├── domain.yml
│   ├── data/
│   ├── actions.py
│   ├── config.yml
│   ├── credentials.yml
│   └── endpoints.yml
├── utilities/             # Command-line tools
│   ├── rscontrol          # Supervisor CLI tool to manage RavenSpeak components
│   └── rs_net_snapshot.py # Network data snapshot used by rscontrol status hardware
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

### 2. Install Rasa and tools

```bash
pip install rasa
rasa init --no-prompt
```

### 3. Add your preferred voice model to `piper/`

Download `en_US-amy-medium.onnx` and its JSON config into the `piper/` directory.

---

## 🔁 Running the Assistant


You can control all components using the RSControl utility.
This includes: main.py      - main voice assistant python module (Raven)
               rasa_actions - actions server for Rasa NLP component
               rasa_shell   - CLI for Rasa_NLP component
               all          - all of the above


### Start components:
```bash
./utilities/rscontrol start all|rasa_actions|rasa_shell
```

### Check status:
```bash
./utilities/rscontrol status all|rasa_actions|rasa_shell
```

### Stop components:
```bash
./utilities/rscontrol stop all|rasa_actions|rasa_shell
```

### Check system hardware status:
```bash
./utilities/rscontrol status hardware
```

Includes CPU load, memory usage, disk, CPU temperature, and network bandwidth usage by interface (last hour).


---

## 📦 Future Enhancements

* Add streaming STT
* Memory for AI threads
* Joystick/robot control hooks
* Home Assistant integration

---

## ✨ Credits

Created by @stvenmobile for the RavenSpeak voice assistant project, built on:

* Rasa NLU
* Piper TTS
* Ollama (LLM backend)
* Whisper / Vosk / OpenAI STT engines (modular)
