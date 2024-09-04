from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from services import company as CompanyService
from models.company import CompanyUpdateModel, CompanyViewModel, CompanySearchModel, CompanyCreateModel
from schemas.company import Company
from services.exception import ResourceNotFoundError

router = APIRouter(prefix="/company", tags=["Companies"])

@router.get("", response_model=List[CompanyViewModel], status_code=status.HTTP_200_OK)
async def get_all_companies(db: Session = Depends(get_db_context)):
    company = CompanyService.get_all_companies(db)
    
    if company is None:
        raise ResourceNotFoundError()

    return company

@router.get("/search/{name}", response_model=List[CompanyViewModel], status_code=status.HTTP_200_OK)
async def get_companies(name: str, db: Session = Depends(get_db_context)):
    company = CompanyService.get_companies(name, db)
    
    if company is None:
        raise ResourceNotFoundError()

    return company

@router.post("/create", response_model=CompanyViewModel, status_code=status.HTTP_201_CREATED)
async def create_company(data: CompanyCreateModel, db: Session = Depends(get_db_context)):
    company = CompanyService.create_company(data, db)
    return company

@router.put("/update/{name}", response_model=CompanyViewModel, status_code=status.HTTP_200_OK)
async def update_company(name, data: CompanyUpdateModel, db: Session = Depends(get_db_context)):
    company = CompanyService.update_company(name, data, db)
    return company
    
@router.delete("/delete/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(name, db: Session = Depends(get_db_context)):
    company = CompanyService.delete_company(name, db)