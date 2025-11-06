#!/bin/bash

# Build script for Agentic Platform Docker containers

set -e

echo "🐳 Building Agentic Platform Docker containers..."

# Build backend
echo "📦 Building backend container..."
docker build -t agentic-platform-backend ./backend

# Build frontend
echo "📦 Building frontend container..."
docker build -t agentic-platform-frontend ./frontend

echo "✅ All containers built successfully!"
echo ""
echo "To run the application:"
echo "  docker-compose up -d"
echo ""
echo "To run in development mode:"
echo "  docker-compose -f docker-compose.dev.yml up -d"