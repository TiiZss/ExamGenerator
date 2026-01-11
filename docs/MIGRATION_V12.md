# Guía de Migración a ExamGenerator v12

**Versión:** 12.20260111  
**Fecha:** 11 de enero de 2026  
**Tipo de actualización:** MAJOR - Arquitectura Modular Completa

---

## 🎯 Resumen Ejecutivo

ExamGenerator v12 representa una refactorización arquitectónica completa del proyecto, transformándolo de scripts monolíticos a una arquitectura modular profesional. Esta versión introduce:

- **Arquitectura modular** con separación clara de responsabilidades
- **CLI moderno** con Rich UI y comandos intuitivos
- **Sistema de configuración** basado en YAML
- **Mejor mantenibilidad** con módulos reutilizables
- **100% compatible** con comandos anteriores

---

## 📊 Cambios Principales

### 1. Arquitectura Modular

#### Antes (v11):
```
ExamGenerator/
├── eg.py (786 líneas - TODO en un archivo)
├── qg.py (similar)
└── requirements.txt
```

#### Ahora (v12):
```
ExamGenerator/
├── eg.py (refactorizado - 263 líneas)
├── cli.py (CLI moderno)
├── config.yaml (configuración centralizada)
├── examgenerator/
│   ├── core/               # Lógica central
│   │   ├── question_loader.py
│   │   ├── exam_generator.py
│   │   ├── shuffler.py
│   │   ├── time_calculator.py
│   │   └── directory_manager.py
│   ├── exporters/          # Exportación modular
│   │   ├── txt_exporter.py
│   │   ├── docx_exporter.py
│   │   ├── excel_exporter.py
│   │   ├── csv_exporter.py
│   │   └── html_exporter.py
│   ├── ai/                 # IA (próximamente)
│   ├── config.py           # Gestión de configuración
│   └── utils/              # Utilidades
└── pyproject.toml (moderno)
```

### 2. CLI Moderno vs CLI Tradicional

#### CLI Tradicional (Sigue funcionando):
```bash
python eg.py preguntas.txt Parcial 3 10 both plantilla.docx xlsx
```

#### CLI Moderno (Nuevo - Recomendado):
```bash
# Comando equivalente con mejor UX
python cli.py generate preguntas.txt Parcial 3 10 \
  --format both \
  --template plantilla.docx \
  --answers xlsx

# O usando la instalación global (después de uv tool install)
examgen generate preguntas.txt Parcial 3 10 --format both
```

**Ventajas del CLI Moderno:**
- ✅ Ayuda interactiva con `--help`
- ✅ Validación automática de argumentos
- ✅ Output visual con Rich (colores, tablas, paneles)
- ✅ Progress bars para operaciones largas
- ✅ Manejo de errores mejorado
- ✅ Comandos semánticos (generate, validate, config)

### 3. Comandos del Nuevo CLI

```bash
# Ver información del sistema
python cli.py info

# Generar exámenes (múltiples formatos)
python cli.py generate preguntas.txt Final 5 20 \
  --format both \
  --answers html

# Validar archivo de preguntas
python cli.py validate preguntas.txt

# Generar preguntas con IA
python cli.py ai-generate documento.pdf \
  --num-questions 15 \
  --engine gemini \
  --language español

# Gestionar configuración
python cli.py config --show
python cli.py config --create --path mi_config.yaml

# Iniciar interfaz web
python cli.py web --port 8080
```

---

## 🔄 Guía de Migración Paso a Paso

### Paso 1: Actualizar Dependencias

```bash
# Con UV (recomendado)
uv add pyyaml click rich python-docx

# O con pip tradicional
pip install pyyaml click rich python-docx
```

### Paso 2: Verificar Compatibilidad

Tus scripts antiguos **siguen funcionando** sin cambios:

```bash
# ✅ Esto sigue funcionando exactamente igual
python eg.py preguntas.txt Parcial 3 10
python qg.py documento.pdf --num_preguntas 10
```

### Paso 3: Adoptar Nueva Arquitectura (Opcional pero Recomendado)

#### Opción A: Migración Gradual

1. **Usa el CLI moderno** para nuevos proyectos:
   ```bash
   python cli.py generate preguntas.txt Parcial 3 10
   ```

2. **Mantén scripts legacy** para proyectos existentes:
   ```bash
   python eg_legacy.py preguntas.txt Parcial 3 10  # Respaldo del original
   ```

#### Opción B: Migración Completa

1. **Crea archivo de configuración**:
   ```bash
   python cli.py config --create
   ```

