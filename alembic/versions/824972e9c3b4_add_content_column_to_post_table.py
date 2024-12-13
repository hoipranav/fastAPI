"""add content column to post table

Revision ID: 824972e9c3b4
Revises: edcd6a529716
Create Date: 2024-12-13 17:57:07.765909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '824972e9c3b4'
down_revision: Union[str, None] = 'edcd6a529716'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts', sa.Column('content', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column('posts', 'content')