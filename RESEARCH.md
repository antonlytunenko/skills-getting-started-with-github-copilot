# Research: Make Launch JSON use venv to run the app (Issue #3)

## Problem Analysis

The `.vscode/launch.json` configuration for the "Launch Mergington WebApp" debug configuration does not specify a Python interpreter, so VS Code will use whatever Python is resolved globally (currently `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` — see `.vscode/launch.json` line 6–19). The project has a `.venv` virtual environment at the repository root (confirmed by `.venv/pyvenv.cfg`) containing Python 3.11.14 with all project dependencies installed. Running the app outside the venv means project dependencies (fastapi, uvicorn, httpx, watchfiles, pytest — see `requirements.txt`) may not be available to the debugger, causing launch failures.

## Affected Files

| File | Role |
|---|---|
| `.vscode/launch.json` | VS Code debug/launch configuration — the only file directly named in the issue |
| `.venv/pyvenv.cfg` | Confirms venv exists, its location, and Python version (3.11.14) |
| `requirements.txt` | Lists project runtime dependencies that must be available in the chosen interpreter |

## Technical Constraints

- The venv is located at `${workspaceFolder}/.venv` (confirmed by `.venv/pyvenv.cfg`).
- The venv Python binary path is `.venv/bin/python`.
- The `debugpy` launch type (`"type": "debugpy"`) supports a `"python"` key to specify the interpreter path (VS Code Python extension convention).
- The existing launch config uses `"module": "uvicorn"` rather than a script path, which is the correct approach for uvicorn; the interpreter selection is the only missing piece.
- No other VS Code settings files (e.g., `settings.json`) exist in `.vscode/` that could interfere.

## Open Questions

- Should the path use `${workspaceFolder}/.venv/bin/python` (cross-platform on macOS/Linux) or also handle Windows (`.venv/Scripts/python`)? The project appears macOS-only based on `.venv/pyvenv.cfg` (`macos-aarch64`), but the instruction does not state platform scope explicitly.
- The issue title references `launche.json` (typo) — confirmed the actual file is `.vscode/launch.json`.
