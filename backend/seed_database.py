#!/usr/bin/env python3
"""
Standalone script to seed the Agentic Platform database with sample data.
Can be run from the backend directory to populate the database for development.

Usage:
    python seed_database.py [--clear]
    
Options:
    --clear: Clear existing data before seeding (default: True)
    --no-clear: Keep existing data and add sample data
"""

from app.seed_data import seed_database
import asyncio
import sys
import argparse
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Main function to handle command line arguments and run seeding."""
    parser = argparse.ArgumentParser(
        description="Seed the Agentic Platform database with sample people data"
    )
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Keep existing data and add sample data (default: clear existing data)"
    )

    args = parser.parse_args()

    # Determine whether to clear existing data
    clear_existing = not args.no_clear

    try:
        # Run the seeding process
        asyncio.run(seed_database(clear_existing=clear_existing))
        print("\n✅ Database seeding completed successfully!")

    except Exception as e:
        print(f"\n❌ Error during database seeding: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
