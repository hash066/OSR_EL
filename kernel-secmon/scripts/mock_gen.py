import requests
import random
import time
import sys

BACKEND_URL = "http://localhost:8000"

EVENTS = [
    {
        "type": "PRIV_ESC",
        "severity": "HIGH",
        "details": "Process changed effective UID from 1000 to 0 without setuid syscall."
    },
    {
        "type": "HIDDEN_PROCESS",
        "severity": "MEDIUM",
        "details": "Hidden process detected by cross-referencing /proc and scheduler."
    },
    {
        "type": "KERNEL_ANOMALY",
        "severity": "MEDIUM",
        "details": "Unexpected modification of syscall table detected."
    },
    {
        "type": "MODULE_LOAD",
        "severity": "INFO",
        "details": "New kernel module loaded: suspicious_mod.ko"
    }
]

PROCESS_NAMES = ["bash", "sh", "python3", "nc", "kworker", "systemd", "malware_v1"]

def generate_event():
    base_event = random.choice(EVENTS)
    pid = random.randint(100, 30000)
    proc = random.choice(PROCESS_NAMES)
    
    event = {
        "timestamp": str(time.time()), # Backend parses this string, ISO preferred but for mock string is fine
        "pid": pid,
        "process_name": proc,
        "severity": base_event["severity"],
        "type": base_event["type"],
        "details": f"{base_event['details']} (Simulated)"
    }
    return event

def main():
    print(f"Starting Mock Event Generator pointing to {BACKEND_URL}")
    while True:
        try:
            delay = random.uniform(1.0, 5.0)
            time.sleep(delay)
            event = generate_event()
            print(f"Sending event: {event['type']}...")
            requests.post(f"{BACKEND_URL}/api/ingest", json=event)
        except Exception as e:
            print(f"Failed to send: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
