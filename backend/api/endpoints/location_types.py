from typing import Optional

from api.utils.helpers import CustomPaginator, get_object_by_id, order_objects
from api.utils.security import validate_token
from api.utils.swagger_doc import (
    BAD_REQUEST_400,
    FORBIDEN_403,
    LOCATION_LIST_200,
    LOCATION_TYPE_DETAIL_200,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
)
from core.database import get_db as db
from fastapi import APIRouter, Depends, Path, Query
from models.location_type import LocationType
from schemas.location_schema import LocationTypeOut, PaginatedResponse
from sqlalchemy.orm import Session


router = APIRouter(prefix="/location-types", tags=["locations"])


@router.get(
    "/list/",
    response_model=PaginatedResponse,
    responses={
        200: LOCATION_LIST_200,
        400: BAD_REQUEST_400,
        401: UNAUTHORIZED_401,
        403: FORBIDEN_403,
    },
)
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
    """
    Retrieves a paginated list of location types.
    """
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


@router.get(
    "/{location_type_id}/",
    response_model=LocationTypeOut,
    responses={
        200: LOCATION_TYPE_DETAIL_200,
        400: BAD_REQUEST_400,
        401: UNAUTHORIZED_401,
        403: FORBIDEN_403,
        404: NOT_FOUND_404,
    },
)
def detail_location_types(
    location_type_id: int = Path(description="The ID of the location type to retrieve"),
    db: Session = Depends(db),
    user=Depends(validate_token),
) -> LocationTypeOut:
    """
    Retrieves details of a specific location type by its ID.
    """
    location_type = get_object_by_id(LocationType, location_type_id, db)
    return location_type
