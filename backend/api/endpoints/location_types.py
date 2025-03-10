from typing import Optional

from api.utils.helpers import CustomPaginator, get_object_by_id, order_objects
from api.utils.security import validate_token
from core.database import get_db as db
from fastapi import APIRouter, Depends, Query
from models.location_type import LocationType
from schemas.location_schema import LocationTypeOut, PaginatedResponse
from sqlalchemy.orm import Session


router = APIRouter(prefix="/location-types", tags=["locations"])


@router.get("/list/", response_model=PaginatedResponse)
def list_location_types(
    db: Session = Depends(db),
    user=Depends(validate_token),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    order_by: Optional[str] = Query(
        None, description="Order by column (e.g., name, created_at)"
    ),
    order: Optional[str] = Query("asc", description="Order direction (asc or desc)"),
):
    query = db.query(LocationType)
    if order_by:
        query = order_objects(LocationType, order_by, order, query)
    custom_paginator = CustomPaginator(query, page, size)
    items = custom_paginator.paginate_query()
    return PaginatedResponse(
        items=[LocationTypeOut.model_validate(item) for item in items],
        total=custom_paginator.total,
        page=page,
        size=size,
        pages=custom_paginator.pages,
    )


@router.get("/{location_type_id}/", response_model=LocationTypeOut)
def detail_location_types(
    location_type_id: int,
    db: Session = Depends(db),
    user=Depends(validate_token),
) -> LocationTypeOut:
    location_type = get_object_by_id(LocationType, location_type_id, db)
    return location_type
