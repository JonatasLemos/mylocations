from api.utils.exceptions import NotFoundException
from api.utils.helpers import CustomPaginator, order_objects_with_literals
from fastapi import HTTPException, status
from models.location import Location
from models.location_type import LocationType
from models.user_location import UserLocation
from pydantic import BaseModel
from schemas.location_schema import LocationCreateOut
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query


class CreateLocation:
    """Service to create a location"""

    def __init__(self, db: Session, data: dict, user: dict):
        """Class initializer

        Args:
            db (Session): The database session
            data (dict): The validated location data
            user (dict): The user instance
        """
        self.db = db
        self.data = data
        self.user = user
        self.location = None
        self.get_or_create_location()

    def get_or_create_location(self):
        """Check if a Location with the same coordinates and location type
        exists, if not add a new one"""
        location = (
            self.db.query(Location)
            .filter(
                Location.latitude == self.data.latitude,
                Location.longitude == self.data.longitude,
                Location.location_type_id == self.data.location_type_id,
            )
            .first()
        )
        if not location:
            location = Location(
                latitude=self.data.latitude,
                longitude=self.data.longitude,
                location_type_id=self.data.location_type_id,
            )
            self.db.add(location)
            self.db.flush()
        self.create_user_location(location)

    def create_user_location(self, location):
        """Create an UserLocation instance with the user_id, location_id
        Args:
            location: The location model
        Raises:
            HTTPException: Raises 400 if UserLocation with the same user_id
            and location_id exists
        """
        existing_user_location = (
            self.db.query(UserLocation)
            .filter(
                UserLocation.user_id == self.user.id,
                UserLocation.location_id == location.id,
            )
            .first()
        )

        if existing_user_location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has already added this location",
            )

        user_location = UserLocation(
            user_id=self.user.id,
            location_id=location.id,
            name=self.data.name,
            description=self.data.description,
        )
        self.db.add(user_location)
        self.location = location

        self.commit_changes()

    def commit_changes(self):
        """Commit changes to the database"""
        self.db.commit()

    def get_response(self):
        """Create endpoint ready response with the location created"""
        last_location = (
            self.db.query(UserLocation)
            .filter(
                UserLocation.user_id == self.user.id,
                UserLocation.location_id == self.location.id,
            )
            .first()
        )
        return LocationCreateOut(
            id=last_location.id,
            name=last_location.name,
            location_id=last_location.location_id,
            description=last_location.description,
            user_id=last_location.user_id,
            created_at=last_location.created_at,
        )


class ListUserLocations:
    """Service to list all location data related to an user"""

    def __init__(
        self,
        db: Session,
        user: dict,
        order_by: str,
        order: str,
        validation_model: BaseModel,
        page: int,
        size: int,
    ):
        """Constructor

        Args:
            db (Session): The database session
            user (dict): The user object
            order_by (str): The field to order by
            order (str): The order direction asc or desc.
            validation_model (BaseModel): The pydantic validation model
            page (int): The page to paginate
            size (int): Number of items in the page
        """
        self.db = db
        self.user = user
        self.order_by = order_by
        self.order = order
        self.validation_model = validation_model
        self.page = page
        self.size = size
        self.field_mapping: dict = validation_model.Config.field_mappings
        self.query: Query = None
        self.items = []
        self.response = []
        self.total: int = None
        self.pages: int = None
        self.construct_query()

    def construct_query(self):
        """Construct query to get all location data from the user"""
        self.query = (
            self.db.query(UserLocation, Location, LocationType)
            .join(Location, UserLocation.location_id == Location.id)
            .join(LocationType, Location.location_type_id == LocationType.id)
            .filter(UserLocation.user_id == self.user.id)
        )
        self.add_ordering()

    def add_ordering(self):
        """Add order by to user location query"""
        if self.order_by:
            if self.order_by not in self.field_mapping.keys():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Filter: {self.order_by} is not allowed.",
                )
            self.query = order_objects_with_literals(
                self.field_mapping[self.order_by], self.order, self.query
            )
        self.add_pagination()

    def add_pagination(self):
        """Paginate user location query"""
        custom_paginator = CustomPaginator(self.query, self.page, self.size)
        self.items = custom_paginator.paginate_query()
        self.total = custom_paginator.total
        self.pages = custom_paginator.pages
        self.check_user_location_exists()

    def check_user_location_exists(self):
        """Check if user has location data"""
        if not self.items:
            raise NotFoundException()
        self.create_response(self.items)

    def create_response(self, items):
        """Create user location response using validation model"""
        for user_location, location, location_type in items:
            self.response.append(
                self.validation_model(
                    user_location_id=user_location.id,
                    location_id=user_location.location_id,
                    location_name=user_location.name,
                    description=user_location.description,
                    latitude=location.latitude,
                    longitude=location.longitude,
                    location_type_id=location.location_type_id,
                    location_type_name=location_type.name,
                )
            )
