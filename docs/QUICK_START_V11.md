# 🚀 Guía de Inicio Rápido - ExamGenerator v11

## 📋 Instalación Rápida con UV

UV es un gestor de paquetes **10-100x más rápido que pip**!

### Windows
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

### Linux/macOS
```bash
chmod +x install.sh && ./install.sh
```

El script instala UV automáticamente si no está presente.

---

## 🌐 Opción 1: Interfaz Web (Recomendado para Principiantes)

### 1. Iniciar el Servidor
```bash
uv run python run_web.py
```

### 2. Abrir Navegador
Visita: **http://localhost:5000**

### 3. Usar la Interfaz
- **Generar Exámenes**: Sube archivo de preguntas TXT → Configura parámetros → Descarga ZIP
- **Generar Preguntas IA**: Sube PDF/DOCX/PPTX → Selecciona motor IA → Descarga preguntas

---

## 💻 Opción 2: Línea de Comandos (Avanzado)

### Generar Exámenes
```bash
# Básico (3 exámenes, 10 preguntas cada uno, formato TXT)
uv run python eg.py preguntas.txt Parcial 3 10

# Avanzado (con DOCX y plantilla)
uv run python eg.py preguntas.txt Final 5 20 both plantilla.docx xlsx
```

### Generar Preguntas con IA

#### Gemini (Cloud)
```bash
# Configurar API key primero
export GOOGLE_API_KEY="tu-api-key"

# Generar preguntas
uv run python qg.py documento.pdf --num_preguntas 15 --motor gemini
```

#### Ollama (Local)
```bash
# Instalar Ollama: https://ollama.ai
ollama pull llama2

# Generar preguntas (auto-inicia Ollama si es necesario)
uv run python qg.py documento.pdf --num_preguntas 10 --motor ollama --modelo llama2
```

---

## 📝 Formato de Archivo de Preguntas

```
¿Cuál es la capital de Francia?
A) Londres
B) París
C) Madrid
D) Roma
ANSWER: B)

¿Qué lenguaje usa ExamGenerator?
A) Java
B) C++
C) Python
D) JavaScript
ANSWER: C)

(línea en blanco entre preguntas)
```

---

## ✨ Características Nuevas v11

### 🌐 Interfaz Web
- Dashboard moderno con diseño responsive
- Generación sin usar terminal
- Caché inteligente de preguntas IA
- Estadísticas en tiempo real

### 📊 Estadísticas
- Distribución de respuestas correctas
- Análisis de balance
- Advertencias automáticas
- Exportación a JSON

### 🔧 Validaciones
- Verificación de archivos
- Límites de tamaño (50MB)
- Sanitización de nombres
- Mensajes de error claros

### ⚡ Caché
- Evita regenerar preguntas idénticas
- TTL configurable (7 días)
- Ahorro de tiempo y recursos
- API para gestión

---

## 🎯 Casos de Uso Rápidos

### 1. Examen Simple
```bash
# Web: Sube preguntas.txt → Genera 3 exámenes
# CLI: uv run python eg.py preguntas.txt Parcial 3 10
```

### 2. Preguntas desde PDF
```bash
# Web: Sube PDF → Selecciona Gemini → Genera 15 preguntas
# CLI: uv run python qg.py tema.pdf --num_preguntas 15
```

### 3. Examen Profesional con Plantilla
```bash
# CLI: uv run python eg.py preguntas.txt Final 10 50 docx plantilla.docx xlsx
```

---

## 🆘 Solución de Problemas

### Error: "uv: command not found"
```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Error: "No module named 'flask'"
```bash
uv pip install -r requirements.txt
```

### Error: "GOOGLE_API_KEY no configurada"
```bash
# Windows
setx GOOGLE_API_KEY "tu-clave"

# Linux/macOS
export GOOGLE_API_KEY="tu-clave"
```

### Ollama no arranca automáticamente
```bash
# Iniciar manualmente
ollama serve

# Verificar
curl http://localhost:11434/
```

---

## 📚 Recursos

- **CHANGELOG.md**: Historial de cambios completo
- **MEJORAS_PROPUESTAS.md**: 28 mejoras planificadas
- **OLLAMA_SETUP.md**: Guía completa de Ollama
- **.github/copilot-instructions.md**: Guía para desarrolladores

---

## 🤝 Soporte

- **Issues**: https://github.com con UV
uv run python run_web.py
```

**💡 Ventajas de UV:**
- 10-100x más rápido que pip
- Resolución de dependencias inteligente
- Instalación paralela de paquetes
- Caché global de paquetes*Versión**: 11.20260111

---

**¡Empieza ahora!** 🚀

```bash
# Método más fácil: Interfaz Web
python run_web.py
```
