@echo off
setlocal

:: Navigate to project root (one level up from scripts/)
pushd "%~dp0.."

echo 🚀 Starting ExamGenerator...
echo ============================

:: Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Docker is not installed or not in PATH.
    echo Please install Docker Desktop.
    pause
    exit /b 1
)

:: Check .env
if not exist .env (
    echo ⚠️  .env file not found.
    if exist .env.example (
        echo Creating .env from .env.example...
        copy .env.example .env >nul
        echo ✓ .env created.
    ) else (
        echo ❌ Error: .env.example not found. Cannot create config.
        pause
        exit /b 1
    )
)

:: Start Docker Compose
echo 🐳 Lifting containers...
docker-compose up -d app web

echo.
echo ✅ Check complete!
echo -----------------------------------
echo 🌐 Web Interface: http://localhost:5000
echo 📋 Logs: docker-compose logs -f web
echo -----------------------------------

popd
pause
