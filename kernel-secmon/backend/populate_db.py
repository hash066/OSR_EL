"""
Quick script to populate database with sample events for demo
"""
import sqlite3
from datetime import datetime

# Initialize database
conn = sqlite3.connect("kernel_secmon.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        pid INTEGER,
        process_name TEXT,
        severity TEXT,
        type TEXT,
        details TEXT
    )
''')

# Clear existing data
cursor.execute("DELETE FROM events")

# Insert sample events
events = [
    (datetime.now().isoformat(), 1337, "exploit.sh", "HIGH", "PRIV_ESC", 
     "UID transition from 1000 to 0 without execve() - potential exploit-based elevation"),
    (datetime.now().isoformat(), 6666, "rootkit_daemon", "HIGH", "HIDDEN_PROCESS", 
     "Process visible in task_struct but missing from /proc filesystem - cross-view inconsistency"),
    (datetime.now().isoformat(), 9999, "malicious_module.ko", "HIGH", "SYSCALL_HOOK", 
     "sys_call_table[__NR_read] modified to 0xffffffffc0123456 - unauthorized kernel memory modification"),
    (datetime.now().isoformat(), 4242, "crypto_miner", "HIGH", "KERNEL_MODULE", 
     "Unsigned kernel module loaded via insmod - attempting to hide CPU usage from monitoring tools"),
]

for event in events:
    cursor.execute('''
        INSERT INTO events (timestamp, pid, process_name, severity, type, details)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', event)

conn.commit()
conn.close()

print("✓ Database populated with 4 sample events")
print("✓ Events have IDs 1-4")
print("✓ You can now click on events in the dashboard to see AI analysis!")
