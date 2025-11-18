Write-Host "Avvio FastAPI con ambiente di sviluppo..."

$envPath = "backend/.env.development"
$mainModule = "backend.main:app"

if (-Not (Test-Path $envPath)) {
    Write-Host ""
    Write-Host "ERRORE: File .env.development non trovato in backend/. Verifica il percorso." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ File .env trovato: $envPath"
Write-Host "Avvio Uvicorn su http://127.0.0.1:8000..."

try {
    uvicorn $mainModule --reload --env-file $envPath
} catch {
    Write-Host ""
    Write-Host "ERRORE: Avvio Uvicorn fallito. Controlla che sia installato correttamente." -ForegroundColor Red
}
