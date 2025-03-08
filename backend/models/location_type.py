import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class LocationType(Base):
    """LocationType ORM model"""

    __tablename__ = "location_type"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique identifier for the location type",
    )
    name = Column(String, index=True, unique=True, doc="The name of the location type")
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        doc="The date and time the location type was created",
    )
