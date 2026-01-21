#!/bin/bash

echo "========================================================================"
echo "  KERNEL-SECMON - Full Stack Demo with Process Graph & Threat Intel"
echo "========================================================================"
echo ""

# Navigate to backend
cd "/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/backend"

echo "[1/5] Starting Backend API Server..."
echo "------------------------------------------------------------------------"
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "✓ Backend started (PID: $BACKEND_PID)"
echo "  URL: http://localhost:8000"
echo "  Log: /tmp/backend.log"
sleep 3

# Test backend
echo ""
echo "[2/5] Testing Backend..."
curl -s http://localhost:8000/api/stats | python3 -m json.tool || echo "Backend starting..."
echo ""

echo "[3/5] Starting Collector Agent..."
echo "------------------------------------------------------------------------"
cd "/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/collector"
python3 agent.py > /tmp/collector.log 2>&1 &
COLLECTOR_PID=$!
echo "✓ Collector started (PID: $COLLECTOR_PID)"
echo "  Log: /tmp/collector.log"
sleep 2

echo ""
echo "[4/5] Running Red Team Attack Simulation..."
echo "------------------------------------------------------------------------"
cd "/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/scripts"
python3 red_team.py

echo ""
echo "[5/5] Verifying New Features..."
echo "------------------------------------------------------------------------"

sleep 2
echo ""
echo "✓ Process Tree API:"
curl -s http://localhost:8000/api/processes/tree | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"  Nodes: {len(d['nodes'])}, Links: {len(d['links'])}\")"

echo ""
echo "✓ Threat Intelligence (checking event 1):"
curl -s http://localhost:8000/api/analysis/1 | python3 -c "import sys, json; d=json.load(sys.stdin); ti=d.get('threat_intel',{}); print(f\"  Network Activity: {ti.get('has_network_activity')}, Max Threat Score: {ti.get('max_threat_score', 0)}\")" 2>/dev/null || echo "  Event not yet analyzed"

echo ""
echo "========================================================================"
echo "  SERVICES RUNNING"
echo "========================================================================"
echo ""
echo "Backend API:  http://localhost:8000 (PID: $BACKEND_PID)"
echo "Frontend UI:  http://localhost:5173 (should already be running)"
echo "Collector:    Running (PID: $COLLECTOR_PID)"
echo ""
echo "Process IDs saved to stop later:"
echo "  export BACKEND_PID=$BACKEND_PID"
echo "  export COLLECTOR_PID=$COLLECTOR_PID"
echo ""
echo "To stop services:"
echo "  kill $BACKEND_PID $COLLECTOR_PID"
echo ""
echo "View logs:"
echo "  tail -f /tmp/backend.log"
echo "  tail -f /tmp/collector.log"
echo ""
echo "========================================================================"
echo "  FEATURES TO TEST IN DASHBOARD"
echo "========================================================================"
echo ""
echo "1. PROCESS LINEAGE MAP (right sidebar):"
echo "   - Interactive force graph showing process relationships"
echo "   - Red nodes = suspicious, Green = normal"
echo "   - Click nodes to see details"
echo ""
echo "2. THREAT INTELLIGENCE (click any threat event):"
echo "   - Max Threat Score with color coding"
echo "   - Malicious IP alerts with report links"
echo "   - List of all analyzed IPs"
echo ""
echo "Open http://localhost:5173 in your browser to see the dashboard!"
echo "========================================================================"
