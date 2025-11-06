#!/usr/bin/env python3
"""
Integration test script to verify backend functionality and API endpoints.
Tests all major API endpoints and verifies CORS configuration.
"""

from fastapi.testclient import TestClient
from app.database import DATABASE_PATH
from app.main import app
import asyncio
import aiosqlite
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))


def test_cors_configuration():
    """Test CORS configuration in the FastAPI app."""
    print("Testing CORS configuration...")

    # Check if CORS middleware is properly configured
    cors_middleware = None
    for middleware in app.user_middleware:
        if hasattr(middleware, 'cls') and 'CORS' in str(middleware.cls):
            cors_middleware = middleware
            break

    if cors_middleware:
        print("✅ CORS middleware is configured")
        return True
    else:
        print("❌ CORS middleware not found")
        return False


def test_api_endpoints():
    """Test all API endpoints with sample data."""
    print("\nTesting API endpoints...")

    client = TestClient(app)

    # Test root endpoint
    try:
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Root endpoint (/) working")
            data = response.json()
            print(f"   API version: {data.get('version')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

    # Test health endpoint
    try:
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ Health endpoint (/health) working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

    # Test people endpoints
    try:
        response = client.get("/api/people")
        if response.status_code == 200:
            print("✅ People list endpoint (/api/people) working")
            data = response.json()
            print(f"   Found {data.get('total_count', 0)} people")
        else:
            print(f"❌ People endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ People endpoint error: {e}")
        return False

    # Test beach endpoint
    try:
        response = client.get("/api/beach")
        if response.status_code == 200:
            print("✅ Beach endpoint (/api/beach) working")
            data = response.json()
            print(f"   Found {data.get('total_count', 0)} people on beach")
        else:
            print(f"❌ Beach endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Beach endpoint error: {e}")
        return False

    # Test documents endpoint
    try:
        response = client.get("/api/docs")
        if response.status_code == 200:
            print("✅ Documents list endpoint (/api/docs) working")
        else:
            print(f"❌ Documents endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Documents endpoint error: {e}")
        return False

    return True


def test_people_crud_operations():
    """Test CRUD operations for people."""
    print("\nTesting People CRUD operations...")

    client = TestClient(app)

    # Test creating a person
    test_person = {
        "name": "Test User",
        "role": "Test Engineer",
        "department": "Testing",
        "staffing_status": "available"
    }

    try:
        response = client.post("/api/people", json=test_person)
        if response.status_code == 201:
            print("✅ Create person working")
            created_person = response.json()
            person_id = created_person.get('person', {}).get('id')

            if person_id:
                # Test getting the person
                response = client.get(f"/api/people/{person_id}")
                if response.status_code == 200:
                    print("✅ Get person by ID working")

                    # Test updating the person
                    update_data = {"role": "Senior Test Engineer"}
                    response = client.put(
                        f"/api/people/{person_id}", json=update_data)
                    if response.status_code == 200:
                        print("✅ Update person working")
                    else:
                        print(
                            f"❌ Update person failed: {response.status_code}")

                    # Test deleting the person
                    response = client.delete(f"/api/people/{person_id}")
                    if response.status_code == 200:
                        print("✅ Delete person working")
                    else:
                        print(
                            f"❌ Delete person failed: {response.status_code}")
                else:
                    print(f"❌ Get person failed: {response.status_code}")
            else:
                print("❌ Created person has no ID")
        else:
            print(f"❌ Create person failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ CRUD operations error: {e}")
        return False

    return True


async def verify_database_data():
    """Verify that the seeded data is in the database."""
    print("\nVerifying database data...")

    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            # Check total count
            cursor = await db.execute("SELECT COUNT(*) FROM people")
            total_count = (await cursor.fetchone())[0]
            print(f"✅ Database has {total_count} people records")

            # Check beach people
            cursor = await db.execute(
                "SELECT COUNT(*) FROM people WHERE staffing_status IN ('bench', 'available')"
            )
            beach_count = (await cursor.fetchone())[0]
            print(f"✅ Database has {beach_count} people on the beach")

            return total_count > 0
    except Exception as e:
        print(f"❌ Database verification error: {e}")
        return False


def test_cors_headers():
    """Test CORS headers in API responses."""
    print("\nTesting CORS headers...")

    client = TestClient(app)

    # Test preflight request
    try:
        response = client.options(
            "/api/people",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )

        if response.status_code in [200, 204]:
            headers = response.headers
            if "access-control-allow-origin" in headers:
                print("✅ CORS preflight working")
                print(
                    f"   Allowed origin: {headers.get('access-control-allow-origin')}")
                return True
            else:
                print("❌ CORS headers missing in preflight response")
                return False
        else:
            print(f"❌ CORS preflight failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False


async def main():
    """Run all integration tests."""
    print("🚀 Starting Agentic Platform Integration Tests\n")

    tests_passed = 0
    total_tests = 5

    # Test 1: CORS Configuration
    if test_cors_configuration():
        tests_passed += 1

    # Test 2: Database Data
    if await verify_database_data():
        tests_passed += 1

    # Test 3: API Endpoints
    if test_api_endpoints():
        tests_passed += 1

    # Test 4: CRUD Operations
    if test_people_crud_operations():
        tests_passed += 1

    # Test 5: CORS Headers
    if test_cors_headers():
        tests_passed += 1

    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 All integration tests passed! Backend is ready for frontend integration.")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
