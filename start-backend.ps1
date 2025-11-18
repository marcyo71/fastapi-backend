# start-backend.ps1 (da eseguire dalla root del progetto)

Write-Host "🔄 Attivazione ambiente virtuale..."
& ".\backend\.venv\Scripts\Activate.ps1"

Write-Host "🚀 Avvio FastAPI su http://127.0.0.1:8000 ..."
uvicorn backend.main:app --reload

