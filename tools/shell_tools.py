import subprocess
import os

BLOCKED_COMMANDS = [
    "rm -rf",
    "shutdown",
    "reboot",
    "mkfs",
    "dd ",
    ":(){",
]

def run_shell(command: str, cwd="./workspace", timeout=30):
    for blocked in BLOCKED_COMMANDS:
        if blocked in command:
            raise ValueError(f"Blocked dangerous command: {command}")

    workspace_dir = os.path.abspath(cwd)
    os.makedirs(workspace_dir, exist_ok=True)

    try:
        result = subprocess.run(
            command,
            cwd=workspace_dir,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": "Command execution timed out.",
        }
    except Exception as e:
         return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
        }
