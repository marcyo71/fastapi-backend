Write-Host ">>> Eliminazione alembic.old..."
if (Test-Path ".\alembic.old") {
    Remove-Item ".\alembic.old" -Recurse -Force
    Write-Host "✓ alembic.old rimossa"
} else {
    Write-Host "✓ alembic.old non trovata"
}

Write-Host ">>> Rimozione __pycache__ e file .pyc..."
$cacheItems = Get-ChildItem -Recurse -Include "__pycache__", "*.pyc"
foreach ($item in $cacheItems) {
    Remove-Item $item.FullName -Recurse -Force -ErrorAction SilentlyContinue
}
Write-Host "✓ Cache rimossa"

Write-Host ">>> Verifica alembic.ini..."
$ini = Get-Content ".\alembic.ini" -Raw
if ($ini -match "sqlalchemy\.url\s*=\s*\$\{DATABASE_URL\}") {
    Write-Host "✓ alembic.ini usa DATABASE_URL"
} else {
    Write-Host "⚠️  Controlla sqlalchemy.url in alembic.ini"
}
