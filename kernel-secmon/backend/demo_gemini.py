"""
Demo script to populate database with sample events and test Gemini AI integration.
"""
import sqlite3
from datetime import datetime
import time
import json

# Import models directly
class KernelEvent:
    def __init__(self, timestamp, pid, process_name, severity, type, details):
        self.timestamp = timestamp
        self.pid = pid
        self.process_name = process_name
        self.severity = severity
        self.type = type
        self.details = details

def init_db(db_path="kernel_secmon.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

def save_event(event, db_path="kernel_secmon.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (timestamp, pid, process_name, severity, type, details)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (event.timestamp, event.pid, event.process_name, event.severity, event.type, event.details))
    conn.commit()
    conn.close()


# Initialize database
init_db()

# Create sample security events
sample_events = [
    KernelEvent(
        timestamp=datetime.now().isoformat(),
        pid=1337,
        process_name="exploit.sh",
        severity="HIGH",
        type="PRIV_ESC",
        details="UID transition from 1000 to 0 without execve() - potential exploit-based elevation"
    ),
    KernelEvent(
        timestamp=datetime.now().isoformat(),
        pid=6666,
        process_name="rootkit_daemon",
        severity="HIGH",
        type="HIDDEN_PROCESS",
        details="Process visible in task_struct but missing from /proc filesystem - cross-view inconsistency"
    ),
    KernelEvent(
        timestamp=datetime.now().isoformat(),
        pid=9999,
        process_name="malicious_module.ko",
        severity="HIGH",
        type="SYSCALL_HOOK",
        details="sys_call_table[__NR_read] modified to 0xffffffffc0123456 - unauthorized kernel memory modification"
    ),
    KernelEvent(
        timestamp=datetime.now().isoformat(),
        pid=4242,
        process_name="crypto_miner",
        severity="HIGH",
        type="KERNEL_MODULE",
        details="Unsigned kernel module loaded via insmod - attempting to hide CPU usage from monitoring tools"
    ),
]

print("=" * 70)
print("📊 Populating Database with Sample Security Events")
print("=" * 70)

for i, event in enumerate(sample_events, 1):
    save_event(event)
    print(f"\n[{i}] Created event:")
    print(f"    Type: {event.type}")
    print(f"    Process: {event.process_name} (PID {event.pid})")
    print(f"    Severity: {event.severity}")
    print(f"    Details: {event.details[:60]}...")
    time.sleep(0.1)

print("\n" + "=" * 70)
print("✅ Database populated with 4 sample events")
print("=" * 70)

print("\n" + "=" * 70)
print("🤖 Testing Gemini AI Analysis")
print("=" * 70)

# Import analyzer functions
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import gemini service
from gemini_service import generate_xai_explanation, generate_knowledge_graph_data

def get_event_from_db(event_id, db_path="kernel_secmon.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    return row


# Test analysis for each event
for event_id in range(1, 5):
    print(f"\n{'─' * 70}")
    print(f"Event ID: {event_id}")
    print('─' * 70)
    
    row = get_event_from_db(event_id)
    
    if row:
        _, timestamp, pid, name, severity, event_type, details = row
        
        # Generate AI explanation
        explanation = generate_xai_explanation(
            event_type=event_type,
            process_name=name,
            pid=pid,
            severity=severity,
            details=details
        )
        
        # Generate knowledge graph
        graph = generate_knowledge_graph_data(
            event_type=event_type,
            process_name=name,
            pid=pid,
            details=details
        )
        
        print(f"\n📝 XAI Explanation:")
        print(f"{explanation}\n")
        
        print(f"🔗 Knowledge Graph:")
        print(f"   Nodes: {len(graph['nodes'])}")
        print(f"   Links: {len(graph['links'])}")
        
        # Show node details
        for node in graph['nodes']:
            node_type_emoji = {"SYSTEM": "🖥️", "PARENT": "👤", "TARGET": "🎯"}.get(node['type'], "❓")
            print(f"   {node_type_emoji} {node['name']} ({node['type']})")
    else:
        print("❌ Event not found")
    
    time.sleep(2)  # Rate limiting for API

print("\n" + "=" * 70)
print("✅ Gemini AI Integration Demo Complete!")
print("=" * 70)
print("\n💡 Next Steps:")
print("   1. Backend server is running at http://localhost:8000")
print("   2. Test API: curl http://localhost:8000/api/analysis/1")
print("   3. Start frontend and click on events to see AI explanations!")
