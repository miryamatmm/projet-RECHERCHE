from common import *

def main():
        run_admin_command("docker compose down postgres")
        run_admin_command("docker compose down nginx")
        terminate_processes()

import os
import signal

def terminate_processes():
    try:
        with open(PROD_PIDS_PATH, 'r') as pid_file:
            for line in pid_file:
                pid = int(line.strip())
                try:
                    os.kill(pid, signal.SIGTERM)  # Send SIGTERM to gracefully terminate the process
                    print(f"Terminated process with PID: {pid}")
                except ProcessLookupError:
                    print(f"Process with PID {pid} not found.")
                except PermissionError:
                    print(f"Permission denied to kill process {pid}.")
        os.remove(PROD_PIDS_PATH)
        print(f"PID file {PROD_PIDS_PATH} removed.")
    except FileNotFoundError:
        print(f"PID file {PROD_PIDS_PATH} not found.")

if __name__ == "__main__":
    main()