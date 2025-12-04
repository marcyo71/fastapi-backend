from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/status", tags=["status"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def status_page(request: Request):
    return templates.TemplateResponse("status.html", {"request": request})
