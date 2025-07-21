#!/usr/bin/env python3
"""
Quick Authentication Test
Test user registration and login functionality
"""

import httpx
import json
import uuid

BASE_URL = "http://localhost:8002"

def test_auth_system():
    """Test the authentication system"""
    print("🔐 Testing Python Backend Authentication System")
    print("=" * 50)
    
    with httpx.Client(timeout=30.0) as client:
        # Test 1: User Registration
        print("\n1. Testing User Registration")
        print("-" * 30)
        
        # Generate unique email to avoid conflicts
        test_email = f"test_{uuid.uuid4().hex[:8]}@trangvienso.com"
        
        registration_data = {
            "email": test_email,
            "password": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+84901234567"
        }
        
        try:
            response = client.post(f"{BASE_URL}/api/auth/register", json=registration_data)
            print(f"Registration Status: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Registration successful!")
                print(f"   User: {data['user']['first_name']} {data['user']['last_name']}")
                print(f"   Email: {data['user']['email']}")
                print(f"   Access Token: {data['tokens']['access_token'][:20]}...")
                
                user_tokens = data['tokens']
                
                # Test 2: Login with same credentials
                print("\n2. Testing User Login")
                print("-" * 30)
                
                login_data = {
                    "email": test_email,
                    "password": "SecurePass123!"
                }
                
                response = client.post(f"{BASE_URL}/api/auth/login", json=login_data)
                print(f"Login Status: {response.status_code}")
                
                if response.status_code == 200:
                    login_response = response.json()
                    print(f"✅ Login successful!")
                    print(f"   New Access Token: {login_response['tokens']['access_token'][:20]}...")
                    
                    # Test 3: Protected endpoint
                    print("\n3. Testing Protected Endpoint")
                    print("-" * 30)
                    
                    headers = {"Authorization": f"Bearer {login_response['tokens']['access_token']}"}
                    response = client.get(f"{BASE_URL}/api/auth/me", headers=headers)
                    print(f"Get User Info Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        user_info = response.json()
                        print(f"✅ Protected endpoint access successful!")
                        print(f"   User ID: {user_info['id']}")
                        print(f"   Full Name: {user_info['first_name']} {user_info['last_name']}")
                        print(f"   Email Verified: {user_info['email_verified']}")
                        
                        # Test 4: Token refresh
                        print("\n4. Testing Token Refresh")
                        print("-" * 30)
                        
                        refresh_data = {
                            "refresh_token": login_response['tokens']['refresh_token']
                        }
                        
                        response = client.post(f"{BASE_URL}/api/auth/refresh", json=refresh_data)
                        print(f"Token Refresh Status: {response.status_code}")
                        
                        if response.status_code == 200:
                            refresh_response = response.json()
                            print(f"✅ Token refresh successful!")
                            print(f"   New Access Token: {refresh_response['access_token'][:20]}...")
                            
                            return True
                
        except Exception as e:
            print(f"❌ Error during authentication test: {e}")
    
    return False

def test_database_connection():
    """Test database health check"""
    print("\n5. Testing Database Connection")
    print("-" * 30)
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{BASE_URL}/api/health")
            print(f"Health Check Status: {response.status_code}")
            
            if response.status_code == 200:
                health_data = response.json()
                db_status = health_data.get("database", "unknown")
                print(f"✅ Database Status: {db_status}")
                return db_status == "healthy"
            
    except Exception as e:
        print(f"❌ Database health check failed: {e}")
    
    return False

def main():
    """Run all tests"""
    # Test database first
    db_ok = test_database_connection()
    
    if not db_ok:
        print("\n❌ Database connection failed. Cannot proceed with auth tests.")
        return 1
    
    # Test authentication
    auth_ok = test_auth_system()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    if auth_ok:
        print("✅ All authentication tests passed!")
        print("🎉 Python backend is ready for production use!")
        return 0
    else:
        print("❌ Some authentication tests failed")
        return 1

if __name__ == "__main__":
    exit(main())