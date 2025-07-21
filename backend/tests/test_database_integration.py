#!/usr/bin/env python3
"""
Database Integration Test for Python Backend
Tests database connectivity, table access, and basic operations
"""

import asyncio
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import httpx
import json

# Add app directory to path for imports
sys.path.append('/Users/toantrang/02_WORK/09_app/trang_vien_so/backend_python')

from app.core.database import get_db, engine
from app.core.config import settings

async def test_direct_database_connection():
    """Test direct database connection and table access"""
    print("🔍 Testing Direct Database Connection")
    print("=" * 50)
    
    try:
        # Test engine connection
        async with engine.begin() as conn:
            # Test basic connectivity
            result = await conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ Database connectivity test: {row.test}")
            
            # Test database name
            result = await conn.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"✅ Connected to database: {db_name}")
            
            # Test existing tables (from Node.js backend)
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   📄 {table[0]}")
                
            # Test users table specifically (if exists)
            try:
                result = await conn.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.fetchone()[0]
                print(f"✅ Users table accessible with {user_count} records")
            except Exception as e:
                print(f"ℹ️ Users table not found or accessible: {e}")
                
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

async def test_session_manager():
    """Test database session management"""
    print("\n🔧 Testing Session Manager")
    print("=" * 50)
    
    try:
        # Test session creation and cleanup
        async def test_session():
            async with AsyncSession(engine) as session:
                result = await session.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                print(f"✅ Session created successfully")
                print(f"   📊 PostgreSQL version: {version[:50]}...")
                return True
        
        success = await test_session()
        if success:
            print("✅ Session management working correctly")
        return success
        
    except Exception as e:
        print(f"❌ Session management failed: {e}")
        return False

def test_api_database_endpoints():
    """Test API endpoints that use database"""
    print("\n🌐 Testing API Database Endpoints")
    print("=" * 50)
    
    BASE_URL = "http://localhost:8001"
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # Test health endpoint with database
            response = client.get(f"{BASE_URL}/api/health")
            if response.status_code == 200:
                data = response.json()
                db_status = data.get("database", "unknown")
                print(f"✅ Health endpoint: database status = {db_status}")
                
                if db_status == "healthy":
                    print("✅ API successfully connected to database")
                    return True
                else:
                    print(f"⚠️ Database status not healthy: {db_status}")
                    return False
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ API database test failed: {e}")
        return False

async def main():
    """Run all database integration tests"""
    print("🐍 Python Backend Database Integration Tests")
    print("=" * 70)
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    print(f"🔗 Database URL: {settings.DATABASE_URL[:60]}...")
    print("=" * 70)
    
    # Run tests
    tests = [
        ("Direct Database Connection", test_direct_database_connection()),
        ("Session Manager", test_session_manager()),
        ("API Database Endpoints", test_api_database_endpoints())
    ]
    
    results = []
    for test_name, test_coro in tests:
        if asyncio.iscoroutine(test_coro):
            result = await test_coro
        else:
            result = test_coro
        results.append((test_name, result))
    
    # Summary
    print("\n📊 Database Integration Test Results")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print("=" * 70)
    success_rate = (passed / total) * 100
    print(f"📈 Overall: {passed}/{total} tests passed ({success_rate:.1f}%)")
    
    if passed == total:
        print("🎉 All database integration tests passed!")
        print("✅ Python backend is fully integrated with PostgreSQL database")
        return 0
    else:
        print("⚠️ Some database integration tests failed")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)