2. **Personaliza config.yaml**:
   ```yaml
   exam:
     default_export_format: "both"
     default_answers_format: "html"
     default_time_per_question: 2  # 2 min por pregunta
   
   docx:
     default_template: "templates/mi_plantilla.docx"
   ```

3. **Usa CLI con configuración**:
   ```bash
   python cli.py generate preguntas.txt Parcial 3 10 --config mi_config.yaml
   ```

### Paso 4: Aprovechar Nuevas Funcionalidades

#### Validación de Preguntas

Antes tenías que ejecutar y ver errores. Ahora:

```bash
python cli.py validate preguntas.txt
```

**Output:**
```
┏━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
┃ Pregunta # ┃ Opciones ┃ Respuesta ┃
┡━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
│         1 │    4     │    A     │
│         2 │    4     │    B     │
│        .. │   ..     │   ..     │
└───────────┴─────────┴──────────┘

✓ Archivo válido: 20 preguntas cargadas
```

#### Información del Sistema

```bash
python cli.py info
```

Te muestra qué módulos están instalados y configurados.

---

## 📦 Módulos Nuevos - Para Desarrolladores

### examgenerator.core

Módulos centrales reutilizables:

```python
from examgenerator.core import (
    load_questions_from_file,
    validate_questions,
    generate_exam,
    calculate_exam_time,
    create_output_directory
)

# Cargar preguntas
questions = load_questions_from_file("preguntas.txt")

# Validar
validate_questions(questions)

# Generar examen
exam_questions, answers = generate_exam(
    questions,
    num_questions=10,
    seed="MiExamen_1"
)
```

### examgenerator.exporters

Exportadores independientes:

```python
from examgenerator.exporters import (
    create_answers_excel,
    create_answers_html,
    create_exam_docx
)

# Exportar respuestas a HTML
all_exam_data = [
    {'exam_number': 1, 'answers': ['A', 'B', 'C', ...]},
    {'exam_number': 2, 'answers': ['B', 'C', 'A', ...]}
]

create_answers_html(all_exam_data, "Parcial", "output/")
```

### examgenerator.config

Sistema de configuración:

```python
from examgenerator.config import config

# Obtener configuración
time_per_q = config.get('exam.default_time_per_question', 1)
engine = config.get('ai.default_engine', 'gemini')

# Modificar configuración
config.set('exam.default_export_format', 'both')

# Guardar cambios
config.save('mi_config.yaml')
```

---

## 🔧 Cambios en la API Programática

### eg.py

#### Antes (v11):
```python
# No había función reutilizable
# Solo ejecutar: python eg.py ...
```

#### Ahora (v12):
```python
# Función main_generate() exportada
from eg import main_generate

output_dir = main_generate(
    questions_file="preguntas.txt",
    exam_prefix="Parcial",
    num_exams=3,
    num_questions=10,
    export_format="both",
    template_path="plantilla.docx",
    answers_format="xlsx"
)
```

---

## ⚙️ Configuración con config.yaml

Crea `config.yaml` en la raíz del proyecto:

```yaml
# Configuración de Exámenes
exam:
  default_time_per_question: 1
  option_letters: "ABCD"
  default_export_format: "txt"
  default_answers_format: "xlsx"

# Configuración DOCX
docx:
  default_template: "templates/plantilla_universidad.docx"
  fonts:
    title_size: 18
    question_size: 12
    option_size: 11

# Configuración IA
ai:
  default_engine: "gemini"
  gemini:
    default_model: "gemini-1.5-pro"
    temperature: 0.7
  ollama:
    default_model: "llama2"
    url: "http://localhost:11434"
    auto_start: true

# Logging
logging:
  enabled: true
  level: "INFO"
  log_file: "examgenerator.log"

# Validación
validation:
  min_questions_per_exam: 1
  max_questions_per_exam: 100
  min_options: 2
  max_options: 8

# Web Interface
web:
  host: "127.0.0.1"
  port: 5000
  debug: false
```

Luego úsala:

```bash
python cli.py generate preguntas.txt Parcial 3 10 --config config.yaml
```

---

## 🚀 Beneficios de la v12

| Aspecto | v11 | v12 |
|---------|-----|-----|
| **Líneas de código** | eg.py: 786 líneas | eg.py: 263 líneas |
| **Modularidad** | Monolítico | 15+ módulos independientes |
| **CLI** | Args posicionales | Click con --flags |
| **Configuración** | Hardcoded | config.yaml flexible |
| **Validación** | Al ejecutar | Comando `validate` |
| **Output** | Texto plano | Rich UI con colores |
| **Reutilización** | Difícil | Importar módulos |
| **Testing** | Complejo | Unit tests por módulo |
| **Mantenibilidad** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔄 Compatibilidad con Versiones Anteriores

