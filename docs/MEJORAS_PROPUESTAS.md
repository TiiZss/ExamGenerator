# 🚀 Propuestas de Mejora para ExamGenerator

## 📊 Análisis Completo del Proyecto

Después de analizar exhaustivamente el código, documentación y estructura del proyecto, he identificado mejoras en varias categorías.

---

## 🎯 MEJORAS CRÍTICAS (Alta Prioridad)

### 1. **Limpiar Conflictos de Merge en eg.py**
**Problema**: El archivo eg.py todavía contiene marcadores de conflicto de merge
```python
<<<<<<< HEAD
# código...
=======
# código...
>>>>>>> da6a17fb926a5a85bd4d383ef80408fcec706452
```

**Solución**: Limpiar completamente el archivo, elegir la versión correcta.

**Impacto**: ⚠️ CRÍTICO - El código no debería tener conflictos sin resolver en producción.

---

### 2. **Sistema de Logging Profesional**
**Problema Actual**: Uso extensivo de `print()` en todo el código (100+ ocurrencias)

**Propuesta**:
```python
import logging

# En cada módulo
logger = logging.getLogger(__name__)

# Configuración
def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('examgenerator.log'),
            logging.StreamHandler()
        ]
    )

# Uso
logger.info("✅ Texto extraído exitosamente")
logger.error("❌ Error al leer el PDF")
logger.debug("Detalles técnicos...")
```

**Beneficios**:
- Niveles de verbosidad configurables
- Logs persistentes para debugging
- Mejor trazabilidad de errores
- Separación de output de usuario vs logs técnicos

---

### 3. **Validación y Sanitización de Datos**
**Problema**: Falta validación robusta de entrada del usuario

**Propuestas**:
```python
# En qg.py - validar archivo de entrada
def validate_input_file(file_path: str, allowed_extensions: List[str]) -> bool:
    """Valida que el archivo existe y tiene extensión permitida."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError(f"Extensión no soportada: {ext}. Use: {', '.join(allowed_extensions)}")
    
    # Validar tamaño (evitar archivos enormes)
    max_size = 50 * 1024 * 1024  # 50MB
    if os.path.getsize(file_path) > max_size:
        raise ValueError(f"Archivo demasiado grande (>50MB)")
    
    return True

# En eg.py - validar formato de preguntas
def validate_question_data(question: Dict) -> bool:
    """Valida estructura de una pregunta."""
    required_fields = ['question', 'options', 'answer']
    
    for field in required_fields:
        if field not in question:
            raise ValueError(f"Pregunta inválida: falta campo '{field}'")
    
    if len(question['options']) < 2:
        raise ValueError("Pregunta debe tener al menos 2 opciones")
    
    if question['answer'] not in ['A', 'B', 'C', 'D']:
        raise ValueError(f"Respuesta inválida: {question['answer']}")
    
    return True
```

---

## 💡 MEJORAS DE FUNCIONALIDAD (Media Prioridad)

### 4. **Caché de Respuestas de IA**
**Propuesta**: Evitar regenerar preguntas para el mismo contenido

```python
import hashlib
import json
from pathlib import Path

class QuestionCache:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_key(self, text: str, num_questions: int, language: str, model: str) -> str:
        """Genera clave única para el contenido."""
        content = f"{text}{num_questions}{language}{model}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[str]:
        """Obtiene preguntas cacheadas."""
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Verificar si no es muy antiguo (7 días)
                if time.time() - data['timestamp'] < 7 * 24 * 3600:
                    return data['questions']
        return None
    
    def set(self, key: str, questions: str):
        """Guarda preguntas en caché."""
        cache_file = self.cache_dir / f"{key}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                'questions': questions,
                'timestamp': time.time()
            }, f, ensure_ascii=False, indent=2)

# Uso en qg.py
cache = QuestionCache()
cache_key = cache.get_cache_key(text_content, num_questions, language, model_name)
cached = cache.get(cache_key)

if cached:
    print("⚡ Usando preguntas cacheadas")
    return cached

questions = generate_questions_with_ollama(...)
cache.set(cache_key, questions)
```

**Beneficios**:
- Ahorro de tiempo y recursos
- Consistencia en resultados
- Opción de `--no-cache` para forzar regeneración

---

### 5. **Generación de Preguntas en Formato Estructurado**
**Problema**: qg.py genera texto plano, no formato compatible con eg.py

