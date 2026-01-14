"""add is_active=True field to athlete table

Revision ID: ee442e2b725e
Revises: 883f87d2f18b
Create Date: 2025-12-28 18:41:04.307461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee442e2b725e'
down_revision: Union[str, Sequence[str], None] = '883f87d2f18b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('athlete', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.execute("UPDATE athlete SET is_active = TRUE")
    op.alter_column('athlete', 'is_active', nullable=False)
    op.alter_column('athlete', 'is_active', server_default=sa.text('TRUE'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('athlete', 'is_active')
