#!/bin/bash

# Gemini AI Integration - WSL Demonstration Script
# This script demonstrates the AI-powered XAI and Knowledge Graph features

echo "========================================================================"
echo "GEMINI AI INTEGRATION - WSL DEMONSTRATION"
echo "========================================================================"
echo ""

# Navigate to backend directory
cd "/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/backend"

echo "[1/4] Installing Python dependencies..."
echo "------------------------------------------------------------------------"
# Use --break-system-packages flag for WSL Ubuntu
python3 -m pip install --break-system-packages -q fastapi uvicorn pydantic python-multipart websockets google-generativeai python-dotenv 2>/dev/null
echo "✓ Dependencies installed"
echo ""

echo "[2/4] Starting Backend Server..."
echo "------------------------------------------------------------------------"
# Start backend in background
nohup python3 -m uvicorn main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "✓ Backend started (PID: $BACKEND_PID) on http://localhost:8000"
echo "  Log file: /tmp/backend.log"
sleep 3
echo ""

echo "[3/4] Running Gemini AI Demo..."
echo "------------------------------------------------------------------------"
# Run the demo script
python3 simple_demo.py
echo ""

echo "[4/4] Testing API Endpoint..."
echo "------------------------------------------------------------------------"
echo "Fetching AI analysis from: http://localhost:8000/api/analysis/1"
echo ""
curl -s http://localhost:8000/api/analysis/1 | python3 -m json.tool 2>/dev/null || echo "Note: Backend may need a moment to start. Try: curl http://localhost:8000/api/analysis/1"
echo ""

echo "========================================================================"
echo "DEMONSTRATION COMPLETE"
echo "========================================================================"
echo ""
echo "Backend Server Status:"
echo "  URL: http://localhost:8000"
echo "  PID: $BACKEND_PID"
echo "  Docs: http://localhost:8000/docs"
echo ""
echo "To stop the backend server:"
echo "  kill $BACKEND_PID"
echo ""
echo "To start the frontend:"
echo "  cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/frontend'"
echo "  npm run dev"
echo ""
echo "========================================================================"
