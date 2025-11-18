Write-Host "Avvio Stripe CLI in modalità webhook listener..."

$cliPath = "C:\stripe-cli\stripe.exe"
$forwardUrl = "127.0.0.1:8000/webhook/stripe"

if (-Not (Test-Path $cliPath)) {
    Write-Host ""
    Write-Host "ERRORE: Stripe CLI non trovato in $cliPath. Verifica il percorso." -ForegroundColor Red
    exit 1
}

& $cliPath listen --forward-to $forwardUrl
