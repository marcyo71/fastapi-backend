from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import os
import sys
import platform
import sqlalchemy
from sqlalchemy import text
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(title="FastAPI Backend", docs_url="/docs", redoc_url=None)

# ===== Environment & DB =====
DATABASE_URL = os.getenv("DATABASE_URL")  # es.: postgresql://user:pass@host/dbname
engine = None
db_ready = False
db_error = None

if DATABASE_URL:
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_ready = True
    except Exception as e:
        db_error = str(e)
else:
    db_error = "DATABASE_URL not set"


# ===== Helpers =====
def card(label: str, value: str) -> str:
    return f"""
    <div style="padding:10px 14px;border:1px solid #e5e7eb;border-radius:8px;background:#fafafa;">
      <div style="font-weight:600;color:#374151;">{label}</div>
      <div style="color:#111827;">{value}</div>
    </div>
    """

def link(label: str, href: str) -> str:
    return f'<a href="{href}" style="color:#2563eb;text-decoration:none;">{label}</a>'


# ===== Endpoints =====
@app.get("/", response_class=HTMLResponse)
def root():
    # Mini homepage HTML
    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <title>FastAPI backend dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body style="font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,'Helvetica Neue',Arial,sans-serif;background:#ffffff;margin:24px;">
        <h1 style="margin:0 0 12px 0;color:#111827;">FastAPI backend</h1>
        <p style="margin:0 0 16px 0;color:#4b5563;">Minimal dashboard per stato servizio e collegamento al database.</p>

        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-bottom:18px;">
          {card("Service status", "online")}
          {card("Docs", link("/docs", "/docs"))}
          {card("Health", link("/health", "/health"))}
          {card("Status", link("/status", "/status"))}
        </div>

        <h2 style="color:#111827;margin:18px 0 8px;">Database</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-bottom:18px;">
          {card("Connected", "yes" if db_ready else "no")}
          {card("Engine", "SQLAlchemy")}
          {card("Env var", "DATABASE_URL: " + ("set" if os.getenv("DATABASE_URL") else "missing"))}
        </div>
        {"<div style='color:#b91c1c;border:1px solid #fecaca;background:#ffe4e6;padding:10px;border-radius:8px;margin-bottom:18px;'>DB error: " + db_error + "</div>" if db_error else ""}

        <h2 style="color:#111827;margin:18px 0 8px;">Endpoints</h2>
        <table style="width:100%;border-collapse:collapse;">
          <thead>
            <tr style="text-align:left;border-bottom:1px solid #e5e7eb;">
              <th style="padding:8px;">Method</th>
              <th style="padding:8px;">Path</th>
              <th style="padding:8px;">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #f3f4f6;">
              <td style="padding:8px;">GET</td><td style="padding:8px;">/</td><td style="padding:8px;">Home dashboard</td>
            </tr>
            <tr style="border-bottom:1px solid #f3f4f6;">
              <td style="padding:8px;">GET</td><td style="padding:8px;">/docs</td><td style="padding:8px;">Swagger UI</td>
            </tr>
            <tr style="border-bottom:1px solid #f3f4f6;">
              <td style="padding:8px;">GET</td><td style="padding:8px;">/health</td><td style="padding:8px;">Ping al DB (SELECT 1)</td>
            </tr>
            <tr style="border-bottom:1px solid #f3f4f6;">
              <td style="padding:8px;">GET</td><td style="padding:8px;">/status</td><td style="padding:8px;">Info ambiente e servizio</td>
            </tr>
          </tbody>
        </table>

        <div style="margin-top:24px;color:#6b7280;">
          Tip: aggiorna variabili su Render → Save, Rebuild and Deploy.
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)


@app.get("/health")
def health_check():
    if not engine:
        return JSONResponse({"status": "error", "details": "DATABASE_URL not set"}, status_code=500)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return JSONResponse({"status": "error", "details": str(e)}, status_code=500)


@app.get("/status")
def status():
    return {
        "service": "fastapi-backend",
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "db_connected": db_ready,
        "env": {
            "DATABASE_URL": "set" if os.getenv("DATABASE_URL") else "missing",
            "SECRET_KEY": "set" if os.getenv("SECRET_KEY") else "missing",
            "DEBUG": os.getenv("DEBUG", "missing"),
        },
    }
