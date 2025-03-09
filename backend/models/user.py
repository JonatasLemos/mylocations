import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base


UserBase = declarative_base()


class User(UserBase):
    """User ORM model"""

    __tablename__ = "user"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique identifier for the user",
    )
    username = Column(String, index=True, unique=True, doc="The username")
    password = Column(String, doc="The user hashed password")
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        doc="The date and time the user was created",
    )
