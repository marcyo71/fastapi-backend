"""create user_status table

Revision ID: 38a570cedaf9
Revises: a1946162aa95
Create Date: 2025-11-15 19:15:07.052831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38a570cedaf9'
down_revision: Union[str, Sequence[str], None] = 'a1946162aa95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
