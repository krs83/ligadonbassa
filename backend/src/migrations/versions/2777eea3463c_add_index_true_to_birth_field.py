"""add index true to birth field

Revision ID: 2777eea3463c
Revises: 6faa55b0bc84
Create Date: 2025-09-25 15:31:33.816981

"""

from typing import Sequence, Union

from alembic import op


revision: str = "2777eea3463c"
down_revision: Union[str, Sequence[str], None] = "6faa55b0bc84"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(op.f("ix_athlete_city"), table_name="athlete")
    op.create_index(op.f("ix_athlete_birth"), "athlete", ["birth"], unique=False)
    op.create_index(op.f("ix_athlete_points"), "athlete", ["points"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_athlete_points"), table_name="athlete")
    op.drop_index(op.f("ix_athlete_birth"), table_name="athlete")
    op.create_index(op.f("ix_athlete_city"), "athlete", ["city"], unique=False)
