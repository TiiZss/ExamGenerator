# 📋 Propuestas de Reorganización y Mejora - ExamGenerator

**Fecha**: 11 de enero de 2026  
**Versión**: 11.20260111.1  
**Autor**: Análisis completo del proyecto

---

## ✅ REORGANIZACIÓN COMPLETADA

### 📁 Nueva Estructura de Carpetas

```
ExamGenerator/
├── .github/                    # Configuración GitHub
│   └── copilot-instructions.md
├── .venv/                      # Entorno virtual (ignorado)
├── docs/                       # 📚 TODA la documentación
│   ├── CHANGELOG.md
│   ├── CHANGELOG_OLLAMA.md
│   ├── copilot-instructions.md
│   ├── IMPLEMENTACION_V11.md
│   ├── MEJORAS_PROPUESTAS.md
│   ├── MIGRACION_UV.md
│   ├── OLLAMA_AUTOSTART.md
│   ├── OLLAMA_SETUP.md
│   ├── QUICK_START.md
│   ├── QUICK_START_V11.md
│   ├── RESUMEN_MIGRACION_UV.md
│   └── UV_INFO.md
├── examples/                   # 📂 Archivos de ejemplo y demos
│   ├── preguntas.txt           # Archivo de ejemplo
│   ├── documento_ia.docx       # Documento para IA
│   ├── documento_prueba.txt    # Texto de prueba
│   └── demo_features.py        # Demo de funcionalidades
├── examgenerator/              # 📦 Paquete principal
│   ├── ai/                     # Módulos de IA
│   ├── core/                   # Lógica core
│   ├── exporters/              # Exportadores
│   ├── utils/                  # Utilidades
│   │   ├── cache.py
│   │   ├── logging_config.py
│   │   ├── statistics.py
│   │   └── validators.py
│   └── web/                    # Interfaz web
│       ├── app.py
│       └── templates/
│           ├── base.html
│           ├── generate_exams.html
│           ├── generate_questions.html
│           └── index.html
├── scripts/                    # 🛠️ Scripts de instalación y utilidades
│   ├── install.ps1             # Windows
│   ├── install.sh              # Linux/macOS
│   ├── install_quick.sh        # Instalación rápida
│   ├── MAKEFILE                # Make targets
│   └── setup.sh                # Setup universal
├── templates/                  # 📄 Plantillas DOCX de usuario
├── tests/                      # 🧪 Tests unitarios
│   ├── test_autostart.py
│   ├── test_cache.py
│   ├── test_setup.py
│   └── test_validators.py
├── .gitignore                  # Git ignore mejorado
├── .python-version             # Python 3.11
├── eg.py                       # Script principal generador
├── qg.py                       # Script generador IA
├── run_web.py                  # Launcher web app
├── LICENSE                     # GPL v3
├── README.md                   # Documentación principal
├── pyproject.toml              # Configuración moderna
└── requirements.txt            # Dependencias
```

### 🔄 Cambios Realizados

1. **✅ Documentación centralizada** → `docs/`
   - Todos los `.md` (excepto README)
   - 12 archivos reorganizados
   
2. **✅ Scripts organizados** → `scripts/`
   - `install.ps1`, `install.sh`, `install_quick.sh`, `setup.sh`, `MAKEFILE`
   - Separados del código principal

3. **✅ Ejemplos separados** → `examples/`
   - `preguntas.txt`, documentos de prueba
   - `demo_features.py` para demostraciones
   
4. **✅ Tests consolidados** → `tests/`
   - Todos los tests en un solo lugar
   - Mejor organización para pytest

5. **✅ .gitignore mejorado**
   - Ignora: `.venv/`, `Examenes_*/`, `*.log`, cache
   - Preserva: `examples/*.pdf`, `examples/*.docx`

---

## 🚀 PROPUESTAS DE MEJORA TÉCNICAS

### 1. 🏗️ Arquitectura de Código

