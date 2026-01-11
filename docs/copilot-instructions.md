# Instrucciones para Asistentes de IA - ExamGenerator

## 🎯 Reglas Fundamentales

### Codificación de Archivos
- **OBLIGATORIO**: Todos los archivos deben usar codificación **UTF-8**
- Archivos Python: `# -*- coding: utf-8 -*-` al inicio si es necesario
- Al crear o editar archivos: Siempre especificar `encoding='utf-8'`
- PowerShell: Usar `[System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)`
- Bash: Usar `echo -e "content" > file` o verificar con `file -i filename`

### Gestión de Paquetes y Entornos
- **USAR UV, NO PIP**: El proyecto usa UV (10-100x más rápido que pip)
- **NO usar**: `pip install`, `python -m venv`, `virtualenv`
- **SÍ usar**: `uv pip install`, `uv venv`, `uv run`
- Entorno virtual: Siempre `.venv` (creado con `uv venv .venv`)
- Ejecutar scripts: `uv run python script.py` (no requiere activar entorno)
- Dependencias: Definidas en `requirements.txt` y `pyproject.toml`

### Idioma del Proyecto
- **Español**: Todo el código, comentarios, documentación y mensajes al usuario
- Variables y funciones: Nombres en español cuando sea posible
- Comentarios: Siempre en español
- Mensajes de error: En español, claros y descriptivos
- Documentación: Markdown en español

## 📁 Estructura del Proyecto

```
ExamGenerator/
├── eg.py                    # Generador principal de exámenes
├── qg.py                    # Generador AI de preguntas (Gemini/Ollama)
├── preguntas.txt            # Archivo de ejemplo de preguntas
├── requirements.txt         # Dependencias (para UV y pip)
├── pyproject.toml          # Configuración moderna del proyecto
├── .python-version         # Python 3.11 (para UV)
├── install.ps1             # Instalador Windows (auto-instala UV)
├── install.sh              # Instalador Linux/macOS (auto-instala UV)
├── examgenerator/          # Paquete modular (v11)
│   ├── __init__.py
│   ├── app.py              # Interfaz web Flask
│   ├── cache.py            # Sistema de caché
│   ├── validators.py       # Validación de datos
│   ├── statistics.py       # Análisis estadístico
│   ├── logging_config.py   # Sistema de logging
│   └── templates/          # Plantillas HTML
├── tests/                  # Tests unitarios
├── docs/                   # Documentación adicional
├── scripts/                # Scripts de utilidad
├── examples/               # Archivos de ejemplo
├── CHANGELOG.md            # Historial de cambios
├── README.md               # Documentación principal
└── QUICK_START_V11.md      # Guía rápida v11
```

### 🗂️ Organización de Archivos por Carpetas

**REGLA IMPORTANTE**: Cada archivo nuevo debe ir a la carpeta correspondiente según su tipo:

| Tipo de Archivo | Carpeta | Ejemplos |
|-----------------|---------|----------|
| **Módulos Python** | `examgenerator/` | `cache.py`, `validators.py`, `statistics.py` |
| **Plantillas HTML** | `examgenerator/templates/` | `index.html`, `exam_form.html` |
| **Archivos estáticos** (CSS/JS) | `examgenerator/static/` | `style.css`, `app.js` |
| **Tests** | `tests/` | `test_validators.py`, `test_cache.py` |
| **Documentación** | `docs/` o raíz | `UV_INFO.md`, `MIGRACION_UV.md` |
| **Scripts de instalación** | Raíz | `install.ps1`, `install.sh`, `setup.sh` |
| **Scripts de utilidad** | `scripts/` | `cleanup.py`, `migrate_data.py` |
| **Archivos de ejemplo** | `examples/` | `preguntas_ejemplo.txt`, `plantilla_ejemplo.docx` |
| **Configuración** | Raíz | `pyproject.toml`, `requirements.txt`, `.python-version` |
| **Salida generada** | `Examenes_*/` | Carpetas creadas automáticamente |

**Ejemplos de creación correcta**:

```python
# ✅ CORRECTO: Nuevo validador
# Archivo: examgenerator/validators.py (ya existe)
# O añadir función a validators.py existente

# ✅ CORRECTO: Nueva plantilla HTML
# Archivo: examgenerator/templates/results.html

# ✅ CORRECTO: Nuevo test
# Archivo: tests/test_statistics.py

# ✅ CORRECTO: Nueva documentación
# Archivo: docs/API.md o API.md (raíz)

# ✅ CORRECTO: Script de limpieza
# Archivo: scripts/cleanup_old_exams.py

# ❌ INCORRECTO: Validador en raíz
# Archivo: new_validator.py (NO en raíz)

# ❌ INCORRECTO: HTML en examgenerator/
# Archivo: examgenerator/index.html (DEBE estar en templates/)

# ❌ INCORRECTO: Test en examgenerator/
# Archivo: examgenerator/test_cache.py (DEBE estar en tests/)
```

