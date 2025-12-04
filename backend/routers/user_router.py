from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# Router dedicato all'area utente
router = APIRouter(prefix="/user", tags=["user"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def user_page(request: Request):
    # Renderizza il template users.html
    return templates.TemplateResponse("users.html", {"request": request})
