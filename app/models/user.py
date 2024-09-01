from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class UserSearchModel(BaseModel):
    username: str
    
class UserViewModel(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name:  Optional[str]
    is_active: bool
    is_admin: bool
    
class UserCreateModel(BaseModel):
    email: str
    username: str
    first_name: str
    last_name:  Optional[str]
    password: str
    is_active: bool
    is_admin: bool
    
class UserUpdateModel(BaseModel):
    first_name: str
    last_name:  Optional[str]
    is_active: bool