"""change default points field to ZERO

Revision ID: cd43331bdc06
Revises: 8caede7a3e4b
Create Date: 2025-10-23 12:08:24.788025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'cd43331bdc06'
down_revision: Union[str, Sequence[str], None] = '8caede7a3e4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('athlete', 'points',
               existing_type=sa.INTEGER(),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('athlete', 'points',
               existing_type=sa.INTEGER(),
               nullable=True)
