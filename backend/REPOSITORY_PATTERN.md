# Repository Pattern in RouteMate Backend

## 📚 What is the Repository Pattern?

The **Repository Pattern** is a design pattern that creates an abstraction layer between the business logic and data access layers. It encapsulates all database operations in dedicated repository classes.

## 🎯 Why Use Repositories?

### Benefits

✅ **Separation of Concerns**
- Business logic is separated from database queries
- Easier to understand and maintain code
- Clear responsibility boundaries

✅ **Testability**
- Mock repositories in unit tests
- Test business logic without database
- Faster test execution

✅ **Reusability**
- Common queries in one place
- No code duplication
- Consistent data access patterns

✅ **Flexibility**
- Easy to switch databases
- Change queries without affecting business logic
- Centralized query optimization

✅ **Type Safety**
- Typed method signatures
- IDE autocomplete support
- Catch errors at development time

## 📁 Repository Structure

```
app/repositories/
├── __init__.py              # Package documentation
├── base.py                  # BaseRepository with common CRUD
├── bus_repository.py        # Bus-specific operations
├── route_repository.py      # Route-specific operations
└── user_repository.py       # User-specific operations
```

## 🔧 Components

### 1. BaseRepository (`base.py`)

Generic repository with common CRUD operations that all specific repositories inherit from.

**Methods:**
- `get_all()` - Get all records
- `get_by_id()` - Get single record by ID
- `create()` - Create new record
- `update()` - Update existing record
- `delete()` - Delete record
- `filter_by()` - Filter by field values
- `count()` - Count total records

### 2. BusRepository (`bus_repository.py`)

Bus-specific database operations.

**Custom Methods:**
- `get_by_route()` - Get buses for a route
- `get_by_bus_number()` - Find bus by number
- `get_active_buses()` - Get currently active buses
- `update_location()` - Update GPS coordinates
- `search_buses()` - Search by bus number

### 3. RouteRepository (`route_repository.py`)

Route-specific database operations.

**Custom Methods:**
- `get_by_route_number()` - Find route by number
- `get_routes_with_buses()` - Get routes with bus info
- `search_routes()` - Search by location
- `get_routes_by_stops()` - Find routes with specific stop
- `get_popular_routes()` - Get most used routes

### 4. UserRepository (`user_repository.py`)

User-specific database operations.

**Custom Methods:**
- `get_by_email()` - Find user by email
- `create_user()` - Create new user
- `update_profile()` - Update user info
- `get_user_favorites()` - Get user's favorites
- `add_favorite()` - Add to favorites
- `remove_favorite()` - Remove from favorites
- `get_users_by_role()` - Filter by role

## 💻 Usage Examples

### In API Endpoints (Dependency Injection)

```python
from fastapi import APIRouter, Depends
from app.repositories.bus_repository import BusRepository

router = APIRouter()

# Create dependency function
def get_bus_repository(supabase: Client = Depends(get_supabase_client)) -> BusRepository:
    return BusRepository(supabase)

# Use in endpoint
@router.get("/buses")
async def get_buses(repository: BusRepository = Depends(get_bus_repository)):
    buses = await repository.get_all()
    return {"buses": buses}
```

### In Services (Business Logic)

```python
from app.repositories.route_repository import RouteRepository

class RouteService:
    def __init__(self, route_repo: RouteRepository):
        self.route_repo = route_repo
    
    async def find_best_route(self, start: str, end: str):
        # Business logic using repository
        routes = await self.route_repo.search_routes(start, end)
        # Process routes...
        return best_route
```

### Direct Usage

```python
from app.db.supabase import get_supabase_client
from app.repositories.user_repository import UserRepository

supabase = get_supabase_client()
user_repo = UserRepository(supabase)

# Get user by email
user = await user_repo.get_by_email("user@example.com")

# Create new user
new_user = await user_repo.create_user(
    email="new@example.com",
    name="New User"
)
```

## 🧪 Testing with Repositories

Repositories make testing easier by allowing mocking:

