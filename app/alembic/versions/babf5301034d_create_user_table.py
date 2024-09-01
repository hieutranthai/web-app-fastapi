"""create user table

Revision ID: babf5301034d
Revises: 
Create Date: 2024-08-28 10:52:17.207934

"""
from datetime import datetime, timezone
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from services import user as UserService


# revision identifiers, used by Alembic.
revision: str = "babf5301034d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_table = op.create_table(
        "user",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column("username", sa.String(100), unique=True),
        sa.Column("first_name", sa.Unicode(100), nullable=False),
        sa.Column("last_name", sa.Unicode(100), nullable=True),
        sa.Column("password", sa.String(500), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("is_admin", sa.Boolean, default=False, nullable=False),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime)
    )
    op.bulk_insert(
        user_table,
        [
            {
                "id": uuid4(),
                "email": "admin@gmail.com",
                "username": "admin",
                "first_name": "admin",
                "last_name": None,
                "password": UserService.get_password_hash("admin"),
                "is_active": True,
                "is_admin": True,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
        ]
    )

def downgrade() -> None:
    op.drop_table("user")
