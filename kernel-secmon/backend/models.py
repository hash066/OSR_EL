from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class KernelEvent(BaseModel):
    timestamp: str
    pid: int
    parent_pid: int = 0
    process_name: str
    severity: str  # HIGH, MEDIUM, INFO
    type: str      # PRIV_ESC, HIDDEN_PROCESS, KERNEL_ANOMALY
    details: str

class ProcessInfo(BaseModel):
    pid: int
    name: str
    status: str
    last_seen: str
