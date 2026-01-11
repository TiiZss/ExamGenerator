"""
Validadores para entrada de datos en ExamGenerator.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from ..utils.logging_config import get_logger

logger = get_logger('validators')


class ValidationError(Exception):
    """Error de validación personalizado."""
    pass


def validate_file_exists(file_path: str) -> Path:
    """
    Valida que un archivo existe.
    
    Args:
        file_path: Ruta al archivo
    
    Returns:
        Path object del archivo
    
    Raises:
        ValidationError: Si el archivo no existe
    """
    path = Path(file_path)
    if not path.exists():
        raise ValidationError(f"Archivo no encontrado: {file_path}")
    if not path.is_file():
        raise ValidationError(f"La ruta no es un archivo: {file_path}")
    return path


def validate_file_extension(
    file_path: str,
    allowed_extensions: List[str]
) -> Path:
    """
    Valida que un archivo tiene una extensión permitida.
    
    Args:
        file_path: Ruta al archivo
        allowed_extensions: Lista de extensiones permitidas (ej: ['.pdf', '.docx'])
    
    Returns:
        Path object del archivo
    
    Raises:
        ValidationError: Si la extensión no está permitida
    """
    path = validate_file_exists(file_path)
    ext = path.suffix.lower()
    
    if ext not in [e.lower() for e in allowed_extensions]:
        raise ValidationError(
            f"Extensión no soportada: {ext}. "
            f"Extensiones permitidas: {', '.join(allowed_extensions)}"
        )
    
    return path


def validate_file_size(
    file_path: str,
    max_size_mb: int = 50
) -> Path:
    """
    Valida que un archivo no excede el tamaño máximo.
    
    Args:
        file_path: Ruta al archivo
        max_size_mb: Tamaño máximo en MB
    
    Returns:
        Path object del archivo
    
    Raises:
        ValidationError: Si el archivo es demasiado grande
    """
    path = validate_file_exists(file_path)
    size_mb = path.stat().st_size / (1024 * 1024)
    
    if size_mb > max_size_mb:
        raise ValidationError(
            f"Archivo demasiado grande: {size_mb:.1f}MB. "
            f"Máximo permitido: {max_size_mb}MB"
        )
    
    logger.debug(f"Tamaño del archivo: {size_mb:.2f}MB")
    return path


def validate_question_data(question: Dict) -> bool:
    """
    Valida la estructura de una pregunta.
    
    Args:
        question: Diccionario con datos de la pregunta
    
    Returns:
        True si es válida
    
    Raises:
        ValidationError: Si la pregunta tiene formato inválido
    """
    required_fields = ['question', 'options', 'answer']
    
    # Verificar campos requeridos
    for field in required_fields:
        if field not in question:
            raise ValidationError(f"Pregunta inválida: falta campo '{field}'")
    
    # Validar pregunta no vacía
    if not question['question'].strip():
        raise ValidationError("La pregunta no puede estar vacía")
    
    # Validar opciones
    if not isinstance(question['options'], list):
        raise ValidationError("Las opciones deben ser una lista")
    
    if len(question['options']) < 2:
        raise ValidationError("La pregunta debe tener al menos 2 opciones")
    
    if len(question['options']) > 10:
        raise ValidationError("La pregunta no puede tener más de 10 opciones")
    
    # Validar respuesta
    valid_answers = [chr(65 + i) for i in range(len(question['options']))]  # A, B, C, D...
    if question['answer'] not in valid_answers:
        raise ValidationError(
            f"Respuesta inválida: {question['answer']}. "
            f"Debe ser una de: {', '.join(valid_answers)}"
        )
    
    return True


def validate_questions_file(file_path: str) -> Path:
    """
    Valida un archivo de preguntas.
    
    Args:
        file_path: Ruta al archivo de preguntas
    
    Returns:
        Path object del archivo
    
    Raises:
        ValidationError: Si el archivo es inválido
    """
    path = validate_file_exists(file_path)
    
    # Leer contenido
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        raise ValidationError("El archivo debe estar codificado en UTF-8")
    
    if not content.strip():
        raise ValidationError("El archivo de preguntas está vacío")
    
    # Validar que tenga al menos una pregunta
    if 'ANSWER:' not in content:
        raise ValidationError(
            "El archivo no parece contener preguntas con el formato esperado. "
            "Debe incluir 'ANSWER:' para cada pregunta"
        )
    
    logger.debug(f"Archivo de preguntas validado: {path}")
    return path


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Sanitiza un nombre de archivo.
    
    Args:
        filename: Nombre de archivo original
        max_length: Longitud máxima permitida
    
    Returns:
        Nombre de archivo sanitizado
    """
    # Remover caracteres peligrosos
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)
    
    # Remover espacios múltiples y al inicio/fin
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    # Limitar longitud
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        filename = name[:max_length-len(ext)] + ext
    
    # Evitar nombres reservados en Windows
    reserved = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
                'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    
    base_name = os.path.splitext(filename)[0].upper()
    if base_name in reserved:
        filename = f"_{filename}"
    
    return filename or "unnamed"


def validate_positive_int(value: str, name: str) -> int:
    """
    Valida que un string sea un entero positivo.
    
    Args:
        value: Valor a validar
        name: Nombre del parámetro (para mensajes de error)
    
    Returns:
        Valor entero
    
    Raises:
        ValidationError: Si no es un entero positivo válido
    """
    try:
        int_value = int(value)
    except ValueError:
        raise ValidationError(f"{name} debe ser un número entero, recibido: {value}")
    
    if int_value <= 0:
        raise ValidationError(f"{name} debe ser mayor que 0, recibido: {int_value}")
    
    return int_value


def validate_export_format(format_str: str) -> str:
    """
    Valida el formato de exportación.
    
    Args:
        format_str: Formato solicitado
    
    Returns:
        Formato validado
    
    Raises:
        ValidationError: Si el formato no es válido
    """
    valid_formats = ['txt', 'docx', 'both']
    format_lower = format_str.lower()
    
    if format_lower not in valid_formats:
        raise ValidationError(
            f"Formato inválido: {format_str}. "
            f"Formatos válidos: {', '.join(valid_formats)}"
        )
    
    return format_lower


def validate_answers_format(format_str: str) -> str:
    """
    Valida el formato de archivo de respuestas.
    
    Args:
        format_str: Formato solicitado
    
    Returns:
        Formato validado
    
    Raises:
        ValidationError: Si el formato no es válido
    """
    valid_formats = ['xlsx', 'csv', 'html', 'txt']
    format_lower = format_str.lower()
    
    if format_lower not in valid_formats:
        raise ValidationError(
            f"Formato de respuestas inválido: {format_str}. "
            f"Formatos válidos: {', '.join(valid_formats)}"
        )
    
    return format_lower
