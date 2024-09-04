from typing import Annotated, List, Union
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, utils, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from services.exception import ResourceNotFoundError, ResourceExistedError
from schemas.company import Company
from models.company import CompanyCreateModel, CompanyUpdateModel


def get_all_companies(db: Session) -> List[Company]:
    return db.scalars(select(Company).order_by(Company.name)).all()

def get_companies(name, db: Session) -> List[Company]:
    return db.scalars(select(Company).filter(Company.name.like(f"%{name}%"))).all()

def get_company_by_name(name, db: Session) -> Company:
    return db.scalars(select(Company).filter(Company.name == name)).first()

def create_company(data: CompanyCreateModel, db: Session) -> Company:
    company = Company(**data.model_dump())
    
    if get_company_by_name(data.name, db) is not None:
        raise ResourceExistedError()

    company.description = data.description
    company.mode = data.mode
    company.rating = data.rating
    company.created_at = datetime.now(timezone.utc)
    company.updated_at = datetime.now(timezone.utc)
    
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return company

def update_company(name, data: CompanyUpdateModel, db: Session) -> Company:
    company = get_company_by_name(name, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    company.description = data.description
    company.mode = data.mode
    company.rating = data.rating
    company.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(company)
    
    return company

def delete_company(name, db: Session) -> Company:
    company = get_company_by_name(name, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    db.delete(company)
    db.commit()