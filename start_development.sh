#!/bin/bash

# Development startup script for Agentic Platform
# Starts both backend and frontend servers for development

set -e

echo "🚀 Starting Agentic Platform Development Environment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Expected structure: backend/ and frontend/ directories"
    exit 1
fi

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down development servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "✅ Cleanup complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo ""
echo "📦 Setting up backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Please run backend/setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Seed database with sample data
echo "🌱 Seeding database with sample data..."
python seed_database.py

# Start backend server
echo "🔧 Starting backend server on http://localhost:8000..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Test backend
echo "🧪 Testing backend connectivity..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running and healthy"
else
    echo "❌ Backend failed to start properly"
    cleanup
    exit 1
fi

cd ..

echo ""
echo "📦 Setting up frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install
fi

# Test frontend integration
echo "🧪 Testing frontend-backend integration..."
if node test_frontend_integration.js; then
    echo "✅ Frontend-backend integration verified"
else
    echo "❌ Frontend-backend integration test failed"
    cleanup
    exit 1
fi

# Start frontend server
echo "🔧 Starting frontend server on http://localhost:3000..."
npm start &
FRONTEND_PID=$!

cd ..

echo ""
echo "🎉 Development environment is ready!"
echo "=================================="
echo "📍 Backend API: http://localhost:8000"
echo "📍 Frontend App: http://localhost:3000"
echo "📍 API Documentation: http://localhost:8000/docs"
echo ""
echo "💡 Press Ctrl+C to stop both servers"
echo ""

# Wait for user to stop the servers
wait