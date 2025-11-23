"""
Development server runner for the Agentic Platform backend.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="::",
        port=8000,
        # reload=True,
        log_level="info", 
        workers=4
    )
