# RavenSpeak

**RavenSpeak** is a modular voice assistant designed to run locally or hybrid with remote AI backends. It supports real-time voice interaction through STT (Speech-to-Text), intelligent command routing, and TTS (Text-to-Speech) output.

## 🎯 Project Goals

- ✅ Work fully offline with fallback to Ollama or ChatGPT
- 🎤 Enable live voice input via microphone
- 🧠 Route commands to built-in keyword handlers (e.g. weather)
- 🗣️ Speak responses using natural, local voice synthesis
- 🧩 Modular architecture for easily adding new handlers

## ✨ Features

- Modular command handlers (weather, jokes, quotes)
- Local TTS using [Piper](https://github.com/rhasspy/piper)
- Optional remote AI (Ollama, ChatGPT, Claude)
- Easy configuration using `.env` and `config.py`
- Wake word support (planned)

---

## 🚀 Getting Started

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/ravenspeak.git
   cd ravenspeak
   ```

2. Set up the virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Install system dependencies:

   ```bash
   ./system-setup.sh
   ```

4. Run the assistant:

   ```bash
   python3 main.py
   ```

---

## 🔧 Configuration

Edit `config.py` and `.env` to customize:

- OpenWeather API key (for weather handler)
- Ollama or ChatGPT endpoint (optional)
- Default city for weather
- Voice model path (if changed)

---

## 🧩 Handlers

### 📡 Weather Handler

Uses OpenWeather One Call API 3.0 to provide:

- 🌤 Current weather – 1-hour snapshot
- 🕓 Hourly forecast – 48-hour (returns next 3 hours)
- 📅 Daily forecast – 8-day (returns next 3 days)

Users can set a default city or ask about any supported location (e.g. "weather in Seattle").

---

## 🔊 Text-to-Speech (TTS) with Piper

RavenSpeak uses [Piper TTS](https://github.com/rhasspy/piper) to generate high-quality, local speech responses.

### ✅ Voice Model

We use the `en_US-amy-medium` model, a single-speaker voice that:

- Does not require `--speaker`
- Runs efficiently on CPUs without GPU
- Sounds clear and natural

### 🎤 How It Works

Text is sent to Piper via stdin. The response is written to a `.wav` file and played using `aplay`.

### 🧪 Manual Test

```bash
echo "Raven is online." | ./piper/piper \
  --model ./piper/en_US-amy-medium.onnx \
  --output_file test.wav

aplay test.wav
```

---

## 🎙️ Full Voice Flow

Once configured, RavenSpeak:

1. Listens for wake words (future)
2. Records and transcribes microphone input
3. Routes text to handler or AI
4. Speaks the reply using Piper

---

## 📄 License

MIT License. 

