"""
Service layer for database operations.
Implements CRUD operations for People and other business logic.
"""

import aiosqlite
from typing import List, Optional
from datetime import datetime

from app.database import get_database
from app.models import Person, PersonCreate, PersonUpdate, BeachResponse


class PeopleService:
    """Service class for People-related database operations."""

    @staticmethod
    async def create_person(person_data: PersonCreate) -> Person:
        """
        Create a new person in the database.

        Args:
            person_data: PersonCreate model with person information

        Returns:
            Person: Created person with database ID and timestamps

        Raises:
            Exception: If database operation fails
        """
        async with get_database() as db:
            cursor = await db.execute(
                """
                INSERT INTO people (name, role, department, staffing_status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    person_data.name,
                    person_data.role,
                    person_data.department,
                    person_data.staffing_status.value,
                    datetime.utcnow(),
                    datetime.utcnow()
                )
            )
            await db.commit()

            # Get the created person
            person_id = cursor.lastrowid
            return await PeopleService.get_person_by_id(person_id)

    @staticmethod
    async def get_person_by_id(person_id: int) -> Optional[Person]:
        """
        Retrieve a person by their ID.

        Args:
            person_id: Unique identifier for the person

        Returns:
            Person or None if not found
        """
        async with get_database() as db:
            cursor = await db.execute(
                "SELECT * FROM people WHERE id = ?",
                (person_id,)
            )
            row = await cursor.fetchone()

            if row:
                return Person(
                    id=row['id'],
                    name=row['name'],
                    role=row['role'],
                    department=row['department'],
                    staffing_status=row['staffing_status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None

    @staticmethod
    async def get_all_people() -> List[Person]:
        """
        Retrieve all people from the database.

        Returns:
            List of Person objects
        """
        async with get_database() as db:
            cursor = await db.execute(
                "SELECT * FROM people ORDER BY created_at DESC"
            )
            rows = await cursor.fetchall()

            return [
                Person(
                    id=row['id'],
                    name=row['name'],
                    role=row['role'],
                    department=row['department'],
                    staffing_status=row['staffing_status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                for row in rows
            ]

    @staticmethod
    async def update_person(person_id: int, person_data: PersonUpdate) -> Optional[Person]:
        """
        Update an existing person in the database.

        Args:
            person_id: Unique identifier for the person
            person_data: PersonUpdate model with updated information

        Returns:
            Updated Person or None if not found
        """
        # First check if person exists
        existing_person = await PeopleService.get_person_by_id(person_id)
        if not existing_person:
            return None

        # Build update query dynamically based on provided fields
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

        # Always update the updated_at timestamp
        update_fields.append("updated_at = ?")
        update_values.append(datetime.utcnow())

        # Add person_id for WHERE clause
        update_values.append(person_id)

        async with get_database() as db:
            await db.execute(
                f"UPDATE people SET {', '.join(update_fields)} WHERE id = ?",
                update_values
            )
            await db.commit()

            # Return updated person
            return await PeopleService.get_person_by_id(person_id)

    @staticmethod
    async def delete_person(person_id: int) -> bool:
        """
        Delete a person from the database.

        Args:
            person_id: Unique identifier for the person

        Returns:
            True if person was deleted, False if not found
        """
        async with get_database() as db:
            cursor = await db.execute(
                "DELETE FROM people WHERE id = ?",
                (person_id,)
            )
            await db.commit()

            return cursor.rowcount > 0

    @staticmethod
    async def get_people_by_staffing_status(status: str) -> List[Person]:
        """
        Retrieve people by their staffing status.

        Args:
            status: Staffing status to filter by

        Returns:
            List of Person objects with matching status
        """
        async with get_database() as db:
            cursor = await db.execute(
                "SELECT * FROM people WHERE staffing_status = ? ORDER BY created_at DESC",
                (status,)
            )
            rows = await cursor.fetchall()

            return [
                Person(
                    id=row['id'],
                    name=row['name'],
                    role=row['role'],
                    department=row['department'],
                    staffing_status=row['staffing_status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                for row in rows
            ]

    @staticmethod
    async def get_people_count() -> int:
        """
        Get total count of people in the database.

        Returns:
            Total number of people
        """
        async with get_database() as db:
            cursor = await db.execute("SELECT COUNT(*) as count FROM people")
            row = await cursor.fetchone()
            return row['count'] if row else 0


class BeachService:
    """Service class for Beach-related business logic operations."""

    @staticmethod
    async def get_people_on_beach() -> List[Person]:
        """
        Identify and retrieve people currently on the beach.
        People are considered "on the beach" if their staffing status is 'bench' or 'available'.

        Returns:
            List of Person objects who are currently on the beach

        Raises:
            Exception: If database operation fails
        """
        async with get_database() as db:
            cursor = await db.execute(
                """
                SELECT * FROM people 
                WHERE staffing_status IN ('bench', 'available') 
                ORDER BY created_at DESC
                """)
            rows = await cursor.fetchall()

            return [
                Person(
                    id=row['id'],
                    name=row['name'],
                    role=row['role'],
                    department=row['department'],
                    staffing_status=row['staffing_status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                for row in rows
            ]

    @staticmethod
    async def get_beach_count() -> int:
        """
        Get count of people currently on the beach.

        Returns:
            Number of people with 'bench' or 'available' status
        """
        async with get_database() as db:
            cursor = await db.execute(
                "SELECT COUNT(*) as count FROM people WHERE staffing_status IN ('bench', 'available')"
            )
            row = await cursor.fetchone()
            return row['count'] if row else 0
