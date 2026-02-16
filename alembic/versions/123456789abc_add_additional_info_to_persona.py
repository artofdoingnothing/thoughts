"""Add additional_info to Persona

Revision ID: 123456789abc
Revises: 250f1b508c8c
Create Date: 2026-02-16 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '123456789abc'
down_revision: Union[str, None] = '250f1b508c8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('persona', sa.Column('additional_info', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('persona', 'additional_info')