**Crear carpetas si no existen**:

```python
import os
from pathlib import Path

# Crear carpeta si no existe
Path("examgenerator/templates").mkdir(parents=True, exist_ok=True)
Path("tests").mkdir(parents=True, exist_ok=True)
Path("docs").mkdir(parents=True, exist_ok=True)
Path("scripts").mkdir(parents=True, exist_ok=True)
Path("examples").mkdir(parents=True, exist_ok=True)
```

## 🔧 Componentes Principales

### 1. eg.py - Generador de Exámenes
**Propósito**: Generar exámenes aleatorios desde archivo de preguntas

**Características clave**:
- Randomización determinística: `random.seed(f"{exam_prefix}_{exam_number}")`
- Multi-formato: TXT, DOCX, o ambos
- Sistema de plantillas DOCX con 15+ placeholders
- Respuestas transpuestas: exámenes como filas, preguntas como columnas
- Formatos de respuestas: XLSX, CSV, TXT, HTML

**Uso**:
```bash
uv run python eg.py preguntas.txt Parcial 3 10 [formato] [plantilla] [respuestas]
# Ejemplo:
uv run python eg.py preguntas.txt Parcial 3 10 both plantilla.docx xlsx
```

**Funciones importantes**:
- `load_questions_from_file()`: Parser de preguntas
- `shuffle_questions()`: Mezcla con seed
- `create_exam_txt()`: Generador TXT
- `create_exam_docx()`: Generador DOCX
- `create_answers_xlsx()`: Respuestas Excel

### 2. qg.py - Generador AI de Preguntas
**Propósito**: Generar preguntas desde PDF/DOCX/PPTX usando IA

**Motores soportados**:
- **Gemini** (Google Cloud): Requiere `GOOGLE_API_KEY`
- **Ollama** (Local): Requiere Ollama corriendo en `http://localhost:11434`

**Uso**:
```bash
# Gemini (por defecto)
uv run python qg.py documento.pdf --num_preguntas 10 --idioma español

# Ollama (local)
uv run python qg.py documento.pdf --motor ollama --modelo llama2 --num_preguntas 10

# Ver modelos disponibles
uv run python qg.py documento.pdf --list_models
```

**Funciones importantes**:
- `extract_text_from_pdf()`: Extracción PyPDF
- `extract_text_from_docx()`: Extracción python-docx
- `extract_text_from_pptx()`: Extracción python-pptx
- `generate_questions_with_gemini()`: IA Google
- `generate_questions_with_ollama()`: IA local
- `ensure_ollama_running()`: Auto-start Ollama

### 3. Interfaz Web (examgenerator/)
**Propósito**: Interfaz gráfica Flask para generar exámenes

**Uso**:
```bash
uv run python -m examgenerator.app
# Abre: http://localhost:5000
```

**Módulos**:
- `app.py`: Servidor Flask, rutas, lógica
- `cache.py`: Caché SHA256 de archivos procesados
- `validators.py`: Validación robusta de entradas
- `statistics.py`: Análisis de distribución de respuestas
- `logging_config.py`: Logging con colores e iconos

## 📝 Formato de Archivo de Preguntas

**Estructura obligatoria** (`preguntas.txt`):
```
1. ¿Texto de la pregunta?
A) Opción A
B) Opción B
C) Opción C
D) Opción D
ANSWER: C)

2. ¿Segunda pregunta?
A) Opción 1
B) Opción 2
C) Opción 3
D) Opción 4
ANSWER: A)
```

**Reglas críticas**:
- Preguntas: Opcional número `^\d+\.\s*` (se elimina al parsear)
- Opciones: **DEBEN** coincidir con `^[A-D][).]\s`
- Respuesta: `ANSWER: X)` donde X es A-D
- **Delimitador**: Línea vacía entre preguntas (OBLIGATORIO)
- No hay validación de 4 opciones - el parser acepta cualquier número

**Parser** (`load_questions_from_file()`):
- Regex compilados al inicio
- Máquina de estados: `current_question`, `options`, línea vacía → guardar
- Errores: `ValueError` con número de línea

## 🎨 Sistema de Plantillas DOCX

**Placeholders disponibles** (15+):
- `{{EXAM_NUMBER}}`: Número del examen
- `{{EXAM_TITLE}}`: Título (ej: "Parcial 1")
- `{{DATE}}`: Fecha en español (ej: "11 de enero de 2026")
- `{{COURSE}}`: Nombre del curso
- `{{NUM_QUESTIONS}}`: Cantidad de preguntas
- `{{EXAM_TIME}}`: Tiempo estimado (1 min/pregunta)
- `{{CONTENT}}`, `{{QUESTIONS}}`, `{{EXAM_CONTENT}}`: Punto de inserción
- `{{STUDENT_NAME}}`, `{{STUDENT_ID}}`, `{{PROFESSOR}}`, etc.

