#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import signal
import psutil
import webrtcvad
import collections
import numpy as np
import sounddevice as sd
import queue
from faster_whisper import WhisperModel
from datetime import datetime

LOG_FILE = "/tmp/ravenspeak.log"

model = WhisperModel("base.en", compute_type="int8")
vad = webrtcvad.Vad(2)  # 0–3, more aggressive = more filtering
q = queue.Queue()

FRAME_DURATION_MS = 30  # ms
SAMPLE_RATE = 16000
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)
NUM_FRAMES = int(5000 / FRAME_DURATION_MS)  # 5 seconds total

RingBuffer = collections.deque


def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    print(full_message)
    with open(LOG_FILE, "a") as f:
        f.write(full_message + "\n")


def audio_callback(indata, frames, time_info, status):
    q.put(indata.copy())


def frame_generator():
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16', callback=audio_callback):
        ring_buffer = RingBuffer(maxlen=NUM_FRAMES)
        log("🎙️ Listening...")

        while True:
            frame = q.get()
            if frame.shape[0] < FRAME_SIZE:
                continue
            frame = frame[:FRAME_SIZE]
            is_speech = vad.is_speech(frame.tobytes(), SAMPLE_RATE)
            ring_buffer.append((frame, is_speech))

            if sum(1 for _, speech in ring_buffer if speech) > NUM_FRAMES * 0.6:
                audio = np.concatenate([f for f, _ in ring_buffer])
                return audio


def listen_for_command():
    audio = frame_generator()
    audio = np.squeeze(audio)
    log("🧠 Transcribing...")
    segments, _ = model.transcribe(audio, language="en")
    return " ".join(segment.text for segment in segments)


if __name__ == "__main__":
    text = listen_for_command()
    print("🗣️ You said:", text)
