import time
import os
import sys
import random

# Log file that the Collector Agent will watch
LOG_FILE = "../kernel_events.log"

def log_kernel_event(event_type, details):
    timestamp = time.time()
    # Format similar to dmesg, prefixed with SEC_MON
    log_line = f"[{timestamp:.6f}] SEC_MON_{event_type}: {details}\n"
    
    print(f"[ATTACK] Writing to kernel log: {event_type}")
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

def phase_1_infiltration():
    print("\n--- PHASE 1: INFILTRATION ---")
    print("Simulating drop of malicious script...")
    time.sleep(1)
    
    # Actually create a file to make it "real"
    with open("suspicious_payload.sh", "w") as f:
        f.write("#!/bin/bash\n# Malicious payload\necho 'Hacking...'\n")
    
    log_kernel_event("HIDDEN_PROC", "Found hidden process PID=8822 (payload.sh) parent=bash")
    time.sleep(2)
    log_kernel_event("FILE_SCAN", "Suspicious file created: ./suspicious_payload.sh")

def phase_2_priv_esc():
    print("\n--- PHASE 2: PRIVILEGE ESCALATION ---")
    time.sleep(2)
    log_kernel_event("PRIV_ESC", "PID=8822 (payload.sh) changed effective UID: 1000 -> 0 (ROOT)")
    log_kernel_event("ANOMALY", "Unexpected credential change detected in task_struct")

def phase_3_persistence():
    print("\n--- PHASE 3: PERSISTENCE (ROOTKIT) ---")
    time.sleep(2)
    log_kernel_event("MODULE_LOAD", "Kernel module 'rootkit_v1.ko' loaded (unsigned)")
    log_kernel_event("SYSCALL_HOOK", "Syscall table modified: sys_read -> 0xffffffffc028a000")

def main():
    print("Initializing Red Team Attack Simulation...")
    print(f"Targeting Log: {os.path.abspath(LOG_FILE)}")
    
    # Ensure log file exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write(f"[{time.time():.6f}] Kernel Monitor Initialized.\n")

    print("Waiting 3 seconds before starting attack vector...")
    time.sleep(3)
    
    phase_1_infiltration()
    time.sleep(3)
    phase_2_priv_esc()
    time.sleep(3)
    phase_3_persistence()

    print("\n--- ATTACK SIMULATION COMPLETE ---")
    print("Check the dashboard for alerts!")

if __name__ == "__main__":
    main()
