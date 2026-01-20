import os
import argparse
import sys
import time
import random
import subprocess

def load_module(module_name, demo_mode=False):
    """
    Load a kernel module using insmod.
    
    Args:
        module_name (str): The name of the kernel module (without .ko extension).
        demo_mode (bool): If True, simulate loading without actual commands.
    
    Returns:
        None
    """
    print(f"Attempting to load module: {module_name}")
    if demo_mode:
        time.sleep(random.uniform(0.5, 1.5)) # Simulate delay
        print(f"[INFO] Module {module_name} loaded successfully. (DEMO)")
        return

    result = os.system(f"sudo insmod {module_name}.ko")
    if result != 0:
        print(f"[ERROR] Failed to load module: {module_name}")
    else:
        print(f"[INFO] Module {module_name} loaded successfully.")

def unload_module(module_name, demo_mode=False):
    """
    Unload a kernel module using rmmod.
    
    Args:
        module_name (str): The name of the kernel module.
        demo_mode (bool): If True, simulate unloading without actual commands.
    
    Returns:
        None
    """
    print(f"Attempting to unload module: {module_name}")
    if demo_mode:
        time.sleep(0.5)
        print(f"[INFO] Module {module_name} unloaded successfully. (DEMO)")
        return

    result = os.system(f"sudo rmmod {module_name}")
    if result != 0:
        print(f"[ERROR] Failed to unload module: {module_name}")
    else:
        print(f"[INFO] Module {module_name} unloaded successfully.")

def main():
    """
    Main function to manage the loading and unloading of kernel modules.
    
    Modules are loaded sequentially, and the user is prompted to proceed 
    with unloading them.
    """
    parser = argparse.ArgumentParser(description="Rootkit Detector CLI")
    parser.add_argument("command", nargs='?', default="full-scan", choices=["scan-processes", "check-modules", "check-idt-ssdt", "scan-files", "full-scan"], help="Command to run")
    parser.add_argument("--demo", action="store_true", help="Run in Demo Mode (simulation)")
    args = parser.parse_args()

    modules_map = {
        "scan-processes": ["process_scanner"],
        "check-modules": ["module_checker"],
        "check-idt-ssdt": ["idt_ssdt_checker"],
        "scan-files": ["file_scanner"],
        "full-scan": ["syscall_checker", "process_scanner", "idt_ssdt_checker", "file_scanner", "module_checker"]
    }

    selected_modules = modules_map.get(args.command, [])
    
    print(f"[INFO] Starting Rootkit Detector ({'DEMO MODE' if args.demo else 'REAL MODE'})...")

    print("[INFO] Loading modules...")
    for module in selected_modules:
        load_module(module, args.demo)

    print("[INFO] Modules loaded. Performing checks...")
    
    if args.demo:
        print(f"[INFO] Simulating checks for {args.command}...")
        script_map = {
            "scan-processes": "process_scanner.py",
            "check-modules": "module_checker.py",
            "check-idt-ssdt": "idt_ssdt_checker.py",
            "scan-files": "file_scanner.py",
            "full-scan": None 
        }
        
        scripts_to_run = []
        if args.command == "full-scan":
            scripts_to_run = ["process_scanner.py", "module_checker.py", "idt_ssdt_checker.py", "file_scanner.py"]
        else:
            scripts_to_run = [script_map[args.command]]
            
        for script in scripts_to_run:
            print(f"\n--- Running {script} ---")
            subprocess_cmd = [sys.executable, os.path.join(os.path.dirname(__file__), script), "--demo"]
            subprocess.run(subprocess_cmd)
            
    else:
         print("[INFO] Modules loaded. Check 'dmesg' or run individual scripts for details.")
    
    print("\n[INFO] Checks complete.")
    input("Press Enter to unload modules...")

    print("[INFO] Unloading modules...")
    for module in selected_modules:
        unload_module(module, args.demo)

    print("[INFO] Modules unloaded. System cleanup complete.")

if __name__ == "__main__":
    main()
