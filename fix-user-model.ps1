# Script: fix-user-model.ps1
# Sostituisce automaticamente "user_model" con "user" in tutti i file .py

$path = "C:\Users\marcy\Documents\app"   # cartella root del progetto

Get-ChildItem -Path $path -Recurse -Include *.py | ForEach-Object {
    (Get-Content $_.FullName) -replace "user_model", "user" | Set-Content $_.FullName
    Write-Host "Modificato:" $_.FullName
}
