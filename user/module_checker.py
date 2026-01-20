import subprocess
import argparse
import time

def check_modules(demo_mode=False):
    """
    Checks and lists currently loaded kernel modules by reading /proc/modules.

    This function retrieves the contents of /proc/modules and displays them
    in a user-friendly format.
    """
    print("Checking loaded kernel modules...")
    
    if demo_mode:
        time.sleep(1)
        print("Loaded Kernel Modules:")
        print("rootkit_detector 16384 0 - Live 0x0000000000000000 (OE)")
        print("module_checker 16384 0 - Live 0x0000000000000000 (OE)")
        print("process_scanner 16384 0 - Live 0x0000000000000000 (OE)")
        print("[INFO] Module integrity check passed. No hidden modules detected.")
        return

    try:
        # Read the /proc/modules file
        result = subprocess.run(["cat", "/proc/modules"], capture_output=True, text=True, check=True)
        modules = result.stdout.strip()

        if modules:
            print("Loaded Kernel Modules:")
            print(modules)
        else:
            print("[INFO] No kernel modules are currently loaded (unlikely scenario).")
    
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to read /proc/modules: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run in Demo Mode")
    args = parser.parse_args()
    check_modules(args.demo)
