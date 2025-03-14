from typing import Optional

from api.services.location_service import CreateLocation, ListUserLocations
from api.utils.exceptions import NotFoundException
from api.utils.helpers import CustomPaginator, get_object_by_id, order_objects
from api.utils.security import validate_token
from api.utils.swagger_doc import (
    BAD_REQUEST_400,
    FORBIDEN_403,
    LOCATION_DETAIL_200,
    LOCATION_LIST_200,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
    USER_LOCATION_LIST_200,
    USER_LOCATION_PATCH_REPONSE,
)
from core.database import get_db as db
from fastapi import APIRouter, Depends, Path, Query, status
from models.location import Location
from models.location_type import LocationType
from models.user import User
from models.user_location import UserLocation
from schemas.location_schema import (
    LocationCreate,
    LocationCreateOut,
    LocationOut,
    LocationUpdate,
    PaginatedResponse,
    UserLocationOut,
)
from sqlalchemy.orm import Session


router = APIRouter(prefix="/locations", tags=["locations"])
user_location_router = APIRouter(prefix="/my-locations", tags=["locations"])


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
def list_locations(
    db: Session = Depends(db),
    user=Depends(validate_token),
    location_type_id: Optional[int] = Query(
        None, description="Filter by location type ID"
    ),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    order_by: Optional[str] = Query(
        None, description="Order by column (e.g., latitude, created_at)"
    ),
    order: Optional[str] = Query("asc", description="Order direction (asc or desc)"),
) -> PaginatedResponse:
    """
    Retrieves a paginated list of locations.
    """
    query = db.query(Location)
    if location_type_id:
        query = query.filter(Location.location_type_id == location_type_id)
    if order_by:
        query = order_objects(Location, order_by, order, query)
    custom_paginator = CustomPaginator(query, page, size)
    items = custom_paginator.paginate_query()
    return PaginatedResponse(
        items=[LocationOut.model_validate(item) for item in items],
        total=custom_paginator.total,
        page=page,
        size=size,
        pages=custom_paginator.pages,
    )


@router.get(
    "/{location_id}/",
    responses={
        200: LOCATION_DETAIL_200,
        400: BAD_REQUEST_400,
        401: UNAUTHORIZED_401,
        403: FORBIDEN_403,
        404: NOT_FOUND_404,
    },
)
def detail_location(
    location_id: int = Path(description="The id of the location to retrieve."),
    db: Session = Depends(db),
    user=Depends(validate_token),
) -> LocationOut:
    """
    Retrieves details of a specific location by its ID.
    """
    location = get_object_by_id(Location, location_id, db)
    return location


@user_location_router.get(
    "/list/",
    responses={
        200: USER_LOCATION_LIST_200,
        400: BAD_REQUEST_400,
        401: UNAUTHORIZED_401,
        403: FORBIDEN_403,
    },
)
def list_user_locations(
    db: Session = Depends(db),
    user: User = Depends(validate_token),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    order_by: Optional[str] = Query(
        None, description="Order by column (e.g., latitude, created_at)"
    ),
    order: Optional[str] = Query("asc", description="Order direction (asc or desc)"),
) -> PaginatedResponse:
    """
    Retrieves a paginated list of user locations.
    """
    user_locations = ListUserLocations(
        db=db,
        user=user,
        order_by=order_by,
        order=order,
        validation_model=UserLocationOut,
        page=page,
        size=size,
    )
    return PaginatedResponse(
        items=[
            UserLocationOut.model_validate(item) for item in user_locations.response
        ],
        total=user_locations.total,
        page=page,
        size=size,
        pages=user_locations.pages,
    )


@user_location_router.post(
    "/create/",
    status_code=status.HTTP_201_CREATED,
    responses={400: BAD_REQUEST_400, 401: UNAUTHORIZED_401, 403: FORBIDEN_403},
)
def create_location(
    data: LocationCreate,
    db: Session = Depends(db),
    user: User = Depends(validate_token),
) -> LocationCreateOut:
    """Add a new location for the user."""
    get_object_by_id(
        LocationType,
        data.location_type_id,
        db,
        status_code=400,
        msg="Invalid location_type_id: Location type not found",
    )
    create_location = CreateLocation(db, data, user)
    response = create_location.get_response()

    return response


@user_location_router.patch(
    "/{user_location_id}/",
    responses={
        200: USER_LOCATION_PATCH_REPONSE,
        400: BAD_REQUEST_400,
        401: UNAUTHORIZED_401,
        403: FORBIDEN_403,
        404: NOT_FOUND_404,
    },
)
def update_user_location(
    data: LocationUpdate,
    user_location_id: int = Path(
        description=("The id of the user location to update.")
    ),
    db: Session = Depends(db),
    user: User = Depends(validate_token),
):
    """Update description and name for a specific user location"""
    user_location = (
        db.query(UserLocation).filter(UserLocation.id == user_location_id).first()
    )
    if not user_location:
        raise NotFoundException()
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user_location, field, value)
    db.commit()
    db.refresh(user_location)
    return user_location


@user_location_router.delete(
    "/{user_location_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: UNAUTHORIZED_401,
        403: FORBIDEN_403,
        404: NOT_FOUND_404,
    },
)
def delete_user_location(
    user_location_id: int = Path(description="The id of the user location to delete."),
    db: Session = Depends(db),
    user: User = Depends(validate_token),
):
    """Delete specific user location"""
    location = (
        db.query(UserLocation).filter(UserLocation.id == user_location_id).first()
    )
    if not location:
        raise NotFoundException()
    db.delete(location)
    db.commit()
