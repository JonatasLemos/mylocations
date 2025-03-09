from fastapi import HTTPException, status
from models.location import Location
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
