"""
Aplicación web Flask para ExamGenerator.
"""

from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for, Response
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from functools import wraps
import os
import sys
import requests
from pathlib import Path
import tempfile
import shutil
from datetime import datetime

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from examgenerator.utils.logging_config import setup_logging, get_logger
from examgenerator.utils.validators import (
    validate_file_extension, validate_file_size, ValidationError
)
from examgenerator.utils.cache import QuestionCache
from examgenerator.utils.statistics import generate_exam_statistics, print_statistics
from examgenerator.utils.settings import get_settings, save_settings, get_gemini_api_key, set_gemini_api_key
from examgenerator.config import config as app_config

# Import modular functions
from examgenerator.core.question_loader import load_questions_from_file, validate_questions
from examgenerator.core.exam_generator import generate_exam
from examgenerator.exporters.txt_exporter import create_exam_txt, create_answers_txt
from examgenerator.exporters.excel_exporter import create_answers_excel
from examgenerator.exporters.docx_exporter import create_exam_docx

logger = get_logger('web')

# Crear aplicación Flask
# Crear aplicación Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Initialize CSRF Protection
csrf = CSRFProtect(app)

# Basic Auth Configuration
BASIC_AUTH_USER = os.environ.get('BASIC_AUTH_USER')
BASIC_AUTH_PASS = os.environ.get('BASIC_AUTH_PASS')

def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username == BASIC_AUTH_USER and password == BASIC_AUTH_PASS

def authenticate():
    """Sends a 401 response that enables basic auth."""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not BASIC_AUTH_USER or not BASIC_AUTH_PASS:
            # If auth not configured, skip (or fail secure? let's fail secure if prod)
            if app.config['ENV'] == 'production':
                 return Response("Server Misconfiguration: Auth credentials not set.", 500)
            return f(*args, **kwargs)

        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Apply auth globally to all routes except health check (if exists) or static
@app.before_request
def require_login():
    if request.endpoint == 'static': 
        return
    # Exclude health check if you have one
    if request.endpoint == 'health_check':
        return
    
    # We apply auth manually here instead of decorator on every route
    if not BASIC_AUTH_USER or not BASIC_AUTH_PASS:
        # Auth disabled if no credentials set
        return

    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

# Rutas absolutas basadas en la ubicación de app.py
BASE_DIR = Path(__file__).parent.absolute()
app.config['UPLOAD_FOLDER'] = str(BASE_DIR / 'uploads')
app.config['OUTPUT_FOLDER'] = str(BASE_DIR / 'outputs')

# Crear directorios
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)

logger.info(f"UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")
logger.info(f"OUTPUT_FOLDER: {app.config['OUTPUT_FOLDER']}")

# Configurar logging
setup_logging(verbose=False, log_file='webapp.log')

# Inicializar caché
cache = QuestionCache()


@app.route('/')
def index():
    """Página principal."""
    from examgenerator.utils.counter import get_exam_count
    total_exams = get_exam_count()
    return render_template('index.html', total_exams=total_exams)


