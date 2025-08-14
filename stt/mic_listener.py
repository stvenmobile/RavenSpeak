# stt/mic_listener.py

import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from utilities.logger import log

SAMPLE_RATE = 16000
DURATION = 5  # seconds

model = WhisperModel("base.en", compute_type="int8")

def listen_for_command():
    log("🎙️ Listening...")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32') as stream:
        frames = []
        for _ in range(int(SAMPLE_RATE * DURATION / 1024)):
            data, _ = stream.read(1024)
            frames.append(data)

    audio = np.concatenate(frames, axis=0)
    audio = np.squeeze(audio)

    log("🧠 Transcribing...")
    segments, _ = model.transcribe(audio, language="en")
    result = " ".join(segment.text for segment in segments)
    log(f"🗣️ Transcribed: {result}")
    return result
