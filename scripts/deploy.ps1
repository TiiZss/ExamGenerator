# Deploy Script Wrapper
# Delegates to Python for full automation handling (SSH passwords)

# Navigate to project root
Set-Location "$PSScriptRoot\.."

Write-Host "Launching Python Deployment Script..." -ForegroundColor Cyan

if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv run python scripts\deploy.py
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Warning "UV not found, falling back to system Python..."
    python scripts\deploy.py
}
else {
    Write-Error "Neither UV nor Python found!"
    Pause
}


