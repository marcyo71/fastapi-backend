"""init schema

Revision ID: 50891b7beb08
Revises: 
Create Date: 2025-11-18 16:47:54.625785
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '50891b7beb08'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    # Users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Transactions
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('session_id', sa.String(), nullable=True, unique=True),
        sa.Column('customer_email', sa.String(), nullable=True),
        sa.Column('amount_total', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=True),
    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)

    # User status
    op.create_table(
        'user_status',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('status', sa.String(), nullable=True, unique=True),
    )

    # Referrals
    op.create_table(
        'referrals',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('inviter_id', sa.Integer(), nullable=False),
        sa.Column('invited_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['inviter_id'], ['users.id']),
        sa.ForeignKeyConstraint(['invited_id'], ['users.id']),
    )
    op.create_index(op.f('ix_referrals_id'), 'referrals', ['id'], unique=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index