
from typing import Annotated, List, Union
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, utils, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext

from services.exception import ResourceNotFoundError
from settings import JWT_SECRET, JWT_ALGORITHM
from models.token import TokenData
from schemas.user import User
from models.user import UserCreateModel, UserUpdateModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_all_users(db: Session) -> List[User]:
    return db.scalars(select(User).order_by(User.created_at)).all()

def get_users(username, db: Session) -> List[User]:
    return db.scalars(select(User).filter(User.username.like(f"%{username}%"))).all()

def get_user_by_email(email, db: Session) -> User:
    return db.scalars(select(User).filter(User.email == email)).first()

def create_user(data: UserCreateModel, db: Session) -> User:
    user = User(**data.model_dump())

    user.password = get_password_hash(data.password)
    user.created_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

def update_user(email, data: UserUpdateModel, db: Session) -> User:
    user = get_user_by_email(email, db)
    
    if user is None:
        raise ResourceNotFoundError()
    
    user.first_name = data.first_name
    user.last_name = data.last_name
    
    db.commit()
    db.refresh(user)
    
    return user

def delete_user(email, db: Session) -> User:
    user = get_user_by_email(email, db)
    
    if user is None:
        raise ResourceNotFoundError()
    
    db.delete(user)
    db.commit()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    print(user.password)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user