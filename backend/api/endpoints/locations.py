from typing import Optional

from api.services.location_service import CreateLocation, ListUserLocations
from api.utils.helpers import CustomPaginator, get_object_by_id, order_objects
from api.utils.security import validate_token
from core.database import get_db as db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models.location import Location
from models.location_type import LocationType
from models.user import User
from models.user_location import UserLocation
from schemas.location_schema import (
    LocationCreate,
    LocationOut,
    LocationUpdate,
    PaginatedResponse,
    UserLocationOut,
)
from sqlalchemy.orm import Session


router = APIRouter(prefix="/locations", tags=["locations"])
user_location_router = APIRouter(prefix="/user-locations", tags=["locations"])


@router.get("/list/", response_model=PaginatedResponse)
def list_locations(
    db: Session = Depends(db),
    user=Depends(validate_token),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    location_type_id: Optional[int] = Query(
        None, description="Filter by location type ID"
    ),
    order_by: Optional[str] = Query(
        None, description="Order by column (e.g., latitude, created_at)"
    ),
    order: Optional[str] = Query("asc", description="Order direction (asc or desc)"),
):
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


@router.get("/{location_id}/")
def detail_location(
    location_id: int,
    db: Session = Depends(db),
    user=Depends(validate_token),
) -> LocationOut:
    location = get_object_by_id(Location, location_id, db)
    return location


@user_location_router.get("/list/")
def list_user_locations(
    db: Session = Depends(db),
    user: User = Depends(validate_token),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    order_by: Optional[str] = Query(
        None, description="Order by column (e.g., latitude, created_at)"
    ),
    order: Optional[str] = Query("asc", description="Order direction (asc or desc)"),
):
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
        pages=user_locations.page,
    )


@user_location_router.post("/create/", status_code=status.HTTP_201_CREATED)
def create_location(
    data: LocationCreate,
    db: Session = Depends(db),
    user: User = Depends(validate_token),
):
    get_object_by_id(
        LocationType,
        data.location_type_id,
        db,
        status_code=400,
        msg="Invalid location_type_id: Location type not found",
    )
    CreateLocation(db, data, user)

    return {"detail": "Location created successfully"}


@user_location_router.patch("/{user_location_id}/")
def update_user_location(
    data: LocationUpdate,
    user_location_id: int,
    db: Session = Depends(db),
    user: User = Depends(validate_token),
):
    user_location = (
        db.query(UserLocation).filter(UserLocation.id == user_location_id).first()
    )
    if not user_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user_location, field, value)
    db.commit()
    db.refresh(user_location)
    return user_location


@user_location_router.delete(
    "/{user_location_id}/", status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_location(
    user_location_id,
    db: Session = Depends(db),
    user: User = Depends(validate_token),
):
    location = (
        db.query(UserLocation).filter(UserLocation.id == user_location_id).first()
    )
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )
    db.delete(location)
    db.commit()
