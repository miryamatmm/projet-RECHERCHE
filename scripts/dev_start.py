import subprocess
import atexit

from common import *
backend_path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), ".."), "backend"))
sys.path.insert(0, backend_path)

from env import *

subprocesses = []

def terminate_subprocesses():
    """Terminate all subprocesses when the script exits."""
    for proc in subprocesses:
        proc.terminate()
        proc.wait()
    run_admin_command("docker compose down postgres")
    
atexit.register(terminate_subprocesses)

def main():
    run_admin_command('docker pull postgres')
    run_admin_command("docker compose up -d postgres")

    run_user_command("npm install", {'cwd': project_dir / 'frontend'})
    
    subprocesses.extend([
        run_user_command_popen("npm run dev", {'cwd': project_dir / 'frontend'}),
        run_user_command_popen("uvicorn main:app --reload",  {'cwd': project_dir / 'backend'}),
    ])
    
    if qwen_enabled:
        subprocesses.extend([
            run_user_command_popen("uvicorn qwen:app --host 0.0.0.0 --port 8888",  {'cwd': project_dir / 'llm'})
        ])
        
    if biobert_enabled:
        subprocesses.extend([
            run_user_command_popen("uvicorn biobert:app --host 0.0.0.0 --port 8889 --reload",  {'cwd': project_dir / 'llm'})
        ])
        
    
    for proc in subprocesses:
        proc.wait()

if __name__ == "__main__":
    main()
