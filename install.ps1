# ExamGenerator - Script de Instalación Automática
# by TiiZss

Write-Host "🎓 EXAMGENERATOR - Instalación Automática" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Verificar Python
Write-Host "🔍 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python no está instalado o no está en PATH" -ForegroundColor Red
    Write-Host "Por favor instala Python 3.8+ desde https://python.org" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual
Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
python -m venv .venv

# Activar entorno virtual
Write-Host "🔧 Activando entorno virtual..." -ForegroundColor Yellow
try {
    .\.venv\Scripts\Activate.ps1
    Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Problemas con política de ejecución, aplicando solución..." -ForegroundColor Yellow
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    .\.venv\Scripts\Activate.ps1
    Write-Host "✅ Entorno virtual activado con permisos actualizados" -ForegroundColor Green
}

# Instalar dependencias
Write-Host "📚 Instalando dependencias..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "🎉 ¡Instalación completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. Para usar el generador básico:" -ForegroundColor White
Write-Host "   python eg.py preguntas.txt MiExamen 5 10" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Para usar el generador con IA (opcional):" -ForegroundColor White
Write-Host "   Configura tu API key: " -NoNewline -ForegroundColor Gray
Write-Host "`$env:GOOGLE_API_KEY = 'tu-api-key'" -ForegroundColor Yellow
Write-Host "   python qg.py documento.pdf --num_preguntas 10" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Lee el README.md para más opciones avanzadas" -ForegroundColor White