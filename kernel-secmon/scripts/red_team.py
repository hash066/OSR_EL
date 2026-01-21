import time
import os
import sys
import random

# Log file that the Collector Agent will watch
LOG_FILE = "../kernel_events.log"

# Sample malicious IPs for threat intelligence testing
MALICIOUS_IPS = [
    "185.220.101.41",  # Known Tor exit node
    "45.142.212.61",   # Known malicious
    "89.248.165.181",  # Known scanner
]

NORMAL_IPS = [
    "8.8.8.8",         # Google DNS
    "1.1.1.1",         # Cloudflare DNS
]

def log_kernel_event(event_type, details, pid=None, parent_pid=None):
    timestamp = time.time()
    # Format similar to dmesg, prefixed with SEC_MON
    log_line = f"[{timestamp:.6f}] SEC_MON_{event_type}: {details}\n"
    
    print(f"[ATTACK] Writing to kernel log: {event_type} (PID={pid})")
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

def phase_1_infiltration():
    print("\n--- PHASE 1: INFILTRATION ---")
    print("Simulating drop of malicious script...")
    time.sleep(1)
    
    # Actually create a file to make it "real"
    with open("suspicious_payload.sh", "w") as f:
        f.write("#!/bin/bash\n# Malicious payload\necho 'Hacking...'\n")
    
    log_kernel_event("HIDDEN_PROC", "Found hidden process PID=8822 (payload.sh) parent=1234", pid=8822, parent_pid=1234)
    time.sleep(2)
    log_kernel_event("FILE_SCAN", "Suspicious file created: ./suspicious_payload.sh", pid=8822, parent_pid=1234)

def phase_2_priv_esc():
    print("\n--- PHASE 2: PRIVILEGE ESCALATION ---")
    time.sleep(2)
    log_kernel_event("PRIV_ESC", "PID=8822 (payload.sh) changed effective UID: 1000 -> 0 (ROOT)", pid=8822, parent_pid=1234)
    log_kernel_event("ANOMALY", "Unexpected credential change detected in task_struct", pid=8822, parent_pid=1234)

def phase_3_persistence():
    print("\n--- PHASE 3: PERSISTENCE (ROOTKIT) ---")
    time.sleep(2)
    log_kernel_event("MODULE_LOAD", "Kernel module 'rootkit_v1.ko' loaded (unsigned)", pid=9001, parent_pid=8822)
    log_kernel_event("SYSCALL_HOOK", "Syscall table modified: sys_read -> 0xffffffffc028a000", pid=9001, parent_pid=8822)

def phase_4_network_activity():
    print("\n--- PHASE 4: COMMAND & CONTROL (C2) COMMUNICATION ---")
    time.sleep(2)
    
    # Generate network events with malicious IPs for threat intelligence
    malicious_ip = random.choice(MALICIOUS_IPS)
    log_kernel_event(
        "NETWORK_CONNECTION", 
        f"Suspicious outbound connection: PID=8822 -> {malicious_ip}:4444 (reverse shell)",
        pid=8822,
        parent_pid=1234
    )
    
    time.sleep(1)
    
    # Another suspicious connection
    malicious_ip2 = random.choice(MALICIOUS_IPS)
    log_kernel_event(
        "NETWORK_CONNECTION",
        f"Data exfiltration detected: PID=8822 sending 5MB to {malicious_ip2}:443",
        pid=8822,
        parent_pid=1234
    )
    
    time.sleep(1)
    
    # Normal traffic for comparison
    normal_ip = random.choice(NORMAL_IPS)
    log_kernel_event(
        "NETWORK_CONNECTION",
        f"DNS query: PID=1234 -> {normal_ip}:53",
        pid=1234,
        parent_pid=1
    )

def phase_5_lateral_movement():
    print("\n--- PHASE 5: LATERAL MOVEMENT ---")
    time.sleep(2)
    
    # Simulate process spawning for tree visualization
    log_kernel_event("PROCESS_SPAWN", "PID=8822 spawned child PID=8823 (scanner)", pid=8823, parent_pid=8822)
    time.sleep(1)
    
    log_kernel_event("PROCESS_SPAWN", "PID=8823 spawned child PID=8824 (backdoor)", pid=8824, parent_pid=8823)
    time.sleep(1)
    
    # More suspicious network activity from child processes
    malicious_ip = random.choice(MALICIOUS_IPS)
    log_kernel_event(
        "NETWORK_CONNECTION",
        f"Port scan detected: PID=8823 scanning {malicious_ip}:1-1024",
        pid=8823,
        parent_pid=8822
    )

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
    time.sleep(3)
    phase_4_network_activity()
    time.sleep(3)
    phase_5_lateral_movement()

    print("\n--- ATTACK SIMULATION COMPLETE ---")
    print("Check the dashboard for alerts!")
    print("Features to verify:")
    print("  ✓ Process relationship graph with parent-child links")
    print("  ✓ Threat intelligence enrichment with malicious IP indicators")

if __name__ == "__main__":
    main()