#### Problema: Código monolítico en eg.py y qg.py
**Estado actual**: 785 líneas en eg.py, todas las funciones en un solo archivo

**Propuesta**: Modularización completa
```
examgenerator/
├── core/
│   ├── __init__.py
│   ├── question_loader.py      # load_questions_from_file()
│   ├── exam_generator.py       # generate_exam()
│   ├── shuffler.py              # Lógica de randomización
│   └── time_calculator.py      # calculate_exam_time()
├── exporters/
│   ├── __init__.py
│   ├── txt_exporter.py         # Exportación TXT
│   ├── docx_exporter.py        # Exportación DOCX
│   ├── excel_exporter.py       # create_answers_excel()
│   ├── csv_exporter.py         # create_answers_csv()
│   └── html_exporter.py        # create_answers_html()
├── ai/
│   ├── __init__.py
│   ├── gemini.py               # generate_questions_with_gemini()
│   ├── ollama.py               # generate_questions_with_ollama()
│   └── extractors.py           # extract_text_from_*()
```

**Ventajas**:
- ✅ Código más mantenible
- ✅ Tests más fáciles
- ✅ Reutilización entre eg.py y qg.py
- ✅ Separación de responsabilidades

**Prioridad**: 🔴 Alta

---

### 2. 📝 Sistema de Configuración

#### Problema: Parámetros hardcodeados en código

**Propuesta**: Archivo de configuración `config.yaml`
```yaml
# config.yaml
exam:
  default_format: "both"
  default_answers_format: "xlsx"
  minutes_per_question: 1.0
  
paths:
  output_dir: "Examenes_{prefix}"
  cache_dir: ".cache"
  templates_dir: "templates"
  
ai:
  gemini:
    default_model: "gemini-1.5-flash"
    max_tokens: 2048
  ollama:
    default_model: "llama2"
    url: "http://localhost:11434"
    
validation:
  min_questions_per_exam: 1
  max_questions_per_exam: 100
  max_file_size_mb: 50
```

**Implementación**:
```python
# examgenerator/config.py
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class ExamConfig:
    default_format: str = "both"
    default_answers_format: str = "xlsx"
    minutes_per_question: float = 1.0

@dataclass
class Config:
    exam: ExamConfig
    
    @classmethod
    def load(cls, config_file: Path = Path("config.yaml")):
        if not config_file.exists():
            return cls(exam=ExamConfig())  # Defaults
        
        with open(config_file, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return cls(
            exam=ExamConfig(**data.get('exam', {}))
        )
```

**Ventajas**:
- ✅ Configuración centralizada
- ✅ Fácil personalización por usuario
- ✅ Sin recompilar para cambios
- ✅ Defaults sensatos si no existe archivo

**Prioridad**: 🟡 Media

---

### 3. 🧪 Cobertura de Tests

#### Estado actual: 2 archivos de tests (validators, cache)

**Propuesta**: Suite completa de tests
```
tests/
├── __init__.py
├── conftest.py                 # Fixtures compartidos
├── unit/
│   ├── test_question_loader.py
│   ├── test_exam_generator.py
│   ├── test_shuffler.py
│   ├── test_validators.py
│   ├── test_cache.py
│   └── test_statistics.py
├── integration/
│   ├── test_eg_full_workflow.py
│   ├── test_qg_gemini.py
│   ├── test_qg_ollama.py
│   └── test_web_app.py
└── fixtures/
    ├── preguntas_test.txt
    ├── plantilla_test.docx
    └── documento_test.pdf
```

