# 📁 File principali da mantenere
$mainFiles = @("user_model.py", "survey_model.py", "transaction.py")

# 🔍 Cerca tutte le classi duplicate
$classes = Get-ChildItem -Recurse -Filter *.py | Where-Object {
    $_.FullName -notmatch "\\(\.venv|venv|__pycache__|migrations|logs)\\"
} | Select-String "class " | ForEach-Object {
    $parts = ($_ -split "class ")[1] -split "[:\(]"
    [PSCustomObject]@{
        ClassName = $parts[0].Trim()
        FilePath  = $_.Path
    }
}

# 📊 Raggruppa per nome
$duplicates = $classes | Group-Object ClassName | Where-Object { $_.Count -gt 1 }

# 🧹 Elimina i file non principali
foreach ($group in $duplicates) {
    $className = $group.Name
    $filesToDelete = $group.Group | Where-Object {
        $mainFiles -notcontains ([System.IO.Path]::GetFileName($_.FilePath))
    }

    if ($filesToDelete.Count -gt 0) {
        Write-Host "`nClasse duplicata: $className"
        foreach ($f in $filesToDelete) {
            Write-Host "   - Candidato per rimozione: $($f.FilePath)"
        }

        $confirm = Read-Host "Vuoi eliminare questi file? (s/n)"
        if ($confirm -eq "s") {
            foreach ($f in $filesToDelete) {
                Remove-Item $f.FilePath -Force
                Write-Host "✅ Eliminato: $($f.FilePath)"
            }
        } else {
            Write-Host "⏭️ Salto la rimozione per $className"
        }
    }
}
