# ExamGenerator - Quick Start Docker Script (PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "🐳 ExamGenerator Docker - Quick Start" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check Docker
try {
    docker --version | Out-Null
} catch {
    Write-Host "❌ Error: Docker no está instalado" -ForegroundColor Red
    Write-Host "Instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
}

try {
    docker-compose --version | Out-Null
} catch {
    Write-Host "❌ Error: Docker Compose no está instalado" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Docker y Docker Compose detectados" -ForegroundColor Green
Write-Host ""

# Check .env
if (-not (Test-Path .env)) {
    Write-Host "⚠️ Archivo .env no encontrado" -ForegroundColor Yellow
    Write-Host "Creando desde .env.example..."
    Copy-Item .env.example .env
    Write-Host "✓ .env creado" -ForegroundColor Green
    Write-Host "⚠️ IMPORTANTE: Edita .env y añade tu GOOGLE_API_KEY si vas a usar IA" -ForegroundColor Yellow
    Write-Host ""
}

# Check output directory
if (-not (Test-Path output)) {
    Write-Host "📁 Creando directorio output..."
    New-Item -ItemType Directory -Path output | Out-Null
}

# Menu
Write-Host "Elige una opción:"
Write-Host ""
Write-Host "1) Build - Construir imágenes Docker"
Write-Host "2) Start - Iniciar stack básico (App + Web)"
Write-Host "3) Start AI - Iniciar con soporte de IA (Gemini)"
Write-Host "4) Start Ollama - Iniciar con Ollama (IA local)"
Write-Host "5) Stop - Detener todos los contenedores"
Write-Host "6) Logs - Ver logs en tiempo real"
Write-Host "7) Shell - Abrir terminal en contenedor"
Write-Host "8) Demo - Ejecutar demo completo"
Write-Host "9) Clean - Limpiar outputs generados"
Write-Host "0) Exit"
Write-Host ""
$option = Read-Host "Opción"

switch ($option) {
    "1" {
        Write-Host "🔨 Construyendo imágenes..." -ForegroundColor Yellow
        docker-compose build
        Write-Host "✓ Build completado" -ForegroundColor Green
    }
    "2" {
        Write-Host "🚀 Iniciando stack básico..." -ForegroundColor Yellow
        docker-compose up -d app web
        Write-Host "✓ Stack iniciado" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Web UI: http://localhost:5000"
        Write-Host "Ver logs: docker-compose logs -f web"
    }
    "3" {
        Write-Host "🚀 Iniciando con IA Gemini..." -ForegroundColor Yellow
        $envContent = Get-Content .env -Raw
        if ($envContent -notmatch "GOOGLE_API_KEY=.+") {
            Write-Host "⚠️ ADVERTENCIA: GOOGLE_API_KEY no configurada en .env" -ForegroundColor Red
            Write-Host "Edita .env y añade tu API key de Google"
        }
        docker-compose --profile ai up -d
        Write-Host "✓ Stack con IA iniciado" -ForegroundColor Green
    }
    "4" {
        Write-Host "🚀 Iniciando con Ollama..." -ForegroundColor Yellow
        docker-compose --profile ollama up -d
        Write-Host ""
        Write-Host "⬇️ Descargando modelo llama2..." -ForegroundColor Yellow
        Write-Host "Esto puede tardar varios minutos..."
        docker-compose exec ollama ollama pull llama2
        Write-Host "✓ Stack con Ollama listo" -ForegroundColor Green
    }
    "5" {
        Write-Host "🛑 Deteniendo contenedores..." -ForegroundColor Yellow
        docker-compose down
        Write-Host "✓ Contenedores detenidos" -ForegroundColor Green
    }
    "6" {
        Write-Host "📋 Mostrando logs (Ctrl+C para salir)..." -ForegroundColor Yellow
        docker-compose logs -f
    }
    "7" {
        Write-Host "🐚 Abriendo shell en ExGen-App..." -ForegroundColor Yellow
        docker-compose exec app /bin/bash
    }
    "8" {
        Write-Host "🎬 Ejecutando demo..." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "1. Validando preguntas..."
        docker-compose run --rm app cli.py validate /data/questions/preguntas.txt
        Write-Host ""
        Write-Host "2. Generando 2 exámenes de 5 preguntas..."
        docker-compose run --rm -v ${PWD}/output:/output app cli.py generate /data/questions/preguntas.txt Demo 2 5 --format both --answers html
        Write-Host ""
        Write-Host "✓ Demo completado" -ForegroundColor Green
        Write-Host "📁 Revisa: output/Examenes_Demo/"
    }
    "9" {
        Write-Host "🧹 Limpiando outputs..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force output/Examenes_* -ErrorAction SilentlyContinue
        Write-Host "✓ Limpieza completada" -ForegroundColor Green
    }
    "0" {
        Write-Host "👋 ¡Hasta luego!"
        exit 0
    }
    default {
        Write-Host "❌ Opción inválida" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Para más opciones: make -f Makefile.docker help"
Write-Host "Documentación: docs/DOCKER.md"
