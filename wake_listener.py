import sounddevice as sd
import numpy as np
from openwakeword.model import Model

# Settings
wake_word = "alexa"
SAMPLE_RATE = 16000
BLOCK_DURATION = 0.5  # seconds
BLOCK_SIZE = int(SAMPLE_RATE * BLOCK_DURATION)

# Load model
model = Model(wakeword_models=[wake_word])

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio stream status: {status}")
    audio_data = indata[:, 0]

    # Ignore non-speech input
    if not model.vad_model.is_speech(audio_data, SAMPLE_RATE):
        return

    # Get wake word prediction probabilities
    probs = model.get_probs(audio_data)
    confidence = probs.get(wake_word, 0)

    if confidence > 0.6:
        print(f"🔊 Wake word '{wake_word}' detected with confidence {confidence:.2f}")


# Main loop
def main():
    print(f"🎤 Listening for wake word: '{wake_word}'")
    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, callback=audio_callback):
        try:
            while True:
                sd.sleep(1000)  # sleep in 1-second intervals to keep stream alive
        except KeyboardInterrupt:
            print("🛑 Wake listener stopped.")

if __name__ == "__main__":
    main()
