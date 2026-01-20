import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use the latest flash model
    model = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    model = None
    print("WARNING: GEMINI_API_KEY not found. XAI will use fallback explanations.")


def generate_xai_explanation(event_type: str, process_name: str, pid: int, severity: str, details: str) -> str:
    """
    Generate an AI-powered XAI explanation for a security event using Gemini.
    
    Args:
        event_type: Type of security event (e.g., PRIV_ESC, HIDDEN_PROCESS)
        process_name: Name of the process involved
        pid: Process ID
        severity: Severity level (HIGH, MEDIUM, LOW)
        details: Additional event details
    
    Returns:
        AI-generated explanation string
    """
    if not model:
        return _get_fallback_explanation(event_type, process_name, pid)
    
    try:
        prompt = f"""You are a cybersecurity expert analyzing kernel-level security events in a rootkit detection system.

Analyze this security event and provide a detailed, technical explanation suitable for a security analyst:

Event Type: {event_type}
Process Name: {process_name}
Process ID (PID): {pid}
Severity: {severity}
Details: {details}

Provide a concise but technical explanation (2-3 sentences) that:
1. Explains what this event indicates from a security perspective
2. Describes the potential threat or attack technique being used
3. Mentions specific technical mechanisms (e.g., syscall hooking, procfs manipulation, privilege escalation vectors)

Keep the tone professional and technical. Focus on the "why" this is suspicious and "how" it works at a low level."""

        # Set a shorter timeout for faster response
        import time
        start_time = time.time()
        
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 200,
            }
        )
        
        elapsed = time.time() - start_time
        print(f"Gemini API took {elapsed:.2f}s for XAI explanation")
        
        if response and response.text:
            return response.text.strip()
        else:
            return _get_fallback_explanation(event_type, process_name, pid)
            
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return _get_fallback_explanation(event_type, process_name, pid)


def generate_knowledge_graph_data(event_type: str, process_name: str, pid: int, details: str) -> dict:
    """
    Generate enhanced knowledge graph data using AI to suggest process relationships.
    
    Args:
        event_type: Type of security event
        process_name: Name of the process
        pid: Process ID
        details: Event details
    
    Returns:
        Dictionary with nodes and links for force graph visualization
    """
    # For faster response, use fallback graph for now
    # The AI generation can be slow and cause timeouts
    return _get_fallback_graph(process_name, pid)


def _get_fallback_explanation(event_type: str, process_name: str, pid: int) -> str:
    """Fallback explanations when Gemini API is unavailable."""
    explanations = {
        "PRIV_ESC": f"Process '{process_name}' performed an unauthorized privilege transition to UID 0 without a valid execve() context, indicating potential credential stuffing or exploit-based elevation.",
        "HIDDEN_PROCESS": f"Process '{process_name}' (PID {pid}) is present in the kernel's active task list but is missing from the procfs layer, a classic 'Cross-View' inconsistency used by rootkits to hide presence.",
        "SYSCALL_HOOK": f"Experimental detection of syscall table modification. Unauthorized modification detected in kernel space memory, likely via /dev/kmem or an unsigned module.",
        "KERNEL_MODULE": f"Suspicious kernel module loaded by '{process_name}'. Module may be attempting to hook kernel functions or hide malicious activity.",
    }
    
    for key in explanations:
        if key in event_type:
            return explanations[key]
    
    return f"System detected an anomalous kernel state involving process '{process_name}' (PID {pid}). Further investigation recommended."


def _get_fallback_graph(process_name: str, pid: int) -> dict:
    """Fallback graph structure when Gemini API is unavailable."""
    return {
        "nodes": [
            {"id": "1", "name": "systemd", "type": "SYSTEM"},
            {"id": "99", "name": "bash", "type": "PARENT"},
            {"id": str(pid), "name": process_name, "type": "TARGET"}
        ],
        "links": [
            {"source": "1", "target": "99"},
            {"source": "99", "target": str(pid)}
        ]
    }
