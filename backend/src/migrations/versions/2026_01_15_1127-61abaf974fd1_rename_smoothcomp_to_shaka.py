"""rename smoothcomp to shaka

Revision ID: 61abaf974fd1
Revises: ee442e2b725e
Create Date: 2026-01-15 11:27:37.231535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61abaf974fd1'
down_revision: Union[str, Sequence[str], None] = 'ee442e2b725e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('tournament', sa.Column('shaka_id', sa.Integer(), nullable=False))
    op.add_column('tournament', sa.Column('shaka_date', sa.Date(), nullable=True))
    op.drop_constraint(op.f('tournament_smoothcomp_id_key'), 'tournament', type_='unique')
    op.create_unique_constraint(None, 'tournament', ['shaka_id'])
    op.drop_column('tournament', 'smoothcomp_id')
    op.drop_column('tournament', 'smoothcomp_date')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('tournament', sa.Column('smoothcomp_date', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('tournament', sa.Column('smoothcomp_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'tournament', type_='unique')
    op.create_unique_constraint(op.f('tournament_smoothcomp_id_key'), 'tournament', ['smoothcomp_id'], postgresql_nulls_not_distinct=False)
    op.drop_column('tournament', 'shaka_date')
    op.drop_column('tournament', 'shaka_id')
