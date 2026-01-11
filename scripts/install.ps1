# ExamGenerator - Script de Instalacion Automatica con UV
# by TiiZss
# Version 11.20260111

Write-Host "EXAMGENERATOR - Instalacion Automatica (UV)" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "[1/5] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python no esta instalado o no esta en PATH" -ForegroundColor Red
    Write-Host "Por favor instala Python 3.8+ desde https://python.org" -ForegroundColor Red
    exit 1
}

# Verificar/Instalar UV
Write-Host ""
Write-Host "[2/5] Verificando UV (ultra-fast package manager)..." -ForegroundColor Yellow
try {
    $uvVersion = uv --version 2>&1
    Write-Host "[OK] UV encontrado: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "[!] UV no encontrado, instalando..." -ForegroundColor Yellow
    Write-Host "    UV es 10-100x mas rapido que pip!" -ForegroundColor Cyan
    
    # Instalar UV usando PowerShell
    try {
        irm https://astral.sh/uv/install.ps1 | iex
        
        # Agregar UV al PATH de la sesion actual
        $env:Path += ";$env:USERPROFILE\.cargo\bin"
        
        # Verificar instalacion
        $uvVersion = uv --version 2>&1
        Write-Host "[OK] UV instalado correctamente: $uvVersion" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Error instalando UV. Intenta manualmente:" -ForegroundColor Red
        Write-Host "   powershell -c 'irm https://astral.sh/uv/install.ps1 | iex'" -ForegroundColor Yellow
        exit 1
    }
}

# Crear entorno virtual con UV (mucho mas rapido que venv)
Write-Host ""
Write-Host "[3/5] Creando entorno virtual con UV..." -ForegroundColor Yellow
try {
    if (Test-Path ".venv") {
        Write-Host "[!] Eliminando entorno virtual anterior..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force .venv
    }
    
    uv venv .venv
    Write-Host "[OK] Entorno virtual creado" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Error creando entorno virtual" -ForegroundColor Red
    exit 1
}

# Instalar dependencias con UV (ultra rapido!)
Write-Host ""
Write-Host "[4/5] Instalando dependencias con UV..." -ForegroundColor Yellow
Write-Host "    (Esto es 10-100x mas rapido que pip)" -ForegroundColor Cyan

$startTime = Get-Date

try {
    uv pip install -r requirements.txt
    
    $endTime = Get-Date
    $elapsed = ($endTime - $startTime).TotalSeconds
    Write-Host "[OK] Dependencias instaladas en $([math]::Round($elapsed, 2)) segundos" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Error instalando dependencias" -ForegroundColor Red
    Write-Host "Intenta ejecutar manualmente:" -ForegroundColor Yellow
    Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "   uv pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Verificar instalacion
Write-Host ""
Write-Host "[5/5] Verificando instalacion..." -ForegroundColor Yellow
try {
    & .venv\Scripts\python.exe -c "import docx; import openpyxl; import google.generativeai; print('Todas las dependencias OK')"
    Write-Host "[OK] Instalacion completada correctamente!" -ForegroundColor Green
} catch {
    Write-Host "[!] Algunas dependencias podrian faltar, pero las basicas estan instaladas" -ForegroundColor Yellow
}

# Informacion final
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  INSTALACION COMPLETADA!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "COMO USAR:" -ForegroundColor Cyan
Write-Host "  1. Ejecutar scripts:" -ForegroundColor White
Write-Host "     uv run python eg.py examples/preguntas.txt Parcial 3 10" -ForegroundColor Yellow
Write-Host "     uv run python qg.py examples/documento_ia.docx --num_preguntas 10" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Interfaz Web:" -ForegroundColor White
Write-Host "     uv run python -m examgenerator.app" -ForegroundColor Yellow
Write-Host "     (Abre: http://localhost:5000)" -ForegroundColor Cyan
Write-Host ""
Write-Host "  3. Activar entorno (opcional):" -ForegroundColor White
Write-Host "     .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "VENTAJAS DE UV:" -ForegroundColor Cyan
Write-Host "  - 10-100x mas rapido que pip" -ForegroundColor White
Write-Host "  - No requiere activar entorno (usa 'uv run')" -ForegroundColor White
Write-Host "  - Cache inteligente de paquetes" -ForegroundColor White
Write-Host "  - Resuelve dependencias mas rapido" -ForegroundColor White
Write-Host ""
Write-Host "Documentacion: README.md y docs/QUICK_START_V11.md" -ForegroundColor Gray
Write-Host ""
