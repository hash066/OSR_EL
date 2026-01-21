import subprocess
import requests
import time
import json
import datetime
import os
import re

# Configuration
BACKEND_URL = "http://localhost:8001/api/ingest"
API_KEY = "SEC_MON_SECRET_KEY_2026"
KERNEL_TAG = "SEC_MON"
LOG_FILE = "../kernel_events.log" # Relative to collector/ dir (assuming run from collector/)

def parse_line(line):
    """
    Parses a dmesg line.
    Expected format examples:
    [  123.456] SEC_MON_PRIV_ESC: PID=123 (bash) changed creds
    """
    if KERNEL_TAG not in line:
        return None

    try:
        match = re.search(r"SEC_MON_(\w+): (.*)", line)
        if not match:
            return None
        
        event_type = match.group(1) 
        details = match.group(2)
        
        pid = 0
        parent_pid = 0
        process_name = "unknown"
        
        pid_match = re.search(r"PID=(\d+)", details)
        if pid_match:
            pid = int(pid_match.group(1))
        
        # Extract parent PID if present
        parent_match = re.search(r"parent[=:]?\s*(\d+)", details, re.IGNORECASE)
        if parent_match:
            parent_pid = int(parent_match.group(1))
            
        proc_match = re.search(r"\(([^)]+)\)", details)
        if proc_match:
            process_name = proc_match.group(1)
        elif "payload" in details:
            process_name = "payload.sh"

        severity = "INFO"
        if "PRIV_ESC" in event_type or "ROOTKIT" in event_type:
            severity = "HIGH"
        elif "HIDDEN" in event_type or "ANOMALY" in event_type or "SYSCALL" in event_type or "NETWORK" in event_type:
            severity = "MEDIUM"

        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "pid": pid,
            "parent_pid": parent_pid,
            "process_name": process_name,
            "severity": severity,
            "type": event_type,
            "details": details
        }
    except Exception as e:
        print(f"Error parsing line: {e}")
        return None

def main():
    print("Starting Kernel SecMon Collector Agent...")
    print(f"Watching Log File: {os.path.abspath(LOG_FILE)} (Fallback to dmesg if missing)")
    
    # File Tailing Mode
    if os.path.exists(LOG_FILE):
        print("Log file found. Tailing...")
        f = open(LOG_FILE, "r")
        f.seek(0, 2) # Go to end
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
                
            event = parse_line(line)
            if event:
                print(f"Forwarding Event: {event['type']}")
                try:
                    requests.post(BACKEND_URL, json=event, params={"api_key": API_KEY})
                except Exception as e:
                    print(f"Failed to push to backend: {e}")
    else:
        print("Log file not found. Falling back to dmesg...")
        cmd = ["dmesg", "-w"]
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except:
            print("dmesg -w failed. Exiting.")
            return

        while True:
            line = process.stdout.readline()
            if not line:
                break
            event = parse_line(line)
            if event:
                requests.post(BACKEND_URL, json=event, params={"api_key": API_KEY})

if __name__ == "__main__":
    main()
