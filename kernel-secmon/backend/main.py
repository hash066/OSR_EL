from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Deque
from collections import deque
import random
from models import KernelEvent
from database import init_db, save_event, get_recent_events, get_stats, get_suspicious_processes
from analyzer import analyze_event, check_behavioral_patterns, get_event_analysis
from response import execute_mitigation
import json

app = FastAPI(title="Kernel SecMon API")

# Security
API_KEY = "SEC_MON_SECRET_KEY_2026"

# Initialize DB
init_db()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"status": "Kernel Monitor Active", "version": "1.0.0"}

@app.get("/api/events")
async def fetch_events(limit: int = 50):
    return get_recent_events(limit)

@app.get("/api/stats")
async def fetch_stats():
    return get_stats()

@app.get("/api/analysis/{event_id}")
async def fetch_event_analysis(event_id: int):
    analysis = get_event_analysis(event_id)
    if not analysis:
        return JSONResponse(status_code=404, content={"error": "Event not found"})
    return analysis

@app.get("/api/processes/suspicious")
async def fetch_suspicious_procs():
    return get_suspicious_processes()

@app.post("/api/ingest")
async def ingest_event(event: KernelEvent, api_key: str = None):
    # Simple Hash-based or string comparison
    if api_key != API_KEY:
        return JSONResponse(status_code=401, content={"status": "unauthorized"})
    # Store event in DB
    save_event(event)

    # Analyze for immediate anomalies
    anomalies = analyze_event(event)
    for anomaly in anomalies:
        # Broadcast findings as special events
        await manager.broadcast(json.dumps({
            "timestamp": event.timestamp,
            "type": "SECURITY_ALERT",
            "severity": "HIGH",
            "details": anomaly
        }))
        
        # Trigger Automated Response
        action = execute_mitigation(event.type, event.pid, event.process_name)
        if action:
            await manager.broadcast(json.dumps({
                "timestamp": event.timestamp,
                "type": "RESPONSE_ACTION",
                "severity": "INFO",
                "details": f"Automated Action: {action}"
            }))

    # Every 10th event, check for broader behavioral patterns
    # (Simplified trigger logic)
    if random.randint(1, 10) == 1:
        patterns = check_behavioral_patterns()
        for pattern in patterns:
            await manager.broadcast(json.dumps(pattern))

    # Broadcast to WebSocket clients
    await manager.broadcast(event.model_dump_json())
    return {"status": "received"}

@app.websocket("/ws/feed")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep connection open
    except WebSocketDisconnect:
        manager.disconnect(websocket)
