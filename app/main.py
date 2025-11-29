from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.routers import admin_router, user_router 
from backend.auth import create_access_token, verify_token
from datetime import datetime
from fastapi.database import SessionLocal  # importa dal file database.py
from sqlalchemy.orm import Session
from backend.config.settings import settings  # importa le configurazioni

app = FastAPI(title="FastAPI Backend", version="1.0.0")

# Monta static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Includi router modulari
app.include_router(admin_router.router)
app.include_router(user_router.router)

# Templates
templates = Jinja2Templates(directory="templates")

# -------------------
# Dependency per DB
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------
# Middleware di protezione admin
# -------------------
@app.middleware("http")
async def check_admin_access(request: Request, call_next):
    if request.url.path.startswith(("/admin", "/utenti", "/transazioni", "/dashboard", "/stato")):
        token = request.cookies.get("session")
        payload = verify_token(token) if token else None
        if not payload or payload.get("role") != "admin":
            return RedirectResponse(url="/login")
    return await call_next(request)

# -------------------
# LOGIN
# -------------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "segreto":
        token = create_access_token({"sub": username, "role": "admin"})
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie(
            key="session",
            value=token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=3600
        )
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenziali errate"})

# -------------------
# ROTTE UTENTE
# -------------------
@app.get("/")
def home():
    return {"msg": "Benvenuto nella home utente"}

@app.get("/pagamenti", response_class=HTMLResponse)
async def pagamenti(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})

# -------------------
# ROTTE ADMIN
# -------------------
@app.get("/admin", response_class=HTMLResponse)
async def admin_home(request: Request):
    return templates.TemplateResponse("admin_home.html", {"request": request})

@app.get("/utenti", response_class=HTMLResponse)
async def utenti(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

@app.get("/transazioni", response_class=HTMLResponse)
async def transazioni(request: Request):
    return templates.TemplateResponse("transactions.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/stato", response_class=HTMLResponse)
async def stato(request: Request):
    return templates.TemplateResponse(
        "status.html",
        {"request": request, "now": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    )

# -------------------
# ENDPOINT DI TEST DB
# -------------------
@app.get("/ping")
def ping(db: Session = Depends(get_db)):
    return {
        "msg": "DB connesso correttamente!",
        "database_url": str(db.bind.url)
    }
