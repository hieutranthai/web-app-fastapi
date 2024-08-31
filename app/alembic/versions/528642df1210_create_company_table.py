"""create company table

Revision ID: 528642df1210
Revises: babf5301034d
Create Date: 2024-08-28 14:24:25.258315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '528642df1210'
down_revision: Union[str, None] = 'babf5301034d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'company',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('description', sa.String(500), unique=True),
        sa.Column('mode', sa.String(100), nullable=True),
        sa.Column('rating', sa.String(100), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('company')
