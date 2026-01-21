import sqlite3
import json
from datetime import datetime
from models import KernelEvent

DB_PATH = "kernel_secmon.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            pid INTEGER,
            process_name TEXT,
            severity TEXT,
            type TEXT,
            details TEXT,
            parent_pid INTEGER DEFAULT 0
        )
    ''')
    
    # Suspicious processes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suspicious_processes (
            pid INTEGER PRIMARY KEY,
            name TEXT,
            reason TEXT,
            last_seen TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_event(event: KernelEvent):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (timestamp, pid, process_name, severity, type, details, parent_pid)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (event.timestamp, event.pid, event.process_name, event.severity, event.type, event.details, event.parent_pid))
    
    if event.type in ["HIDDEN_PROCESS", "PRIV_ESC"]:
        cursor.execute('''
            INSERT OR REPLACE INTO suspicious_processes (pid, name, reason, last_seen)
            VALUES (?, ?, ?, ?)
        ''', (event.pid, event.process_name, event.type, event.timestamp))
        
    conn.commit()
    conn.close()


def get_recent_events(limit=50):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM events')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM events WHERE severity = "HIGH"')
    high = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM events WHERE severity = "MEDIUM"')
    medium = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM suspicious_processes')
    suspicious_count = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total_events": total,
        "high_severity": high,
        "medium_severity": medium,
        "suspicious_processes": suspicious_count
    }

def get_suspicious_processes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM suspicious_processes')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_process_tree():
    """
    Returns all processes with their parent relationships for graph visualization.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all unique processes from events
    cursor.execute('''
        SELECT DISTINCT 
            pid, 
            process_name,
            parent_pid,
            MAX(CASE WHEN severity = 'HIGH' THEN 1 ELSE 0 END) as is_suspicious,
            COUNT(*) as event_count
        FROM events
        GROUP BY pid, process_name
    ''')
    
    processes = cursor.fetchall()
    
    # Build nodes and links for force graph
    nodes = []
    links = []
    
    for pid, name, parent_pid, is_suspicious, event_count in processes:
        nodes.append({
            'id': str(pid),
            'name': name,
            'pid': pid,
            'suspicious': bool(is_suspicious),
            'event_count': event_count
        })
        
        # Add link to parent if exists and parent is in our dataset
        if parent_pid and parent_pid != 0:
            links.append({
                'source': str(parent_pid),
                'target': str(pid)
            })
    
    conn.close()
    
    return {
        'nodes': nodes,
        'links': links
    }
