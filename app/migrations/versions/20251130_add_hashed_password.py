"""add hashed_password column to users"""

from alembic import op
import sqlalchemy as sa

# Identificatori revisione
revision = "20251130_add_hashed_password"

down_revision = '03af37a7b7bd'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("users", sa.Column("hashed_password", sa.String(200), nullable=False))

def downgrade():
    op.drop_column("users", "hashed_password")
