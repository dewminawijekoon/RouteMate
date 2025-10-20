# Backend setup (Windows / PowerShell)

## Prerequisites
1. Install Python 3.13.1
2. Install `uv` (https://docs.astral.sh/uv/getting-started/installation/)

## 1) Create a virtual environment
Open PowerShell in the `backend` folder and run:
```powershell
uv venv
```

## 2) Activate the virtual environment (PowerShell)

### PowerShell (default):
```powershell
.venv\Scripts\Activate.ps1
# You should see the venv name in your prompt, e.g. '(.venv) PS D:\RouteMate\backend>'
```

If PowerShell blocks the activation script due to execution policy, either temporarily allow scripts or use the cmd-style activator:
```powershell
# Temporarily bypass for the current PowerShell session (run this once before activation)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
# Then run the activation
.\.venv\Scripts\Activate.ps1
# Or use the cmd-style activator from PowerShell
.\.venv\Scripts\activate.bat
```

### Command Prompt (cmd.exe):
```cmd
.venv\Scripts\activate.bat
```

### Git Bash / WSL-style shells:
```bash
source .venv/Scripts/activate
```

## 3) Install dependencies with uv
```powershell
uv sync
```

## 4) Run the FastAPI backend with uvicorn
Replace `app.main:app` with the import path to your FastAPI app (module:variable).

```powershell
# Run with auto-reload for development
uv run uvicorn main:app
```
or 

```powershell
fastapi dev main.py
```

Open http://127.0.0.1:8000 in your browser or API client. FastAPI also provides an interactive API docs at http://127.0.0.1:8000/docs.

## 5) Update dependencies before committing
After adding or updating packages during development, update your dependencies:

```powershell
uv sync  # Install any new dependencies
uv lock  # Generate/update uv.lock with pinned versions
```

Commit the updated `uv.lock` file with your changes. This ensures everyone uses the exact same dependency versions.