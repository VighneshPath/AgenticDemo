#!/bin/bash

# Start script for Agentic Platform

set -e

MODE=${1:-production}

if [ "$MODE" = "dev" ] || [ "$MODE" = "development" ]; then
    echo "🚀 Starting Agentic Platform in development mode..."
    docker-compose -f docker-compose.dev.yml up -d
    echo "✅ Development environment started!"
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
else
    echo "🚀 Starting Agentic Platform in production mode..."
    docker-compose up -d
    echo "✅ Production environment started!"
    echo "🌐 Application: http://localhost"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
fi

echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"