```python
from unittest.mock import AsyncMock
import pytest

@pytest.fixture
def mock_bus_repository():
    repo = AsyncMock(spec=BusRepository)
    repo.get_all.return_value = [
        {"id": "1", "bus_number": "138"},
        {"id": "2", "bus_number": "177"}
    ]
    return repo

async def test_get_buses(mock_bus_repository):
    # Use mock repository in test
    buses = await mock_bus_repository.get_all()
    assert len(buses) == 2
    assert buses[0]["bus_number"] == "138"
```

## 📝 Adding New Repositories

### Step 1: Create Repository File

Create `app/repositories/station_repository.py`:

```python
from typing import List, Dict, Any
from supabase import Client
from app.repositories.base import BaseRepository

class StationRepository(BaseRepository):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "stations")
    
    async def get_nearby_stations(self, lat: float, lon: float, radius: float):
        # Custom query logic
        pass
```

### Step 2: Use in Endpoints

Update `app/api/stations.py`:

```python
from app.repositories.station_repository import StationRepository

def get_station_repository(supabase: Client = Depends(get_supabase_client)):
    return StationRepository(supabase)

@router.get("/nearby")
async def get_nearby(
    lat: float,
    lon: float,
    repository: StationRepository = Depends(get_station_repository)
):
    stations = await repository.get_nearby_stations(lat, lon, 5.0)
    return {"stations": stations}
```

## 🎨 Best Practices

### ✅ DO

- Keep repositories focused on data access only
- Use descriptive method names
- Return consistent data types
- Handle errors at the repository level
- Document complex queries
- Use type hints

### ❌ DON'T

- Put business logic in repositories
- Mix multiple concerns in one method
- Return different types from same method
- Ignore error handling
- Create overly generic methods

## 🔄 Repository vs Direct Database Access

### ❌ Without Repository (Direct Access)

```python
@router.get("/buses")
async def get_buses(supabase: Client = Depends(get_supabase_client)):
    # Query logic in endpoint
    response = supabase.table("buses").select("*").execute()
    return {"buses": response.data}
```

**Problems:**
- Query logic scattered across endpoints
- Hard to test
- Duplicated queries
- Tight coupling to Supabase

### ✅ With Repository

```python
@router.get("/buses")
async def get_buses(repository: BusRepository = Depends(get_bus_repository)):
    # Clean, testable, reusable
    buses = await repository.get_all()
    return {"buses": buses}
```

**Benefits:**
- Clean separation
- Easy to test and mock
- Reusable queries
- Loose coupling

## 🚀 Advanced Patterns

### Combining Repositories in Services

```python
class BusTrackingService:
    def __init__(
        self,
        bus_repo: BusRepository,
        route_repo: RouteRepository
    ):
        self.bus_repo = bus_repo
        self.route_repo = route_repo
    
    async def get_route_with_active_buses(self, route_id: str):
        route = await self.route_repo.get_by_id(route_id)
        buses = await self.bus_repo.get_by_route(route_id)
        active_buses = [b for b in buses if b["status"] == "active"]
        
        return {
            "route": route,
            "active_buses": active_buses,
            "bus_count": len(active_buses)
        }
```

### Transaction Support (Future)

```python
class TransactionalRepository:
    async def create_with_transaction(self, data):
        async with self.supabase.transaction():
            # Multiple operations in transaction
            result1 = await self.table1.insert(data1)
            result2 = await self.table2.insert(data2)
            return result1, result2
```

## 📚 Further Reading

- [Repository Pattern - Martin Fowler](https://martinfowler.com/eaaCatalog/repository.html)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)

## 🎓 Summary

The Repository Pattern provides:
1. **Clean Architecture** - Separates concerns
2. **Better Testing** - Easy to mock
3. **Code Reuse** - DRY principle
4. **Flexibility** - Easy to change database
5. **Type Safety** - Better IDE support

Use repositories to keep your codebase maintainable, testable, and scalable! 🚀
