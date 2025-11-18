"""add user_id foreign key to transactions

Revision ID: 6403a44625f5
Revises: 50891b7beb08
Create Date: 2025-11-18 16:59:53.658315
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6403a44625f5'
down_revision: Union[str, Sequence[str], None] = '50891b7beb08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema: add user_id foreign key to transactions (SQLite batch mode)."""
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer, nullable=True))
        batch_op.create_foreign_key(
            "fk_transactions_user_id",
            "users",
            ["user_id"],
            ["id"],
        )

def downgrade() -> None:
    """Downgrade schema: remove user_id foreign key from transactions (SQLite batch mode)."""
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.drop_constraint("fk_transactions_user_id", type_="foreignkey")
        batch_op.drop_column("user_id")
