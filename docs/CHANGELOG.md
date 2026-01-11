# 📝 Changelog - ExamGenerator

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [11.20260111.1] - 2026-01-11

### 🚀 Añadido
- **UV Package Manager**: Migración completa de pip a UV (10-100x más rápido)
  - Auto-instalación de UV en install.ps1 e install.sh
  - Instalación completa en ~5 segundos (vs ~53s con pip)
  - Resolución de dependencias en 448ms
  - 45 paquetes instalados en 822ms
  - pyproject.toml para gestión moderna de proyecto (PEP 518/621)
  - .python-version especifica Python 3.11
  - Cache inteligente de paquetes
  - Comando `uv run` elimina necesidad de activar entorno

### 🔧 Cambiado
- **install.ps1**: Reescrito completamente sin emojis (compatibilidad PowerShell)
  - Auto-detección y auto-instalación de UV
  - Medición de tiempo de instalación
  - Mensajes de progreso [1/5], [2/5], etc.
- **install.sh**: Versión Linux/macOS con colores y auto-instalación UV
- **pyproject.toml**: `requires-python = ">=3.9"` (requerido por google-generativeai)
- **eg.py**: Limpiado de código duplicado y conflictos de merge
- Todos los comandos en documentación usan `uv run python ...`

### 📚 Documentación
- **UV_INFO.md** (NUEVO): Guía completa de UV con comparaciones y ejemplos
- **RESUMEN_MIGRACION_UV.md** (NUEVO): Resumen ejecutivo de la migración
- **MIGRACION_UV.md** (NUEVO): Guía detallada de migración
- README.md: Sección de instalación actualizada con UV
- QUICK_START_V11.md: 6 secciones actualizadas con comandos UV
- Tabla comparativa: pip vs UV (10.6x más rápido)

### ✅ Pruebas
- Instalación exitosa en Windows con PowerShell
- Generación de exámenes funcionando: `uv run python eg.py`
- 45 paquetes instalados correctamente
- Tiempo total de instalación: 4.2 segundos
- Instrucciones de instalación manual de UV
- Comandos actualizados en guías de inicio rápido

---

## [11.20260111] - 2026-01-11

### 🎉 Añadido
- **Interfaz Web con Flask**: Aplicación web completa para generar exámenes y preguntas sin usar la terminal
  - Página principal con dashboard
  - Formulario para generar exámenes desde archivo de preguntas
  - Formulario para generar preguntas con IA desde documentos
  - Diseño responsive y moderno con gradientes
  - Estadísticas de caché en tiempo real
