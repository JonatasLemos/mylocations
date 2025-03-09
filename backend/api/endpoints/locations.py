from typing import Optional

from api.utils.helpers import get_object_by_id, order_objects
from api.utils.security import validate_token
from core.database import get_db as db
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from models.location import Location
from schemas.location_schema import LocationOut
from sqlalchemy.orm import Session


router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("")
def list_locations(
    db: Session = Depends(db),
    _: None = Depends(validate_token),
    location_type_id: Optional[int] = Query(
        None, description="Filter by location type ID"
    ),
    order_by: Optional[str] = Query(
        None, description="Order by column (e.g., latitude, created_at)"
    ),
    order: Optional[str] = Query("asc", description="Order direction (asc or desc)"),
) -> Page[LocationOut]:
    query = db.query(Location)
    if location_type_id:
        query = query.filter(Location.location_type_id == location_type_id)
    if order_by:
        query = order_objects(Location, order_by, order, query)
    return paginate(db, query)


@router.get("/location_id/")
def detail_location(
    location_id: int,
    db: Session = Depends(db),
    _: None = Depends(validate_token),
) -> LocationOut:
    location = get_object_by_id(Location, location_id, db)
    return location
