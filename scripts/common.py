import subprocess
import os
import shutil
import sys
import logging
import time
from pathlib import Path

DB_STARTUP_TIME=5 #in seconds

project_dir = Path(__file__).resolve().parent.parent
backend_path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), ".."), "backend"))
sys.path.insert(0, backend_path)

PROD_PIDS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '.prod_pids'))


from env import *

logger = logger

logger.addHandler(logging.StreamHandler())

#=============================================
#============  OS MGMT      ==================
#=============================================

def run_user_command(command, options = {'cwd': project_dir}):
        return subprocess.run(command.split(), **options)

def run_admin_command(command, options = {'cwd': project_dir}):
    """Run a command with administrative privileges."""
    print("command: ", command)
    if os.name == "nt":
        return subprocess.run(["powershell", "Start-Process", "cmd", "-ArgumentList", f"'/c {command}'", "-Verb", "runAs"], **options)
    else:
        return subprocess.run(["sudo"] + command.split(), **options)

def run_user_command_popen(command, options = {'cwd': project_dir}):
    """Run a command using subprocess.Popen."""
    # Split the command into a list and start the process
    return subprocess.Popen(command.split(), **options)

def remove_folder(relative_path):
    """Remove a folder relative to the project_dir path."""
    data_path = os.path.abspath(os.path.join(project_dir, relative_path))
    if os.path.exists(data_path):
        confirm = input(f"Are you sure you want to remove {data_path}? (yes/no): ")
        if confirm.lower() == "yes":
            if os.name == "nt":
                run_admin_command("rmdir /s /q " + data_path)
            else:
                run_admin_command("rm -rf " + data_path)
            logger.info("Folder removed.")
        else:
            logger.info("Folder not removed.")
 
def create_folder(relative_path):
    """Create a folder relative to the project_dir path."""
    os.makedirs(os.path.join(project_dir, relative_path), exist_ok=True)
            
#=============================================
#=========  DOCKER SERVICES ==================
#=============================================

def is_service_running(service_name):
    """Check if a Docker service is running."""
    result = run_admin_command(f"docker ps --filter name={service_name} " + "--format {{.Names}}", {'cwd': project_dir, 'capture_output': True, 'text': True})
    output = service_name in result.stdout.strip()
    if output:
        logger.info(f"{service_name} is running.")
    else:
        logger.info(f"{service_name} is not running.")
    return output