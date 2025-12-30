import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.session import Base, engine

# ✅ Import dei router
from app.api import users, auth, payments

app = FastAPI(
    title="FastAPI Backend",
    version="1.0.0",
    debug=settings.debug
)

# ✅ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringi ai domini che ti servono
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Eventi di startup/shutdown
@app.on_event("startup")
def on_startup():
    # Crea le tabelle se non usi Alembic
    Base.metadata.create_all(bind=engine)
    print("🚀 Backend avviato con DB:", settings.database_url)

@app.on_event("shutdown")
def on_shutdown():
    print("🛑 Backend spento")

# ✅ Gestione errori globali
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# ✅ Inclusione dei router
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])

# ✅ Endpoint di test
@app.get("/")
def read_root():
    return {
        "status": "ok",
        "env": settings.env,
        "db_url": settings.database_url,
        "async_db_url": settings.async_database_url
    }

# ✅ Avvio locale (non serve su Railway, ma utile per test)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)