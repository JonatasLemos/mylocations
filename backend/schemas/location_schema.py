from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class LocationOut(BaseModel):
    """Data schema for location response"""

    id: int
    location_type_id: int
    latitude: float
    longitude: float
    created_at: Optional[datetime]


class LocationTypeOut(BaseModel):
    """Data schema for location type response"""

    id: int
    name: str
    created_at: Optional[datetime]


class LocationCreate(BaseModel):
    """Data schema for location input"""

    latitude: float
    longitude: float
    location_type_id: int
    name: str
    description: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)

    @field_validator("latitude")
    def latitude_exists(cls, value):
        """Check if latitude float is within range

        Args:
            value (_type_): The latitude value

        Raises:
            HTTPException: If value is not within range

        Returns:
            _type_: The validated latitude value
        """
        if not (-90 <= value <= 90):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid latitude: Latitude must be between -90 and 90",
            )
        return value

    @field_validator("longitude")
    def longitude_exists(cls, value):
        """Check if longitude float is within range

        Args:
            value (_type_): The longitude value

        Raises:
            HTTPException: If value is not within range

        Returns:
            _type_: The validated longitude value
        """
        if not (-180 <= value <= 180):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid longitude: Longitude must be between -180 and 180",
            )
        return value

    @field_validator("name", "description")
    def strip_whitespace(cls, value):
        """Strip whitespace from string values"""
        if isinstance(value, str):
            return value.strip()
        return value


class UserLocationOut(BaseModel):
    """Data schema for user location response"""

    location_id: int
    location_name: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    location_type_id: int
    location_type_name: str

    class Config:
        field_mappings = {
            "location_id": "location.id",
            "location_name": "user_location.name",
            "latitude": "latitude",
            "longitude": "longitude",
            "location_type_id": "location_type.id",
            "location_type_name": "location_type.name",
        }
