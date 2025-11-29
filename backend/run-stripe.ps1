Write-Host "Avvio Stripe CLI listener..."

try {
    $processInfo = New-Object System.Diagnostics.ProcessStartInfo
    $processInfo.FileName = "C:\stripe-cli\stripe.exe"
    $processInfo.Arguments = "listen --forward-to 127.0.0.1:8000/webhooks/stripe"
    $processInfo.RedirectStandardOutput = $true
    $processInfo.UseShellExecute = $false
    $processInfo.CreateNoWindow = $true

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $processInfo
    $process.Start() | Out-Null

    while (-not $process.StandardOutput.EndOfStream) {
        $line = $process.StandardOutput.ReadLine()
        Write-Host $line

        if ($line -like "*Your webhook signing secret is*") {
            $secret = ($line -split "is ")[1]
            Write-Host "`nWebhook secret rilevato:"
            Write-Host "STRIPE_WEBHOOK_SECRET=$secret" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "`n[!] Errore: Stripe CLI non trovato. Aggiungilo al PATH o usa PowerShell normale."
}
