#!/usr/bin/env python3
import argparse
import subprocess
import os
import shutil
import sys
import time
from pathlib import Path
import psutil
import json

# Constants for process names
COMPONENTS = {
    "rasa_shell": {
        "cmd": ["rasa", "shell"],
        "cwd": os.getcwd(),
        "ready_signal": "Starting Rasa server on",
    },
    "rasa_actions": {
        "cmd": ["rasa", "run", "actions"],
        "cwd": os.getcwd(),
        "ready_signal": "Action endpoint is up and running",
    },
    "main": {
        "cmd": ["python3", "main.py"],
        "cwd": os.getcwd(),
    }
}

PROCESS_HANDLES = {}
NET_STATS_SNAPSHOT = "/tmp/rscontrol_net_stats.json"


def find_process_by_command(cmd_list):
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')
            if not isinstance(cmdline, list):
                continue
            if all(any(part in segment for segment in cmdline) for part in cmd_list):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None


def wait_until_running(name, timeout=60):
    cmd_list = COMPONENTS[name]['cmd']
    for _ in range(timeout):
        proc = find_process_by_command(cmd_list)
        if proc:
            return proc
        time.sleep(1)
    return None


def wait_for_output_signal(process, signal, timeout=60):
    start_time = time.time()
    while True:
        if process.poll() is not None:
            return False
        line = process.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        try:
            decoded = line.decode("utf-8", errors="replace").strip()
        except Exception:
            continue
        if signal.lower() in decoded.lower():
            return True
        if time.time() - start_time > timeout:
            return False


def start_component(name):
    if name == "rasa_shell":
        if not find_process_by_command(COMPONENTS["rasa_actions"]["cmd"]):
            response = input("⚠️ 'rasa_actions' is not running. Start it now? (y/n): ").strip().lower()
            if response == 'y':
                start_component("rasa_actions")
                time.sleep(2)
                if not find_process_by_command(COMPONENTS["rasa_actions"]["cmd"]):
                    print("❌ rasa_actions failed to start. Aborting rasa_shell startup.")
                    return
            else:
                print("❌ Cannot start 'rasa_shell' without 'rasa_actions' running.")
                return

    if name in COMPONENTS:
        comp = COMPONENTS[name]
        try:
            full_cwd = os.path.abspath(comp["cwd"])
            if not os.path.exists(full_cwd):
                raise FileNotFoundError(f"Working directory does not exist: {full_cwd}")
            print(f"⏳ Starting {name}...")
            process = subprocess.Popen(
                comp["cmd"], cwd=full_cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            PROCESS_HANDLES[name] = process

            success = True
            if "ready_signal" in comp:
                success = wait_for_output_signal(process, comp["ready_signal"], timeout=60)
                if not success:
                    print(f"❌ {name} failed to signal ready state within timeout")

            proc = wait_until_running(name, timeout=60)
            if success and proc:
                print(f"✅ {name} is now running (PID {proc.pid})")
            elif success and not proc:
                print(f"⚠️ {name} may have started, but could not verify PID.")
            else:
                print(f"❌ {name} failed to start correctly.")
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
    else:
        print(f"⚠️ Unknown component: {name}")


def stop_component(name):
    proc = find_process_by_command(COMPONENTS[name]['cmd']) if name in COMPONENTS else None
    if proc:
        try:
            proc.terminate()
            proc.wait(timeout=10)
            print(f"🛑 Stopped {name}")
        except Exception as e:
            print(f"❌ Error stopping {name}: {e}")
    else:
        print(f"⚠️ {name} is not running")


def status_component(name):
    cmd_list = COMPONENTS[name]['cmd'] if name in COMPONENTS else [name]
    proc = find_process_by_command(cmd_list)
    if proc:
        print(f"✅ {name} is running (PID {proc.pid})")
    else:
        print(f"❌ {name} is not running")


def read_cpu_temperature():
    thermal_paths = Path("/sys/class/thermal").glob("thermal_zone*/temp")
    for path in thermal_paths:
        try:
            with open(path) as f:
                temp_millic = int(f.read().strip())
                temp_c = temp_millic / 1000.0
                return f"{temp_c:.1f}°C"
        except Exception:
            continue
    return "Unavailable"


def read_network_delta():
    current = psutil.net_io_counters(pernic=True)
    try:
        with open(NET_STATS_SNAPSHOT, 'r') as f:
            previous = json.load(f)
    except Exception:
        return current, None

    delta = {}
    for iface, stats in current.items():
        if iface in previous:
            delta[iface] = {
                'sent': stats.bytes_sent - previous[iface]['sent'],
                'recv': stats.bytes_recv - previous[iface]['recv']
            }
    return current, delta


def status_hardware():
    mem = psutil.virtual_memory()
    disk = shutil.disk_usage("/")
    load1, load5, load15 = os.getloadavg()
    cpu_temp = read_cpu_temperature()
    current, delta = read_network_delta()

    print("\n📊 Hardware Status:")
    print(f"CPU Load (1/5/15 min): {load1:.2f}, {load5:.2f}, {load15:.2f}")
    print(f"Memory: {mem.percent}% used ({mem.used // (1024 ** 2)} MB / {mem.total // (1024 ** 2)} MB)")
    print(f"Disk: {disk.used // (1024 ** 3)} GB used of {disk.total // (1024 ** 3)} GB")
    print(f"CPU Temp: {cpu_temp}")

    print("\n📶 Network Interfaces:")
    for iface, stats in current.items():
        if delta and iface in delta:
            sent = delta[iface]['sent'] // (1024 ** 2)
            recv = delta[iface]['recv'] // (1024 ** 2)
            print(f"  {iface}: ↑ {sent} MB (last hour), ↓ {recv} MB (last hour)")
        else:
            print(f"  {iface}: sent {stats.bytes_sent // (1024 ** 2)} MB, received {stats.bytes_recv // (1024 ** 2)} MB")
    print()


def help_command(subcmd=None):
    if subcmd == "status":
        print("""
status [component] - Show status of a specific component
    Valid components: rasa_shell, rasa_actions, main, hardware
        """)
    else:
        print("""
Available commands:
    start [component]    - Start the specified RavenSpeak component
    stop [component]     - Stop the specified component
    status [component]   - Show running status (use 'hardware' to show system load)
    help [command]       - Show this help message or help for a command
        """)


def main():
    parser = argparse.ArgumentParser(description="RSControl - RavenSpeak Supervisor")
    parser.add_argument("command", choices=["start", "stop", "status", "help"], help="Action to perform")
    parser.add_argument("component", nargs="?", help="Component name or subcommand")
    args = parser.parse_args()

    if args.command == "start":
        if args.component == "all":
            for name in COMPONENTS:
                start_component(name)
        else:
            start_component(args.component)

    elif args.command == "stop":
        if args.component == "all":
            for name in list(COMPONENTS):
                stop_component(name)
        else:
            stop_component(args.component)

    elif args.command == "status":
        if args.component == "hardware":
            status_hardware()
        elif args.component == "all":
            for name in COMPONENTS:
                status_component(name)
        else:
            status_component(args.component)

    elif args.command == "help":
        help_command(args.component)


if __name__ == "__main__":
    main()