**Ejemplos de tests faltantes**:
```python
# tests/unit/test_question_loader.py
def test_load_questions_invalid_format():
    """Test que falla con formato incorrecto"""
    with pytest.raises(ValueError, match="Formato de ANSWER incorrecto"):
        load_questions_from_file("fixtures/invalid_format.txt")

def test_load_questions_missing_answer():
    """Test con pregunta sin ANSWER"""
    with pytest.raises(ValueError, match="sin una pregunta previa"):
        load_questions_from_file("fixtures/no_answer.txt")

# tests/integration/test_eg_full_workflow.py
def test_full_exam_generation_txt(tmp_path):
    """Test completo de generación TXT"""
    result = generate_exams(
        questions_file="fixtures/preguntas_test.txt",
        exam_prefix="Test",
        num_exams=2,
        questions_per_exam=5,
        export_format="txt",
        output_dir=tmp_path
    )
    
    assert (tmp_path / "examen_Test_1.txt").exists()
    assert (tmp_path / "examen_Test_2.txt").exists()
    assert (tmp_path / "respuestas_Test_completas.xlsx").exists()
```

**Objetivo**: >80% de cobertura de código

**Prioridad**: 🟡 Media-Alta

---

### 4. 📊 Logging Mejorado

#### Estado actual: Logging básico implementado

**Propuesta**: Logging estructurado con niveles
```python
# examgenerator/utils/logging_config.py (mejorado)
import logging
import json
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "message": record.getMessage(),
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)

# Uso
logger.info("Examen generado", extra={
    "exam_number": 1,
    "questions": 20,
    "format": "docx",
    "duration_ms": 1234
})
```

**Ventajas**:
- ✅ Logs parseables (JSON)
- ✅ Análisis y debugging más fácil
- ✅ Integración con herramientas de monitoreo
- ✅ Métricas de rendimiento

**Prioridad**: 🟢 Baja

---

### 5. 🔄 API REST (Opcional)

#### Propuesta: API REST además de interfaz web

**Implementación**:
```python
# examgenerator/api/routes.py
from flask import Blueprint, jsonify, request
from examgenerator.core.exam_generator import generate_exam
from examgenerator.utils.validators import validate_exam_params

api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/exams/generate', methods=['POST'])
def generate_exam_api():
    """
    POST /api/v1/exams/generate
    
    Body:
    {
        "questions_file": "path/to/questions.txt",
        "exam_prefix": "Parcial",
        "num_exams": 3,
        "questions_per_exam": 10,
        "format": "both"
    }
    
    Response:
    {
        "status": "success",
        "exams_generated": 3,
        "output_dir": "Examenes_Parcial",
        "files": ["examen_Parcial_1.txt", ...]
    }
    """
    data = request.json
    
    # Validar
    errors = validate_exam_params(data)
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400
    
    # Generar
    result = generate_exam(**data)
    
    return jsonify({
        "status": "success",
        **result
    })

@api.route('/questions/parse', methods=['POST'])
def parse_questions():
    """Parse y validate archivo de preguntas"""
    # ...

@api.route('/ai/generate', methods=['POST'])
def ai_generate_questions():
    """Generar preguntas con IA"""
    # ...
```

**Casos de uso**:
- ✅ Integración con otros sistemas
- ✅ Automatización CI/CD
- ✅ Clientes móviles/desktop
- ✅ Webhooks y triggers

**Prioridad**: 🟢 Baja (feature avanzada)

---

### 6. 🎨 Mejoras de Interfaz Web

#### Propuestas específicas:

**6.1 Drag & Drop para archivos**
```html
<!-- examgenerator/web/templates/generate_exams.html -->
<div class="dropzone" id="file-drop">
    <i class="icon-upload"></i>
    <p>Arrastra tu archivo de preguntas aquí</p>
    <p class="hint">o haz clic para seleccionar</p>
</div>

<script>
// JavaScript para drag & drop
const dropzone = document.getElementById('file-drop');

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('drag-over');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    handleFileUpload(files[0]);
});
</script>
```

