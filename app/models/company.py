from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class CompanySearchModel(BaseModel):
    name: str
    
class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    mode: Optional[str]
    rating:  Optional[str]
    
class CompanyCreateModel(BaseModel):
    name: str
    description: Optional[str]
    mode: Optional[str]
    rating:  Optional[str]
    
class CompanyUpdateModel(BaseModel):
    description: Optional[str]
    mode: Optional[str]
    rating:  Optional[str]