@app.route('/generate-exams', methods=['GET', 'POST'])
def generate_exams():
    """Generar exámenes desde archivo de preguntas."""
    if request.method == 'GET':
        return render_template(
            'generate_exams.html',
            default_time_per_question=app_config.get('exam.default_time_per_question', 1)
        )
    
    try:
        # Obtener archivo de preguntas
        if 'questions_file' not in request.files:
            flash('No se proporcionó archivo de preguntas', 'error')
            return redirect(url_for('generate_exams'))
        
        file = request.files['questions_file']
        if not file or not file.filename or file.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('generate_exams'))
        
        # Validar extensión manualmente ya que no guardamos archivo
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext != '.txt':
            flash('Solo se permiten archivos .txt', 'error')
            return redirect(url_for('generate_exams'))

        # Leer archivo en memoria
        # Flask FileStorage stream está en memoria o temp file, pero es seekable
        import io
        stream = io.TextIOWrapper(file.stream._file, encoding='utf-8') if hasattr(file.stream, '_file') else io.TextIOWrapper(file.stream, encoding='utf-8')
        
        # Obtener parámetros
        exam_prefix = request.form.get('exam_prefix', 'Examen')
        num_exams = int(request.form.get('num_exams', 1))
        questions_per_exam = int(request.form.get('questions_per_exam', 10))
        export_format = request.form.get('export_format', 'txt')
        minutes_per_question = float(request.form.get(
            'minutes_per_question',
            app_config.get('exam.default_time_per_question', 1)
        ))
        if minutes_per_question <= 0:
            minutes_per_question = 1
        
        # Manejar plantilla DOCX si se subió
        template_path = None
        use_template = request.form.get('use_template') == 'on'
        
        if use_template and 'template_file' in request.files:
            template_file = request.files['template_file']
            if template_file and template_file.filename:
                # Plantillas necesitamos guardarlas temporalmente porque docx-mailmerge/others suelen pedir path
                # O podemos intentar streams si el exporter lo soporta. Revisemos docx_exporter luego.
                # Por ahora, para templates mantendremos temp file por compatibilidad de librerías de terceros (python-docx-template)
                # Ojo: el usuario pidió 'ficheros' (general), asumamos input principal.
                # Pero intentemos secure temp file
                import tempfile
                t_ext = os.path.splitext(template_file.filename)[1]
                t_fd, t_path = tempfile.mkstemp(suffix=t_ext)
                os.close(t_fd)
                template_file.save(t_path)
                template_path = t_path
        
        # Cargar preguntas usando API modular desde stream
        from examgenerator.core.question_loader import load_questions_from_stream
        questions_data = load_questions_from_stream(stream)
        
        # Crear directorio de salida
        output_dir = Path(app.config['OUTPUT_FOLDER']) / f"Examenes_{exam_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar exámenes
        try:
            all_exam_data = []
            
            for i in range(1, num_exams + 1):
                # Set deterministic random seed
                seed = f"{exam_prefix}_{i}"
                
                # Generate exam using modular API
                exam_questions, exam_answers = generate_exam(
                    questions_data,
                    questions_per_exam,
                    seed
                )
                
                all_exam_data.append({
                    'exam_number': i,
                    'questions': exam_questions,
                    'answers': list(exam_answers.values())
                })
                
                # Guardar archivos TXT
                if export_format in ['txt', 'both']:
                    # Create exam content
                    exam_content = f"--- EXAMEN {exam_prefix} {i} ---\n\n"
                    option_letters = ['A', 'B', 'C', 'D']
                    
                    for q in exam_questions:
                        exam_content += f"{q['number']}. {q['question']}\n"
                        for j, option in enumerate(q['options']):
                            exam_content += f"   {option_letters[j]}) {option}\n"
                        exam_content += "\n"
                    
                    # Save exam file using exporter
                    create_exam_txt(exam_content, exam_prefix, i, str(output_dir))
                
                # Guardar archivos DOCX
                if export_format in ['docx', 'both']:
                    create_exam_docx(
                        exam_prefix, 
                        i, 
                        exam_questions, 
                        str(output_dir),
                        str(template_path) if template_path else None,
                        minutes_per_question
                    )
            
            # Generar archivo de respuestas usando exporter
            create_answers_excel(all_exam_data, exam_prefix, str(output_dir), minutes_per_question)
            
            # Generar estadísticas
            stats = generate_exam_statistics(all_exam_data)
            
            # Incrementar contador persistente
            try:
                from examgenerator.utils.counter import increment_exam_count
                increment_exam_count(num_exams)
            except Exception as e:
                logger.error(f"Error incrementing counter: {e}")
                
            flash(f'¡Éxito! Se generaron {num_exams} exámenes en: {output_dir}', 'success')
            
        except Exception as e:
            flash(f'Error generando exámenes: {str(e)}', 'error')
            logger.error(f"Error generation: {e}")
            return redirect(url_for('generate_exams'))
            
        # Comprimir archivos
        import zipfile
        zip_filename = f"{output_dir.name}.zip"
        zip_path = (output_dir.parent / zip_filename).absolute()
        
        logger.info(f"Creando ZIP: {zip_path}")
        logger.info(f"Tipo de zip_path: {type(zip_path)}")
        logger.info(f"Desde directorio: {output_dir}")
        logger.info(f"output_dir es absoluto: {output_dir.is_absolute()}")
        
        with zipfile.ZipFile(str(zip_path), 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in output_dir.rglob('*'):
                if file.is_file():
                    # Añadir archivo con path relativo al directorio de output
                    arcname = file.relative_to(output_dir.parent)
                    logger.info(f"Añadiendo al ZIP: {arcname}")
                    zipf.write(str(file), str(arcname))
        
        if not zip_path.exists():
            raise FileNotFoundError(f"No se pudo crear el archivo ZIP: {zip_path}")
        
        logger.info(f"ZIP creado exitosamente: {zip_path} ({zip_path.stat().st_size} bytes)")
        logger.info(f"ZIP existe: {zip_path.exists()}")
        logger.info(f"ZIP path absoluto final: {zip_path.absolute()}")
        flash(f'✅ Generados {num_exams} exámenes correctamente', 'success')
        
        return send_file(str(zip_path), as_attachment=True, download_name=zip_filename)
    
    except Exception as e:
        logger.error(f"Error generando exámenes: {e}", exc_info=True)
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('generate_exams'))


