# 🚀 Quick Setup Guide

## Step 1: Install Dependencies
```powershell
cd backend
uv sync
```

## Step 2: Configure Environment
```powershell
# Copy the example environment file
Copy-Item .env.example .env

# Edit .env with your actual Supabase credentials
notepad .env
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon/public key
- `SECRET_KEY`: Generate with `openssl rand -hex 32`

## Step 3: Run the Server
```powershell
# Development mode (auto-reload)
uv run uvicorn main:app --reload

# Or use FastAPI CLI
uv run fastapi dev main.py
```

## Step 4: Test the API
Visit:
- Root: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health
- API: http://127.0.0.1:8000/api/health/
- Docs: http://127.0.0.1:8000/docs

## API Endpoints

### Core
- `GET /` - API information
- `GET /health` - Basic health check

### API (`/api`)
- `GET /health/` - Detailed health check
- `GET /buses/` - List all buses
- `GET /buses/{bus_id}` - Get specific bus
- `GET /routes/` - List all routes
- `GET /routes/{route_id}` - Get specific route
- `GET /users/me` - Get current user (TODO)
- `GET /users/{user_id}` - Get user by ID

## Testing
```powershell
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# View coverage report
start htmlcov/index.html
```

## Next Steps

1. **Set up Supabase Database**
   - Create tables: `buses`, `routes`, `users`
   - Configure RLS policies
   - Add sample data

2. **Implement Authentication**
   - Add JWT token handling
   - Implement login/signup endpoints
   - Add protected routes

3. **Add More Features**
   - Real-time bus tracking
   - Route planning
   - User preferences
   - Notifications

## Troubleshooting

### Import errors
If you see import errors in your IDE:
```powershell
# Activate the virtual environment
. .venv\Scripts\Activate.ps1

# Verify Python can find the app module
python -c "import app; print(app.__version__)"
```

### Supabase connection errors
- Verify your `.env` file has correct credentials
- Check if Supabase project is active
- Test connection at https://supabase.com/dashboard

### Port already in use
```powershell
# Find and kill process on port 8000
netstat -aon | Select-String ":8000"
taskkill /PID <PID> /F
```
