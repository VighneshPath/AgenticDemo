"""
Validation script to test the FastAPI application setup.
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.main import app
    print("✓ FastAPI application imported successfully")

    # Check if the app has the expected attributes
    assert hasattr(app, 'title'), "App should have a title"
    assert app.title == "Agentic Implementation Platform", f"Expected title 'Agentic Implementation Platform', got '{app.title}'"
    print("✓ App configuration is correct")

    # Check if routes are registered
    routes = [route.path for route in app.routes]
    expected_routes = ["/", "/health"]

    for route in expected_routes:
        assert route in routes, f"Expected route '{route}' not found"
    print("✓ Basic routes are registered")

    print("\n🎉 Backend foundation setup is complete and valid!")
    print("Next steps:")
    print("1. Create virtual environment: python3 -m venv venv")
    print("2. Activate it: source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Run server: python run.py")

except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except AssertionError as e:
    print(f"❌ Validation error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
