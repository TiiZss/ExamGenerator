"""
Sistema de logging profesional para ExamGenerator.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class ColoredFormatter(logging.Formatter):
    """Formateador con colores para la consola."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'
    }
    
    ICONS = {
        'DEBUG': '🔍',
        'INFO': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨'
    }
    
    def format(self, record):
        """Formatea el registro con color e icono."""
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            icon = self.ICONS.get(record.levelname, '')
            record.levelname = f"{color}{icon} {record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logging(
    verbose: bool = False,
    quiet: bool = False,
    log_file: Optional[str] = None,
    log_dir: str = "logs"
) -> logging.Logger:
    """
    Configura el sistema de logging.
    
    Args:
        verbose: Modo verboso (DEBUG level)
        quiet: Modo silencioso (solo ERRORS)
        log_file: Nombre del archivo de log (opcional)
        log_dir: Directorio para logs
    
    Returns:
        Logger configurado
    """
    # Determinar nivel de logging
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    # Crear logger raíz
    logger = logging.getLogger('examgenerator')
    logger.setLevel(logging.DEBUG)  # Capturar todo, filtrar por handler
    
    # Limpiar handlers existentes
    logger.handlers.clear()
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Formato para consola (más simple)
    console_format = ColoredFormatter(
        '%(levelname)s %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # Handler para archivo (si se especifica)
    if log_file:
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_path / log_file,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Formato para archivo (más detallado)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger hijo con el nombre especificado.
    
    Args:
        name: Nombre del módulo
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(f'examgenerator.{name}')
