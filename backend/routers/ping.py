from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["ping"])

@router.get("/")
def health_check():
    return {"status": "ok"}
