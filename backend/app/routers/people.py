"""
People management API router for the Agentic Platform.
Provides CRUD operations for managing people data.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
import aiosqlite
from datetime import datetime

from app.models import Person, PersonCreate, PersonUpdate, PersonResponse, PeopleListResponse
from app.database import get_db_connection

router = APIRouter()


@router.get("/people", response_model=PeopleListResponse)
async def get_all_people(db: aiosqlite.Connection = Depends(get_db_connection)):
    """
    Retrieve all people from the database.

    Returns:
        PeopleListResponse: List of all people with total count
    """
    try:
        cursor = await db.execute("""
            SELECT id, name, role, department, staffing_status, created_at, updated_at 
            FROM people 
            ORDER BY created_at DESC
        """)
        rows = await cursor.fetchall()

        people = []
        for row in rows:
            person = Person(
                id=row["id"],
                name=row["name"],
                role=row["role"],
                department=row["department"],
                staffing_status=row["staffing_status"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"])
            )
            people.append(person)

        return PeopleListResponse(
            success=True,
            message=f"Retrieved {len(people)} people successfully",
            people=people,
            total_count=len(people)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve people: {str(e)}"
        )


@router.post("/people", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
async def create_person(person_data: PersonCreate, db: aiosqlite.Connection = Depends(get_db_connection)):
    """
    Create a new person in the database.

    Args:
        person_data: PersonCreate model with person information

    Returns:
        PersonResponse: Created person data with success status
    """
    try:
        current_time = datetime.now().isoformat()

        cursor = await db.execute("""
            INSERT INTO people (name, role, department, staffing_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            person_data.name,
            person_data.role,
            person_data.department,
            person_data.staffing_status.value,
            current_time,
            current_time
        ))

        await db.commit()
        person_id = cursor.lastrowid

        # Retrieve the created person
        cursor = await db.execute("""
            SELECT id, name, role, department, staffing_status, created_at, updated_at 
            FROM people WHERE id = ?
        """, (person_id,))
        row = await cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created person"
            )

        created_person = Person(
            id=row["id"],
            name=row["name"],
            role=row["role"],
            department=row["department"],
            staffing_status=row["staffing_status"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"])
        )

        return PersonResponse(
            success=True,
            message="Person created successfully",
            person=created_person
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create person: {str(e)}"
        )


@router.get("/people/{person_id}", response_model=PersonResponse)
async def get_person_by_id(person_id: int, db: aiosqlite.Connection = Depends(get_db_connection)):
    """
    Retrieve a specific person by their ID.

    Args:
        person_id: Unique identifier of the person

    Returns:
        PersonResponse: Person data if found

    Raises:
        HTTPException: 404 if person not found
    """
    try:
        cursor = await db.execute("""
            SELECT id, name, role, department, staffing_status, created_at, updated_at 
            FROM people WHERE id = ?
        """, (person_id,))
        row = await cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person with ID {person_id} not found"
            )

        person = Person(
            id=row["id"],
            name=row["name"],
            role=row["role"],
            department=row["department"],
            staffing_status=row["staffing_status"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"])
        )

        return PersonResponse(
            success=True,
            message="Person retrieved successfully",
            person=person
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve person: {str(e)}"
        )


@router.put("/people/{person_id}", response_model=PersonResponse)
async def update_person(person_id: int, person_data: PersonUpdate, db: aiosqlite.Connection = Depends(get_db_connection)):
    """
    Update an existing person's information.

    Args:
        person_id: Unique identifier of the person to update
        person_data: PersonUpdate model with fields to update

    Returns:
        PersonResponse: Updated person data

    Raises:
        HTTPException: 404 if person not found
    """
    try:
        # First check if person exists
        cursor = await db.execute("SELECT id FROM people WHERE id = ?", (person_id,))
        if not await cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person with ID {person_id} not found"
            )

        # Build dynamic update query based on provided fields
        update_fields = []
        update_values = []

        if person_data.name is not None:
            update_fields.append("name = ?")
            update_values.append(person_data.name)

        if person_data.role is not None:
            update_fields.append("role = ?")
            update_values.append(person_data.role)

        if person_data.department is not None:
            update_fields.append("department = ?")
            update_values.append(person_data.department)

        if person_data.staffing_status is not None:
            update_fields.append("staffing_status = ?")
            update_values.append(person_data.staffing_status.value)

        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )

        # Add updated_at timestamp
        update_fields.append("updated_at = ?")
        update_values.append(datetime.now().isoformat())
        update_values.append(person_id)

        # Execute update
        update_query = f"UPDATE people SET {', '.join(update_fields)} WHERE id = ?"
        await db.execute(update_query, update_values)
        await db.commit()

        # Retrieve updated person
        cursor = await db.execute("""
            SELECT id, name, role, department, staffing_status, created_at, updated_at 
            FROM people WHERE id = ?
        """, (person_id,))
        row = await cursor.fetchone()

        updated_person = Person(
            id=row["id"],
            name=row["name"],
            role=row["role"],
            department=row["department"],
            staffing_status=row["staffing_status"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"])
        )

        return PersonResponse(
            success=True,
            message="Person updated successfully",
            person=updated_person
        )

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update person: {str(e)}"
        )


@router.delete("/people/{person_id}", response_model=PersonResponse)
async def delete_person(person_id: int, db: aiosqlite.Connection = Depends(get_db_connection)):
    """
    Delete a person from the database.

    Args:
        person_id: Unique identifier of the person to delete

    Returns:
        PersonResponse: Success status with deleted person data

    Raises:
        HTTPException: 404 if person not found
    """
    try:
        # First retrieve the person to return in response
        cursor = await db.execute("""
            SELECT id, name, role, department, staffing_status, created_at, updated_at 
            FROM people WHERE id = ?
        """, (person_id,))
        row = await cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person with ID {person_id} not found"
            )

        deleted_person = Person(
            id=row["id"],
            name=row["name"],
            role=row["role"],
            department=row["department"],
            staffing_status=row["staffing_status"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"])
        )

        # Delete the person
        await db.execute("DELETE FROM people WHERE id = ?", (person_id,))
        await db.commit()

        return PersonResponse(
            success=True,
            message="Person deleted successfully",
            person=deleted_person
        )

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete person: {str(e)}"
        )
