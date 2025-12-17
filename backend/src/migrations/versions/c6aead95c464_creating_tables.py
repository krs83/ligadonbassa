"""creating tables

Revision ID: c6aead95c464
Revises:
Create Date: 2025-09-21 21:04:06.965545

"""

from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c6aead95c464"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "athlete",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("place", sa.Integer(), nullable=False),
        sa.Column("fullname", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("birth", sa.Date(), nullable=True),
        sa.Column("city", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("region", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_athlete_city"), "athlete", ["city"], unique=False)
    op.create_index(op.f("ix_athlete_fullname"), "athlete", ["fullname"], unique=False)
    op.create_index(op.f("ix_athlete_region"), "athlete", ["region"], unique=False)
    op.create_table(
        "tournament",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("smoothcomp_id", sa.Integer(), nullable=False),
        sa.Column("smoothcomp_date", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tournament_title"), "tournament", ["title"], unique=False)
    op.create_table(
        "athletetournamentlink",
        sa.Column("athlete_id", sa.Integer(), nullable=False),
        sa.Column("tournament_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["athlete_id"],
            ["athlete.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tournament_id"],
            ["tournament.id"],
        ),
        sa.PrimaryKeyConstraint("athlete_id", "tournament_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("athletetournamentlink")
    op.drop_index(op.f("ix_tournament_title"), table_name="tournament")
    op.drop_table("tournament")
    op.drop_index(op.f("ix_athlete_region"), table_name="athlete")
    op.drop_index(op.f("ix_athlete_fullname"), table_name="athlete")
    op.drop_index(op.f("ix_athlete_city"), table_name="athlete")
    op.drop_table("athlete")
