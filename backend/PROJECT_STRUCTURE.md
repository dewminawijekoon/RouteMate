# RouteMate Backend Project Structure

This document explains the organization of the RouteMate backend codebase.

## 📁 Directory Structure

```
backend/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       ├── router.py         # Router aggregation
│   │       ├── health.py         # Health check endpoints
│   │       ├── buses.py          # Bus-related endpoints
│   │       ├── routes.py         # Route-related endpoints
│   │       └── users.py          # User-related endpoints
│   │
│   ├── core/                     # Core application config
│   │   ├── __init__.py
│   │   └── config.py             # Settings & configuration
│   │
│   ├── db/                       # Database layer
│   │   ├── __init__.py
│   │   └── supabase.py           # Supabase client
│   │
│   ├── repositories/             # Data access layer (NEW!)
│   │   ├── __init__.py
│   │   ├── base.py              # Base repository with CRUD
│   │   ├── bus_repository.py    # Bus data operations
│   │   ├── route_repository.py  # Route data operations
│   │   └── user_repository.py   # User data operations
│   │
│   ├── models/                   # Database models (optional)
│   │   └── __init__.py
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   └── common.py             # Common schemas
│   │
│   ├── services/                 # Business logic layer
│   │   └── __init__.py
│   │
│   ├── middleware/               # Custom middleware
│   │   ├── __init__.py
│   │   └── cors.py               # CORS configuration
│   │
│   └── utils/                    # Utility functions
│       └── __init__.py
│
├── tests/                        # Test suite
│   ├── conftest.py               # Test configuration
│   └── test_health.py            # Health endpoint tests
│
├── main.py                       # Application entry point
├── pyproject.toml                # Project dependencies
├── uv.lock                       # Locked dependencies
├── .env.example                  # Environment template
├── .env                          # Your environment (create this)
├── .gitignore                    # Git ignore rules
└── README.md                     # Setup documentation
```

## 📦 Key Components

### `main.py`
- Application entry point
- FastAPI app initialization
- Router registration
- Middleware setup

### `app/core/config.py`
- Centralized configuration using Pydantic Settings
- Environment variable loading
- Settings validation

### `app/db/supabase.py`
- Supabase client initialization
- Database connection management
- Admin client for server-side operations

### `app/repositories/`
- **Data access layer** using Repository Pattern
- Encapsulates all database queries
- Separates data access from business logic
- Makes code more testable and maintainable
- See `REPOSITORY_PATTERN.md` for detailed guide

### `app/api/`
- API version 1 endpoints
- Organized by resource (buses, routes, users)
- Router aggregation in `router.py`
- Uses repositories via dependency injection

### `app/schemas/`
- Pydantic models for request/response validation
- Type-safe data structures
- Documentation generation

### `app/services/`
- Business logic layer
- Complex operations
- Reusable service functions

### `app/middleware/`
- Custom middleware components
- CORS configuration
- Authentication/logging (future)

## 🔧 Configuration

### Environment Variables (.env)
Copy `.env.example` to `.env` and configure:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
SECRET_KEY=generate-with-openssl
```

## 🚀 Adding New Features

### 1. Add a New Endpoint
1. Create/edit file in `app/api/` (e.g., `stations.py`)
2. Define routes with FastAPI decorators
3. Add router to `app/api/router.py`

### 2. Add Business Logic
1. Create service in `app/services/` (e.g., `station_service.py`)
2. Implement functions
3. Use in API endpoints

### 3. Add Data Models
1. Define Pydantic schemas in `app/schemas/`
2. Use for request/response validation

### 4. Add Database Operations
- Use Supabase client from `app/db/supabase.py`
- Query tables directly via API endpoints or services

## 📝 Best Practices

### File Organization
- **One resource per file** in `app/api/`
- **Related schemas together** in `app/schemas/`
- **Reusable logic** in `app/services/`

### Naming Conventions
- **Files**: lowercase with underscores (`bus_service.py`)
- **Classes**: PascalCase (`BusService`)
- **Functions**: lowercase with underscores (`get_bus_by_id`)
- **Constants**: UPPERCASE (`MAX_RETRY_COUNT`)

### Dependency Injection
Use FastAPI's `Depends()` for:
- Database connections
- Authentication
- Configuration access

Example:
```python
from fastapi import Depends
from app.db.supabase import get_supabase_client

@router.get("/")
async def get_items(supabase: Client = Depends(get_supabase_client)):
    # Use supabase client
    pass
```

## 🧪 Testing

- Tests in `tests/` directory
- Run with: `uv run pytest`
- Test coverage: `uv run pytest --cov`

## 📚 API Documentation

Once running, visit:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🔐 Security Notes

- Never commit `.env` file
- Use service key only for admin operations
- Validate all input with Pydantic schemas
- Use Supabase RLS (Row Level Security) policies
