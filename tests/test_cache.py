"""
Tests básicos para sistema de caché.
"""

import pytest
import sys
import tempfile
import shutil
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from examgenerator.utils.cache import QuestionCache


@pytest.fixture
def temp_cache_dir():
    """Crea directorio temporal para tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_cache_set_and_get(temp_cache_dir):
    """Test guardar y recuperar del caché."""
    cache = QuestionCache(cache_dir=temp_cache_dir, ttl_days=7)
    
    text = "Texto de prueba para generar preguntas"
    questions = "Pregunta 1?\nA) Opción 1\nB) Opción 2\nANSWER: A)"
    
    # Guardar en caché
    cache.set(text, 10, "español", "gemini-1.5-flash", "gemini", questions)
    
    # Recuperar del caché
    cached_questions = cache.get(text, 10, "español", "gemini-1.5-flash", "gemini")
    
    assert cached_questions == questions


def test_cache_miss(temp_cache_dir):
    """Test cuando no hay caché disponible."""
    cache = QuestionCache(cache_dir=temp_cache_dir)
    
    result = cache.get("texto diferente", 5, "english", "llama2", "ollama")
    
    assert result is None


def test_cache_stats(temp_cache_dir):
    """Test estadísticas del caché."""
    cache = QuestionCache(cache_dir=temp_cache_dir)
    
    # Agregar algunas entradas
    for i in range(3):
        cache.set(f"texto_{i}", 10, "español", "gemini", "gemini", f"preguntas_{i}")
    
    stats = cache.stats()
    
    assert stats['total_entries'] == 3
    assert stats['total_size_mb'] > 0
    assert 'cache_dir' in stats


def test_cache_clear(temp_cache_dir):
    """Test limpieza de caché."""
    cache = QuestionCache(cache_dir=temp_cache_dir)
    
    # Agregar entradas
    cache.set("texto1", 10, "español", "gemini", "gemini", "preguntas1")
    cache.set("texto2", 10, "español", "gemini", "gemini", "preguntas2")
    
    # Limpiar todo
    cache.clear()
    
    stats = cache.stats()
    assert stats['total_entries'] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
