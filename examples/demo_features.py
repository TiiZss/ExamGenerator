"""
Script de ejemplo para demostrar todas las funcionalidades nuevas de v11.
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from examgenerator.utils.logging_config import setup_logging, get_logger
from examgenerator.utils.validators import (
    validate_positive_int,
    validate_export_format,
    sanitize_filename,
    ValidationError
)
from examgenerator.utils.cache import QuestionCache
from examgenerator.utils.statistics import generate_exam_statistics, print_statistics


def demo_logging():
    """Demuestra el sistema de logging."""
    print("\n" + "="*60)
    print("🔍 DEMO: Sistema de Logging")
    print("="*60)
    
    # Configurar logging
    setup_logging(verbose=True, log_file='demo.log')
    logger = get_logger('demo')
    
    logger.debug("Mensaje de DEBUG (solo en modo verbose)")
    logger.info("Mensaje de INFO (predeterminado)")
    logger.warning("Mensaje de WARNING")
    logger.error("Mensaje de ERROR")
    logger.critical("Mensaje de CRITICAL")
    
    print("\n✅ Logs también guardados en logs/demo.log")


def demo_validators():
    """Demuestra el sistema de validación."""
    print("\n" + "="*60)
    print("✅ DEMO: Sistema de Validación")
    print("="*60)
    
    logger = get_logger('demo')
    
    # Validar entero positivo
    try:
        num = validate_positive_int("10", "número de exámenes")
        logger.info(f"Validación exitosa: {num} exámenes")
    except ValidationError as e:
        logger.error(f"Error de validación: {e}")
    
    # Validar formato
    try:
        fmt = validate_export_format("docx")
        logger.info(f"Formato válido: {fmt}")
    except ValidationError as e:
        logger.error(f"Error de validación: {e}")
    
    # Sanitizar nombre
    original = "Mi Examen <Final> 2024.docx"
    sanitized = sanitize_filename(original)
    logger.info(f"Nombre sanitizado: {original} → {sanitized}")


def demo_cache():
    """Demuestra el sistema de caché."""
    print("\n" + "="*60)
    print("⚡ DEMO: Sistema de Caché")
    print("="*60)
    
    logger = get_logger('demo')
    cache = QuestionCache(cache_dir=".demo_cache")
    
    # Simular texto y preguntas
    text = "Contenido del documento de prueba..."
    questions = """
    ¿Pregunta de prueba?
    A) Opción 1
    B) Opción 2
    C) Opción 3
    D) Opción 4
    ANSWER: B)
    """
    
    # Guardar en caché
    cache.set(text, 10, "español", "gemini-1.5-flash", "gemini", questions)
    logger.info("Preguntas guardadas en caché")
    
    # Recuperar de caché
    cached = cache.get(text, 10, "español", "gemini-1.5-flash", "gemini")
    if cached:
        logger.info("⚡ Preguntas recuperadas del caché")
    
    # Estadísticas
    stats = cache.stats()
    logger.info(f"Estadísticas del caché: {stats['total_entries']} entradas, "
                f"{stats['total_size_mb']:.2f} MB")
    
    # Limpiar
    cache.clear()
    logger.info("Caché limpiado")


def demo_statistics():
    """Demuestra el sistema de estadísticas."""
    print("\n" + "="*60)
    print("📊 DEMO: Sistema de Estadísticas")
    print("="*60)
    
    # Datos simulados de exámenes
    all_exam_data = [
        {
            'exam_number': 1,
            'questions': [
                {'question': '¿Pregunta 1?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'A'},
                {'question': '¿Pregunta 2?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'B'},
                {'question': '¿Pregunta 3?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'C'},
            ],
            'answers': ['A', 'B', 'C']
        },
        {
            'exam_number': 2,
            'questions': [
                {'question': '¿Pregunta 1?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'C'},
                {'question': '¿Pregunta 4?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'D'},
                {'question': '¿Pregunta 5?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'A'},
            ],
            'answers': ['C', 'D', 'A']
        },
    ]
    
    # Generar estadísticas
    stats = generate_exam_statistics(all_exam_data)
    
    # Mostrar estadísticas
    print_statistics(stats)


def main():
    """Ejecuta todas las demos."""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         📝 ExamGenerator v11 - Demo de Funcionalidades       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        demo_logging()
        demo_validators()
        demo_cache()
        demo_statistics()
        
        print("\n" + "="*60)
        print("✨ DEMO COMPLETADO")
        print("="*60)
        print("""
        Funcionalidades demostradas:
          ✅ Sistema de logging con colores e iconos
          ✅ Validaciones robustas de datos
          ✅ Caché inteligente de preguntas
          ✅ Estadísticas y análisis de exámenes
        
        Para más información:
          📚 README.md
          📝 CHANGELOG.md
          🚀 QUICK_START_V11.md
          💡 MEJORAS_PROPUESTAS.md
        
        ¡Prueba la interfaz web!
          python run_web.py
        """)
    
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