@app.route('/generate-questions', methods=['GET', 'POST'])
def generate_questions():
    """Generar preguntas con IA."""
    if request.method == 'GET':
        # Verificar si Gemini está disponible
        gemini_available = False
        try:
            import qg
            api_key = qg.get_gemini_api_key()
            gemini_available = bool(api_key)
        except:
            gemini_available = False
        
        return render_template('generate_questions.html', gemini_available=gemini_available)
    
    try:
        # Obtener archivo
        if 'document' not in request.files:
            flash('No se proporcionó documento', 'error')
            return redirect(url_for('generate_questions'))
        
        file = request.files['document']
        if not file or not file.filename or file.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('generate_questions'))
        
        # Procesar archivo en memoria
        filename = secure_filename(file.filename)
        ext = Path(filename).suffix.lower()
        
        if ext not in ['.pdf', '.docx', '.pptx']:
            flash('Formato de archivo no soportado (use PDF, DOCX, PPTX)', 'error')
            return redirect(url_for('generate_questions'))

        # Importar qg.py functions
        import qg
        import io
        
        # Leer a BytesIO
        file_stream = io.BytesIO(file.read())
        
        # Extraer texto
        if ext == '.pdf':
            text_content = qg.extract_text_from_pdf(file_stream)
        elif ext == '.docx':
            text_content = qg.extract_text_from_docx(file_stream)
        elif ext == '.pptx':
            text_content = qg.extract_text_from_pptx(file_stream)
        else:
            flash('Formato no soportado', 'error')
            return redirect(url_for('generate_questions'))
        
        if not text_content or not text_content.strip():
            flash('No se pudo extraer texto del documento', 'error')
            return redirect(url_for('generate_questions'))
        
        # Verificar caché
        questions = None
        if use_cache and text_content:
            questions = cache.get(text_content, num_questions, language, model, engine)
        
        # Generar preguntas si no hay caché
        if questions is None:
            if engine == 'gemini':
                questions = qg.generate_questions_with_gemini(
                    text_content=text_content,
                    num_questions=num_questions,
                    language=language,
                    model_name=model
                )
            else:
                # Ollama en modo no-interactivo para web
                import os
                ollama_url = os.getenv('OLLAMA_URL', 'http://ollama:11434')
                
                questions = qg.generate_questions_with_ollama(
                    text_content=text_content,
                    num_questions=num_questions,
                    language=language,
                    model_name=model,
                    ollama_url=ollama_url,
                    interactive=False
                )
            
            # Guardar en caché
            if use_cache and questions and text_content:
                cache.set(text_content, num_questions, language, model, engine, questions)
        
        # Validar que se generaron preguntas
        if questions is None:
            error_msg = f"No se pudieron generar preguntas con {engine}."
            if engine == 'ollama':
                error_msg += f" Verifica que el modelo '{model}' esté descargado. "
                error_msg += f"Descárgalo con: <code>ollama pull {model}</code>"
            else:
                error_msg += " Verifica tu API key de Gemini."
            
            flash(error_msg, 'error')
            return redirect(url_for('generate_questions'))
        
        # Guardar resultado
        output_file = Path(app.config['OUTPUT_FOLDER']) / f"preguntas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(questions)
        
        flash(f'✅ Generadas {num_questions} preguntas con {engine}', 'success')
        return send_file(str(output_file), as_attachment=True)
    
    except Exception as e:
        logger.error(f"Error generando preguntas: {e}", exc_info=True)
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('generate_questions'))


@app.route('/cache/stats')
def cache_stats():
    """Estadísticas del caché."""
    stats = cache.stats()
    return jsonify(stats)


@app.route('/api/ollama/models')
def ollama_models():
    """Obtener lista de modelos disponibles en Ollama."""
    try:
        import requests
        ollama_url = os.getenv('OLLAMA_URL', 'http://ollama:11434')
        
        # Intentar obtener modelos de Ollama
        response = requests.get(f"{ollama_url}/api/tags", timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            return jsonify({
                'success': True,
                'models': models,
                'count': len(models)
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Ollama respondió con código {response.status_code}',
                'models': []
            })
    
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': 'No se puede conectar a Ollama. ¿Está corriendo el servicio?',
            'models': []
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'models': []
        })


@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Limpiar caché."""
    older_than_days = request.form.get('older_than_days', type=int)
    cache.clear(older_than_days)
    flash('Caché limpiado correctamente', 'success')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Página de configuración."""
    if request.method == 'POST':
        # Guardar API key de Gemini
        gemini_api_key = request.form.get('gemini_api_key', '').strip()
        
        if gemini_api_key:
            if set_gemini_api_key(gemini_api_key):
                flash('✅ API Key de Gemini guardada correctamente', 'success')
            else:
                flash('❌ Error al guardar la API Key', 'error')
        else:
            flash('⚠️ La API Key no puede estar vacía', 'error')
        
        return redirect(url_for('settings'))
    
    # GET: Mostrar configuración actual
    current_key = get_gemini_api_key()
    return render_template('settings.html', current_key=current_key or '')


@app.route('/settings/test-api-key', methods=['POST'])
def test_api_key():
    """Probar API key de Gemini."""
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'success': False, 'error': 'API key vacía'})
        
        # Probar la API key listando modelos
        import google.generativeai as genai
        genai.configure(api_key=api_key)  # type: ignore
        
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]  # type: ignore
        
        return jsonify({
            'success': True,
            'models': models[:10],
            'count': len(models)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.errorhandler(413)
def too_large(e):
    """Error de archivo demasiado grande."""
    flash('Archivo demasiado grande (máximo 50MB)', 'error')
    return redirect(url_for('index')), 413


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
