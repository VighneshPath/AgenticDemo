"""
Beach API router for the Agentic Platform.
Provides business logic to identify people currently on the beach.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
import aiosqlite

from app.models import BeachResponse
from app.services import BeachService
from app.database import get_db_connection

router = APIRouter()


@router.get("/beach", response_model=BeachResponse)
async def get_people_on_beach(db: aiosqlite.Connection = Depends(get_db_connection)):
    """
    Retrieve all people currently on the beach.

    People are considered "on the beach" if their staffing status is 'bench' or 'available'.
    This endpoint demonstrates business logic that spans database queries and data aggregation.

    Returns:
        BeachResponse: List of people on the beach with metadata

    Raises:
        HTTPException: 500 if database operation fails
    """
    try:
        # Get people on the beach using the beach service
        people_on_beach = await BeachService.get_people_on_beach()

        return BeachResponse(
            success=True,
            message=f"Retrieved {len(people_on_beach)} people currently on the beach",
            people_on_beach=people_on_beach,
            total_count=len(people_on_beach),
            last_updated=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve beach data: {str(e)}"
        )
