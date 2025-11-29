# reset-db.ps1
param(
    [string]$Message = "init schema"
)

Write-Host ">>> Cancello il database app.db"
Remove-Item app.db -Force -ErrorAction SilentlyContinue

Write-Host ">>> Svuoto la cartella migrations/versions"
Get-ChildItem -Path backend/migrations/versions -File | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host ">>> Rigenero migrazione iniziale con messaggio: $Message"
alembic revision --autogenerate -m $Message

Write-Host ">>> Applico migrazione fino a head"
alembic upgrade head

Write-Host ">>> Stato corrente del database:"
alembic current
