#!/bin/bash

# Validation script for Docker setup

set -e

echo "🔍 Validating Docker setup for Agentic Platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed"
    exit 1
fi

echo "✅ docker-compose is available"

# Validate docker-compose configuration
echo "🔍 Validating docker-compose configuration..."
if docker-compose config > /dev/null; then
    echo "✅ docker-compose.yml is valid"
else
    echo "❌ docker-compose.yml has errors"
    exit 1
fi

# Validate development docker-compose configuration
echo "🔍 Validating development docker-compose configuration..."
if docker-compose -f docker-compose.dev.yml config > /dev/null; then
    echo "✅ docker-compose.dev.yml is valid"
else
    echo "❌ docker-compose.dev.yml has errors"
    exit 1
fi

# Check if required files exist
echo "🔍 Checking required files..."

required_files=(
    "backend/Dockerfile"
    "backend/.dockerignore"
    "frontend/Dockerfile"
    "frontend/Dockerfile.dev"
    "frontend/.dockerignore"
    "frontend/nginx.conf"
    "docker-compose.yml"
    "docker-compose.dev.yml"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing"
        exit 1
    fi
done

# Test building images
echo "🔍 Testing Docker image builds..."

echo "📦 Building backend image..."
if docker build -t agentic-platform-backend-test ./backend > /dev/null 2>&1; then
    echo "✅ Backend image builds successfully"
    docker rmi agentic-platform-backend-test > /dev/null 2>&1
else
    echo "❌ Backend image build failed"
    exit 1
fi

echo "📦 Building frontend image..."
if docker build -t agentic-platform-frontend-test ./frontend > /dev/null 2>&1; then
    echo "✅ Frontend image builds successfully"
    docker rmi agentic-platform-frontend-test > /dev/null 2>&1
else
    echo "❌ Frontend image build failed"
    exit 1
fi

echo ""
echo "🎉 All Docker setup validations passed!"
echo ""
echo "Next steps:"
echo "  1. Build and start: ./docker-scripts/build.sh && ./docker-scripts/start.sh"
echo "  2. Access frontend: http://localhost"
echo "  3. Access backend API: http://localhost:8000"
echo "  4. View API docs: http://localhost:8000/docs"
echo ""
echo "For development mode:"
echo "  ./docker-scripts/start.sh dev"