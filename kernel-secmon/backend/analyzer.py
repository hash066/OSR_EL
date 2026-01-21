import sqlite3
from models import KernelEvent
from datetime import datetime, timedelta
from gemini_service import generate_xai_explanation, generate_knowledge_graph_data
from threat_intel import enrich_event_with_threat_intel

def analyze_event(event: KernelEvent):
    """
    Analyzes a single incoming event for immediate red flags.
    """
    anomalies = []
    
    # 1. Critical Severity immediate flag
    if event.severity == "HIGH":
        anomalies.append(f"Critical Event: {event.type} in {event.process_name}")

    # 2. Sequential Hooking Pattern
    # This would usually look at history, for now we flag the event itself
    if "HOOK" in event.type or "MODIFIED" in event.details:
        anomalies.append(f"Persistence Technique: {event.type}")

    return anomalies

def check_behavioral_patterns(db_path="kernel_secmon.db"):
    """
    Scans the database for patterns over time (e.g., brute force, ritualistic hiding).
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    findings = []
    
    # Example: Look for PID that has triggered multiple security events in 5 minutes
    five_min_ago = (datetime.now() - timedelta(minutes=5)).isoformat()
    
    cursor.execute('''
        SELECT pid, process_name, COUNT(*) as event_count 
        FROM events 
        WHERE severity != 'INFO' AND timestamp > ?
        GROUP BY pid 
        HAVING event_count > 3
    ''', (five_min_ago,))
    
    results = cursor.fetchall()
    for row in results:
        pid, name, count = row
        findings.append({
            "type": "BEHAVIORAL_ANOMALY",
            "details": f"Process {name} (PID {pid}) triggered {count} events in 5 minutes.",
            "severity": "HIGH"
        })
        
    conn.close()
    return findings

def get_event_analysis(event_id, db_path="kernel_secmon.db"):
    """
    Returns enriched analysis and graph data for a specific event using Gemini AI
    and threat intelligence.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
        
    _, timestamp, pid, name, severity, type, details = row[:7]  # Handle optional parent_pid
    
    # 1. Generate XAI explanation using Gemini AI
    explanation = generate_xai_explanation(
        event_type=type,
        process_name=name,
        pid=pid,
        severity=severity,
        details=details
    )

    # 2. Build Knowledge Graph using Gemini AI
    graph = generate_knowledge_graph_data(
        event_type=type,
        process_name=name,
        pid=pid,
        details=details
    )

    # 3. Enrich with Threat Intelligence
    threat_intel = enrich_event_with_threat_intel(details)

    conn.close()
    return {
        "event_id": event_id,
        "xai_explanation": explanation,
        "graph": graph,
        "threat_intel": threat_intel,
        "raw_details": details
    }


