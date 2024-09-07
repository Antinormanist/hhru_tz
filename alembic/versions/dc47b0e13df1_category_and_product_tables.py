"""category and product tables

Revision ID: dc47b0e13df1
Revises: e1197dcdca17
Create Date: 2024-09-07 12:34:37.035903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc47b0e13df1'
down_revision: Union[str, None] = 'e1197dcdca17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String, unique=True, nullable=False)
    )
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('price', sa.Integer, nullable=False),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('now()')),
    )


def downgrade() -> None:
    op.drop_table('categories')
    op.drop_table('products')
