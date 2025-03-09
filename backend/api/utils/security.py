from datetime import datetime, timedelta

from api import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from core.database import get_db as db
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from models.user import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash plain text password

    Args:
        password (str): The plaint text password

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if plain password matches hashed password

    Args:
        plain_password (str): Plain text password
        hashed_password (str): Hashed password

    Returns:
        bool: True if plain password matches hashed password, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create access token given user data

    Args:
        data (dict): User data dictionary

    Returns:
        str: Bearer token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


security = HTTPBearer()


def validate_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(db),
):
    """Validate if provided token is correct

    Args:
        credentials (HTTPAuthorizationCredentials, optional): _description_.
        Defaults to Security(security).
        db: The db session. Defaults to Depends(db).
    Raises:
        HTTPException: Raises 401 if token is invalid
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
