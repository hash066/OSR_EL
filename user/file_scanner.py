import os
import subprocess
import argparse
import time

def scan_files(demo_mode=False):
    """
    Scans kernel logs for entries related to found files or hidden files.

    This function runs `dmesg` and filters the output for entries containing
    "Found file" or any relevant logs related to file scanning.
    """
    print("Scanning for hidden files...")
    
    if demo_mode:
        time.sleep(1.5)
        print("Hidden files or scanned entries detected:")
        print("- [ALERT] Found hidden file: /etc/.rootkit_config (hidden attribute set)")
        print("- [ALERT] Found hidden file: /tmp/.hidden_payload (not visible in ls)")
        return

    try:
        # Execute the dmesg command and capture its output
        result = subprocess.run(["dmesg"], capture_output=True, text=True, check=True)
        logs = result.stdout
        
        # Filter for lines mentioning "Found file"
        hidden_files = [line for line in logs.splitlines() if "Found entry" in line]

        if hidden_files:
            print("Hidden files or scanned entries detected:")
            for file_entry in hidden_files:
                print(f"- {file_entry}")
        else:
            print("No hidden files or suspicious entries found.")
    
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to retrieve kernel logs: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run in Demo Mode")
    args = parser.parse_args()
    scan_files(args.demo)
