# RavenSpeak

**RavenSpeak** is a modular, privacy-first voice assistant that runs locally with optional AI integration. It supports real-time voice interaction using microphone input, speech-to-text transcription, intelligent command routing (via Snips NLU), and text-to-speech output using Piper.

---

## 🎯 Project Goals

- ✅ Run fully offline on local hardware
- ✅ Support fallback to AI backends (Ollama, ChatGPT)
- 🎤 Accept real-time voice input
- 🧠 Understand user intent via structured NLP
- 🗣️ Speak responses clearly using local TTS
- 🧩 Be modular, hackable, and fun to extend

---

## 🧠 Intent Recognition with Snips NLU

RavenSpeak uses [Snips NLU](https://github.com/snipsco/snips-nlu) to extract intent and parameters from user speech.

- 🌱 Intents are defined using sample utterances
- 🧠 Slots/entities (e.g., city names) can be extracted
- ⚡ Fast and lightweight, runs entirely offline
- 🔌 Routes user input to the appropriate handler (weather, joke, etc.)
- 🤖 Future fallback: if Snips cannot match, text may be passed to an AI model

> Example: “What’s the weather in Boston today?” → `get_weather` with `{location: boston}`

---

## 🔊 Text-to-Speech (TTS) with Piper

RavenSpeak uses [Piper TTS](https://github.com/rhasspy/piper) to generate natural-sounding, offline speech.

- Uses `en_US-amy-medium` voice model (single-speaker, no speaker ID needed)
- Converts text → `.wav` → audio playback via `aplay`

### 🧪 Manual TTS Test

```bash
echo "Raven is online." | ./piper/piper \
  --model ./piper/en_US-amy-medium.onnx \
  --output_file test.wav

aplay test.wav

🎙️ Full Voice Interaction Flow

    User speaks (mic input via PyAudio)

    STT transcribes voice to text

    Snips NLU parses intent and parameters

    Raven routes to correct handler (get_weather, etc.)

    Text response is synthesized by Piper and played

🧩 Modular Handlers

Each function (weather, jokes, quotes, etc.) is implemented as a handler module. Raven uses intent-to-handler mapping to dispatch requests.
📡 Weather Handler

Uses OpenWeather One Call API 3.0 to provide:

    🌤 Current weather – 1-hour snapshot

    🕓 Hourly forecast – next 3 hours

    📅 Daily forecast – next 3 days

Works with specific city/state/country or a default fallback.
🧰 Getting Started
1. Clone the repository

git clone https://github.com/yourusername/ravenspeak.git
cd ravenspeak

2. Set up Python virtual environment

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3. Install system dependencies

./system-setup.sh

4. Run RavenSpeak

python3 main.py

🔧 Configuration

Edit config.py and .env to control:

    OpenWeather API key

    Default city, state, and country

    Piper model location

    Optional AI endpoint (Ollama or OpenAI)

🐚 Controlling ALSA Output

To suppress noisy ALSA error messages:

python3 main.py 2>/dev/null

📦 Planned Enhancements

    Wake word detection

    AI fallback via LLM (Ollama)

    More handler types (Home Assistant, system commands, reminders, etc.)

    Whisper-based offline STT

📄 License

MIT License.
