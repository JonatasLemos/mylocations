import datetime

from models.base import Base
from sqlalchemy import Column, DateTime, Integer, String


class User(Base):
    """User ORM model"""

    __tablename__ = "user"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique identifier for the user",
    )
    username = Column(
        String, index=True, unique=True, nullable=False, doc="The username"
    )
    password = Column(String, nullable=False, doc="The user hashed password")
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        doc="The date and time the user was created",
    )
