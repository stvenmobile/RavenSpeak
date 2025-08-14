#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import signal
import psutil
import re
from datetime import datetime

LOG_FILE = "/tmp/ravenspeak.log"

COMPONENTS = {
    "rasa_actions": {
        "cmd": ["rasa", "run", "actions"],
        "port": 5055,
        "ready_signal": "Action endpoint is up and running"
    },
    "rasa_shell": {
        "cmd": ["rasa", "shell", "--port", "5005", "--enable-api"],
        "port": 5005,
        "ready_signal": "Rasa server is up and running."
    },
    "main": {
        "cmd": ["python3", "main.py"],
        "port": None,
        "ready_signal": "Raven is listening..."
    }
}

READY_TIMEOUT = 45  # seconds

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    print(full_message)
    with open(LOG_FILE, "a") as f:
        f.write(full_message + "\n")

def stop_process_on_port(port):
    for proc in psutil.process_iter(attrs=['pid']):
        try:
            conns = proc.net_connections(kind='inet')
            for conn in conns:
                if conn.laddr.port == port:
                    log(f"Killing process {proc.pid} bound to port {port}")
                    proc.kill()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

def is_component_running(name):
    for proc in psutil.process_iter(attrs=['pid', 'cmdline']):
        try:
            if all(token in ' '.join(proc.info['cmdline']) for token in COMPONENTS[name]["cmd"]):
                return proc.info['pid']
        except (psutil.AccessDenied, psutil.NoSuchProcess, TypeError):
            continue
    return None

def start_component(name):
    pid = is_component_running(name)
    if pid:
        log(f"✅ {name} is already running (PID {pid})")
        return True

    log(f"Starting {name}...")
    logfile = open(LOG_FILE, "a")
    proc = subprocess.Popen(COMPONENTS[name]["cmd"], stdout=logfile, stderr=logfile)

    start_time = time.time()
    while time.time() - start_time < READY_TIMEOUT:
        with open(LOG_FILE) as f:
            lines = f.readlines()[-50:]
            if any(COMPONENTS[name]["ready_signal"] in line for line in lines):
                new_pid = is_component_running(name)
                log(f"✅ {name} is now running (PID {new_pid})")
                return True
        time.sleep(1)

    log(f"❌ {name} failed to start within timeout")
    return False

def stop_component(name):
    pid = is_component_running(name)
    if not pid:
        log(f"❌ {name} is not running")
    else:
        log(f"Stopping {name} (PID {pid})")
        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)
        except Exception as e:
            log(f"❌ Failed to stop {name}: {e}")

    if COMPONENTS[name]["port"]:
        stop_process_on_port(COMPONENTS[name]["port"])

    log(f"✅ {name} has been terminated successfully")

def start_all():
    log("🧠 Starting Raven Voice Assistant...")
    success = True
    for name in COMPONENTS:
        if not start_component(name):
            success = False
            break
    if success:
        log("✅ Raven is fully operational.")
    else:
        log("❌ Raven failed to start completely.")

def stop_all():
    log("🛑 Stopping Raven Voice Assistant...")
    for name in COMPONENTS:
        stop_component(name)

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ["start", "stop"] or sys.argv[2] != "raven":
        print("Usage: rscontrol [start|stop] raven")
        sys.exit(1)

    action = sys.argv[1]

    if action == "start":
        with open(LOG_FILE, "w") as f:
            f.write(f"=== RavenSpeak Log Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        start_all()
    elif action == "stop":
        stop_all()

if __name__ == "__main__":
    main()
