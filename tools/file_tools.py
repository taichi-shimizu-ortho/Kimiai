import os
from pathlib import Path

# Workspace is set to the current working directory of the agent
WORKSPACE = Path("./workspace").resolve()

# Create workspace if it doesn't exist
WORKSPACE.mkdir(parents=True, exist_ok=True)

def safe_path(path: str) -> Path:
    p = (WORKSPACE / path).resolve()
    if not str(p).startswith(str(WORKSPACE)):
        raise ValueError(f"Workspace outside access is not allowed: {path}")
    return p

def read_file(path: str) -> str:
    p = safe_path(path)
    if not p.is_file():
        return f"Error: File not found {path}"
    return p.read_text(encoding="utf-8")

def write_file(path: str, content: str):
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def list_files(directory: str = "."):
    p = safe_path(directory)
    if not p.is_dir():
        return []
    return [str(x.relative_to(WORKSPACE)).replace('\\', '/') for x in p.rglob("*") if x.is_file()]
