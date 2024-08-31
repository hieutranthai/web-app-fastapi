from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from services import user as UserService
from models.user import UserUpdateModel, UserViewModel, UserSearchModel, UserCreateModel
from schemas.user import User
from services.exception import ResourceNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserViewModel])
async def get_all_users(db: Session = Depends(get_db_context)):
    user = UserService.get_all_users(db)
    
    if user is None:
        raise ResourceNotFoundError()

    return user

@router.get("/search/{username}", response_model=List[UserViewModel])
async def get_users(username: str, db: Session = Depends(get_db_context)):
    user = UserService.get_users(username, db)
    
    if user is None:
        raise ResourceNotFoundError()

    return user

@router.post("/create", response_model=UserViewModel)
async def create_user(data: UserCreateModel, db: Session = Depends(get_db_context)):
    user = UserService.create_user(data, db)
    return user

@router.put("/update", response_model=UserViewModel)
async def update_user(data: UserUpdateModel, db: Session = Depends(get_db_context)):
    user = UserService.update_user(data, db)
    return user
    
@router.delete("/delete/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email, db: Session = Depends(get_db_context)):
    user = UserService.delete_user(email, db)