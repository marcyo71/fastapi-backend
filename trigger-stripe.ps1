Write-Host "Simulazione evento Stripe: checkout.session.completed..."

$cliPath = "C:\stripe-cli\stripe.exe"

if (-Not (Test-Path $cliPath)) {
    Write-Host ""
    Write-Host "ERRORE: Stripe CLI non trovato in $cliPath. Verifica il percorso." -ForegroundColor Red
    exit 1
}

& $cliPath trigger checkout.session.completed
