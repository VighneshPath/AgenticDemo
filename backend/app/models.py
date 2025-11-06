"""
Pydantic models for the Agentic Platform.
Defines data models with validation for API requests and responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
from datetime import datetime
from enum import Enum


class StaffingStatus(str, Enum):
    """Enumeration for valid staffing status values."""
    STAFFED = "staffed"
    BENCH = "bench"
    AVAILABLE = "available"


class PersonBase(BaseModel):
    """Base model for Person with common fields."""
    name: str = Field(..., min_length=1, max_length=100,
                      description="Full name of the person")
    role: str = Field(..., min_length=1, max_length=100,
                      description="Job role or title")
    department: str = Field(..., min_length=1, max_length=100,
                            description="Department or team")
    staffing_status: StaffingStatus = Field(...,
                                            description="Current staffing status")

    @validator('name', 'role', 'department')
    def validate_text_fields(cls, v):
        """Validate that text fields are not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError(
                'Field cannot be empty or contain only whitespace')
        return v.strip()


class PersonCreate(PersonBase):
    """Model for creating a new person."""
    pass


class PersonUpdate(BaseModel):
    """Model for updating an existing person. All fields are optional."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = Field(None, min_length=1, max_length=100)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    staffing_status: Optional[StaffingStatus] = None

    @validator('name', 'role', 'department')
    def validate_text_fields(cls, v):
        """Validate that text fields are not empty or just whitespace."""
        if v is not None and (not v or not v.strip()):
            raise ValueError(
                'Field cannot be empty or contain only whitespace')
        return v.strip() if v else v


class Person(PersonBase):
    """Complete Person model with database fields."""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class PersonResponse(BaseModel):
    """Response model for person operations."""
    success: bool
    message: str
    person: Optional[Person] = None


class PeopleListResponse(BaseModel):
    """Response model for listing people."""
    success: bool
    message: str
    people: list[Person]
    total_count: int


class BeachResponse(BaseModel):
    """Response model for beach API - people currently on the beach."""
    success: bool
    message: str
    people_on_beach: list[Person]
    total_count: int
    last_updated: datetime
