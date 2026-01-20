# 🚀 Rootkit Detector with Gemini AI - Complete Setup Guide

## Your System: Windows with WSL

You're running on **Windows**, but the Rootkit Detector monitors **Linux kernels**. Here's how to run everything:

---

## Option 1: Quick Demo (Windows Only - For Dashboard Testing)

This runs the backend and frontend on Windows to test the Gemini AI integration.

### Terminal 1 - Backend (Already Running ✅)
```powershell
cd "e:\SEM 3\Rootkit-Detector\kernel-secmon\backend"
python -m uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend
```powershell
cd "e:\SEM 3\Rootkit-Detector\kernel-secmon\frontend"
npm run dev
```

### Terminal 3 - Red Team (Generate Events)
```powershell
cd "e:\SEM 3\Rootkit-Detector\kernel-secmon\scripts"
python red_team.py
```

Then open: **http://localhost:5173**

---

## Option 2: Full System (WSL - For Real Kernel Monitoring)

For actual Linux kernel monitoring, use WSL:

### Terminal 1 - Backend in WSL
```bash
wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/backend' && python3 -m pip install --break-system-packages -r requirements.txt && python3 -m uvicorn main:app --reload --port 8000"
```

### Terminal 2 - Frontend (Windows)
```powershell
cd "e:\SEM 3\Rootkit-Detector\kernel-secmon\frontend"
npm run dev
```

### Terminal 3 - Red Team in WSL
```bash
wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/scripts' && python3 red_team.py"
```

### Terminal 4 - Collector Agent (WSL - Monitors Kernel Events)
```bash
wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/collector' && python3 agent.py"
```

---

## What Each Component Does

| Component | Where It Runs | Purpose |
|-----------|---------------|---------|
| **Backend** | Windows or WSL | FastAPI server with Gemini AI integration |
| **Frontend** | Windows | React dashboard (browser-based) |
| **Red Team** | Windows or WSL | Generates fake security events for testing |
| **Collector** | WSL (Linux) | Monitors real Linux kernel events |
| **Kernel Module** | WSL (Linux) | Actual kernel-level monitoring |

---

## Current Status

✅ **Backend:** Running on Windows (port 8000)  
✅ **Gemini AI:** Integrated and working  
✅ **Database:** Has 4 sample events  
⏳ **Frontend:** Ready to start  
⏳ **Red Team:** Ready to generate events  

---

## Recommended: Simple Windows Demo

Since you're testing the **Gemini AI integration**, just run everything on Windows:

**1. Backend is already running ✅**

**2. Start Frontend (New PowerShell):**
```powershell
cd "e:\SEM 3\Rootkit-Detector\kernel-secmon\frontend"
npm run dev
```

**3. Generate Events (New PowerShell):**
```powershell
cd "e:\SEM 3\Rootkit-Detector\kernel-secmon\scripts"
python red_team.py
```

**4. Open Dashboard:**
- Go to: http://localhost:5173
- Click any event
- See AI-generated XAI explanation and knowledge graph!

---

## Why Windows Commands?

- Your files are on `e:\` (Windows drive)
- Backend is already running in Windows PowerShell
- Frontend (React) runs in browser - works on any OS
- For **testing AI integration**, Windows is fine!

For **real kernel monitoring**, you'd:
1. Load the kernel module in WSL/Linux
2. Run collector agent in WSL
3. Monitor actual Linux kernel events

But for **demonstrating Gemini AI**, the Windows setup works perfectly!

---

## Quick Commands Summary

**Windows (Current Setup):**
```powershell
# Terminal 1 (Already running)
cd "e:\SEM 3\Rootkit-Detector\kernel-secmon\backend"
python -m uvicorn main:app --reload --port 8000

# Terminal 2
cd "e:\SEM 3\Rootkit-Detector\kernel-secmon\frontend"
npm run dev

# Terminal 3
cd "e:\SEM 3\Rootkit-Detector\kernel-secmon\scripts"
python red_team.py
```

**WSL (For Linux Kernel Monitoring):**
```bash
# Backend
wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/backend' && python3 -m uvicorn main:app --reload --port 8000"

# Red Team
wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/scripts' && python3 red_team.py"

# Collector
wsl bash -c "cd '/mnt/e/SEM 3/Rootkit-Detector/kernel-secmon/collector' && python3 agent.py"
```

---

## What You'll See

1. **Dashboard** shows security events
2. **Click event** → Modal opens
3. **XAI Section** shows AI-generated explanation
4. **Knowledge Graph** shows process lineage

**The Gemini AI integration works the same on Windows or WSL!** 🎉
