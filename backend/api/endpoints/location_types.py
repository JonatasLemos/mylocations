from typing import Optional

from api.utils.helpers import get_object_by_id, order_objects
from api.utils.security import validate_token
from core.database import get_db as db
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from models.location_type import LocationType
from schemas.location_schema import LocationTypeOut
from sqlalchemy.orm import Session


router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/location-types/")
def list_location_types(
    db: Session = Depends(db),
    _: None = Depends(validate_token),
    order_by: Optional[str] = Query(
        None, description="Order by column (e.g., name, created_at)"
    ),
    order: Optional[str] = Query("asc", description="Order direction (asc or desc)"),
) -> Page[LocationTypeOut]:
    query = db.query(LocationType)
    if order_by:
        query = order_objects(LocationType, order_by, order, query)
    return paginate(db, query)


@router.get("/location-types/{location_type_id}/")
def detail_location_types(
    location_type_id: int,
    db: Session = Depends(db),
    _: None = Depends(validate_token),
) -> LocationTypeOut:
    location_type = get_object_by_id(LocationType, location_type_id, db)
    return location_type
