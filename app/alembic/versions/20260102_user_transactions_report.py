"""create or replace view user_transactions_report"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260102_user_transactions_report"
down_revision = "45a1e85e4614"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        CREATE OR REPLACE VIEW user_transactions_report AS
        SELECT
            u.id AS user_id,
            u.email,
            COALESCE(SUM(CASE WHEN t.status = 'completed' THEN t.amount ELSE 0 END), 0) AS totale_completed,
            COALESCE(SUM(CASE WHEN t.status = 'pending' THEN t.amount ELSE 0 END), 0) AS totale_pending,
            COALESCE(COUNT(CASE WHEN t.status = 'completed' THEN 1 END), 0) AS num_completed,
            COALESCE(COUNT(CASE WHEN t.status = 'pending' THEN 1 END), 0) AS num_pending,
            COUNT(t.id) AS num_totale,
            COALESCE(
                ROUND((
                    SUM(CASE WHEN t.status = 'completed' THEN t.amount ELSE 0 END) * 100.0
                )::numeric / NULLIF(SUM(t.amount), 0), 2), 0
            ) AS percentuale_completed_importi,
            COALESCE(
                ROUND((
                    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) * 100.0
                )::numeric / NULLIF(COUNT(t.id), 0), 2), 0
            ) AS percentuale_completed_transazioni
        FROM users u
        LEFT JOIN transactions t ON u.id = t.user_id
        GROUP BY u.id, u.email;
    """)

def downgrade():
    op.execute("DROP VIEW IF EXISTS user_transactions_report;")
