from sqlalchemy import event
from sqlalchemy.engine import Engine
from app.core.logger import get_logger

logger = get_logger("sql")

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = context._query_start_time = conn.info.setdefault('query_start_time', 0)
    logger.info(f"SQL START → {statement}")

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    logger.info("SQL END")
