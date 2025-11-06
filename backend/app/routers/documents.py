"""
Documents API router for the Agentic Platform.
Provides secure access to policy documents and static files.
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from typing import List
import os
from pathlib import Path

router = APIRouter()

# Define the static policies directory path
POLICIES_DIR = Path(__file__).parent.parent.parent / "static" / "policies"

# Define allowed file extensions for security
ALLOWED_EXTENSIONS = {".md", ".txt", ".pdf", ".doc", ".docx"}

# Define available policy documents
AVAILABLE_DOCUMENTS = {
    "employee-handbook.md": "Employee Handbook - Company policies and procedures",
    "code-of-conduct.md": "Code of Conduct - Ethical standards and behavioral expectations",
    "security-policy.md": "Security Policy - Information security guidelines and requirements"
}


@router.get("/docs")
async def list_available_documents():
    """
    List all available policy documents.

    Returns:
        dict: Available documents with descriptions
    """
    try:
        # Verify that the policies directory exists
        if not POLICIES_DIR.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Policy documents directory not found"
            )

        # Get actual files in the directory (excluding .gitkeep)
        actual_files = []
        for file_path in POLICIES_DIR.iterdir():
            if file_path.is_file() and file_path.name != ".gitkeep":
                actual_files.append(file_path.name)

        # Build response with available documents
        available_docs = {}
        for filename, description in AVAILABLE_DOCUMENTS.items():
            if filename in actual_files:
                available_docs[filename] = description

        return {
            "success": True,
            "message": f"Found {len(available_docs)} available policy documents",
            "documents": available_docs,
            "base_url": "/api/docs/"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list documents: {str(e)}"
        )


@router.get("/docs/{filename}")
async def get_document(filename: str):
    """
    Retrieve a specific policy document by filename.

    Args:
        filename: Name of the document file to retrieve

    Returns:
        FileResponse: The requested document file

    Raises:
        HTTPException: 400 for invalid filename, 404 if file not found, 403 for security violations
    """
    try:
        # Input validation - check for path traversal attempts
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename: path traversal not allowed"
            )

        # Validate file extension for security
        file_extension = Path(filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"File type not allowed. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Check if filename is in our allowed documents list
        if filename not in AVAILABLE_DOCUMENTS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document '{filename}' not found. Use /api/docs to see available documents."
            )

        # Construct the full file path
        file_path = POLICIES_DIR / filename

        # Verify the file exists and is actually a file
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document file '{filename}' not found on disk"
            )

        if not file_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"'{filename}' is not a valid file"
            )

        # Additional security check - ensure the resolved path is still within policies directory
        try:
            file_path.resolve().relative_to(POLICIES_DIR.resolve())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: file path outside allowed directory"
            )

        # Determine media type based on file extension
        media_type_map = {
            ".md": "text/markdown",
            ".txt": "text/plain",
            ".pdf": "application/pdf",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }

        media_type = media_type_map.get(
            file_extension, "application/octet-stream")

        # Return the file
        return FileResponse(
            path=str(file_path),
            media_type=media_type,
            filename=filename,
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "Cache-Control": "public, max-age=3600"  # Cache for 1 hour
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve document: {str(e)}"
        )


@router.get("/docs/{filename}/info")
async def get_document_info(filename: str):
    """
    Get metadata information about a specific document.

    Args:
        filename: Name of the document file

    Returns:
        dict: Document metadata including size, modification time, and description
    """
    try:
        # Input validation
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename: path traversal not allowed"
            )

        # Check if filename is in our allowed documents list
        if filename not in AVAILABLE_DOCUMENTS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document '{filename}' not found"
            )

        # Construct the full file path
        file_path = POLICIES_DIR / filename

        # Verify the file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document file '{filename}' not found on disk"
            )

        # Get file statistics
        stat = file_path.stat()

        return {
            "success": True,
            "filename": filename,
            "description": AVAILABLE_DOCUMENTS[filename],
            "size_bytes": stat.st_size,
            "modified_at": stat.st_mtime,
            "extension": file_path.suffix,
            "download_url": f"/api/docs/{filename}"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get document info: {str(e)}"
        )
