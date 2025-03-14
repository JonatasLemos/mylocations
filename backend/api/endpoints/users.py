from datetime import timedelta

from api import REFRESH_SECRET_KEY
from api.utils.security import (
    create_token,
    decode_token,
    hash_password,
    validate_token,
    verify_password,
)
from api.utils.swagger_doc import (
    AUTHENTICATION_TOKEN_200_RESPONSE,
    FORBIDEN_403,
    REFRESH_TOKEN_200_RESPONSE,
    UNAUTHORIZED_401,
)
from core.database import get_db as db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from schemas.user_schema import (
    Login,
    RegistrationOut,
    TokenRefreshRequest,
    UserOut,
    UserRegistration,
)
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register/", status_code=status.HTTP_201_CREATED)
def register_user(data: UserRegistration, db: Session = Depends(db)) -> RegistrationOut:
    """Register a new user."""
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(username=data.username, password=hash_password(data.password))
    db.add(new_user)
    db.commit()
    response = RegistrationOut(
        user_id=new_user.id,
        username=new_user.username,
        created_at=new_user.created_at,
    )
    return response


@router.post(
    "/auth/token/",
    responses={200: AUTHENTICATION_TOKEN_200_RESPONSE, 401: UNAUTHORIZED_401},
)
def login(data: Login, db: Session = Depends(db)):
    """Get access token providing username and password"""
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = create_token(data={"sub": user.username})
    refresh_token = create_token(
        data={"sub": user.username},
        token_type="refresh",
        expiration_delta=timedelta(days=7),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/auth/refresh/",
    responses={200: REFRESH_TOKEN_200_RESPONSE, 401: UNAUTHORIZED_401},
)
def refresh_token(data: TokenRefreshRequest):
    """Get a new access token using the refresh token"""
    payload = decode_token(data.refresh_token, REFRESH_SECRET_KEY)

    username: str = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    new_access_token = create_token(data={"sub": username})

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/me/", responses={403: FORBIDEN_403})
def user_detail(db: Session = Depends(db), user=Depends(validate_token)) -> UserOut:
    """Get username."""

    return {"username": user.username}
