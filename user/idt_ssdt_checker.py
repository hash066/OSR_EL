import subprocess
import argparse
import time

def check_idt_ssdt(demo_mode=False):
    """
    Checks kernel logs for entries related to IDT and SSDT integrity.

    This function uses `dmesg` to search for log entries mentioning IDT and SSDT,
    typically indicating anomalies or integrity checks logged by kernel modules.
    """
    print("Checking IDT and SSDT integrity...")

    if demo_mode:
        time.sleep(1.2)
        print("Potential IDT or SSDT anomalies detected:")
        print("- [WARNING] IDT entry 0x80 corrupted or hooked.")
        print("- [WARNING] SSDT index 12 (NtOpenProcess) mismatch. Expected: 0xFFFFF8000420, Found: 0xFFFFF8000999")
        return

    try:
        # Run the dmesg command and capture the output
        result = subprocess.run(["dmesg"], capture_output=True, text=True, check=True)
        logs = result.stdout

        # Filter for lines containing both "IDT" and "SSDT"
        relevant_logs = [line for line in logs.splitlines() if "IDT" in line and "SSDT" in line]

        if relevant_logs:
            print("Potential IDT or SSDT anomalies detected:")
            for log_entry in relevant_logs:
                print(f"- {log_entry}")
        else:
            print("No IDT or SSDT anomalies found in kernel logs.")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to retrieve kernel logs: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run in Demo Mode")
    args = parser.parse_args()
    check_idt_ssdt(args.demo)
