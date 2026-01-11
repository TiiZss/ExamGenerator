"""
Tests básicos para validadores.
"""

import pytest
import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from examgenerator.utils.validators import (
    validate_positive_int,
    validate_export_format,
    validate_answers_format,
    sanitize_filename,
    ValidationError
)


def test_validate_positive_int():
    """Test validación de enteros positivos."""
    assert validate_positive_int("5", "test") == 5
    assert validate_positive_int("100", "test") == 100
    
    with pytest.raises(ValidationError):
        validate_positive_int("0", "test")
    
    with pytest.raises(ValidationError):
        validate_positive_int("-5", "test")
    
    with pytest.raises(ValidationError):
        validate_positive_int("abc", "test")


def test_validate_export_format():
    """Test validación de formatos de exportación."""
    assert validate_export_format("txt") == "txt"
    assert validate_export_format("TXT") == "txt"
    assert validate_export_format("docx") == "docx"
    assert validate_export_format("both") == "both"
    
    with pytest.raises(ValidationError):
        validate_export_format("pdf")
    
    with pytest.raises(ValidationError):
        validate_export_format("invalid")


def test_validate_answers_format():
    """Test validación de formatos de respuestas."""
    assert validate_answers_format("xlsx") == "xlsx"
    assert validate_answers_format("XLSX") == "xlsx"
    assert validate_answers_format("csv") == "csv"
    assert validate_answers_format("html") == "html"
    assert validate_answers_format("txt") == "txt"
    
    with pytest.raises(ValidationError):
        validate_answers_format("pdf")


def test_sanitize_filename():
    """Test sanitización de nombres de archivo."""
    # Caracteres normales
    assert sanitize_filename("test.txt") == "test.txt"
    
    # Caracteres peligrosos
    assert sanitize_filename("test<>:file.txt") == "test___file.txt"
    assert sanitize_filename("test/file.txt") == "test_file.txt"
    
    # Espacios múltiples
    assert sanitize_filename("test    file.txt") == "test file.txt"
    
    # Nombres reservados Windows
    assert sanitize_filename("CON") == "_CON"
    assert sanitize_filename("PRN") == "_PRN"
    assert sanitize_filename("con.txt") == "_con.txt"
    
    # Longitud máxima
    long_name = "a" * 300 + ".txt"
    sanitized = sanitize_filename(long_name, max_length=50)
    assert len(sanitized) <= 50
    assert sanitized.endswith(".txt")
    
    # Nombre vacío
    assert sanitize_filename("") == "unnamed"
    assert sanitize_filename("   ") == "unnamed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
