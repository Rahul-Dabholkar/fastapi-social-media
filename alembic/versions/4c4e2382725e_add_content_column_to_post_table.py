"""add content column to post table

Revision ID: 4c4e2382725e
Revises: a1304270c409
Create Date: 2023-01-10 15:57:56.607378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c4e2382725e'
down_revision = 'a1304270c409'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
