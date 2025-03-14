import datetime

from models.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, UniqueConstraint


class Location(Base):
    """Model to store location related data"""

    __tablename__ = "location"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique identifier for the location",
    )
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        doc="The date and time the location type was created",
    )
    latitude = Column(
        Numeric(precision=8, scale=3),
        index=True,
        nullable=False,
        doc="The latitude of the location",
    )
    longitude = Column(
        Numeric(precision=8, scale=3),
        index=True,
        nullable=False,
        doc="The longitude of the location",
    )
    location_type_id = Column(
        "location_type_id",
        Integer,
        ForeignKey("location_type.id", ondelete="CASCADE"),
        nullable=False,
        doc="The location type",
    )
    __table_args__ = (
        UniqueConstraint(
            "latitude",
            "longitude",
            "location_type_id",
            name="uq_location_lat_long_type",
        ),
    )
