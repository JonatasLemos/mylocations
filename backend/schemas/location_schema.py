from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LocationOut(BaseModel):
    id: int
    location_type_id: int
    latitude: float
    longitude: float
    created_at: Optional[datetime]


class LocationTypeOut(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime]
