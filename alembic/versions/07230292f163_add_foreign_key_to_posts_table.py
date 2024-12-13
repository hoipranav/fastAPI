"""add foreign key to posts table

Revision ID: 07230292f163
Revises: 6d414dcf8521
Create Date: 2024-12-13 18:11:14.275951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07230292f163'
down_revision: Union[str, None] = '6d414dcf8521'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    
    op.create_foreign_key(
        'post_user_fkey',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('post_user_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')