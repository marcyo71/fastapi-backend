"""merge heads

Revision ID: abf072246ec2
Revises: ('20260102_user_transactions_report', '45a1e85e4614')
Create Date: 2026-01-02 14:27:05.274592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abf072246ec2'
down_revision = ('20260102_user_transactions_report', '45a1e85e4614')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
