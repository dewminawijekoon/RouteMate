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

---

## API Endpoints

Current app entry is `main.py` exposing `app`.

### Available Routes

- **GET /** → Health/welcome check
  
  Example request (PowerShell):
  ```powershell
  # Using curl.exe (not PowerShell's Invoke-WebRequest alias)
  curl.exe http://127.0.0.1:8000/
  
  # Or using PowerShell's native cmdlet
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/" -Method GET
  ```
  
  Example response:
  ```json
  { "message": "Hello World" }
  ```

## Testing

Pytest is included in the dev dependency group. To run tests:

```powershell
uv run pytest
```

To run tests with coverage:
```powershell
uv run pytest --cov=. --cov-report=html
```

Create test files under a `tests/` directory (e.g., `tests/test_root.py`).

## Dependency Management

### Adding dependencies
```powershell
uv add <package>              # Add production dependency
uv add --group dev <package>  # Add development dependency
```

### Updating dependencies
```powershell
uv sync   # Sync environment with pyproject.toml
uv lock   # Update uv.lock with latest compatible versions
```

## Project Structure

```
backend/
  main.py            # FastAPI app entry point (exposes `app`)
  pyproject.toml     # Project metadata and dependencies
  uv.lock            # Locked dependency versions (commit this)
  README.md          # This file
  .venv/             # Virtual environment (do not commit)
```

## Troubleshooting (Windows / PowerShell)

### Execution policy error when activating venv
Use session-scoped policy (safest, affects only current terminal):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
. .venv\Scripts\Activate.ps1
```

Or use CurrentUser scope (persists):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
. .venv\Scripts\Activate.ps1
```

### Port already in use
Find and kill the process using port 8000:
```powershell
# Find process ID (PID) using port 8000
netstat -aon | Select-String ":8000"

# Kill process by PID (replace <PID> with actual number)
taskkill /PID <PID> /F
```

### Virtual environment not activating in VS Code
- Ensure your terminal profile is set to PowerShell
- Make sure you're in the `backend/` directory
- Try restarting VS Code

### Clean slate (reset environment)
If dependencies or environment get corrupted:
```powershell
# Remove the virtual environment
Remove-Item -Recurse -Force .venv

# Recreate and reinstall
uv venv
. .venv\Scripts\Activate.ps1
uv sync
```

## Notes

- Python version requirement: `>=3.13.1` (specified in `pyproject.toml`)
- App entry point: `main:app` (if you rename files or the app variable, update uvicorn commands accordingly)
- The app uses FastAPI with Uvicorn as the ASGI server