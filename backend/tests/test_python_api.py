#!/usr/bin/env python3
"""
Quick API test script for Python backend
Tests basic functionality and compatibility
"""

import httpx
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8001"

def test_endpoint(client, method, endpoint, expected_status=200, data=None):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = client.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = client.post(f"{BASE_URL}{endpoint}", json=data)
        
        success = response.status_code == expected_status
        print(f"{'✅' if success else '❌'} {method} {endpoint} - Status: {response.status_code}")
        
        if success and response.headers.get("content-type", "").startswith("application/json"):
            data = response.json()
            if "timestamp" in data:
                print(f"   📅 Timestamp: {data['timestamp']}")
            if "version" in data:
                print(f"   🔢 Version: {data['version']}")
            if "message" in data:
                print(f"   💬 Message: {data['message']}")
        
        return success, response
        
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False, None

def main():
    """Run basic API tests"""
    print("🐍 Python Backend API Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    with httpx.Client(timeout=10.0) as client:
        # Test endpoints
        test_cases = [
            ("GET", "/", 200),
            ("GET", "/api/health/simple", 200),
            ("GET", "/api/status", 200), 
            ("GET", "/api/auth/", 200),
            ("GET", "/api/users/", 200),
            ("GET", "/openapi.json", 200),
            ("GET", "/api/docs", 200),
        ]
        
        for method, endpoint, expected_status in test_cases:
            success, response = test_endpoint(client, method, endpoint, expected_status)
            total_tests += 1
            if success:
                tests_passed += 1
    
    print("=" * 50)
    print(f"📊 Results: {tests_passed}/{total_tests} tests passed ({tests_passed/total_tests*100:.1f}%)")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Python backend is working correctly.")
        sys.exit(0)
    else:
        print("⚠️ Some tests failed. Check the server logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()