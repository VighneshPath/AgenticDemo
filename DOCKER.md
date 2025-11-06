# Docker Deployment Guide

This guide explains how to run the Agentic Platform using Docker containers.

## Quick Start

### Production Deployment

1. **Build and start the application:**

   ```bash
   # Build containers
   ./docker-scripts/build.sh

   # Start in production mode
   ./docker-scripts/start.sh
   ```

2. **Access the application:**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Development Mode

1. **Start in development mode:**

   ```bash
   ./docker-scripts/start.sh dev
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000 (with hot reload)
   - Backend API: http://localhost:8000 (with auto-reload)

## Docker Compose Files

### `docker-compose.yml` (Production)

- Optimized builds with multi-stage Docker files
- Nginx serving static files and proxying API calls
- Health checks for both services
- Persistent volumes for data

### `docker-compose.dev.yml` (Development)

- Volume mounts for live code reloading
- Development servers with hot reload
- Exposed ports for direct access

## Container Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Nginx)       │    │   (FastAPI)     │
│   Port: 80      │◄──►│   Port: 8000    │
└─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Static Files   │    │   SQLite DB     │
│  (React Build)  │    │   (Volume)      │
└─────────────────┘    └─────────────────┘
```

## Environment Variables

### Backend

- `PYTHONPATH`: Set to `/app` for proper module imports
- `ALLOWED_ORIGINS`: CORS origins for frontend access

### Frontend

- `REACT_APP_API_URL`: Backend API URL (empty for nginx proxy)
- `GENERATE_SOURCEMAP`: Disabled in production for security

## Data Persistence

### Database

- SQLite database is stored in `./backend/data/` volume
- Persists across container restarts

### Static Files

- Policy documents in `./backend/static/` volume
- Accessible via API endpoints

## Health Checks

Both containers include health checks:

### Backend

- Endpoint: `GET /health`
- Interval: 30 seconds
- Timeout: 10 seconds

### Frontend

- Check: HTTP request to nginx
- Interval: 30 seconds
- Timeout: 10 seconds

## Networking

- Internal network: `agentic-network`
- Frontend proxies API calls to backend
- Backend accessible directly on port 8000

## Scripts

### `./docker-scripts/build.sh`

Builds both Docker images with proper tags.

### `./docker-scripts/start.sh [mode]`

Starts the application:

- `start.sh` or `start.sh production`: Production mode
- `start.sh dev`: Development mode

### `./docker-scripts/stop.sh [--clean]`

Stops all containers:

- `stop.sh`: Stop containers
- `stop.sh --clean`: Stop and clean up images

## Manual Docker Commands

### Build Images

```bash
# Backend
docker build -t agentic-platform-backend ./backend

# Frontend
docker build -t agentic-platform-frontend ./frontend
```

### Run Containers

```bash
# Start with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Development Commands

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# View development logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop development environment
docker-compose -f docker-compose.dev.yml down
```

## Troubleshooting

### Container Won't Start

1. Check logs: `docker-compose logs [service-name]`
2. Verify ports aren't in use: `lsof -i :80` or `lsof -i :8000`
3. Rebuild images: `./docker-scripts/build.sh`

### Database Issues

1. Check volume permissions: `ls -la backend/data/`
2. Reset database: Remove `backend/data/*.db` files
3. Restart backend: `docker-compose restart backend`

### Frontend API Connection Issues

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS configuration in backend
3. Verify nginx proxy configuration

### Performance Issues

1. Allocate more resources to Docker
2. Use development mode for faster rebuilds
3. Check container resource usage: `docker stats`

## Security Considerations

### Production

- Static files served by nginx (not FastAPI)
- Health checks don't expose sensitive data
- CORS properly configured
- No source maps in production build

### Development

- Source maps enabled for debugging
- Hot reload for faster development
- Direct port access for testing

## Extending the Docker Setup

### Adding New Services

1. Add service to `docker-compose.yml`
2. Update networking configuration
3. Add health checks
4. Update nginx proxy if needed

### Custom Environment Variables

1. Add to `.env` file in project root
2. Reference in docker-compose files
3. Update documentation

### SSL/HTTPS Setup

1. Add SSL certificates to nginx configuration
2. Update ports and proxy settings
3. Configure HTTPS redirects

## Monitoring and Logging

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Monitor Resources

```bash
# Container stats
docker stats

# System usage
docker system df
```

### Health Status

```bash
# Check health
docker-compose ps

# Manual health check
curl http://localhost/health
curl http://localhost:8000/health
```
