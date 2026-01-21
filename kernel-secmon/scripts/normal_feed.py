#!/usr/bin/env python3
"""
Normal Kernel Event Feed Generator
Continuously generates realistic benign kernel events to simulate normal system activity.
This runs in the background and creates a baseline of normal activity.
When red_team.py is executed, malicious events will appear alongside these normal events.
"""

import time
import os
import random
from datetime import datetime

# Log file that the Collector Agent will watch
LOG_FILE = "../kernel_events.log"

# Normal process names that might appear in a typical system
NORMAL_PROCESSES = [
    "systemd", "sshd", "bash", "python3", "node", "npm", "nginx", "chrome",
    "code", "firefox", "gnome-shell", "NetworkManager", "dockerd", "postgres"
]

# Normal IPs (DNS, CDNs, etc.)
NORMAL_IPS = [
    "8.8.8.8",         # Google DNS
    "1.1.1.1",         # Cloudflare DNS
    "13.107.42.14",    # Microsoft
    "151.101.1.140",   # Fastly CDN
    "172.217.14.206",  # Google
]

def log_kernel_event(event_type, details):
    """Write a kernel event to the log file."""
    timestamp = time.time()
    log_line = f"[{timestamp:.6f}] SEC_MON_{event_type}: {details}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

def generate_process_spawn():
    """Generate a normal process spawn event."""
    pid = random.randint(1000, 9999)
    parent_pid = random.randint(100, 999)
    process = random.choice(NORMAL_PROCESSES)
    
    log_kernel_event(
        "PROCESS_SPAWN",
        f"PID={pid} ({process}) spawned by parent={parent_pid}"
    )

def generate_file_access():
    """Generate a normal file access event."""
    pid = random.randint(1000, 9999)
    process = random.choice(NORMAL_PROCESSES)
    files = [
        "/var/log/syslog", "/etc/hosts", "/home/user/.bashrc",
        "/tmp/cache.tmp", "/usr/bin/python3", "/etc/resolv.conf"
    ]
    file = random.choice(files)
    
    log_kernel_event(
        "FILE_ACCESS",
        f"PID={pid} ({process}) accessed {file}"
    )

def generate_network_connection():
    """Generate a normal network connection event."""
    pid = random.randint(1000, 9999)
    process = random.choice(NORMAL_PROCESSES)
    ip = random.choice(NORMAL_IPS)
    port = random.choice([80, 443, 53, 22, 3000, 5432])
    
    log_kernel_event(
        "NETWORK_CONNECTION",
        f"PID={pid} ({process}) -> {ip}:{port}"
    )

def generate_syscall():
    """Generate a normal syscall event."""
    pid = random.randint(1000, 9999)
    process = random.choice(NORMAL_PROCESSES)
    syscalls = ["read", "write", "open", "close", "socket", "bind"]
    syscall = random.choice(syscalls)
    
    log_kernel_event(
        "SYSCALL",
        f"PID={pid} ({process}) called sys_{syscall}"
    )

def main():
    """Main loop that continuously generates normal kernel events."""
    print("=" * 70)
    print("NORMAL KERNEL EVENT FEED GENERATOR")
    print("=" * 70)
    print(f"Writing to: {os.path.abspath(LOG_FILE)}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("Generating continuous normal kernel activity...")
    print("(malicious events will appear when red_team.py is run)")
    print("=" * 70)
    print()
    
    # Ensure log file exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write(f"[{time.time():.6f}] Kernel Monitor Initialized.\n")
    
    # Event generators with their weights (probability)
    event_generators = [
        (generate_process_spawn, 2),      # 20% chance
        (generate_file_access, 3),        # 30% chance
        (generate_network_connection, 3), # 30% chance
        (generate_syscall, 2),            # 20% chance
    ]
    
    event_count = 0
    
    try:
        while True:
            # Choose a random event type based on weights
            generators, weights = zip(*event_generators)
            generator = random.choices(generators, weights=weights)[0]
            
            # Generate the event
            generator()
            event_count += 1
            
            # Print status every 10 events
            if event_count % 10 == 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Generated {event_count} normal events...")
            
            # Random delay between events (1-5 seconds for realistic timing)
            time.sleep(random.uniform(1, 5))
            
    except KeyboardInterrupt:
        print("\n")
        print("=" * 70)
        print(f"Normal feed generator stopped. Total events generated: {event_count}")
        print("=" * 70)

if __name__ == "__main__":
    main()
