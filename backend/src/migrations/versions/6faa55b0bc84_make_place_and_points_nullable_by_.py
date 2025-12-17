"""make place and points nullable by default

Revision ID: 6faa55b0bc84
Revises: c6aead95c464
Create Date: 2025-09-25 14:50:02.152761

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6faa55b0bc84"
down_revision: Union[str, Sequence[str], None] = "c6aead95c464"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("athlete", "place", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("athlete", "points", existing_type=sa.INTEGER(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("athlete", "points", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("athlete", "place", existing_type=sa.INTEGER(), nullable=False)
