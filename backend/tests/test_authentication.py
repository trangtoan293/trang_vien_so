#!/usr/bin/env python3
"""
Complete Authentication System Test
Tests user registration, login, token refresh, and logout functionality
"""

import httpx
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8001"

def test_api_endpoint(client, method, endpoint, expected_status=200, data=None, headers=None):
    """Test an API endpoint with detailed response handling"""
    try:
        kwargs = {}
        if headers:
            kwargs["headers"] = headers
        
        if method == "GET":
            response = client.get(f"{BASE_URL}{endpoint}", **kwargs)
        elif method == "POST":
            response = client.post(f"{BASE_URL}{endpoint}", json=data, **kwargs)
        elif method == "PUT":
            response = client.put(f"{BASE_URL}{endpoint}", json=data, **kwargs)
        elif method == "DELETE":
            response = client.delete(f"{BASE_URL}{endpoint}", **kwargs)
        
        success = response.status_code == expected_status
        status_icon = "✅" if success else "❌"
        
        print(f"{status_icon} {method} {endpoint} - Status: {response.status_code}")
        
        # Show response details for successful requests
        if success and response.headers.get("content-type", "").startswith("application/json"):
            try:
                response_data = response.json()
                if "message" in response_data:
                    print(f"   💬 {response_data['message']}")
                if "user" in response_data:
                    user = response_data["user"]
                    print(f"   👤 User: {user.get('first_name', '')} {user.get('last_name', '')} ({user.get('email', '')})")
                if "tokens" in response_data:
                    print(f"   🔑 Access token received")
                if "session_id" in response_data:
                    print(f"   🔗 Session ID: {str(response_data['session_id'])[:8]}...")
            except:
                pass
        elif not success:
            try:
                error_data = response.json()
                print(f"   ❌ Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   ❌ Error: HTTP {response.status_code}")
        
        return success, response
        
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False, None

def main():
    """Run complete authentication system tests"""
    print("🔐 Python Backend Authentication System Tests")
    print("=" * 60)
    
    test_results = []
    user_tokens = None
    
    with httpx.Client(timeout=30.0) as client:
        # Test 1: Basic API status
        print("\n📊 1. Testing API Status")
        print("-" * 40)
        success, _ = test_api_endpoint(client, "GET", "/")
        test_results.append(("API Status", success))
        
        success, _ = test_api_endpoint(client, "GET", "/api/auth/")
        test_results.append(("Auth Router Status", success))
        
        # Test 2: User Registration
        print("\n🆕 2. Testing User Registration")
        print("-" * 40)
        
        registration_data = {
            "email": "test@trangvienso.com",
            "password": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+84901234567",
            "language": "vi",
            "timezone": "Asia/Ho_Chi_Minh"
        }
        
        success, response = test_api_endpoint(
            client, "POST", "/api/auth/register", 
            expected_status=201, data=registration_data
        )
        test_results.append(("User Registration", success))
        
        if success:
            user_data = response.json()
            user_tokens = {
                "access_token": user_data["tokens"]["access_token"],
                "refresh_token": user_data["tokens"]["refresh_token"]
            }
            print(f"   🎉 Registration successful! User ID: {user_data['user']['id']}")
        
        # Test 3: User Login
        print("\n🔓 3. Testing User Login")
        print("-" * 40)
        
        login_data = {
            "email": "test@trangvienso.com",
            "password": "SecurePass123!",
            "remember_me": False
        }
        
        success, response = test_api_endpoint(
            client, "POST", "/api/auth/login", 
            expected_status=200, data=login_data
        )
        test_results.append(("User Login", success))
        
        if success:
            login_response = response.json()
            user_tokens = {
                "access_token": login_response["tokens"]["access_token"],
                "refresh_token": login_response["tokens"]["refresh_token"]
            }
            print(f"   🎉 Login successful!")
        
        # Test 4: Protected Endpoints (if we have tokens)
        if user_tokens:
            print("\n🛡️ 4. Testing Protected Endpoints")
            print("-" * 40)
            
            auth_headers = {
                "Authorization": f"Bearer {user_tokens['access_token']}"
            }
            
            # Get current user info
            success, _ = test_api_endpoint(
                client, "GET", "/api/auth/me", 
                headers=auth_headers
            )
            test_results.append(("Get Current User", success))
            
            # Verify token
            success, _ = test_api_endpoint(
                client, "GET", "/api/auth/verify-token", 
                headers=auth_headers
            )
            test_results.append(("Verify Token", success))
            
            # Get user sessions
            success, _ = test_api_endpoint(
                client, "GET", "/api/auth/sessions", 
                headers=auth_headers
            )
            test_results.append(("Get User Sessions", success))
        
        # Test 5: Token Refresh
        if user_tokens:
            print("\n🔄 5. Testing Token Refresh")
            print("-" * 40)
            
            refresh_data = {
                "refresh_token": user_tokens["refresh_token"]
            }
            
            success, response = test_api_endpoint(
                client, "POST", "/api/auth/refresh", 
                data=refresh_data
            )
            test_results.append(("Token Refresh", success))
            
            if success:
                refresh_response = response.json()
                user_tokens["access_token"] = refresh_response["access_token"]
                print(f"   🔄 Token refreshed successfully!")
        
        # Test 6: Logout
        if user_tokens:
            print("\n🔒 6. Testing User Logout")
            print("-" * 40)
            
            auth_headers = {
                "Authorization": f"Bearer {user_tokens['access_token']}"
            }
            
            success, _ = test_api_endpoint(
                client, "POST", "/api/auth/logout", 
                headers=auth_headers
            )
            test_results.append(("User Logout", success))
        
        # Test 7: Health check with database
        print("\n🏥 7. Testing Health Endpoints")
        print("-" * 40)
        
        success, _ = test_api_endpoint(client, "GET", "/api/health")
        test_results.append(("Database Health Check", success))
        
        success, _ = test_api_endpoint(client, "GET", "/api/health/simple")
        test_results.append(("Simple Health Check", success))
    
    # Summary
    print("\n📊 Authentication System Test Results")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print("=" * 60)
    success_rate = (passed / total) * 100
    print(f"📈 Overall: {passed}/{total} tests passed ({success_rate:.1f}%)")
    
    if passed == total:
        print("🎉 All authentication tests passed!")
        print("✅ Python backend authentication system is fully functional")
        return 0
    else:
        print("⚠️ Some authentication tests failed")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)