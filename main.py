from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

# Import DB e modelli
from backend.db.engine import Base, engine
import backend.models  # importa i tuoi modelli

# Inizializza il DB (crea le tabelle se non esistono)
Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None)  # Disattiva la UI automatica su /docs

@app.get("/", response_class=HTMLResponse)
def read_root():
    now = datetime.now().strftime("%d %B %Y, %H:%M")
    return f"""
    <html>
        <head>
            <title>🚀 FastAPI Backend Dashboard</title>
        </head>
        <body style="font-family: sans-serif; background-color: #f9f9f9; padding: 2rem;">
            <h1>🚀 FastAPI Backend Dashboard</h1>
            <p><strong>Stato:</strong> <span style="color: green;">LIVE (locale)</span></p>
            <ul>
                <li><a href="/"><code>/</code></a> → Homepage HTML</li>
                <li><a href="/docs"><code>/docs</code></a> → Swagger UI</li>
                <li><a href="/health"><code>/health</code></a> → Stato del servizio</li>
            </ul>
            <p style="margin-top: 2rem; font-size: 0.9em; color: #666;">
                Ultimo aggiornamento: {now}<br>
                Powered by Marcello & Copilot ⚡️
            </p>
        </body>
    </html>
    """

@app.get("/health", response_class=HTMLResponse)
def health_check():
    now = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    return f"""
    <html>
        <head>
            <title>🩺 Stato del Servizio</title>
        </head>
        <body style="font-family: sans-serif; background-color: #f0fff0; padding: 2rem;">
            <h1>🩺 Stato del Servizio</h1>
            <p><strong>Status:</strong> <span style="color: green;">OK</span></p>
            <p><strong>Servizio:</strong> FastAPI backend</p>
            <p><strong>Timestamp:</strong> {now}</p>
            <p style="margin-top: 2rem;"><a href="/">← Torna alla dashboard</a></p>
        </body>
    </html>
    """

@app.get("/docs", response_class=HTMLResponse)
def custom_docs():
    return """
    <html>
        <head>
            <title>📚 Documentazione API</title>
        </head>
        <body style="font-family: sans-serif; background-color: #fff; padding: 2rem;">
            <h1>📚 Documentazione API</h1>
            <p><a href="/" style="font-weight: bold;">← Torna alla dashboard</a></p>
            <iframe src="/swagger" width="100%" height="800px" style="border: 1px solid #ccc;"></iframe>
        </body>
    </html>
    """

from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/swagger", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")
