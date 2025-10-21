"""Quick test to check if user exists and sign in works"""
import asyncio
from app.db.supabase import get_supabase_client
from app.schemas.auth import UserSignUp, UserSignIn
from app.services.auth_service import AuthService


async def test_auth_flow():
    """Test authentication with the user's email"""
    
    supabase = get_supabase_client()
    auth_service = AuthService(supabase)
    
    test_email = "ranugaweerasekara2@gmail.com"
    test_password = "string"
    
    print("🔍 Testing Authentication Flow...")
    print("=" * 60)
    print(f"Email: {test_email}")
    print("=" * 60)
    
    # Test 1: Try to sign in first
    print("\n1️⃣ Attempting to sign in...")
    try:
        signin_data = UserSignIn(email=test_email, password=test_password)
        response = await auth_service.sign_in(signin_data)
        print("✅ Sign in successful!")
        print(f"   User ID: {response.user['id']}")
        print(f"   Email: {response.user['email']}")
        print(f"   Token: {response.access_token[:50]}...")
        return
    except Exception as e:
        print(f"❌ Sign in failed: {str(e)}")
        print("\n   This means the user doesn't exist or password is wrong.")
    
    # Test 2: Try to sign up
    print("\n2️⃣ Attempting to sign up...")
    try:
        signup_data = UserSignUp(
            email=test_email,
            password=test_password,
            full_name="Ranuga Weerasekara"
        )
        response = await auth_service.sign_up(signup_data)
        print("✅ Sign up successful!")
        print(f"   User ID: {response.user['id']}")
        print(f"   Email: {response.user['email']}")
        print(f"   Token: {response.access_token[:50]}...")
        
        print("\n📧 IMPORTANT:")
        print("   If you don't receive a token above, check your email!")
        print("   Supabase may require email confirmation.")
        
    except Exception as e:
        error_msg = str(e)
        if "already" in error_msg.lower() or "exists" in error_msg.lower():
            print(f"❌ User already exists!")
            print(f"   Error: {error_msg}")
            print("\n💡 Solutions:")
            print("   1. The user exists but you used wrong password")
            print("   2. Or email confirmation is pending - check your email")
            print("   3. Try password reset if you forgot the password")
        else:
            print(f"❌ Sign up failed: {error_msg}")
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY:")
    print("=" * 60)
    print("If sign in failed AND sign up failed with 'already exists':")
    print("  → User exists but password is wrong")
    print("  → OR email confirmation is required")
    print("\nIf sign up succeeded:")
    print("  → Check for email confirmation requirement")
    print("  → Try signing in again")
    print("\nCheck Supabase Dashboard:")
    print("  → Authentication → Users")
    print("  → Look for:", test_email)
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_auth_flow())
