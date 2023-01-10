"""add last few columns to post table

Revision ID: 2660f32671e3
Revises: b0b2fc6e7374
Create Date: 2023-01-10 16:15:53.494736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2660f32671e3'
down_revision = 'b0b2fc6e7374'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE' ),)
    op.add_column('posts',
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)    
    pass

def downgrade() -> None:
    op.drop_column('posts', 'publised')
    op.drop_column('posts', 'created_at')
    pass
