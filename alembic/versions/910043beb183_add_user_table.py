"""add user table

Revision ID: 910043beb183
Revises: 4c4e2382725e
Create Date: 2023-01-10 16:03:23.712400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '910043beb183'
down_revision = '4c4e2382725e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass

def downgrade() -> None:
    op.drop_table('users')
    pass
