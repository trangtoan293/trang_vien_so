#!/usr/bin/env python3
"""
Simple API test for deceased profile endpoints
"""

import asyncio
import json
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.core.database import AsyncSessionLocal
from app.services.auth_service import AuthService

def test_deceased_api():
    """Test deceased profile API endpoints with authentication"""
    
    print("🧪 Testing Deceased Profile API")
    print("=" * 40)
    
    # Create test client
    with TestClient(app) as client:
        
        # Step 1: Register/Login to get token
        print("\n1️⃣ Getting authentication token...")
        
        # Try login first
        login_response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "SecurePassword123!"
        })
        
        if login_response.status_code != 200:
            print("   Login failed, registering new user...")
            register_response = client.post("/api/auth/register", json={
                "email": "test@example.com",
                "password": "SecurePassword123!",
                "first_name": "Test",
                "last_name": "User"
            })
            
            if register_response.status_code != 201:
                print(f"   ❌ Registration failed: {register_response.status_code}")
                print(f"   Response: {register_response.text}")
                return False
            
            auth_data = register_response.json()
        else:
            auth_data = login_response.json()
        
        token = auth_data["tokens"]["access_token"]
        print(f"   ✅ Got token: {token[:20]}...")
        
        # Step 2: Test deceased profile creation
        print("\n2️⃣ Testing deceased profile creation...")
        
        headers = {"Authorization": f"Bearer {token}"}
        profile_data = {
            "vietnamese_name": "Nguyễn Văn Test API",
            "english_name": "Nguyen Van Test API",
            "common_name": "Test API Person",
            "gender": "male",
            "biography": "Test deceased profile created via API",
            "privacy_level": "family"
        }
        
        create_response = client.post(
            "/api/deceased/",
            json=profile_data,
            headers=headers
        )
        
        print(f"   Status: {create_response.status_code}")
        print(f"   Response: {create_response.text[:200]}...")
        
        if create_response.status_code == 201:
            print("   ✅ Profile created successfully")
            profile = create_response.json()
            profile_id = profile["id"]
            
            # Step 3: Test profile retrieval
            print("\n3️⃣ Testing profile retrieval...")
            
            get_response = client.get(
                f"/api/deceased/{profile_id}",
                headers=headers
            )
            
            print(f"   Status: {get_response.status_code}")
            if get_response.status_code == 200:
                print("   ✅ Profile retrieved successfully")
                retrieved_profile = get_response.json()
                print(f"   Profile name: {retrieved_profile['vietnamese_name']}")
            else:
                print(f"   ❌ Profile retrieval failed: {get_response.text}")
            
            # Step 4: Test profile list
            print("\n4️⃣ Testing profile list...")
            
            list_response = client.get(
                "/api/deceased/",
                headers=headers
            )
            
            print(f"   Status: {list_response.status_code}")
            if list_response.status_code == 200:
                print("   ✅ Profile list retrieved successfully")
                profiles_list = list_response.json()
                print(f"   Total profiles: {profiles_list['total']}")
            else:
                print(f"   ❌ Profile list failed: {list_response.text}")
            
            return True
            
        else:
            print(f"   ❌ Profile creation failed")
            print(f"   Error: {create_response.text}")
            return False

if __name__ == "__main__":
    success = test_deceased_api()
    if success:
        print("\n🎉 API test passed!")
    else:
        print("\n💥 API test failed!")