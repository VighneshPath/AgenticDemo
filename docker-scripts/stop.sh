#!/bin/bash

# Stop script for Agentic Platform

set -e

echo "🛑 Stopping Agentic Platform containers..."

# Stop production containers
docker-compose down

# Stop development containers if running
docker-compose -f docker-compose.dev.yml down 2>/dev/null || true

echo "✅ All containers stopped!"

# Optional: Remove containers and images
if [ "$1" = "--clean" ]; then
    echo "🧹 Cleaning up containers and images..."
    docker system prune -f
    echo "✅ Cleanup complete!"
fi