**Propuesta**: Generar directamente en formato `preguntas.txt`

```python
def format_questions_for_exam(ai_response: str) -> str:
    """
    Convierte respuesta de IA en formato preguntas.txt.
    Usa prompt mejorado que pide formato específico.
    """
    prompt = f"""
    Genera exactamente {num_questions} preguntas de opción múltiple.
    
    FORMATO REQUERIDO (ejemplo):
    ¿Pregunta aquí?
    A) Opción 1
    B) Opción 2
    C) Opción 3
    D) Opción 4
    ANSWER: B)
    
    (línea en blanco entre preguntas)
    
    IMPORTANTE:
    - Siempre 4 opciones (A, B, C, D)
    - Una línea en blanco entre cada pregunta
    - ANSWER: seguido de letra y paréntesis
    
    Texto base:
    {text_content}
    """
    
    # Generar y validar formato
    response = generate_questions(prompt)
    
    # Validar que tiene el formato correcto
    if not validate_question_format(response):
        logger.warning("Formato incorrecto, intentando corregir...")
        response = fix_question_format(response)
    
    return response

# Agregar opción para guardar directamente
parser.add_argument("--output", type=str, 
                   help="Guardar preguntas en archivo (formato eg.py)")

if args.output:
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(formatted_questions)
    print(f"✅ Preguntas guardadas en {args.output}")
    print("💡 Ahora puedes usar: python eg.py {args.output} ...")
```

---

### 6. **Modo Interactivo para Editar Preguntas Generadas**
**Propuesta**: Editor simple en terminal para revisar/corregir preguntas de IA

```python
def interactive_question_editor(questions_text: str) -> str:
    """Editor interactivo para revisar preguntas."""
    questions = parse_questions(questions_text)
    
    for i, q in enumerate(questions, 1):
        clear_screen()
        print(f"\n📝 Pregunta {i}/{len(questions)}")
        print("="*60)
        print(f"\n{q['question']}")
        for opt in q['options']:
            print(f"  {opt}")
        print(f"\nRespuesta correcta: {q['answer']}")
        print("="*60)
        
        print("\nOpciones:")
        print("  [Enter] - Aceptar y continuar")
        print("  [e] - Editar pregunta")
        print("  [d] - Eliminar pregunta")
        print("  [q] - Guardar y salir")
        
        choice = input("\n> ").strip().lower()
        
        if choice == 'e':
            q['question'] = input("Nueva pregunta: ")
            # Editar opciones...
        elif choice == 'd':
            questions.remove(q)
        elif choice == 'q':
            break
    
    return format_questions(questions)

# Agregar opción
parser.add_argument("--interactive", action="store_true",
                   help="Modo interactivo para editar preguntas")
```

---

### 7. **Soporte para Imágenes en Exámenes**
**Propuesta**: Permitir preguntas con imágenes en DOCX

```python
# En eg.py - extender formato de preguntas.txt
"""
¿Qué muestra la imagen?
IMAGE: diagrama.png
A) Opción 1
B) Opción 2
C) Opción 3
D) Opción 4
ANSWER: A)
"""

def add_image_to_docx(doc, image_path: str, width_inches=3):
    """Añade imagen al documento."""
    if os.path.exists(image_path):
        doc.add_picture(image_path, width=Inches(width_inches))
    else:
        doc.add_paragraph(f"[IMAGEN NO ENCONTRADA: {image_path}]")

# En generate_exam: detectar IMAGE: en preguntas
if 'image' in q_data:
    add_image_to_docx(exam_doc, q_data['image'])
```

---

### 8. **Estadísticas y Análisis de Exámenes**
**Propuesta**: Generar informe de estadísticas

