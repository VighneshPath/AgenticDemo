"""
Database seeding script for the Agentic Platform.
Provides sample people data with various staffing statuses for development and testing.
"""

import asyncio
import aiosqlite
from datetime import datetime
from app.database import DATABASE_PATH, init_database
from app.models import StaffingStatus


# Sample people data with diverse roles, departments, and staffing statuses
SAMPLE_PEOPLE = [
    # Engineering Department - Mix of staffed and available
    {
        "name": "Alice Johnson",
        "role": "Senior Software Engineer",
        "department": "Engineering",
        "staffing_status": StaffingStatus.STAFFED
    },
    {
        "name": "Bob Chen",
        "role": "Frontend Developer",
        "department": "Engineering",
        "staffing_status": StaffingStatus.BENCH
    },
    {
        "name": "Carol Martinez",
        "role": "DevOps Engineer",
        "department": "Engineering",
        "staffing_status": StaffingStatus.AVAILABLE
    },
    {
        "name": "David Kim",
        "role": "Full Stack Developer",
        "department": "Engineering",
        "staffing_status": StaffingStatus.STAFFED
    },
    {
        "name": "Eva Rodriguez",
        "role": "Backend Engineer",
        "department": "Engineering",
        "staffing_status": StaffingStatus.BENCH
    },

    # Product Department
    {
        "name": "Frank Wilson",
        "role": "Product Manager",
        "department": "Product",
        "staffing_status": StaffingStatus.STAFFED
    },
    {
        "name": "Grace Lee",
        "role": "UX Designer",
        "department": "Product",
        "staffing_status": StaffingStatus.AVAILABLE
    },
    {
        "name": "Henry Thompson",
        "role": "Product Analyst",
        "department": "Product",
        "staffing_status": StaffingStatus.BENCH
    },

    # Data Science Department
    {
        "name": "Iris Patel",
        "role": "Data Scientist",
        "department": "Data Science",
        "staffing_status": StaffingStatus.STAFFED
    },
    {
        "name": "Jack Brown",
        "role": "ML Engineer",
        "department": "Data Science",
        "staffing_status": StaffingStatus.AVAILABLE
    },
    {
        "name": "Kate Singh",
        "role": "Data Analyst",
        "department": "Data Science",
        "staffing_status": StaffingStatus.BENCH
    },

    # Marketing Department
    {
        "name": "Liam Davis",
        "role": "Marketing Manager",
        "department": "Marketing",
        "staffing_status": StaffingStatus.STAFFED
    },
    {
        "name": "Maya Gonzalez",
        "role": "Content Strategist",
        "department": "Marketing",
        "staffing_status": StaffingStatus.AVAILABLE
    },

    # Sales Department
    {
        "name": "Noah Miller",
        "role": "Sales Representative",
        "department": "Sales",
        "staffing_status": StaffingStatus.STAFFED
    },
    {
        "name": "Olivia Taylor",
        "role": "Account Manager",
        "department": "Sales",
        "staffing_status": StaffingStatus.BENCH
    },

    # HR Department
    {
        "name": "Paul Anderson",
        "role": "HR Business Partner",
        "department": "Human Resources",
        "staffing_status": StaffingStatus.STAFFED
    },
    {
        "name": "Quinn White",
        "role": "Recruiter",
        "department": "Human Resources",
        "staffing_status": StaffingStatus.AVAILABLE
    },

    # Finance Department
    {
        "name": "Rachel Green",
        "role": "Financial Analyst",
        "department": "Finance",
        "staffing_status": StaffingStatus.STAFFED
    },
    {
        "name": "Sam Cooper",
        "role": "Accounting Specialist",
        "department": "Finance",
        "staffing_status": StaffingStatus.BENCH
    },

    # Operations Department
    {
        "name": "Tina Clark",
        "role": "Operations Manager",
        "department": "Operations",
        "staffing_status": StaffingStatus.STAFFED
    }
]


async def clear_existing_data():
    """Clear existing people data from the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM people")
        await db.commit()
        print("Cleared existing people data")


async def seed_people_data():
    """Insert sample people data into the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        current_time = datetime.now().isoformat()

        for person_data in SAMPLE_PEOPLE:
            await db.execute(
                """
                INSERT INTO people (name, role, department, staffing_status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    person_data["name"],
                    person_data["role"],
                    person_data["department"],
                    person_data["staffing_status"].value,
                    current_time,
                    current_time
                )
            )

        await db.commit()
        print(f"Successfully seeded {len(SAMPLE_PEOPLE)} people records")


async def verify_seeded_data():
    """Verify that the data was seeded correctly by checking counts by status."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Get total count
        cursor = await db.execute("SELECT COUNT(*) FROM people")
        total_count = (await cursor.fetchone())[0]

        # Get counts by staffing status
        cursor = await db.execute(
            "SELECT staffing_status, COUNT(*) FROM people GROUP BY staffing_status"
        )
        status_counts = await cursor.fetchall()

        print(f"\nData verification:")
        print(f"Total people: {total_count}")
        print("By staffing status:")
        for status, count in status_counts:
            print(f"  {status}: {count}")

        # Show people on the beach (bench + available)
        cursor = await db.execute(
            """
            SELECT name, role, department, staffing_status 
            FROM people 
            WHERE staffing_status IN ('bench', 'available')
            ORDER BY department, name
            """
        )
        beach_people = await cursor.fetchall()

        print(f"\nPeople on the beach ({len(beach_people)}):")
        for person in beach_people:
            print(f"  {person[0]} - {person[1]} ({person[2]}) - {person[3]}")


async def seed_database(clear_existing: bool = True):
    """
    Main function to seed the database with sample data.

    Args:
        clear_existing: Whether to clear existing data before seeding
    """
    print("Starting database seeding...")

    # Initialize database schema
    await init_database()
    print("Database initialized")

    # Clear existing data if requested
    if clear_existing:
        await clear_existing_data()

    # Seed new data
    await seed_people_data()

    # Verify the seeded data
    await verify_seeded_data()

    print("\nDatabase seeding completed successfully!")


if __name__ == "__main__":
    # Run the seeding script
    asyncio.run(seed_database())
