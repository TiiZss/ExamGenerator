"""
Sistema de caché para respuestas de IA.
"""

import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from ..utils.logging_config import get_logger

logger = get_logger('cache')


class QuestionCache:
    """Cache para evitar regenerar preguntas idénticas con IA."""
    
    def __init__(self, cache_dir: str = ".cache", ttl_days: int = 7):
        """
        Inicializa el sistema de caché.
        
        Args:
            cache_dir: Directorio para almacenar caché
            ttl_days: Tiempo de vida del caché en días
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl_seconds = ttl_days * 24 * 3600
        logger.debug(f"Cache inicializado en: {self.cache_dir.absolute()}")
    
    def _get_cache_key(
        self,
        text: str,
        num_questions: int,
        language: str,
        model: str,
        engine: str
    ) -> str:
        """
        Genera clave única para el contenido.
        
        Args:
            text: Texto del contenido
            num_questions: Número de preguntas
            language: Idioma
            model: Modelo de IA
            engine: Motor (gemini/ollama)
        
        Returns:
            Hash SHA256 del contenido
        """
        content = f"{text}{num_questions}{language}{model}{engine}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(
        self,
        text: str,
        num_questions: int,
        language: str,
        model: str,
        engine: str
    ) -> Optional[str]:
        """
        Obtiene preguntas cacheadas si existen y son válidas.
        
        Args:
            text: Texto del contenido
            num_questions: Número de preguntas
            language: Idioma
            model: Modelo de IA
            engine: Motor de IA
        
        Returns:
            Preguntas cacheadas o None si no existen/están expiradas
        """
        key = self._get_cache_key(text, num_questions, language, model, engine)
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            logger.debug("Caché no encontrado")
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar tiempo de vida
            age_seconds = time.time() - data['timestamp']
            if age_seconds > self.ttl_seconds:
                logger.info(f"Caché expirado ({age_seconds/3600:.1f}h), regenerando...")
                cache_file.unlink()  # Eliminar caché antiguo
                return None
            
            logger.info(f"⚡ Usando preguntas cacheadas ({age_seconds/3600:.1f}h de antigüedad)")
            return data['questions']
        
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Error leyendo caché: {e}")
            return None
    
    def set(
        self,
        text: str,
        num_questions: int,
        language: str,
        model: str,
        engine: str,
        questions: str
    ):
        """
        Guarda preguntas en caché.
        
        Args:
            text: Texto del contenido
            num_questions: Número de preguntas
            language: Idioma
            model: Modelo de IA
            engine: Motor de IA
            questions: Preguntas generadas
        """
        key = self._get_cache_key(text, num_questions, language, model, engine)
        cache_file = self.cache_dir / f"{key}.json"
        
        data = {
            'questions': questions,
            'timestamp': time.time(),
            'metadata': {
                'num_questions': num_questions,
                'language': language,
                'model': model,
                'engine': engine,
                'text_length': len(text)
            }
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug(f"Preguntas guardadas en caché: {cache_file.name}")
        except Exception as e:
            logger.error(f"Error guardando caché: {e}")
    
    def clear(self, older_than_days: Optional[int] = None):
        """
        Limpia archivos de caché.
        
        Args:
            older_than_days: Si se especifica, solo elimina archivos más antiguos
        """
        count = 0
        threshold = time.time() - (older_than_days * 24 * 3600) if older_than_days else 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            if older_than_days is None or cache_file.stat().st_mtime < threshold:
                cache_file.unlink()
                count += 1
        
        logger.info(f"Eliminados {count} archivos de caché")
    
    def stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del caché.
        
        Returns:
            Diccionario con estadísticas
        """
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'total_entries': len(cache_files),
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(self.cache_dir.absolute())
        }
