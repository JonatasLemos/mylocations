import datetime

from models.base import Base
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)


class UserLocation(Base):
    """Model to store user location related data"""

    __tablename__ = "user_location"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique identifier for the location",
    )
    name = Column(String, index=True, nullable=False, doc="The name of the location")
    description = Column(Text, doc="Description for the location")
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        doc="The date and time the location type was created",
    )
    user_id = Column(
        "user_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        doc="The user that added the location",
    )
    location_id = Column(
        "location_id",
        Integer,
        ForeignKey("location.id", ondelete="CASCADE"),
        nullable=False,
        doc="The location id ",
    )
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "location_id",
            name="uq_user_location",
        ),
    )
