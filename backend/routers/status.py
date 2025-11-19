from fastapi import APIRouter
from backend.services.status_service import get_status

router = APIRouter()

@router.get("/status")
def status():
    return get_status()
