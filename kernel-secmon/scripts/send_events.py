"""
Send events directly to the backend API for immediate dashboard display
"""
import requests
import time
from datetime import datetime

# Backend API endpoint
API_URL = "http://localhost:8000/api/ingest"
API_KEY = "SEC_MON_SECRET_KEY_2026"

# Sample security events
events = [
    {
        "timestamp": datetime.now().isoformat(),
        "pid": 1337,
        "process_name": "exploit.sh",
        "severity": "HIGH",
        "type": "PRIV_ESC",
        "details": "UID transition from 1000 to 0 without execve() - potential exploit-based elevation"
    },
    {
        "timestamp": datetime.now().isoformat(),
        "pid": 6666,
        "process_name": "rootkit_daemon",
        "severity": "HIGH",
        "type": "HIDDEN_PROCESS",
        "details": "Process visible in task_struct but missing from /proc filesystem"
    },
    {
        "timestamp": datetime.now().isoformat(),
        "pid": 9999,
        "process_name": "malicious_module.ko",
        "severity": "HIGH",
        "type": "SYSCALL_HOOK",
        "details": "sys_call_table[__NR_read] modified to 0xffffffffc0123456"
    },
    {
        "timestamp": datetime.now().isoformat(),
        "pid": 4242,
        "process_name": "crypto_miner",
        "severity": "HIGH",
        "type": "KERNEL_MODULE",
        "details": "Unsigned kernel module loaded via insmod"
    },
    {
        "timestamp": datetime.now().isoformat(),
        "pid": 8822,
        "process_name": "payload.sh",
        "severity": "HIGH",
        "type": "HIDDEN_PROCESS",
        "details": "Found hidden process parent=bash"
    },
    {
        "timestamp": datetime.now().isoformat(),
        "pid": 8822,
        "process_name": "payload.sh",
        "severity": "HIGH",
        "type": "PRIV_ESC",
        "details": "Changed effective UID: 1000 -> 0 (ROOT)"
    },
]

print("=" * 60)
print("Sending Security Events to Dashboard")
print("=" * 60)

for i, event in enumerate(events, 1):
    print(f"\n[{i}/{len(events)}] Sending {event['type']} event...")
    print(f"    Process: {event['process_name']} (PID {event['pid']})")
    
    try:
        response = requests.post(
            API_URL,
            json=event,
            params={"api_key": API_KEY},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"    ✓ Event sent successfully!")
        else:
            print(f"    ✗ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    time.sleep(0.5)

print("\n" + "=" * 60)
print("✓ All events sent to backend!")
print("=" * 60)
print("\nRefresh your dashboard at http://localhost:5173")
print("Events should now appear in the AlertFeed!")
print("\nClick any event to see AI-generated XAI explanation!")
