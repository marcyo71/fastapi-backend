$allowed = @(
    '^from backend\.',
    '^from fastapi',
    '^from pydantic',
    '^from pydantic_settings',
    '^from sqlalchemy',
    '^from typing',
    '^from datetime',
    '^from os',
    '^from logging',
    '^from dotenv',
    '^from uuid',
    '^from enum',
    '^from decimal',
    '^from starlette',
    '^from passlib',
    '^from bcrypt',
    '^from jwt',
    '^from re',
    '^from json',
    '^from httpx',
    '^from typing_extensions',
    '^from builtins',
    '^from collections',
    '^from email',
    '^from base64',
    '^from hashlib',
    '^from pathlib'
)

Get-ChildItem -Recurse -Filter *.py | ForEach-Object {
    $file = $_.FullName
    $lines = Get-Content $file
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i].Trim()
        if ($line -match '^from ' -and -not ($allowed | Where-Object { $line -match $_ })) {
            Write-Host "Import sospetto in ${file}:$($i+1): $line" -ForegroundColor Yellow
        }
    }
}
