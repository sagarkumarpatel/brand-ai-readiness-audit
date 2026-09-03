import sys
import os
import subprocess

def main():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(root_dir, "scripts", "audit-orchestrator.py")
    
    # Forward all arguments directly to the existing script
    result = subprocess.run(
        [sys.executable, script_path] + sys.argv[1:],
    )
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
