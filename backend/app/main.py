"""
Main FastAPI application entry point for the Agentic Platform.
Provides foundational structure for multi-agent system development.
"""

from app.routers import documents
from app.routers import beach
from app.routers import people
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.database import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup: Initialize database
    await init_database()
    yield
    # Shutdown: cleanup if needed

# Create FastAPI application instance
app = FastAPI(
    title="Agentic Implementation Platform",
    description="Foundational system for multi-agent development with structured data, APIs, and chat interface",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend integration
# Support both development and production environments
allowed_origins = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",  # Alternative localhost
    "http://localhost:3001",  # Alternative React port
]

# Add production origins from environment variable if available
production_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if production_origins and production_origins[0]:  # Check if not empty
    allowed_origins.extend([origin.strip() for origin in production_origins])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Mount static files for policy documents
static_path = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def root():
    """Root endpoint providing basic system information."""
    return {
        "message": "Agentic Implementation Platform API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "people": "/api/people",
            "beach": "/api/beach",
            "documents": "/api/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for system monitoring."""
    return {"status": "healthy", "service": "agentic-platform-api"}

# Include API routers

app.include_router(people.router, prefix="/api", tags=["people"])
app.include_router(beach.router, prefix="/api", tags=["beach"])

# Documents router for policy document access
app.include_router(documents.router, prefix="/api", tags=["documents"])
