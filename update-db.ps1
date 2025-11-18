# update-db.ps1
param(
    [string]$Message = "auto migration"
)

Write-Host ">>> Genero nuova migrazione con messaggio: $Message"
alembic revision --autogenerate -m $Message

Write-Host ">>> Applico migrazione fino a head"
alembic upgrade head

Write-Host ">>> Stato corrente del database:"
alembic current
