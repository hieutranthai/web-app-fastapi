from sqlalchemy import Column, Uuid, Time
import enum

class Gender(enum.Enum):
    NONE = 'N'
    FEMALE = 'F'
    MALE = 'M'


class BaseEntity:
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)