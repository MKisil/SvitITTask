from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth import schemas, utils
from src.auth.models import User
from src.database import get_db
from src.config import settings

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=schemas.UserGet, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    is_exists = utils.check_user_exists(user.username, db)
    if is_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists."
        )
    new_user = utils.create_user(user, db)
    return new_user


@router.post("/login")
def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = utils.authenticate_user(user_data.username, user_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=schemas.UserGet)
def get_user(current_user: Annotated[User, Depends(utils.get_current_user)]):
    return current_user