```python
def generate_exam_statistics(all_exam_data: List[Dict]) -> Dict:
    """Genera estadísticas sobre los exámenes generados."""
    stats = {
        'total_exams': len(all_exam_data),
        'total_questions': sum(len(e['answers']) for e in all_exam_data),
        'answer_distribution': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
        'question_reuse': {},  # Cuántas veces se usó cada pregunta
        'difficulty_balance': None  # Si tuviéramos niveles de dificultad
    }
    
    for exam in all_exam_data:
        for answer in exam['answers']:
            stats['answer_distribution'][answer] += 1
        
        for q in exam['questions']:
            q_id = q['question']
            stats['question_reuse'][q_id] = stats['question_reuse'].get(q_id, 0) + 1
    
    # Analizar balance
    total_answers = sum(stats['answer_distribution'].values())
    for letter in stats['answer_distribution']:
        percentage = (stats['answer_distribution'][letter] / total_answers) * 100
        stats['answer_distribution'][letter] = {
            'count': stats['answer_distribution'][letter],
            'percentage': round(percentage, 2)
        }
    
    return stats

def print_statistics(stats: Dict):
    """Imprime estadísticas de forma visual."""
    print("\n📊 ESTADÍSTICAS DE GENERACIÓN")
    print("="*60)
    print(f"Total de exámenes: {stats['total_exams']}")
    print(f"Total de preguntas: {stats['total_questions']}")
    print("\nDistribución de respuestas correctas:")
    for letter, data in stats['answer_distribution'].items():
        bar = '█' * int(data['percentage'] / 2)
        print(f"  {letter}) {bar} {data['percentage']}% ({data['count']})")
    
    # Advertencias
    if any(d['percentage'] < 15 or d['percentage'] > 35 for d in stats['answer_distribution'].values()):
        print("\n⚠️  ADVERTENCIA: Distribución de respuestas desbalanceada")
        print("   Considera revisar las preguntas para mejor balance")

# Agregar al final de main() en eg.py
stats = generate_exam_statistics(all_exam_data)
print_statistics(stats)
save_statistics_to_file(stats, output_dir)
```

---

## 🏗️ MEJORAS DE ARQUITECTURA

### 9. **Refactorizar en Módulos**
**Problema**: eg.py tiene 1572 líneas, difícil de mantener

**Propuesta**:
```
examgenerator/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── question_loader.py      # load_questions_from_file
│   ├── exam_generator.py       # generate_exam, shuffle logic
│   └── validators.py            # validate_args, validate_question_data
├── exporters/
│   ├── __init__.py
│   ├── txt_exporter.py
│   ├── docx_exporter.py         # Todo lo de DOCX
│   ├── excel_exporter.py
│   ├── csv_exporter.py
│   └── html_exporter.py
├── ai/
│   ├── __init__.py
│   ├── gemini_client.py
│   ├── ollama_client.py
│   └── text_extractors.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_config.py
│   └── cache.py
└── cli/
    ├── __init__.py
    ├── eg_cli.py                # CLI para eg
    └── qg_cli.py                # CLI para qg
```

**Beneficios**:
- Código más mantenible
- Tests más fáciles
- Reutilización de componentes
- Separación de responsabilidades

---

### 10. **Configuración Centralizada**
**Propuesta**: Archivo de configuración

```python
# config.py
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    # Paths
    cache_dir: Path = Path(".cache")
    output_base_dir: Path = Path("Examenes")
    
    # AI
    ollama_url: str = "http://localhost:11434"
    ollama_timeout: int = 300
    ollama_default_model: str = "llama2"
    gemini_default_model: str = "gemini-1.5-flash"
    
    # Exam generation
    default_minutes_per_question: float = 1.0
    max_questions_per_exam: int = 100
    
    # File processing
    max_file_size_mb: int = 50
    allowed_pdf_extensions: List[str] = ['.pdf']
    allowed_docx_extensions: List[str] = ['.docx']
    allowed_pptx_extensions: List[str] = ['.pptx']
    
    # Export
    default_export_format: str = 'txt'
    default_answers_format: str = 'xlsx'
    
    @classmethod
    def from_file(cls, config_file: str = "config.yaml"):
        """Carga configuración desde archivo YAML."""
        if Path(config_file).exists():
            import yaml
            with open(config_file) as f:
                data = yaml.safe_load(f)
            return cls(**data)
        return cls()

# Uso
config = Config.from_file()
```

---

## 🧪 MEJORAS DE TESTING

### 11. **Suite de Tests Automatizados**
**Propuesta**: Tests con pytest

