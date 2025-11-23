import requests
from langchain_core.tools import tool


@tool
def call_api() -> str:
    """
    This tool calls the beach API to get all the people that are on the beach.
    If someone asks for a specific person or thing, you can still call the API and filter the response.
    """
    print("Calling API")
    response = requests.get("http://host.docker.internal:8000/api/beach")
    print(f"Response {response.content}")
    return response.content
    
    
