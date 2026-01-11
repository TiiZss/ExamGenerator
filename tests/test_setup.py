# Script de verificación para nuevas funcionalidades
# Prueba las importaciones y configuración básica

import sys
import os

print("=" * 60)
print("🔍 Verificación de ExamGenerator - Soporte Ollama")
print("=" * 60)

# Test 1: Verificar imports básicos
print("\n1. Verificando imports básicos...")
try:
    import pypdf
    import docx
    from pptx import Presentation
    print("   ✅ pypdf, docx, pptx - OK")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Verificar import de requests (para Ollama)
print("\n2. Verificando soporte para Ollama...")
try:
    import requests
    print("   ✅ requests instalado - Ollama soportado")
except ImportError:
    print("   ⚠️  requests no instalado - Ollama no disponible")
    print("      Instalar con: pip install requests")

# Test 3: Verificar import de Google Gemini
print("\n3. Verificando soporte para Google Gemini...")
try:
    import google.generativeai as genai
    print("   ✅ google-generativeai instalado - Gemini soportado")
except ImportError:
    print("   ⚠️  google-generativeai no instalado - Gemini no disponible")
    print("      Instalar con: pip install google-generativeai")

# Test 4: Verificar API Key de Gemini
print("\n4. Verificando configuración de Gemini...")
api_key = os.environ.get('GOOGLE_API_KEY')
if api_key:
    print(f"   ✅ GOOGLE_API_KEY configurada ({api_key[:10]}...)")
else:
    print("   ⚠️  GOOGLE_API_KEY no configurada")
    print("      Configurar con: $env:GOOGLE_API_KEY = 'tu-api-key'")

# Test 5: Verificar disponibilidad de Ollama
print("\n5. Verificando servidor Ollama...")
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        print("   ✅ Servidor Ollama detectado en http://localhost:11434")
        models = response.json().get('models', [])
        if models:
            print(f"   📋 Modelos disponibles: {len(models)}")
            for model in models[:3]:  # Mostrar solo los primeros 3
                print(f"      - {model.get('name', 'unknown')}")
        else:
            print("   ⚠️  No hay modelos descargados")
            print("      Descargar con: ollama pull llama2")
    else:
        print(f"   ⚠️  Servidor Ollama respondió con código {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ⚠️  Servidor Ollama no detectado")
    print("      ℹ️  qg.py puede iniciar Ollama automáticamente")
    print("      O iniciar manualmente con: ollama serve")
except ImportError:
    print("   ⚠️  requests no instalado, no se puede verificar Ollama")
except Exception as e:
    print(f"   ⚠️  Error al conectar con Ollama: {e}")

# Test 6: Verificar archivos del proyecto
print("\n6. Verificando archivos del proyecto...")
files_to_check = [
    'eg.py',
    'qg.py', 
    'requirements.txt',
    'preguntas.txt',
    '.github/copilot-instructions.md',
    'OLLAMA_SETUP.md'
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - NO ENCONTRADO")

# Resumen
print("\n" + "=" * 60)
print("📊 RESUMEN")
print("=" * 60)

motors_available = []
if 'google.generativeai' in sys.modules and api_key:
    motors_available.append("Gemini (nube)")
if 'requests' in sys.modules:
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            motors_available.append("Ollama (local)")
    except:
        pass

if motors_available:
    print(f"✅ Motores disponibles: {', '.join(motors_available)}")
else:
    print("⚠️  Ningún motor de IA configurado completamente")

print("\n💡 Comandos de ejemplo:")
print("   # Con Gemini:")
print("   python qg.py documento.pdf --motor gemini --num_preguntas 10")
print("\n   # Con Ollama:")
print("   python qg.py documento.pdf --motor ollama --num_preguntas 10")

print("\n📚 Ver OLLAMA_SETUP.md para guía completa de configuración")
print("=" * 60)
