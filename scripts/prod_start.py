from common import *

backend_path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), ".."), "backend"))
sys.path.insert(0, backend_path)

from env import *

def main():
        run_admin_command("docker compose up -d postgres")
        run_admin_command("docker compose up -d nginx")

        run_user_command("npm install", {'cwd': project_dir / 'frontend'})
        run_user_command("npm run build", {'cwd':  project_dir / 'frontend'})
    
        procs = []
        procs.extend([
                run_user_command_popen("uvicorn main:app --reload",  {'cwd': project_dir / 'backend'})
        ])
        if qwen_enabled:
            procs.extend([
                    run_user_command_popen("uvicorn qwen:app --host 0.0.0.0 --port 8888 ",  {'cwd': project_dir / 'llm'})
            ])
            
        if biobert_enabled:
            procs.extend([
                    run_user_command_popen("uvicorn biobert:app --host 0.0.0.0 --port 8889 ",  {'cwd': project_dir / 'llm'})
            ])
            
        with open(PROD_PIDS_PATH, 'w') as pid_file:
                for proc in procs:
                        pid_file.write(f"{proc.pid}\n")  # Write the PID followed by a newline
        
if __name__ == "__main__":
    main()