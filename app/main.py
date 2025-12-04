
import os
from datetime import datetime
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.routers import auth_router, home_router, payments_router
from backend.routers import admin_router, user_router, status
from backend.auth import create_access_token, verify_token
from backend.database import SessionLocal
from backend.config.settings import settings

app = FastAPI(title="FastAPI Backend")

# -------------------
# Static files
# -------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# -------------------
# Routers
# -------------------
app.include_router(admin_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(payments_router.router)
app.include_router(home_router.router)
app.include_router(status.router)

# -------------------
# Templates
# -------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory="app/templates")

@app.get("/favicon.ico")
def favicon():
    path = os.path.join("app", "static", "favicon.ico")
    return FileResponse(path)

# -------------------
# DB dependency
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------
# Middleware
# -------------------
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.cookies.get("session")
    payload = verify_token(token) if token else None

    print("Cookie session:", token)
    print("Middleware payload:", payload)

    if request.url.path.startswith(("/admin", "/utenti", "/transazioni", "/dashboard", "/stato")):
        if not payload or payload.get("role") != "admin":
            return RedirectResponse(url="/login", status_code=302)

    if request.url.path.startswith("/pagamenti"):
        if not payload or payload.get("role") != "user":
            return RedirectResponse(url="/login", status_code=302)

    return await call_next(request)

# -------------------
# LOGIN
# -------------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    if username == "admin" and password == "segreto":
        token = create_access_token({"sub": username, "role": "admin"})
        response = RedirectResponse(url="/admin", status_code=303)
        response.set_cookie(
            key="session",
            value=token,
            httponly=True,
            samesite="Lax",
            max_age=3600,
            path="/"
        )
        return response

    elif username == "marcy" and password == "123":
        token = create_access_token({"sub": username, "role": "user"})
        response = RedirectResponse(url="/pagamenti", status_code=303)
        response.set_cookie(
            key="session",
            value=token,
            httponly=True,
            samesite="Lax",
            max_age=3600,
            path="/"
        )
        return response

    return RedirectResponse(url="/login", status_code=303)

# -------------------
# LOGOUT
# -------------------
@app.get("/logout")
def logout(response: Response):
    response.delete_cookie("session")
    return RedirectResponse(url="/login", status_code=302)

# -------------------
# ROTTE UTENTE
# -------------------
@app.get("/home")
def home_redirect(request: Request):
    token = request.cookies.get("session")
    payload = verify_token(token) if token else None

    if payload and payload.get("role") == "admin":
        return RedirectResponse(url="/admin", status_code=302)
    elif payload and payload.get("role") == "user":
        return RedirectResponse(url="/pagamenti", status_code=302)
    else:
        return RedirectResponse(url="/login", status_code=302)

@app.get("/pagamenti", response_class=HTMLResponse)
async def pagamenti(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})

@app.post("/pagamenti", response_class=HTMLResponse)
async def pagamenti_post(request: Request, plan: str = Form(...)):
    return templates.TemplateResponse("payment_result.html", {"request": request, "plan": plan})

# -------------------
# ROTTE ADMIN
# -------------------
@app.get("/admin", response_class=HTMLResponse)
async def admin_home(request: Request):
    return templates.TemplateResponse("admin_home.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
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

@app.get("/config", response_class=HTMLResponse)
def read_config():
    stripe_public = settings.stripe_public_key if settings.debug else "***hidden***"
    html_content = f"""
    <html>
        <head><title>Configurazione Backend</title></head>
        <body>
            <h1>Configurazione Backend</h1>
            <table>
                <tr><th>Variabile</th><th>Valore</th></tr>
                <tr><td>DATABASE_URL</td><td>{settings.database_url}</td></tr>
                <tr><td>DATABASE_URL_LOCAL</td><td>{settings.database_url_local}</td></tr>
                <tr><td>POSTGRES_USER</td><td>{settings.postgres_user}</td></tr>
                <tr><td>POSTGRES_DB</td><td>{settings.postgres_db}</td></tr>
                <tr><td>PORT</td><td>{settings.port}</td></tr>
                <tr><td>DEBUG</td><td>{settings.debug}</td></tr>
                <tr><td>ALGORITHM</td><td>{settings.algorithm}</td></tr>
                <tr><td>ACCESS_TOKEN_EXPIRE_MINUTES</td><td>{settings.access_token_expire_minutes}</td></tr>
                <tr><td>STRIPE_PUBLIC_KEY</td><td>***hidden***</td></tr>
                <tr><td>STRIPE_SECRET_KEY</td><td>***hidden***</td></tr>
                <tr><td>STRIPE_WEBHOOK_SECRET</td><td>***hidden***</td></tr>
            </table>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# -------------------
# ENDPOINT DI TEST DB
# -------------------
@app.get("/ping")
def ping(db: Session = Depends(get_db)):
    return {"msg": "DB connesso correttamente!", "database_url": str(db.bind.url)}

# -------------------
# WHOAMI
# -------------------
@app.get("/whoami")
def whoami(request: Request):
    token = request.cookies.get("session")
    payload = verify_token(token) if token else None
    return {"cookie": token, "payload": payload}