✅ **100% compatible**: Tus scripts antiguos siguen funcionando

```bash
# ✅ Funcionan igual que en v11
python eg.py preguntas.txt Parcial 3 10
python eg.py preguntas.txt Final 5 20 docx plantilla.docx
python qg.py documento.pdf --num_preguntas 10
```

📝 **Respaldo disponible**: `eg_legacy.py` contiene el código original completo

---

## 📚 Ejemplos de Migración

### Ejemplo 1: Script Básico

**v11:**
```bash
python eg.py preguntas.txt Parcial 3 10 txt
```

**v12 (Opción A - Compatible):**
```bash
python eg.py preguntas.txt Parcial 3 10 txt  # Funciona igual
```

**v12 (Opción B - Recomendado):**
```bash
python cli.py generate preguntas.txt Parcial 3 10 --format txt
```

### Ejemplo 2: Con Plantilla DOCX

**v11:**
```bash
python eg.py preguntas.txt Final 5 20 docx plantilla.docx xlsx
```

**v12 (Moderno):**
```bash
python cli.py generate preguntas.txt Final 5 20 \
  --format docx \
  --template plantilla.docx \
  --answers xlsx
```

### Ejemplo 3: Generación con IA

**v11:**
```bash
python qg.py documento.pdf --num_preguntas 15 --idioma español
```

**v12 (Moderno):**
```bash
python cli.py ai-generate documento.pdf \
  --num-questions 15 \
  --language español \
  --engine gemini
```

---

## 🛠️ Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'examgenerator'"

**Solución:**
```bash
# Instalar en modo editable
uv pip install -e .

# O configurar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/ruta/a/ExamGenerator"
```

### Problema: "Configuración no encontrada"

**Solución:**
```bash
# Crear configuración por defecto
python cli.py config --create

# O especificar ruta
python cli.py generate ... --config /ruta/a/config.yaml
```

### Problema: "python-docx not installed"

**Solución:**
```bash
uv add python-docx
# O con pip:
pip install python-docx
```

---

## 📖 Recursos Adicionales

- **README.md**: Guía de uso completa
- **docs/copilot-instructions.md**: Documentación técnica detallada
- **docs/PROPUESTAS_REORGANIZACION.md**: Propuestas implementadas
- **examples/**: Ejemplos de preguntas y documentos
- **config.yaml**: Configuración de referencia

---

## 🎓 Próximos Pasos

1. **Familiarízate con el CLI moderno**: Ejecuta `python cli.py --help`
2. **Crea tu configuración**: `python cli.py config --create`
3. **Valida tus preguntas**: `python cli.py validate preguntas.txt`
4. **Genera exámenes**: Usa el nuevo CLI o el tradicional
5. **Explora módulos**: Si desarrollas, importa desde `examgenerator.core`

---

## 💬 Preguntas Frecuentes

**P: ¿Necesito migrar inmediatamente?**  
R: No. La v12 es 100% compatible con comandos antiguos. Migra cuando estés listo.

**P: ¿Puedo mezclar CLI antiguo y moderno?**  
R: Sí, usa el que prefieras para cada tarea.

**P: ¿Se perdieron funcionalidades?**  
R: No. Todas las funcionalidades de v11 están en v12, con mejoras.

**P: ¿Cómo reporto problemas?**  
R: GitHub Issues: https://github.com/TiiZss/ExamGenerator/issues

---

## 📜 Changelog v12

**Nuevas Funcionalidades:**
- ✨ Arquitectura modular completa
- ✨ CLI moderno con Click y Rich
- ✨ Sistema de configuración YAML
- ✨ Comando `validate` para preguntas
- ✨ Comando `config` para gestión
- ✨ Comando `info` para diagnóstico
- ✨ API programática con funciones exportadas

**Mejoras:**
- 🚀 67% reducción en líneas de código principal (786 → 263)
- 🚀 Módulos reutilizables e independientes
- 🚀 Mejor separación de responsabilidades
- 🚀 Output visual mejorado con colores y tablas
- 🚀 Validación de argumentos automática
- 🚀 Manejo de errores mejorado

**Mantenimiento:**
- 🔧 Código más limpio y mantenible
- 🔧 Tests unitarios más fáciles
- 🔧 Documentación actualizada
- 🔧 Respaldo del código original (eg_legacy.py)

---

**¡Bienvenido a ExamGenerator v12!** 🎉

Para soporte: https://github.com/TiiZss/ExamGenerator
