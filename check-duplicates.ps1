# 📁 Cartelle da escludere
$excludeDirs = @("venv", ".venv", "__pycache__", "migrations", "logs")

# 🔍 Filtra solo i file Python rilevanti
$files = Get-ChildItem -Recurse -Filter *.py | Where-Object {
    foreach ($ex in $excludeDirs) {
        if ($_.FullName -like "*\$ex\*") { return $false }
    }
    return $true
}

# 🔍 Estrai classi
$classes = $files | Select-String "class " | ForEach-Object {
    $parts = ($_ -split "class ")[1] -split "[:\(]"
    [PSCustomObject]@{
        ClassName = $parts[0].Trim()
        FilePath  = $_.Path
    }
}

# 📊 Raggruppa e mostra duplicati
$duplicates = $classes | Group-Object ClassName | Where-Object { $_.Count -gt 1 }

if ($duplicates.Count -eq 0) {
    Write-Host "✅ Nessuna classe duplicata trovata."
} else {
    Write-Host "⚠️ Classi duplicate trovate:`n"
    foreach ($group in $duplicates) {
        Write-Host "Classe: $($group.Name)"
        foreach ($item in $group.Group) {
            Write-Host "   - $($item.FilePath)"
        }
        Write-Host ""
    }
}
