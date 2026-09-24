"""add content col 

Revision ID: 62495683bd20
Revises: 4ab6f257c87d
Create Date: 2026-09-23 20:00:36.489979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62495683bd20'
down_revision: Union[str, Sequence[str], None] = '4ab6f257c87d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
