import uuid

from sqlalchemy import Boolean, Column, String, UUID
from sqlalchemy.orm import DeclarativeBase
from database import Base
from .base_entity import BaseEntity

class User(BaseEntity, Base):
    __tablename__ = "company"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    mode = Column(String, nullable=True)
    rating = Column(String, nullable=True)