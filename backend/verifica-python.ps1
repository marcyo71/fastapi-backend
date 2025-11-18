Write-Host "`nVerifica installazione Python, pip e Uvicorn..." -ForegroundColor Cyan

# Verifica Python
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    $version = python --version
    Write-Host "Python rilevato: $version" -ForegroundColor Green
} else {
    Write-Host 'Python non trovato. Verifica che sia installato e che il PATH sia configurato.' -ForegroundColor Red
    exit 1
}

# Verifica pip
$pip = Get-Command pip -ErrorAction SilentlyContinue
if ($pip) {
    $pipVersion = pip --version
    Write-Host "pip rilevato: $pipVersion" -ForegroundColor Green
} else {
    Write-Host 'pip non trovato. Esegui: python -m ensurepip --upgrade' -ForegroundColor Red
    exit 1
}

# Verifica uvicorn
$uvicorn = Get-Command uvicorn -ErrorAction SilentlyContinue
if ($uvicorn) {
    $uvicornVersion = uvicorn --version
    Write-Host "Uvicorn installato: $uvicornVersion" -ForegroundColor Green
} else {
    Write-Host 'Uvicorn non trovato. Puoi installarlo con: pip install uvicorn' -ForegroundColor Yellow
}
