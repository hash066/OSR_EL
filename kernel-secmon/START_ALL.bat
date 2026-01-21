@echo off
echo ========================================================================
echo   KERNEL-SECMON - Starting All Services
echo ========================================================================
echo.

echo [1/3] Starting Backend API Server...
echo ------------------------------------------------------------------------
start "Backend API" wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/backend' && python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak > nul
echo Backend started on http://localhost:8000
echo.

echo [2/4] Starting Normal Feed Generator (Background Activity)...
echo ------------------------------------------------------------------------
start "Normal Feed" wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/scripts' && python3 normal_feed.py"
timeout /t 2 /nobreak > nul
echo Normal feed generator started
echo.

echo [3/4] Starting Collector Agent...
echo ------------------------------------------------------------------------
start "Collector Agent" wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/collector' && python3 agent.py"
timeout /t 3 /nobreak > nul
echo Collector started
echo.

echo [4/4] Frontend is already running at http://localhost:5173
echo.

echo ========================================================================
echo   ALL SERVICES STARTED
echo ========================================================================
echo.
echo Backend API:   http://localhost:8000
echo Frontend UI:   http://localhost:5173
echo.
echo Press any key to run Red Team attack simulation...
pause > nul

echo.
echo Running Red Team Attack Simulation...
echo ========================================================================
wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/scripts' && python3 red_team.py"

echo.
echo ========================================================================
echo   ATTACK SIMULATION COMPLETE!
echo ========================================================================
echo.
echo Open http://localhost:5173 in your browser to see:
echo   1. Process Lineage Map (right sidebar) - Interactive graph
echo   2. Threat Intelligence (click any event) - IP reputation data
echo.
echo Press any key to exit...
pause > nul