**Lógica de reemplazo**:
1. Reemplazar placeholders en TODOS los párrafos y celdas de tabla
2. Buscar marcador de inserción (`{{CONTENT}}`, `{{QUESTIONS}}`, `{{EXAM_CONTENT}}`)
3. Insertar preguntas y opciones
4. Aplicar estilos personalizados si existen (`'Custom Title'`, `'Question'`)
5. Fallback a formato manual si no hay estilos

**Meses en español**:
```python
meses = {1: 'enero', 2: 'febrero', ..., 12: 'diciembre'}
```

## 🔄 Randomización Determinística

**Crítico**: Garantiza mismos exámenes en TXT y DOCX

```python
# Antes de cada examen
random.seed(f"{exam_prefix}_{exam_number}")

# Mezclar preguntas
shuffled = random.sample(questions, k=questions_per_exam)

# Mezclar opciones y recalcular respuesta correcta
shuffled_options = random.sample(options, len(options))
new_correct_letter = option_letters[shuffled_options.index(correct_answer_text)]
```

**NO modificar** esta lógica - rompe la consistencia entre formatos.

## 📊 Formato de Respuestas

**Layout transpuesto** (exámenes como filas, preguntas como columnas):
```
        P1  P2  P3  P4  P5
Exam 1  B   A   D   C   A
Exam 2  C   B   A   D   B
Exam 3  A   D   C   B   C
```

**Formatos soportados**:
- **XLSX** (por defecto): `openpyxl`, colores, formato condicional
- **CSV**: Compatible con Excel
- **TXT**: Texto plano tabulado
- **HTML**: Tabla con estilos

**Funciones**:
- `create_answers_xlsx()`: Excel con formato
- `create_answers_csv()`: CSV simple
- `create_answers_txt()`: Texto tabulado
- `create_answers_html()`: HTML con CSS

## 🚀 Comandos Comunes

### Instalación
```bash
# Windows
powershell -ExecutionPolicy Bypass -File install.ps1

# Linux/macOS
bash install.sh
```

### Desarrollo
```bash
# Ejecutar generador principal
uv run python eg.py preguntas.txt Parcial 3 10

# Ejecutar generador AI
uv run python qg.py documento.pdf --num_preguntas 10

# Interfaz web
uv run python -m examgenerator.app

# Tests
uv run python -m pytest tests/

# Instalar paquete adicional
uv pip install nombre-paquete

# Actualizar dependencias
uv pip install --upgrade -r requirements.txt
```

### Verificación
```bash
# Listar paquetes instalados
uv pip list

# Verificar imports
uv run python -c "import docx; import openpyxl; import google.generativeai; print('OK')"

# Congelar dependencias
uv pip freeze > requirements.txt
```

## 🛠️ Dependencias Críticas

**Core**:
- `python-docx>=1.1.0`: Manipulación DOCX
- `openpyxl>=3.1.5`: Excel (XLSX)
- `flask>=3.1.2`: Interfaz web

**IA**:
- `google-generativeai>=0.3.0`: Gemini API
- `pypdf>=3.17.0`: Extracción PDF
- `python-pptx>=0.6.23`: Extracción PowerPoint

**Utilidades**:
- `requests>=2.32.5`: HTTP (para Ollama)
- `reportlab>=4.4.7`: Generación PDF
- `xlsxwriter>=3.2.9`: Alternativa Excel

## ⚠️ Anti-Patrones (NO HACER)

1. ❌ **NO modificar la lógica de seed**: Rompe consistencia TXT/DOCX
2. ❌ **NO usar pip/venv**: Usar UV siempre
3. ❌ **NO hardcodear API keys**: Usar `GOOGLE_API_KEY` env var
4. ❌ **NO romper delimitador de línea vacía**: Parser depende de esto
5. ❌ **NO cambiar layout transpuesto**: Todas las funciones dependen
6. ❌ **NO crear archivos sin UTF-8**: Causará errores de encoding
7. ❌ **NO usar emojis en PowerShell**: Problemas de encoding
8. ❌ **NO duplicar código**: Verificar antes de pegar
9. ❌ **NO crear archivos en carpetas incorrectas**: Respetar organización por tipo (ver sección 🗂️)
10. ❌ **NO mezclar archivos**: Código en `examgenerator/`, tests en `tests/`, docs en `docs/`

## 🧪 Testing

**Tests existentes**:
- `tests/test_validators.py`: Validación de entradas
- `tests/test_cache.py`: Sistema de caché

