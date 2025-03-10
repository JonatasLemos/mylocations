from api.utils.helpers import order_objects_with_literals
from fastapi import HTTPException, status
from models.location import Location
from models.location_type import LocationType
from models.user_location import UserLocation
from sqlalchemy.orm import Session


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
        self.get_or_create_location()

    def get_or_create_location(self):
        """Check if a Location with the same coordinates and location type
        exists, if not create a new one"""
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
        self.commit_changes()

    def commit_changes(self):
        """Commit changes to the database"""
        self.db.commit()


class ListUserLocations:
    def __init__(self, db: Session, user: dict, order_by, order, validation_model):
        """Class initializer

        Args:
            db (Session): The database session
            user (dict): The user instance
        """
        self.db = db
        self.user = user
        self.order_by = order_by
        self.order = order
        self.validation_model = validation_model
        self.field_mapping = validation_model.Config.field_mappings
        self.query = None
        self.response = []
        self.construct_query()

    def construct_query(self):
        self.query = (
            self.db.query(UserLocation, Location, LocationType)
            .join(Location, UserLocation.location_id == Location.id)
            .join(LocationType, Location.location_type_id == LocationType.id)
            .filter(UserLocation.user_id == self.user.id)
        )
        self.add_ordering()

    def add_ordering(self):
        if self.order_by not in self.field_mapping.keys():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Filter: {self.order_by} is not allowed.",
            )
        self.query = order_objects_with_literals(
            self.field_mapping[self.order_by], self.order, self.query
        )
        self.check_user_location_exists()

    def check_user_location_exists(self):
        user_locations = self.query.all()
        if not user_locations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No locations found for the user {self.user.id}",
            )
        self.create_response(user_locations)

    def create_response(self, user_locations):
        for user_location, location, location_type in user_locations:
            self.response.append(
                self.validation_model(
                    location_id=user_location.location_id,
                    location_name=user_location.name,
                    description=user_location.description,
                    latitude=location.latitude,
                    longitude=location.longitude,
                    location_type_id=location.location_type_id,
                    location_type_name=location_type.name,
                )
            )