```python
# tests/test_question_loader.py
import pytest
from examgenerator.core.question_loader import load_questions_from_file

def test_load_valid_questions(tmp_path):
    """Test carga de preguntas válidas."""
    questions_file = tmp_path / "test.txt"
    questions_file.write_text("""
¿Pregunta de prueba?
A) Opción 1
B) Opción 2
C) Opción 3
D) Opción 4
ANSWER: A)
    """, encoding='utf-8')
    
    questions = load_questions_from_file(str(questions_file))
    assert len(questions) == 1
    assert questions[0]['question'] == '¿Pregunta de prueba?'
    assert len(questions[0]['options']) == 4
    assert questions[0]['answer'] == 'A'

def test_load_invalid_format():
    """Test error con formato inválido."""
    with pytest.raises(ValueError):
        load_questions_from_file("nonexistent.txt")

# tests/test_ollama_client.py
def test_check_ollama_running(monkeypatch):
    """Test detección de Ollama."""
    # Mock requests
    ...

# Ejecutar tests
# pytest tests/ -v --cov=examgenerator
```

**Archivos de test**:
- `tests/test_question_loader.py`
- `tests/test_exam_generator.py`
- `tests/test_exporters.py`
- `tests/test_ai_clients.py`
- `tests/test_validators.py`

---

## 🎨 MEJORAS DE UX

### 12. **Barra de Progreso**
**Propuesta**: Feedback visual para operaciones largas

```python
from tqdm import tqdm

# En eg.py - al generar múltiples exámenes
for i in tqdm(range(1, num_exams + 1), desc="Generando exámenes"):
    random.seed(f"{exam_prefix}_{i}")
    # ... generar examen

# En qg.py - al procesar documento largo
for page in tqdm(reader.pages, desc="Extrayendo texto"):
    text += page.extract_text() or ""
```

---

### 13. **Modo Verboso/Silencioso**
**Propuesta**: Control de output

```python
parser.add_argument("-v", "--verbose", action="store_true",
                   help="Modo verboso con detalles técnicos")
parser.add_argument("-q", "--quiet", action="store_true",
                   help="Modo silencioso, solo errores")

# Ajustar logging según flags
if args.quiet:
    logging.getLogger().setLevel(logging.ERROR)
elif args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
```

---

### 14. **Modo Preview/Dry-Run**
**Propuesta**: Ver qué se generaría sin crear archivos

```python
parser.add_argument("--dry-run", action="store_true",
                   help="Mostrar qué se generaría sin crear archivos")

if args.dry_run:
    print("\n🔍 MODO PREVIEW - No se crearán archivos\n")
    print(f"Se generarían:")
    print(f"  - {num_exams} exámenes en formato {export_format}")
    print(f"  - Carpeta: Examenes_{exam_prefix}/")
    print(f"  - Archivo de respuestas: {answers_format}")
    print(f"  - {num_questions_per_exam} preguntas por examen")
    print(f"  - Tiempo estimado: {exam_time}")
    sys.exit(0)
```

---

## 🔒 MEJORAS DE SEGURIDAD

### 15. **Sanitización de Nombres de Archivo**
**Mejora**: La función actual es buena, pero se puede mejorar

```python
def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """Sanitiza nombre de archivo de forma más robusta."""
    # Remover caracteres peligrosos
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)
    
    # Remover espacios múltiples y al inicio/fin
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    # Limitar longitud
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        filename = name[:max_length-len(ext)] + ext
    
    # Evitar nombres reservados en Windows
    reserved = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'LPT1']
    if filename.upper() in reserved:
        filename = f"_{filename}"
    
    return filename or "unnamed"
```

---

### 16. **Validación de Tamaño de Archivos**
**Propuesta**: Evitar procesar archivos masivos

```python
def check_file_size(file_path: str, max_size_mb: int = 50):
    """Verifica que el archivo no sea demasiado grande."""
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > max_size_mb:
        raise ValueError(
            f"Archivo demasiado grande: {size_mb:.1f}MB. "
            f"Máximo permitido: {max_size_mb}MB"
        )
```

---

## ⚡ MEJORAS DE PERFORMANCE

### 17. **Generación Paralela de Exámenes**
**Propuesta**: Usar multiprocessing para generar múltiples exámenes

```python
from multiprocessing import Pool
from functools import partial

def generate_single_exam_wrapper(args):
    """Wrapper para multiprocessing."""
    exam_num, exam_prefix, questions_data, num_questions, export_format = args
    random.seed(f"{exam_prefix}_{exam_num}")
    return generate_exam(exam_num, exam_prefix, questions_data, num_questions, export_format)

# En main()
if num_exams > 5:  # Solo para muchos exámenes
    print("🚀 Generación paralela activada...")
    with Pool() as pool:
        exam_args = [
            (i, exam_prefix, questions_data, questions_per_exam, export_format)
            for i in range(1, num_exams + 1)
        ]
        results = pool.map(generate_single_exam_wrapper, exam_args)
```

