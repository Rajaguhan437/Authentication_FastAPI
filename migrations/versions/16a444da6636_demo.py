"""demo

Revision ID: 16a444da6636
Revises: 
Create Date: 2024-10-23 10:04:00.033524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import INTEGER, VARCHAR, Column

# revision identifiers, used by Alembic.
revision: str = '16a444da6636'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'User',
        Column('id','INTEGER',primary_key=True, autoincrement=True, nullable=False),
        Column('username', VARCHAR(50), unique=True, nullable=False),
        Column('email', VARCHAR(100), nullable=False),
        Column('password', VARCHAR(100), nullable=False),
        Column('Role')
    )


def downgrade() -> None:
    pass
