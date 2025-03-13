from datetime import datetime, timedelta

import bcrypt
from api import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, REFRESH_SECRET_KEY, SECRET_KEY
from core.database import get_db as db
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from models.user import User
from sqlalchemy.orm import Session


def hash_password(password: str) -> str:
    """Hash plain text password

    Args:
        password (str): The plaint text password

    Returns:
        str: Hashed password
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if plain password matches hashed password

    Args:
        plain_password (str): Plain text password
        hashed_password (str): Hashed password

    Returns:
        bool: True if plain password matches hashed password, False otherwise
    """
    password_byte_enc = plain_password.encode("utf-8")
    hashed_password_byte_enc = hashed_password.encode("utf-8")
    return bcrypt.checkpw(
        password=password_byte_enc, hashed_password=hashed_password_byte_enc
    )


def create_token(
    data: dict,
    token_type: str = "access",
    expiration_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    """Create access token given user data

    Args:
        data (dict): User data dictionary

    Returns:
        str: Bearer token
    """
    secret_keys = dict(refresh=REFRESH_SECRET_KEY, access=SECRET_KEY)
    to_encode = data.copy()
    expire = datetime.utcnow() + expiration_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_keys[token_type], algorithm=ALGORITHM)


security = HTTPBearer()


def validate_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(db),
):
    """Validate if the provided token is correct.

    Args:
        credentials (HTTPAuthorizationCredentials, optional): Token credentials.
        db (Session, optional): The database session.

    Raises:
        HTTPException: If the token is invalid or the user is not found.

    Returns:
        User: The authenticated user.
    """
    token = credentials.credentials
    payload = decode_token(token, SECRET_KEY)  # Use the new function

    username: str = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing subject",
        )

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    return user


def decode_token(token: str, secret_key: str) -> dict:
    """Decode and validate a JWT token.

    Args:
        token (str): The JWT token to decode.
        secret_key (str): The secret key used to decode the token.

    Returns:
        dict: The decoded payload.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