---

### 18. **Lazy Loading de Dependencias**
**Propuesta**: Importar solo lo necesario

```python
# En lugar de importar todo al inicio
def export_to_excel(data, output_dir):
    """Exporta a Excel con lazy import."""
    try:
        import openpyxl
        from openpyxl.styles import Font, Alignment
        # ... resto del código
    except ImportError:
        raise ImportError("Instala openpyxl: pip install openpyxl")

# Similar para docx, etc.
```

---

## 📚 MEJORAS DE DOCUMENTACIÓN

### 19. **Docstrings Completos con Type Hints**
**Mejora**: Muchas funciones tienen buenos docstrings, pero agregar ejemplos

```python
def generate_exam(
    exam_number: int,
    exam_name_prefix: str,
    all_questions: List[Dict[str, Any]],
    num_questions_per_exam: int,
    export_format: str = 'txt'
) -> Tuple[str, str, List[Dict], List[str]]:
    """
    Genera un examen individual con preguntas aleatorias.
    
    Args:
        exam_number: Número del examen (1, 2, 3, ...)
        exam_name_prefix: Prefijo para el nombre (ej: "Parcial")
        all_questions: Lista de todas las preguntas disponibles
        num_questions_per_exam: Cuántas preguntas incluir
        export_format: Formato de salida ('txt', 'docx', 'both')
    
    Returns:
        Tupla con:
        - exam_content: Contenido del examen en texto
        - answers_content: Contenido de respuestas en texto
        - selected_questions: Lista de preguntas seleccionadas
        - exam_answers: Lista de respuestas correctas
    
    Example:
        >>> questions = load_questions_from_file("preguntas.txt")
        >>> exam, answers, selected, answers_list = generate_exam(
        ...     1, "Parcial", questions, 10, "txt"
        ... )
        >>> print(f"Generado examen con {len(selected)} preguntas")
        Generado examen con 10 preguntas
    
    Notes:
        - Usa random.seed() para reproducibilidad
        - Las opciones se mezclan aleatoriamente
        - La respuesta correcta se ajusta al nuevo orden
    """
```

---

### 20. **Tutorial Interactivo**
**Propuesta**: Script guiado para nuevos usuarios

```python
# tutorial.py
def run_tutorial():
    """Tutorial interactivo para nuevos usuarios."""
    print("🎓 TUTORIAL DE EXAMGENERATOR")
    print("="*60)
    
    print("\n¿Qué deseas hacer?")
    print("1. Generar exámenes desde un archivo de preguntas existente")
    print("2. Crear preguntas usando IA desde un documento")
    print("3. Ver ejemplos completos")
    print("4. Configurar Ollama")
    
    choice = input("\nElige una opción (1-4): ").strip()
    
    if choice == "1":
        tutorial_generate_exams()
    elif choice == "2":
        tutorial_ai_questions()
    elif choice == "3":
        show_examples()
    elif choice == "4":
        tutorial_ollama_setup()

# python tutorial.py
```

---

## 🆕 NUEVAS FUNCIONALIDADES

### 21. **Exportar a PDF**
**Propuesta**: Generar PDFs directamente

```python
def export_to_pdf(exam_content: str, output_path: str):
    """Exporta examen a PDF."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        
        c = canvas.Canvas(output_path, pagesize=letter)
        # ... generar PDF
        c.save()
    except ImportError:
        logger.error("Instala reportlab: pip install reportlab")
```

---

### 22. **Integración con Google Forms**
**Propuesta**: Exportar exámenes a Google Forms

```python
def export_to_google_forms(questions: List[Dict], form_title: str):
    """Crea un Google Form con las preguntas."""
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    
    # ... código para crear form
```

---

### 23. **Modo de Autoevaluación**
**Propuesta**: Generar examen para que el estudiante se autoevalúe

