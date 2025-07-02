import subprocess

PIPER_BINARY = "./piper/piper"
VOICE_MODEL = "./piper/en_US-amy-medium.onnx"
OUTPUT_FILE = "response.wav"

def speak(text):
    print(f"[🗣️ RavenSpeak] {text}")
    try:
        # Pass text via stdin, just like echo | ./piper ...
        piper_proc = subprocess.Popen(
            [PIPER_BINARY, "--model", VOICE_MODEL, "--output_file", OUTPUT_FILE],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        piper_proc.communicate(input=text.encode("utf-8"), timeout=10)

        # Play the result
        subprocess.run(["aplay", OUTPUT_FILE], check=True)
    except subprocess.TimeoutExpired:
        piper_proc.kill()
        print("[ERROR] Piper timed out.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] aplay failed: {e}")
