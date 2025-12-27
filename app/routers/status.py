from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/status", tags=["status"])

@router.get("/")
def status_root():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