```python
# Generar HTML interactivo con JavaScript
def create_interactive_exam(questions: List[Dict], output_file: str):
    """Crea examen HTML interactivo con auto-corrección."""
    html = """
    <html>
    <head><title>Autoevaluación</title></head>
    <body>
        <div id="exam">...</div>
        <script>
        function checkAnswers() {
            // Validar respuestas y mostrar resultados
        }
        </script>
    </body>
    </html>
    """
    # Guardar HTML
```

---

### 24. **Niveles de Dificultad**
**Propuesta**: Clasificar preguntas por dificultad

```python
# En preguntas.txt
"""
¿Pregunta fácil?
DIFFICULTY: easy
A) ...
ANSWER: A)

¿Pregunta difícil?
DIFFICULTY: hard
A) ...
ANSWER: C)
"""

# Al generar examen
parser.add_argument("--difficulty", choices=['easy', 'medium', 'hard', 'mixed'],
                   help="Nivel de dificultad del examen")

# Filtrar preguntas según dificultad
def filter_by_difficulty(questions, difficulty):
    if difficulty == 'mixed':
        return questions
    return [q for q in questions if q.get('difficulty') == difficulty]
```

---

### 25. **Banco de Preguntas con Tags**
**Propuesta**: Organizar preguntas por temas

```python
# preguntas.txt
"""
¿Pregunta sobre redes?
TAGS: redes, seguridad, tcp/ip
A) ...
ANSWER: A)
"""

# Generar examen temático
parser.add_argument("--tags", nargs="+",
                   help="Filtrar preguntas por tags")

# python eg.py preguntas.txt Parcial 3 10 --tags redes seguridad
```

---

## 🔧 MEJORAS TÉCNICAS MENORES

### 26. **requirements.txt más específico**
```txt
# Actual
python-docx>=1.1.0

# Mejorado con versiones exactas probadas
python-docx==1.1.0  # Específico
openpyxl==3.1.2
google-generativeai==0.3.2
pypdf==3.17.1
python-pptx==0.6.23
requests==2.31.0

# Dev dependencies (separar)
pytest==7.4.3
pytest-cov==4.1.0
black==23.12.0
mypy==1.7.1
```

---

### 27. **Pre-commit Hooks**
**Propuesta**: Automatizar checks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
```

---

### 28. **GitHub Actions para CI/CD**
```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

---

## 📈 PRIORIZACIÓN DE MEJORAS

### Implementar AHORA (P0):
1. ✅ Limpiar conflictos de merge en eg.py
2. ✅ Sistema de logging profesional
3. ✅ Validación robusta de datos

### Próxima Versión (P1):
4. ✅ Generación en formato compatible
5. ✅ Caché de respuestas IA
6. ✅ Refactorizar en módulos
7. ✅ Suite de tests

### Futuro (P2):
8. ✅ Imágenes en exámenes
9. ✅ Estadísticas y análisis
10. ✅ Exportación a PDF
11. ✅ Niveles de dificultad

### Opcional (P3):
12. ✅ Google Forms
13. ✅ Modo autoevaluación
14. ✅ Sistema de tags

---

## 💰 ESTIMACIÓN DE ESFUERZO

| Mejora | Tiempo Estimado | Complejidad |
|--------|-----------------|-------------|
| Limpiar merge conflicts | 30 min | Baja |
| Sistema de logging | 2-3 horas | Media |
| Validación de datos | 3-4 horas | Media |
| Caché de IA | 4-5 horas | Media-Alta |
| Formato compatible qg→eg | 5-6 horas | Alta |
| Refactorización modular | 2-3 días | Alta |
| Suite de tests completa | 3-5 días | Alta |
| Exportación PDF | 4-6 horas | Media |

---

## 🎯 RECOMENDACIÓN FINAL

**Plan de 3 fases**:

### Fase 1 (1 semana): Estabilización
- Limpiar merge conflicts
- Implementar logging
- Añadir validaciones
- Tests básicos

### Fase 2 (2 semanas): Funcionalidad
- Caché de IA
- Formato compatible qg→eg
- Estadísticas
- Refactorización parcial

### Fase 3 (3 semanas): Expansión
- Refactorización completa
- Tests exhaustivos
- Nuevas funcionalidades (PDF, dificultad, tags)
- Documentación completa

---

**Total estimado**: 6-8 semanas para implementar todas las mejoras prioritarias.

**Retorno**: Proyecto más robusto, mantenible, con mejor UX y más funcionalidades.
