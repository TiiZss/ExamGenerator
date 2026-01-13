# ExamGenerator - Start Script (PowerShell)

Write-Host "🚀 Starting ExamGenerator..." -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

# Check Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Docker is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Docker Desktop."
    exit 1
}

# Check .env
if (-not (Test-Path .env)) {
    Write-Host "⚠️  .env file not found." -ForegroundColor Yellow
    if (Test-Path .env.example) {
        Write-Host "Creating .env from .env.example..."
        Copy-Item .env.example .env
        Write-Host "✓ .env created." -ForegroundColor Green
    } else {
        Write-Host "❌ Error: .env.example not found. Cannot create config." -ForegroundColor Red
        exit 1
    }
}

# Start Docker Compose
Write-Host "🐳 Lifting containers..." -ForegroundColor Cyan
docker-compose up -d app web

Write-Host ""
Write-Host "✅ Check complete!" -ForegroundColor Green
Write-Host "-----------------------------------"
Write-Host "🌐 Web Interface: http://localhost:5000"
Write-Host "📋 Logs: docker-compose logs -f web"
Write-Host "-----------------------------------"