**6.2 Preview de preguntas antes de generar**
```python
@app.route('/preview', methods=['POST'])
def preview_questions():
    """Vista previa de preguntas cargadas"""
    file = request.files['questions_file']
    
    # Parse temporal
    questions = load_questions_from_file(file)
    
    return jsonify({
        "total": len(questions),
        "preview": questions[:5],  # Primeras 5
        "stats": {
            "avg_options": avg_options(questions),
            "difficulty_dist": analyze_difficulty(questions)
        }
    })
```

**6.3 Descarga múltiple (ZIP)**
```python
@app.route('/download-all/<exam_prefix>')
def download_all_exams(exam_prefix):
    """Descargar todos los exámenes en ZIP"""
    import zipfile
    from io import BytesIO
    
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        exam_dir = f"Examenes_{exam_prefix}"
        for file in Path(exam_dir).iterdir():
            zip_file.write(file, file.name)
    
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'{exam_prefix}_exams.zip'
    )
```

**Prioridad**: 🟡 Media

---

### 7. 🔐 Seguridad y Validación

#### Mejoras propuestas:

**7.1 Validación de plantillas DOCX**
```python
def validate_docx_template(template_path: Path) -> dict:
    """Validar plantilla DOCX antes de usar"""
    errors = []
    warnings = []
    
    try:
        doc = Document(template_path)
    except Exception as e:
        errors.append(f"Archivo corrupto: {e}")
        return {"valid": False, "errors": errors}
    
    # Verificar placeholders
    text = "\n".join([p.text for p in doc.paragraphs])
    
    if "{{CONTENT}}" not in text and "{{QUESTIONS}}" not in text:
        warnings.append("No se encontró punto de inserción ({{CONTENT}} o {{QUESTIONS}})")
    
    # Verificar estilos personalizados
    style_names = [s.name for s in doc.styles]
    if 'Question' not in style_names:
        warnings.append("Estilo 'Question' no encontrado, se usará formato manual")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "placeholders_found": extract_placeholders(text)
    }
```

**7.2 Sanitización de nombres de archivo**
```python
def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """Sanitizar nombres de archivo para evitar problemas"""
    import unicodedata
    import re
    
    # Normalizar unicode
    filename = unicodedata.normalize('NFKD', filename)
    filename = filename.encode('ASCII', 'ignore').decode('ASCII')
    
    # Eliminar caracteres peligrosos
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limitar longitud
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        filename = name[:max_length - len(ext)] + ext
    
    return filename
```

**7.3 Rate limiting en web app**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/generate-exam', methods=['POST'])
@limiter.limit("10 per minute")
def generate_exam_route():
    # ...
```

**Prioridad**: 🔴 Alta (seguridad)

---

### 8. 📈 Performance y Escalabilidad

#### Propuestas:

**8.1 Generación paralela de exámenes**
```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def generate_exam_parallel(exam_number, exam_prefix, questions, num_questions, format):
    """Generar un examen (función independiente para multiprocessing)"""
    random.seed(f"{exam_prefix}_{exam_number}")
    # ... lógica de generación
    return result

def generate_multiple_exams_parallel(exam_prefix, num_exams, questions, 
                                     questions_per_exam, export_format):
    """Generar múltiples exámenes en paralelo"""
    max_workers = min(multiprocessing.cpu_count(), num_exams)
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(1, num_exams + 1):
            future = executor.submit(
                generate_exam_parallel,
                i, exam_prefix, questions, questions_per_exam, export_format
            )
            futures.append(future)
        
        results = [f.result() for f in futures]
    
    return results
```

**Ventajas**:
- ✅ Generación 2-4x más rápida para muchos exámenes
- ✅ Mejor uso de CPUs multi-core
- ✅ Escalable a cientos de exámenes

**8.2 Cache de documentos procesados**
```python
# Ya implementado QuestionCache, extender para documentos IA
class DocumentCache(QuestionCache):
    """Cache especializado para documentos procesados por IA"""
    
    def cache_extracted_text(self, doc_path: Path, text: str):
        """Cachear texto extraído de PDF/DOCX/PPTX"""
        cache_key = self._get_file_hash(doc_path)
        self.set(f"extracted_text_{cache_key}", text, ttl=86400)  # 24h
    
    def get_cached_text(self, doc_path: Path) -> Optional[str]:
        """Recuperar texto cacheado"""
        cache_key = self._get_file_hash(doc_path)
        return self.get(f"extracted_text_{cache_key}")
