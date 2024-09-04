"""create task table

Revision ID: a74a3119b4f3
Revises: 528642df1210
Create Date: 2024-08-28 14:24:35.952317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a74a3119b4f3'
down_revision: Union[str, None] = '528642df1210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'task',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('summary', sa.String(500), nullable=False),
        sa.Column('description', sa.String(500), unique=True),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('priority', sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('task')
