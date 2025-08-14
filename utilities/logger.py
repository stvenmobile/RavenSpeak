# utilities/logger.py

from datetime import datetime

LOG_FILE = "/tmp/ravenspeak.log"

def log(message: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