```

**Prioridad**: 🟡 Media

---

### 9. 🌍 Internacionalización (i18n)

#### Problema: Todo hardcodeado en español

**Propuesta**: Soporte multi-idioma
```python
# examgenerator/i18n/translations.py
TRANSLATIONS = {
    'es': {
        'exam_title': 'Examen',
        'question': 'Pregunta',
        'answer': 'Respuesta',
        'time_estimated': 'Tiempo estimado',
        'minutes': 'minutos',
        'hours': 'horas',
        # ...
    },
    'en': {
        'exam_title': 'Exam',
        'question': 'Question',
        'answer': 'Answer',
        'time_estimated': 'Estimated time',
        'minutes': 'minutes',
        'hours': 'hours',
        # ...
    },
    'ca': {
        'exam_title': 'Examen',
        'question': 'Pregunta',
        'answer': 'Resposta',
        # ...
    }
}

def t(key: str, lang: str = 'es') -> str:
    """Traducir clave"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['es']).get(key, key)

# Uso
title = t('exam_title', lang='en')  # "Exam"
```

**Archivos a internacionalizar**:
- Plantillas HTML
- Mensajes de error
- Logs al usuario
- Exportaciones TXT/DOCX

**Prioridad**: 🟢 Baja (nice-to-have)

---

### 10. 📱 Exportación a Formatos Adicionales

#### Propuestas:

**10.1 Export a PDF nativo**
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_exam_pdf(exam_content, output_file):
    """Crear examen en PDF con reportlab"""
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    
    y = height - inch
    for line in exam_content.split('\n'):
        c.drawString(inch, y, line)
        y -= 15
        
        if y < inch:  # Nueva página
            c.showPage()
            y = height - inch
    
    c.save()
```

**10.2 Export a Moodle XML**
```python
def create_moodle_xml(questions, output_file):
    """Exportar preguntas a formato Moodle XML"""
    import xml.etree.ElementTree as ET
    
    quiz = ET.Element('quiz')
    
    for q in questions:
        question = ET.SubElement(quiz, 'question', type='multichoice')
        
        name = ET.SubElement(question, 'name')
        text = ET.SubElement(name, 'text')
        text.text = q['question'][:50]  # Primeros 50 chars
        
        questiontext = ET.SubElement(question, 'questiontext', format='html')
        text = ET.SubElement(questiontext, 'text')
        text.text = f"<![CDATA[{q['question']}]]>"
        
        for i, option in enumerate(q['options']):
            answer = ET.SubElement(question, 'answer', 
                                  fraction='100' if i == q['correct_index'] else '0')
            text = ET.SubElement(answer, 'text')
            text.text = option
    
    tree = ET.ElementTree(quiz)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
```

**10.3 Export a Google Forms (API)**
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_google_form(questions, form_title):
    """Crear Google Form desde preguntas"""
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('forms', 'v1', credentials=creds)
    
    form = {
        "info": {
            "title": form_title,
        }
    }
    
    # Crear form
    result = service.forms().create(body=form).execute()
    form_id = result['formId']
    
    # Añadir preguntas
    requests = []
    for q in questions:
        requests.append({
            "createItem": {
                "item": {
                    "title": q['question'],
                    "questionItem": {
                        "question": {
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [{"value": opt} for opt in q['options']]
                            }
                        }
                    }
                },
                "location": {"index": len(requests)}
            }
        })
    
    service.forms().batchUpdate(
        formId=form_id,
        body={"requests": requests}
    ).execute()
    
    return f"https://docs.google.com/forms/d/{form_id}/edit"
```

**Prioridad**: 🟢 Baja (features avanzadas)

---

## 📦 PROPUESTAS DE PACKAGING

### 11. Distribución PyPI

**Propuesta**: Publicar en PyPI para instalación con pip/uv

```bash
# Instalación futura
uv pip install examgenerator

# O con pip
pip install examgenerator
```

**Preparación**:
```toml
# pyproject.toml (actualizado)
[project]
name = "examgenerator"
version = "11.20260111.1"
description = "Generador profesional de exámenes aleatorios con IA"
readme = "README.md"
authors = [{name = "TiiZss", email = "your-email@example.com"}]
license = {text = "GPL-3.0-or-later"}
keywords = ["exam", "generator", "education", "ai", "testing"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Education",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Education :: Testing",
]

[project.urls]
Homepage = "https://github.com/TiiZss/ExamGenerator"
Documentation = "https://github.com/TiiZss/ExamGenerator/blob/main/README.md"
Repository = "https://github.com/TiiZss/ExamGenerator"
"Bug Tracker" = "https://github.com/TiiZss/ExamGenerator/issues"

[project.scripts]
examgen = "examgenerator.cli:main"
examgen-web = "examgenerator.web.app:run"
examgen-ai = "examgenerator.ai.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**CLI moderno**:
```python
# examgenerator/cli.py
import click
from pathlib import Path

@click.group()
@click.version_option(version="11.20260111.1")
def main():
    """ExamGenerator - Generador profesional de exámenes"""
    pass

@main.command()
@click.argument('questions_file', type=click.Path(exists=True))
@click.argument('exam_prefix')
@click.option('--num-exams', '-n', default=1, help='Número de exámenes')
@click.option('--questions-per-exam', '-q', default=20, help='Preguntas por examen')
@click.option('--format', '-f', type=click.Choice(['txt', 'docx', 'both']), default='txt')
@click.option('--template', '-t', type=click.Path(exists=True), help='Plantilla DOCX')
def generate(questions_file, exam_prefix, num_exams, questions_per_exam, format, template):
    """Generar exámenes desde archivo de preguntas"""
    from examgenerator.core.generator import generate_exams
    
    click.echo(f"Generando {num_exams} exámenes...")
    
    result = generate_exams(
        questions_file=questions_file,
        exam_prefix=exam_prefix,
        num_exams=num_exams,
        questions_per_exam=questions_per_exam,
        export_format=format,
        template_path=template
    )
    
    click.secho(f"✓ Exámenes generados en: {result['output_dir']}", fg='green')

@main.command()
@click.option('--port', '-p', default=5000, help='Puerto web')
@click.option('--host', '-h', default='127.0.0.1', help='Host')
@click.option('--debug', is_flag=True, help='Modo debug')
def web(port, host, debug):
    """Iniciar interfaz web"""
    from examgenerator.web.app import app
    
    click.echo(f"Iniciando servidor en http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
```

**Uso tras instalación**:
```bash
# Generar exámenes
examgen generate preguntas.txt Parcial -n 3 -q 10

# Iniciar web
examgen-web

# Ayuda
examgen --help
```

**Prioridad**: 🟡 Media-Alta (visibilidad del proyecto)

---

### 12. Docker Support

**Propuesta**: Containerización para fácil deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Instalar UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY pyproject.toml requirements.txt ./
COPY examgenerator/ ./examgenerator/
COPY eg.py qg.py run_web.py ./
COPY examples/ ./examples/

# Instalar dependencias con UV
RUN uv venv .venv && \
    uv pip install -r requirements.txt

# Exponer puerto web
EXPOSE 5000

# Variable de entorno
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_API_KEY=""

# Comando por defecto
CMD ["uv", "run", "python", "run_web.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  examgenerator:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./examples:/app/examples
      - ./output:/app/output
      - ./templates:/app/templates
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    restart: unless-stopped

  # Opcional: Ollama para IA local
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

**Uso**:
```bash
# Build
docker build -t examgenerator .

# Run
docker run -p 5000:5000 -v $(pwd)/output:/app/output examgenerator

# Con docker-compose
docker-compose up -d
```

**Prioridad**: 🟢 Baja

---

## 🎯 ROADMAP PROPUESTO

### Fase 1: Estabilización (1-2 semanas)
- [x] Reorganización de carpetas ✅ HECHO
- [x] .gitignore mejorado ✅ HECHO
- [ ] Tests unitarios básicos (70% cobertura)
- [ ] Documentación actualizada con nuevas rutas
- [ ] CI/CD básico (GitHub Actions)

### Fase 2: Modularización (2-3 semanas)
- [ ] Separar eg.py en módulos (core/)
- [ ] Separar qg.py en módulos (ai/)
- [ ] Refactorizar exporters/
- [ ] Tests de integración

### Fase 3: Features (3-4 semanas)
- [ ] Sistema de configuración (config.yaml)
- [ ] Mejoras de interfaz web (drag & drop, preview)
- [ ] Validación mejorada de plantillas
- [ ] Cache de documentos IA

### Fase 4: Distribución (2 semanas)
- [ ] CLI moderno con Click
- [ ] Packaging para PyPI
- [ ] Docker & docker-compose
- [ ] Documentación completa

### Fase 5: Avanzado (opcional)
- [ ] API REST
- [ ] Generación paralela
- [ ] Exportación a Moodle/Google Forms
- [ ] Internacionalización

---

## 📊 MÉTRICAS DE CALIDAD PROPUESTAS

### Cobertura de Tests
- **Objetivo**: >80% de cobertura
- **Actual**: ~30% (solo validators y cache)

### Complejidad Ciclomática
- **Objetivo**: <10 por función
- **Actual**: eg.py tiene funciones >15

### Documentación
- **Objetivo**: 100% funciones públicas documentadas
- **Actual**: ~60%

### Tiempo de Generación
- **Objetivo**: <100ms por examen (sin DOCX)
- **Actual**: ~200ms

### Memory Usage
- **Objetivo**: <100MB para 100 exámenes
- **Actual**: No medido

---

## 🔧 HERRAMIENTAS RECOMENDADAS

### Development
- **Black**: Formateo automático de código
- **Ruff**: Linter ultra-rápido (sustituto de flake8)
- **MyPy**: Type checking estático
- **Pytest**: Framework de testing
- **Pytest-cov**: Cobertura de tests

### CI/CD
- **GitHub Actions**: Automatización (ya configurado en .github/)
- **Pre-commit hooks**: Validación antes de commits

### Monitoring (producción)
- **Sentry**: Error tracking
- **Prometheus**: Métricas
- **Grafana**: Dashboards

---

## 📝 CONCLUSIONES

### ✅ Completado
1. Reorganización completa de carpetas
2. .gitignore mejorado
3. Estructura profesional
4. Scripts organizados
5. Documentación centralizada

### 🎯 Prioridades Inmediatas
1. **Alta**: Modularización de eg.py y qg.py
2. **Alta**: Tests unitarios completos
3. **Alta**: Seguridad y validación mejoradas
4. **Media**: CLI moderno y packaging PyPI
5. **Media**: Mejoras de interfaz web

### 🚀 Impacto Esperado
- ✅ Código más mantenible (modularización)
- ✅ Menos bugs (tests extensivos)
- ✅ Instalación más fácil (PyPI)
- ✅ Mejor UX (interfaz web mejorada)
- ✅ Mayor seguridad (validaciones)
- ✅ Mejor performance (cache, paralelización)

---

**Próximos pasos**: Revisar propuestas con el equipo y priorizar según recursos disponibles.

**Contacto**: Abrir issues en GitHub para discutir implementación de propuestas específicas.

---

*Documento generado automáticamente el 11 de enero de 2026*
