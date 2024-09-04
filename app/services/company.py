
from typing import Annotated, List, Union
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, utils, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from services.exception import ResourceNotFoundError
from schemas.user import Company
from models.user import CompanyCreateModel, CompanyUpdateModel


def get_all_companies(db: Session) -> List[Company]:
    return db.scalars(select(Company).order_by(Company.created_at)).all()

def get_companies(name, db: Session) -> List[Company]:
    return db.scalars(select(Company).filter(Company.name.like(f"%{name}%"))).all()

def get_company_by_name(name, db: Session) -> Company:
    return db.scalars(select(Company).filter(Company.name == name)).first()

def create_company(data: CompanyCreateModel, db: Session) -> Company:
    company = Company(**data.model_dump())

    company.description = data.description
    company.mode = data.mode
    company.rating = data.rating
    company.created_at = datetime.now(timezone.utc)
    company.updated_at = datetime.now(timezone.utc)
    
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return company

def update_copmany(name, data: CompanyUpdateModel, db: Session) -> Company:
    company = get_company_by_name(name, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    company.description = data.description
    company.mode = data.mode
    company.rating = data.rating
    
    db.commit()
    db.refresh(company)
    
    return company

def delete_company(name, db: Session) -> Company:
    company = get_company_by_name(name, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    db.delete(company)
    db.commit()