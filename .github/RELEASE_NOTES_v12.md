# 🚀 ExamGenerator v12.20260111 - Major Release

## 🎉 Highlights

### 🐳 **Stack Docker Completo**
ExamGenerator ahora viene con una arquitectura Docker completamente integrada:
- **ExGen-Web**: Interfaz web Flask en puerto 5000
- **ExGen-App**: Motor CLI para procesamiento en background
- **ExGen-Ollama**: IA local Ollama preconfigurado en puerto 11434

**Instalación en 1 comando:**
```bash
docker-compose up -d
```
Accede a http://localhost:5000 y empieza a generar exámenes.

### 🤖 **Dual AI Engine**
Dos motores de IA para máxima flexibilidad:

#### Google Gemini 2.5 (Cloud)
- Modelos: `gemini-2.5-flash` (rápido) y `gemini-2.5-pro` (potente)
- Configuración de API key desde interfaz web
- Chunking automático hasta 15 preguntas por llamada
- Detección automática de disponibilidad

#### Ollama (Local - Sin límites)
- Modelos: phi3:mini, llama2, mistral, codellama
- 100% privado, sin costos API
- Chunking automático hasta 10 preguntas por llamada
- Auto-start integrado en el stack Docker

### 🎨 **Interfaz Web Mejorada**

#### Nuevo Header Profesional
- **Logo TiiZss** en esquina superior derecha (fondo blanco con sombra)
- **Badge de versión** (v12.20260111) en esquina superior izquierda (glassmorphism)

#### Página de Configuración
Nueva ruta `/settings` para gestionar:
- API key de Google Gemini
- Test de conectividad
- Guardado persistente en JSON

#### UX Mejorada
- Gemini se deshabilita automáticamente si no hay API key configurada
- Mensaje de advertencia con enlace directo a configuración
- Progress bar animado para generación de preguntas
- Auto-descarga de archivos generados

### 📋 **Generación de Exámenes Profesional**

#### Formato AIKEN Nativo
```
¿Cuál es la capital de Francia?
A) Madrid
B) París
C) Londres
D) Berlín
ANSWER: B
```
Exactamente 4 opciones por pregunta, formato estándar educativo.

#### Chunking Inteligente
Genera **cualquier cantidad** de preguntas sin límites:
- Ollama: divide en chunks de 10 preguntas
- Gemini: divide en chunks de 15 preguntas
- Combina resultados automáticamente
- Mensajes de progreso en tiempo real

#### Múltiples Formatos de Exportación
- **TXT**: Texto plano con formato limpio
- **DOCX**: Documentos Word con plantillas personalizables
- **XLSX**: Excel con respuestas transpuestas
- **CSV**: Compatible con sistemas LMS
- **HTML**: Vista previa en navegador

### 📦 **UV Package Manager**
Migración completa a UV para instalaciones ultrarrápidas:
- **10-100x más rápido** que pip
- Instalación completa en ~5 segundos
- `pyproject.toml` para gestión moderna (PEP 518/621)
- Auto-instalación en scripts de setup

### 📁 **Reorganización Completa del Proyecto**

Nueva estructura profesional:
```
ExamGenerator/
├── assets/              # Logo y recursos estáticos
├── docs/                # Documentación completa con índice
│   ├── README.md       # Índice de documentación
│   ├── CHANGELOG.md    # Historial de cambios
│   ├── DOCKER.md       # Guía Docker
│   └── ...
├── scripts/            # Scripts de instalación
│   ├── install.ps1     # Windows
│   ├── install.sh      # Linux/macOS
│   └── docker-quickstart.*
├── examples/           # Ejemplos y plantillas
├── tests/             # Suite de tests
├── examgenerator/     # Código fuente modular
│   ├── core/          # Lógica central
│   ├── exporters/     # Exportadores
│   ├── ai/            # Clientes IA
│   ├── utils/         # Utilidades
│   └── web/           # Aplicación Flask
└── output/            # Directorio de salida
```

### 🔧 **Mejoras Técnicas**

#### Sistema de Caché Inteligente
- Hash SHA256 para deduplicación
- TTL configurable (7 días por default)
- Estadísticas de hit/miss
- API de limpieza

#### Logging Profesional
- Colores e iconos en consola
- Niveles configurables
- Logs persistentes
- Formato estructurado

#### Validaciones Robustas
- Tipos de archivo permitidos
- Límites de tamaño (50MB max)
- Sanitización de nombres
- Mensajes de error claros en español

#### Hot-Reload en Docker
Código fuente montado como volúmenes:
- Cambios reflejados sin rebuild
- Desarrollo ágil
- Restart rápido del contenedor

### 📝 **Documentación Actualizada**

#### README.md con Badges Completos
- Versión, Python, License, Docker
- GitHub Stars, Issues, Changelog
- **Buy Me A Coffee** para TiiZss
- AI Powered (Gemini | Ollama)

#### Guías Reorganizadas
- Índice central en `docs/README.md`
- Quick Start actualizado
- Guías de migración
- Setup de Ollama
- Feature guides

## 🚀 **Quick Start**

### Docker (Recomendado)
```bash
git clone https://github.com/TiiZss/ExamGenerator.git
cd ExamGenerator
docker-compose up -d
```
Accede a http://localhost:5000

### Manual con UV
```bash
# Instalar
./scripts/install.sh  # Linux/macOS
.\scripts\install.ps1 # Windows

# Ejecutar web
uv run python run_web.py

# CLI
uv run python cli.py --help
```

## 📊 **Archivos Modificados en Esta Versión**

### Nuevos Archivos
- `assets/logo.png` - Logo TiiZss
- `docs/README.md` - Índice de documentación
- `examgenerator/web/templates/settings.html` - Página de configuración
- `.dockerignore`, `.gitignore` optimizados
- `docker-compose.yml` - Stack completo
- `Dockerfile` - Multi-stage build

### Archivos Reorganizados
- Scripts → `scripts/`
- Documentación → `docs/`
- Tests → `tests/`
- Ejemplos → `examples/`

### Archivos Eliminados
- `eg_legacy.py` (obsoleto)
- `eg_v12.py` (duplicado)
- Scripts de instalación en raíz (movidos a scripts/)

## 🐛 **Bugs Corregidos**
- Caché bloqueando nuevas funcionalidades
- Modelos Gemini con nombres incorrectos
- Progress bar sin animación
- Solo 1 pregunta generada (num_predict muy bajo)
- Prompts con placeholders en lugar de ejemplos reales

## 🎯 **Breaking Changes**
- Python 3.11+ requerido (antes 3.8+)
- Rutas de scripts cambiadas (ahora en `scripts/`)
- API de configuración usa JSON en lugar de solo .env

## 🙏 **Agradecimientos**
Gracias a todos los usuarios que reportaron issues y sugirieron mejoras.

## ☕ **Apoya el Proyecto**
Si ExamGenerator te ha sido útil, considera invitarme un café:

[![Buy Me A Coffee](https://img.shields.io/badge/☕-Buy%20me%20a%20coffee-orange?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/tiizss)

## 📋 **Próximos Pasos (v13)**
- Exportación a PDF nativo
- Plantillas adicionales
- Soporte multiidioma en UI
- Banco de preguntas compartido
- Analytics dashboard
- GitHub Actions CI/CD

---

**Versión completa**: v12.20260111  
**Fecha de lanzamiento**: 11 de enero de 2026  
**Changelog completo**: [docs/CHANGELOG.md](../docs/CHANGELOG.md)
