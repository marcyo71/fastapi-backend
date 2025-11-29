# ⚙️ Attiva l'ambiente virtuale
$venvPath = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "✅ Ambiente virtuale attivato"
} else {
    Write-Host "❌ Ambiente virtuale non trovato. Verifica il percorso: $venvPath"
    exit 1
}

$env:PYTHONPATH = "$PSScriptRoot"


# 🧪 Esegui i test con pytest
Write-Host "🚀 Avvio dei test..."
pytest backend/tests --disable-warnings --maxfail=1

# ✅ Risultato
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tutti i test sono passati con successo!"
} else {
    Write-Host "❌ Alcuni test sono falliti. Controlla l'output sopra."
}

