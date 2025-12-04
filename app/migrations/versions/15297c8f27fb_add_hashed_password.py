"""add hashed password

Revision ID: 15297c8f27fb
Revises: 20251130_add_hashed_password
Create Date: 2025-11-30 17:00:21.722919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15297c8f27fb'
down_revision = '20251130_add_hashed_password'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('hashed_password', sa.String(length=200), nullable=False, server_default='')
    )
    op.alter_column('users', 'hashed_password', server_default=None)

def downgrade() -> None:
    op.drop_column('users', 'hashed_password')
