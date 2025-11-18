from datetime import datetime
from app.backend.config import settings
from app.backend.models.status_model import StatusResponse
from app.backend.db import Base

# Tempo di avvio del backend
start_time = datetime.utcnow()

def get_status() -> StatusResponse:
    uptime = str(datetime.utcnow() - start_time).split('.')[0]
    return StatusResponse(
        status="running",
        debug=settings.DEBUG,
        env=settings.ENV,
        uptime=uptime
    )
