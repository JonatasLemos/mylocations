import re
from datetime import datetime

from pydantic import BaseModel, field_validator


class UserBase(BaseModel):
    """User input schema"""

    username: str
    password: str


class Login(UserBase):
    """User login schema"""

    pass


class RegistrationOut(BaseModel):
    """User registration response"""

    user_id: int
    username: str
    created_at: datetime


class UserRegistration(UserBase):
    """User registration input"""

    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, password):
        """Validate if password has lenght > 8 and if password has
        special characters"""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")
        return password


class TokenRefreshRequest(BaseModel):
    """Data schema for token refresh input"""

    refresh_token: str


class UserOut(BaseModel):
    """Data schema user detail output"""

    username: str
