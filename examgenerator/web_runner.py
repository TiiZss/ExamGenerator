"""
Script para iniciar la aplicación web de ExamGenerator.
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path si es necesario
# sys.path.insert(0, str(Path(__file__).parent))

from examgenerator.web.app import app
from examgenerator.utils.logging_config import setup_logging


def run_app(host='0.0.0.0', port=5000, debug=False):
    """
    Función principal para iniciar la aplicación web.
    
    Args:
        host: Host donde correr el servidor
        port: Puerto donde escuchar
        debug: Modo debug
    """
    # Configurar logging
    setup_logging(verbose=debug, log_file='webapp.log')
    
    # Iniciar servidor
    app.run(debug=debug, host=host, port=port)


def main():
    # Configurar logging
    setup_logging(verbose=False, log_file='webapp.log')
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              📝 ExamGenerator Web Interface                  ║
    ║                   Version 13.20260114                        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🚀 Iniciando servidor web...
    🌐 Abre tu navegador en: http://localhost:5000
    
    ⚡ Características disponibles:
       • Generar exámenes desde archivo de preguntas
       • Generar preguntas con IA (Gemini/Ollama)
       • Caché inteligente de respuestas
       • Estadísticas en tiempo real
    
    💡 Presiona Ctrl+C para detener el servidor
    """)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n✅ Servidor detenido correctamente")

if __name__ == '__main__':
    main()
