import datetime

from models.base import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, UniqueConstraint


class Location(Base):
    """Location ORM model"""

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
    latitude = Column(Float(precision=16), doc="The latitude of the location")
    longitude = Column(Float(precision=16), doc="The longitude of the location")
    location_type_id = Column(
        "location_type_id",
        Integer,
        ForeignKey("location_type.id", ondelete="CASCADE"),
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