**Ejecutar**:
```bash
uv run python -m pytest tests/
uv run python -m pytest tests/ -v  # Verbose
uv run python -m pytest tests/test_validators.py  # Específico
```

**Crear nuevos tests**:
```python
import pytest
from examgenerator.validators import validate_question_file

def test_valid_file():
    result = validate_question_file('preguntas.txt')
    assert result['valid'] == True
```

## 📋 Checklist para Nuevas Funcionalidades

Antes de implementar una nueva característica:

- [ ] **Organización**: Crear archivo en la carpeta correcta según su tipo (ver 🗂️)
- [ ] **Encoding**: Verificar codificación UTF-8 en todos los archivos
- [ ] **UV**: Usar UV para instalación de paquetes (`uv pip install`)
- [ ] **Idioma**: Documentar en español
- [ ] **Changelog**: Añadir entrada en CHANGELOG.md
- [ ] **Readme**: Actualizar README.md si es necesario
- [ ] Crear tests si aplica
- [ ] Verificar compatibilidad con randomización determinística
- [ ] Probar con `uv run python script.py`
- [ ] Validar en Windows y Linux si es posible

## 🔐 Seguridad y API Keys

**Google Gemini**:
```bash
# Windows
$env:GOOGLE_API_KEY = "tu-api-key"

# Linux/macOS
export GOOGLE_API_KEY="tu-api-key"

# .env file (NO commitear)
GOOGLE_API_KEY=tu-api-key
```

**Ollama**:
- Local: No requiere API key
- URL por defecto: `http://localhost:11434`
- Customizable: `--ollama_url http://custom:port`

## 📄 Documentación

**Archivos principales**:
- `README.md`: Documentación general
- `QUICK_START_V11.md`: Guía rápida v11
- `CHANGELOG.md`: Historial completo
- `UV_INFO.md`: Guía de UV
- `MIGRACION_UV.md`: Detalles migración a UV
- `RESUMEN_MIGRACION_UV.md`: Resumen ejecutivo

**Actualizar al añadir features**:
1. Añadir en CHANGELOG.md bajo versión correspondiente
2. Actualizar README.md si cambia uso principal
3. Actualizar QUICK_START si afecta inicio rápido
4. Documentar nuevos comandos en este archivo

## 🌐 Multi-Plataforma

**Windows**:
- Scripts: PowerShell (`.ps1`)
- Encoding: UTF-8 sin BOM
- Paths: Usar `os.path.join()` o `pathlib.Path`
- Comandos: Verificar compatibilidad PowerShell

**Linux/macOS**:
- Scripts: Bash (`.sh`)
- Encoding: UTF-8
- Paths: Forward slashes `/`
- Permisos: `chmod +x script.sh`

**Código portable**:
```python
import os
import sys
from pathlib import Path

# Rutas portables
output_dir = Path("Examenes") / exam_prefix
output_file = output_dir / f"{exam_prefix}_{num}.txt"

# Detectar sistema
if sys.platform == 'win32':
    # Windows específico
elif sys.platform.startswith('linux'):
    # Linux específico
elif sys.platform == 'darwin':
    # macOS específico
```

## 🎯 Versionado

**Formato**: `MAJOR.YYYYMMDD[.MINOR]`
- `MAJOR`: Versión principal (actualmente 11)
- `YYYYMMDD`: Fecha de cambio
- `MINOR`: Opcional para múltiples releases en un día

**Ejemplos**:
- `11.20260111`: Primera versión del 11 de enero de 2026
- `11.20260111.1`: Segunda versión del mismo día (migración UV)

**Actualizar**:
```python
# En archivos .py
# by TiiZss v.11.20260111.1

# En pyproject.toml
version = "11.20260111.1"

# En CHANGELOG.md
## [11.20260111.1] - 2026-01-11
```

## 🤝 Colaboración

**Estilo de código**:
- PEP 8 para Python (con nombres en español cuando sea lógico)
- Comentarios descriptivos en español
- Type hints cuando sea posible
- Docstrings en español

**Commits**:
- Mensajes en español o inglés (consistente)
- Descriptivos: "Añade validación de archivo de preguntas"
- Referencia a issues si aplica

**Pull Requests**:
- Describir cambios claramente
- Incluir tests si es posible
- Actualizar documentación relevante

## 📞 Soporte

**Autor**: TiiZss  
**Proyecto**: ExamGenerator  
**GitHub**: TiiZss/ExamGenerator  
**Versión actual**: 11.20260111.1  
**Python requerido**: 3.9+ (recomendado 3.11)  
**Gestión de paquetes**: UV (10-100x más rápido que pip)

---

**Última actualización**: 11 de enero de 2026  
**IA**: Sigue estas instrucciones para mantener consistencia y calidad en el proyecto.
