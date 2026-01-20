# Kernel SecMon - Real-time Kernel Security Dashboard

**Kernel SecMon** is a comprehensive, production-quality dashboard designed to visualize real-time kernel-level security events. It serves as the user-space component for a Linux Kernel Module (LKM) monitoring system.

## 🚀 Features & Academic Spec Mapping

| Academic Objective | Implementation Feature | Component |
| ------------------ | ---------------------- | --------- |
| **Real-time Visualization** | WebSocket-based Live Feed | `frontend/src/components/Dashboard.jsx` |
| **Privilege Escalation** | `PRIV_ESC` event parsing & High Severity Alerts | `collector/agent.py` & Backend Models |
| **Hidden Processes** | `HIDDEN_PROC` event detection & "Suspicious Procs" stats | `backend/main.py` (Suspicious logic) |
| **Kernel Anomalies** | `KERNEL_ANOMALY` type support & stats visualization | `frontend/src/components/StatsCards.jsx` |
| **Lightweight Agent** | Python-based Log Collector (No heavy dependencies) | `collector/agent.py` |

## 🏗️ Architecture

```mermaid
graph LR
    Kernel[Kernel Module (LKM)] -- dmesg/Netlink --> Agent[Collector Agent (Python)]
    Agent -- HTTP POST --> Backend[API Server (FastAPI)]
    Backend -- WebSocket --> Frontend[Dashboard (React)]
    Backend -- REST API --> Frontend
```

-   **Kernel Module**: (External) Detects threats and writes to logs tagged `SEC_MON`.
-   **Collector Agent**: Watches logs, parses structured events, and pushes to API.
-   **Backend**: Aggregates events and broadcasts to connected clients.
-   **Dashboard**: Displays real-time alerts and statistics.

## 🛠️ Tech Stack

-   **Backend**: Python (FastAPI, Uvicorn)
-   **Frontend**: React (Vite), Tailwind CSS, Lucide Icons, Recharts (ready)
-   **Collector**: Python (Requests)

## ⚡ Quick Start (Red Team Demo)

To perform a **Live Security Demonstration**:

1.  **Start the Environment**:
    ```bash
    cd scripts
    bash dev.sh
    ```
    This starts the Backend, Frontend, and Collector (watching `kernel_events.log`).

2.  **Open Dashboard**:
    Navigate to `http://localhost:5173`. You will see a "Live Feed" waiting for data.

3.  **Launch Attack (In a new terminal)**:
    ```bash
    cd scripts
    python red_team.py
    ```
    -   This script will create **real files** on disk (`suspicious_payload.sh`).
    -   It will write to `kernel_events.log`.
    -   Watch the Dashboard detect the infiltration, privilege escalation, and rootkit loading in real-time!

## ⚡ Quick Start (Auto Mock Mode)
If you just want background noise without running the attack script manually:
```bash
bash dev.sh --mock
```

## 📂 Project Structure

-   `backend/`: FastAPI server source code.
-   `frontend/`: React application source code.
-   `collector/`: Agent script for real deployments.
-   `scripts/`: Utilities for development and mocking.

## 📦 Deployment (Real Kernel Monitor)

To connect to a real kernel module:

1.  Ensure your LKM writes logs with the prefix `SEC_MON`.
    -   Example: `[123.456] SEC_MON_PRIV_ESC: PID=1337 (bash) changed creds`
2.  Start the Backend: `cd backend && uvicorn main:app`
3.  Start the Collector: `cd collector && python3 agent.py`
4.  Start the Frontend: `cd frontend && npm run preview`
