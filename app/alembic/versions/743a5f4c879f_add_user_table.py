"""add user table

Revision ID: 743a5f4c879f
Revises: 289ef98429b5
Create Date: 2025-12-29 21:28:39.798433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "743a5f4c879f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False, unique=True, index=True),
    )

def downgrade():
    op.drop_table("users")