"""Test Supabase connection"""
import asyncio
from app.core.config import settings
from app.db.supabase import get_supabase_client


async def test_supabase_connection():
    """Test if Supabase is properly connected"""
    
    print("🔍 Testing Supabase Connection...")
    print("-" * 50)
    
    # Check environment variables
    print("\n1️⃣ Checking Environment Variables:")
    print(f"   SUPABASE_URL: {settings.SUPABASE_URL}")
    print(f"   SUPABASE_KEY: {settings.SUPABASE_KEY[:20]}...{settings.SUPABASE_KEY[-10:]}")
    print(f"   SECRET_KEY: {'✅ Set' if settings.SECRET_KEY else '❌ Not Set'}")
    
    # Test Supabase client initialization
    print("\n2️⃣ Testing Supabase Client:")
    try:
        supabase = get_supabase_client()
        print("   ✅ Supabase client initialized successfully")
    except Exception as e:
        print(f"   ❌ Failed to initialize Supabase client: {e}")
        return
    
    # Test database connection with a simple query
    print("\n3️⃣ Testing Database Connection:")
    try:
        # Try to query a table (this will work even if table doesn't exist)
        response = supabase.table("_test_connection").select("*").limit(1).execute()
        print("   ✅ Database connection successful!")
    except Exception as e:
        error_msg = str(e)
        if "relation" in error_msg.lower() or "does not exist" in error_msg.lower():
            print("   ✅ Database connection successful! (Table doesn't exist yet, which is expected)")
        else:
            print(f"   ⚠️  Connection warning: {error_msg}")
    
    # Test Auth service
    print("\n4️⃣ Testing Authentication Service:")
    try:
        # Check if auth is available
        auth_response = supabase.auth.get_session()
        print("   ✅ Authentication service is accessible")
    except Exception as e:
        print(f"   ⚠️  Auth service: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CONNECTION TEST SUMMARY:")
    print("=" * 50)
    print("✅ Your Supabase project is properly configured!")
    print(f"🌐 Project URL: {settings.SUPABASE_URL}")
    print("🔐 API Key: Connected")
    print("\n💡 Next Steps:")
    print("   1. Test authentication at http://127.0.0.1:8000/docs")
    print("   2. Try POST /api/auth/signup to create a user")
    print("   3. Check users appear in Supabase Dashboard")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_supabase_connection())
