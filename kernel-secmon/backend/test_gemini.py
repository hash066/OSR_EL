"""
Test script to verify Gemini AI integration for XAI explanations and knowledge graphs.
"""
import sys
import os

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.dirname(__file__))

from gemini_service import generate_xai_explanation, generate_knowledge_graph_data
import json

def test_xai_explanation():
    print("=" * 60)
    print("Testing XAI Explanation Generation")
    print("=" * 60)
    
    # Test case 1: Privilege Escalation
    print("\n[Test 1] Privilege Escalation Event")
    explanation = generate_xai_explanation(
        event_type="PRIV_ESC",
        process_name="malicious_proc",
        pid=1337,
        severity="HIGH",
        details="UID transition from 1000 to 0 without execve"
    )
    print(f"Explanation: {explanation}\n")
    
    # Test case 2: Hidden Process
    print("[Test 2] Hidden Process Event")
    explanation = generate_xai_explanation(
        event_type="HIDDEN_PROCESS",
        process_name="rootkit_daemon",
        pid=6666,
        severity="HIGH",
        details="Process visible in task_struct but missing from /proc"
    )
    print(f"Explanation: {explanation}\n")
    
    # Test case 3: Syscall Hook
    print("[Test 3] Syscall Hook Event")
    explanation = generate_xai_explanation(
        event_type="SYSCALL_HOOK",
        process_name="kernel_module",
        pid=0,
        severity="HIGH",
        details="sys_call_table[__NR_read] modified to 0xffffffffc0123456"
    )
    print(f"Explanation: {explanation}\n")

def test_knowledge_graph():
    print("=" * 60)
    print("Testing Knowledge Graph Generation")
    print("=" * 60)
    
    print("\n[Test] Process Lineage Graph for Suspicious Process")
    graph = generate_knowledge_graph_data(
        event_type="PRIV_ESC",
        process_name="exploit.sh",
        pid=9999,
        details="Spawned from web server, escalated to root"
    )
    
    print(f"\nGenerated Graph Structure:")
    print(json.dumps(graph, indent=2))
    
    # Validate structure
    assert "nodes" in graph, "Graph missing 'nodes' field"
    assert "links" in graph, "Graph missing 'links' field"
    assert len(graph["nodes"]) >= 3, "Graph should have at least 3 nodes"
    
    # Check for TARGET node
    target_found = any(node.get("type") == "TARGET" for node in graph["nodes"])
    assert target_found, "Graph should have a TARGET node"
    
    print("\n✓ Graph structure validation passed!")

if __name__ == "__main__":
    print("\n🚀 Starting Gemini AI Integration Tests\n")
    
    try:
        test_xai_explanation()
        test_knowledge_graph()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        print("\nGemini AI integration is working correctly.")
        print("XAI explanations and knowledge graphs are being generated.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
