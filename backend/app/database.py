"""
Database connection utilities and schema management for the Agentic Platform.
Provides SQLite database initialization and connection management.
"""

import aiosqlite
import os
from typing import AsyncGenerator
from contextlib import asynccontextmanager

# Database file path
DATABASE_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "agentic_platform.db")

# SQL schema for People table
PEOPLE_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    department TEXT NOT NULL,
    staffing_status TEXT NOT NULL CHECK (staffing_status IN ('staffed', 'bench', 'available')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Index for performance on common queries
PEOPLE_TABLE_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_people_staffing_status ON people(staffing_status);
CREATE INDEX IF NOT EXISTS idx_people_department ON people(department);
"""


async def init_database() -> None:
    """
    Initialize the database and create tables if they don't exist.
    This function should be called on application startup.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Create People table
        await db.execute(PEOPLE_TABLE_SCHEMA)

        # Create indexes for performance
        await db.execute("CREATE INDEX IF NOT EXISTS idx_people_staffing_status ON people(staffing_status);")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_people_department ON people(department);")

        # Commit the changes
        await db.commit()


@asynccontextmanager
async def get_database() -> AsyncGenerator[aiosqlite.Connection, None]:
    """
    Async context manager for database connections.
    Ensures proper connection handling and cleanup.

    Usage:
        async with get_database() as db:
            cursor = await db.execute("SELECT * FROM people")
            results = await cursor.fetchall()
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Enable row factory for easier data access
        db.row_factory = aiosqlite.Row
        yield db


async def get_db_connection():
    """
    Dependency function for FastAPI to inject database connections.
    Used with FastAPI's dependency injection system.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Enable row factory for easier data access
        db.row_factory = aiosqlite.Row
        yield db
