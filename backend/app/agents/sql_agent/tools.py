import asyncio
import json
from langchain_core.tools import tool
from ...database import get_database

@tool
def call_sql(query: str) -> str:
    """
    This tool calls the database using the query param that is passed. It should only be called for SELECT statements.
    It returns the output in json format which does not have any fixed schema.  
    """
    # print(f"running query: {query}")
    response = asyncio.run(_call_sql(query = query))
    # print(f"got response: {response}")
    return response

async def _call_sql(query: str) -> str:

    async with get_database() as db:
        cursor = await db.execute(
            query)
        rows = await cursor.fetchall()
        
    return json.dumps([dict(row) for row in rows])

