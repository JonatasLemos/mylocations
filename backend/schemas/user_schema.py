import re

from pydantic import BaseModel, field_validator


class UserBase(BaseModel):
    username: str
    password: str


class Login(UserBase):
    pass


class UserRegistration(UserBase):
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")
        return password
