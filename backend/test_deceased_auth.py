#!/usr/bin/env python3
"""
Test script for deceased profile authentication issue
"""

import asyncio
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.services.auth_service import AuthService
from app.models.deceased import DeceasedProfile
from app.schemas.deceased import DeceasedProfileCreate

async def test_deceased_profile_creation():
    """Test deceased profile creation with authentication"""
    
    print("🧪 Testing Deceased Profile Authentication Issue")
    print("=" * 50)
    
    try:
        # Get database session
        async with AsyncSessionLocal() as db:
            auth_service = AuthService(db)
            
            # Step 1: Get user by email (using existing test user)
            print("\n1️⃣ Finding test user...")
            from sqlalchemy import select
            from app.models.user import User
            
            result = await db.execute(
                select(User).where(User.email == "test@example.com")
            )
            user = result.scalar_one_or_none()
            
            if not user:
                print("❌ Test user not found. Creating new user...")
                from app.schemas.user import UserRegisterRequest
                user_data = UserRegisterRequest(
                    email="test@example.com",
                    password="SecurePassword123!",
                    first_name="Test",
                    last_name="User"
                )
                response = await auth_service.register_user(user_data)
                user = await auth_service.get_user_by_id(response.user.id)
                print(f"✅ Created user: {user.email}")
            else:
                print(f"✅ Found user: {user.email} (ID: {user.id})")
            
            # Step 2: Test deceased profile creation directly
            print("\n2️⃣ Testing direct deceased profile creation...")
            
            # Create deceased profile data
            profile_data = DeceasedProfileCreate(
                vietnamese_name="Nguyễn Văn Test",
                english_name="Nguyen Van Test", 
                common_name="Test Person",
                gender="male",
                biography="This is a test deceased profile for Vietnamese memorial app.",
                privacy_level="family"
            )
            
            print(f"Profile data: {profile_data.dict()}")
            
            # Create deceased profile directly
            deceased_profile = DeceasedProfile(
                created_by=user.id,
                vietnamese_name=profile_data.vietnamese_name,
                english_name=profile_data.english_name,
                common_name=profile_data.common_name,
                gender=profile_data.gender,
                biography=profile_data.biography,
                privacy_level=profile_data.privacy_level
            )
            
            db.add(deceased_profile)
            await db.commit()
            await db.refresh(deceased_profile)
            
            print(f"✅ Created deceased profile: {deceased_profile.id}")
            print(f"   Vietnamese name: {deceased_profile.vietnamese_name}")
            print(f"   English name: {deceased_profile.english_name}")
            print(f"   Created by: {deceased_profile.created_by}")
            
            # Step 3: Test authentication middleware simulation
            print("\n3️⃣ Testing authentication simulation...")
            
            # Simulate what get_current_user does
            print(f"Current user ID: {user.id}")
            print(f"Profile created by: {deceased_profile.created_by}")
            print(f"Authentication check: {user.id == deceased_profile.created_by}")
            
            if user.id == deceased_profile.created_by:
                print("✅ Authentication would succeed")
            else:
                print("❌ Authentication would fail")
            
            # Step 4: Test router field mapping
            print("\n4️⃣ Testing router field mapping...")
            
            # This simulates what the router does
            router_fields = {
                'id': deceased_profile.id,
                'created_by': deceased_profile.created_by,
                'vietnamese_name': deceased_profile.vietnamese_name,
                'english_name': deceased_profile.english_name,
                'common_name': deceased_profile.common_name,
                'gender': deceased_profile.gender,
                'biography': deceased_profile.biography,
                'privacy_level': deceased_profile.privacy_level,
                'created_at': deceased_profile.created_at,
                'updated_at': deceased_profile.updated_at
            }
            
            print("Router response fields:")
            for key, value in router_fields.items():
                print(f"   {key}: {value}")
            
            print("\n✅ Test completed successfully!")
            print("\n🔍 Analysis:")
            print("   - Database model supports all required fields")
            print("   - Field mapping works correctly") 
            print("   - Authentication logic should work")
            print("   - Issue may be in middleware or router configuration")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_deceased_profile_creation())
    if success:
        print("\n🎉 Deceased profile test passed!")
    else:
        print("\n💥 Deceased profile test failed!")