- **Sistema de Logging Profesional**: Reemplazo completo de print() por logging
  - Colores e iconos en consola
  - Niveles configurables (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Logs persistentes en archivos
  - Formato detallado para debugging
- **Estructura Modular**: Refactorización completa del proyecto
  - `examgenerator/core/`: Funciones centrales
  - `examgenerator/exporters/`: Exportadores de formatos
  - `examgenerator/ai/`: Clientes de IA
  - `examgenerator/utils/`: Utilidades (logging, validators, cache, statistics)
  - `examgenerator/web/`: Aplicación web Flask
  - `tests/`: Suite de tests
- **Sistema de Caché Inteligente**: Evita regenerar preguntas idénticas
  - Hash SHA256 para identificar contenido único
  - TTL configurable (7 días por defecto)
  - Estadísticas de caché
  - API para limpiar caché antiguo
- **Validaciones Robustas**: Sistema completo de validación
  - Validación de existencia de archivos
  - Validación de extensiones permitidas
  - Validación de tamaño máximo (50MB)
  - Validación de formato de preguntas
  - Sanitización de nombres de archivo
  - Mensajes de error claros en español
- **Estadísticas de Exámenes**: Análisis detallado de exámenes generados
  - Distribución de respuestas correctas con gráficos ASCII
  - Análisis de reutilización de preguntas
  - Detección de desbalance en respuestas
  - Advertencias automáticas
  - Exportación a JSON
- **CHANGELOG.md**: Documentación completa de versiones y cambios
- **Limpieza de Código**: Eliminados conflictos de merge (<<<<<<< HEAD markers)

### 🔧 Cambiado
- Versión actualizada de `9.20251125` a `11.20260111`
- Mejora en la organización del proyecto con estructura modular
- Requirements.txt actualizado con nuevas dependencias

### 🐛 Corregido
- Conflictos de merge en eg.py (líneas 1-10 y 1530-1572)
- Manejo de errores mejorado en todas las funciones
- Validación de entrada antes de procesamiento

### 🔐 Seguridad
- Validación de tamaño de archivos (máximo 50MB)
- Sanitización de nombres de archivo
- Protección contra nombres reservados de Windows
- Validación de caracteres peligrosos en rutas

### 📚 Documentación
- MEJORAS_PROPUESTAS.md con 28 propuestas detalladas
- Este CHANGELOG.md completo
- Docstrings mejorados con ejemplos y type hints

---

## [10.20260111.3] - 2026-01-11

### 🎉 Añadido
- **Auto-inicio de Ollama**: Detección y arranque automático de Ollama si no está corriendo
  - Detección de sistema operativo (Windows/Linux/macOS)
  - Confirmación del usuario antes de iniciar
  - Mensajes informativos en español
  - Verificación de conexión después del inicio
- **Documentación de Ollama**: 
  - OLLAMA_SETUP.md: Guía completa de instalación y configuración
  - OLLAMA_AUTOSTART.md: Explicación del auto-inicio
  - CHANGELOG_OLLAMA.md: Registro de cambios de Ollama
  - QUICK_START.md: Inicio rápido con ejemplos

### 🔧 Cambiado
- `start_ollama_server()` ahora detecta el SO automáticamente
- Mejora en mensajes de error cuando Ollama no está disponible
- URL de Ollama configurable via `--ollama_url`

### 🐛 Corregido
- Manejo de timeouts en conexiones con Ollama (5 minutos)
- Mejor detección de Ollama corriendo en el sistema

---

## [10.20260111.2] - 2026-01-11

### 🎉 Añadido
- **Soporte dual de motores IA**: Google Gemini (cloud) + Ollama (local)
  - `--motor gemini` para usar Google Gemini
  - `--motor ollama` para usar Ollama local
  - Selección de modelo específico con `--modelo`
- **Modelos Gemini soportados**:
  - `gemini-1.5-flash` (por defecto, rápido)
  - `gemini-1.5-pro` (más preciso)
- **Modelos Ollama soportados**:
  - `llama2` (por defecto)
  - `mistral`, `codellama`, `gemma`, `phi`, etc.
- Parámetro `--ollama_url` para servidor Ollama personalizado
- Funciones separadas: `generate_questions_with_gemini()` y `generate_questions_with_ollama()`

### 🔧 Cambiado
- Arquitectura refactorizada para soportar múltiples motores
- Prompts mejorados para generar preguntas en formato específico
- Timeout de Ollama aumentado a 300 segundos (5 minutos)

---

## [10.20260111.1] - 2026-01-11

### 🎉 Añadido
- **.github/copilot-instructions.md**: Guía completa para agentes de IA
  - Descripción de arquitectura del proyecto
  - Patrones de desarrollo clave
  - Formato de archivos de preguntas
  - Comandos de línea de comandos
  - Anti-patrones a evitar
  - Convenciones del proyecto (español-first)

---

## [9.20251125] - 2025-11-25

### 🎉 Inicial
- Generación de exámenes aleatorios desde archivo de preguntas
- Exportación a TXT, DOCX, o ambos
- Sistema de plantillas DOCX con 15+ placeholders
- Generación de archivos de respuestas en múltiples formatos (XLSX, CSV, HTML, TXT)
- Layout transpuesto (exámenes como filas, preguntas como columnas)
- Randomización determinística con `random.seed()`
- Cálculo automático de tiempo de examen
- Sanitización de nombres de carpetas
- Scripts de instalación multiplataforma (Windows/Linux/macOS)
- Soporte para Google Gemini en `qg.py`
- Extracción de texto desde PDF, DOCX, PPTX

### 🔧 Características
- Sistema de opciones mezcladas aleatoriamente
- Respuesta correcta ajustada después del mezclado
- Fechas con nombres de meses en español
- Makefile para comandos comunes
- Argumentos de línea de comandos completos

---

## Tipos de Cambios

- 🎉 **Añadido**: Para nuevas funcionalidades
- 🔧 **Cambiado**: Para cambios en funcionalidad existente
- 🗑️ **Obsoleto**: Para funcionalidades que serán removidas
- ❌ **Removido**: Para funcionalidades removidas
- 🐛 **Corregido**: Para correcciones de bugs
- 🔐 **Seguridad**: Para vulnerabilidades corregidas

---

## Versionado

El proyecto usa versionado basado en fechas: `MAJOR.YYYYMMDD[.PATCH]`

- **MAJOR**: Versión principal (cambios significativos)
- **YYYY**: Año
- **MM**: Mes
- **DD**: Día
- **PATCH** (opcional): Versión de parche del día

Ejemplo: `11.20260111.3` = Versión 11, del 11 de enero de 2026, parche 3

---

## Enlaces

- **Repositorio**: https://github.com/TiiZss/ExamGenerator
- **Documentación**: Ver archivos .md en el repositorio
- **Issues**: https://github.com/TiiZss/ExamGenerator/issues
