import uuid

from sqlalchemy import Boolean, Column, String, UUID
from sqlalchemy.orm import DeclarativeBase
from database import Base
from .base_entity import BaseEntity

class User(BaseEntity, Base):
    __tablename__ = "user"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False)