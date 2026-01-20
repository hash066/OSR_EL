#!/bin/bash
echo "Starting Kernel SecMon Environment..."

# Trap Ctrl+C to kill all background jobs
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# Start Backend
echo "Starting Backend..."
cd backend
# Check if venv exists, if not assume global or user handles it (simplify for this demo)
# pip install -r requirements.txt > /dev/null 2>&1 
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend
# npm install > /dev/null 2>&1
npm run dev &
FRONTEND_PID=$!
cd ..

# Start Collector Agent (Watcher)
echo "Starting Collector Agent..."
cd collector
python3 agent.py &
AGENT_PID=$!
cd ..

# Start Mock Generator (Optional)
if [ "$1" == "--mock" ]; then
    echo "Starting Mock Generator..."
    sleep 5 # Wait for backend
    python3 scripts/mock_gen.py &
    MOCK_PID=$!
fi

echo "Environment Ready!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Collector: Running (Watching kernel_events.log)"

wait
