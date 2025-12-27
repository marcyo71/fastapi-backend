from fastapi import APIRouter

router = APIRouter(tags=["status"])

@router.get("/success")
def success():
    return {"status": "success"}

@router.get("/cancel")
def cancel():
    return {"status": "cancel"}
