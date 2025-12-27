import warnings
warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.db.dependencies import init_db, close_db

# Banner (non usato, ma import richiesto)
from app.core.banner import print_banner

# Routers
from app.routers import payments_router, ping, dashboard
from app.routers.stripe_router import router as stripe_router
from app.routers.payment_status import router as payment_status
from app.routers.checkout_router import router as checkout_router
from app.routers.stripe_events import router as stripe_events_router
from app.routers.stripe_webhook import router as stripe_webhook_router
from app.routers.payment_element import router as payment_element_router
from app.routers import users_api, referrals_api, transactions_api, user_status_api
from app.routers.auth_router import router as auth_router

# Middleware
from app.middleware.request_logger import RequestLogMiddleware, ErrorHandlerMiddleware


# -----------------------------------
# LOGGER PROFESSIONALE (console + file)
# -----------------------------------
logger = logging.getLogger("backend")
if not logger.handlers:
    logger.setLevel(logging.INFO)

    # Console
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File con rotazione giornaliera
    LOG_DIR = "logs"
    Path(LOG_DIR).mkdir(exist_ok=True)

    file_handler = TimedRotatingFileHandler(
        filename=f"{LOG_DIR}/backend.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# -----------------------------------
# PROFILING SQL
# -----------------------------------
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    logger.info(f"SQL START → {statement}")


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    logger.info("SQL END")


# -----------------------------------
# FASTAPI SETUP
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Stripe Integration API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# -----------------------------------
# CORS
# -----------------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip per comprimere le risposte
app.add_middleware(GZipMiddleware, minimum_size=500)

# Middleware globali
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(RequestLogMiddleware)


# -----------------------------------
# ROUTERS
# -----------------------------------
# Stripe
app.include_router(stripe_router)
app.include_router(payment_status, prefix="/api/status", tags=["status"])
app.include_router(checkout_router)
app.include_router(stripe_events_router)
app.include_router(stripe_webhook_router)
app.include_router(payment_element_router)

# Business
app.include_router(payments_router.router)
app.include_router(referrals_api.router)
app.include_router(transactions_api.router)
app.include_router(user_status_api.router)

# System
app.include_router(ping.router)
app.include_router(dashboard.router)
app.include_router(users_api.router)
app.include_router(auth_router)


# -----------------------------------
# HANDLER ERRORI PERSONALIZZATI
# -----------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": exc.errors()
        }
    )


# -----------------------------------
# ROOT
# -----------------------------------
@app.get("/")
async def root():
    return {"message": "FastAPI è attivo 🚀"}
