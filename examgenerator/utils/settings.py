"""
Gestor de configuración persistente para ExamGenerator.
"""

import json
import os
from pathlib import Path
from typing import Optional

SETTINGS_FILE = Path("/app/config/settings.json")

def get_settings() -> dict:
    """Obtiene la configuración actual."""
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_settings(settings: dict) -> bool:
    """Guarda la configuración."""
    try:
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
        return True
    except IOError as e:
        print(f"Error guardando configuración: {e}")
        return False

def get_gemini_api_key() -> Optional[str]:
    """
    Obtiene la API key de Gemini.
    Prioridad: 1) settings.json, 2) variable de entorno
    """
    # Primero intentar desde settings.json
    settings = get_settings()
    api_key = settings.get('gemini_api_key')
    
    if api_key:
        return api_key
    
    # Fallback a variable de entorno
    return os.environ.get('GOOGLE_API_KEY')

def set_gemini_api_key(api_key: str) -> bool:
    """Guarda la API key de Gemini."""
    settings = get_settings()
    settings['gemini_api_key'] = api_key
    return save_settings(settings)

def get_ollama_url() -> str:
    """
    Obtiene la URL de Ollama.
    Prioridad: 1) settings.json, 2) variable de entorno, 3) default host.docker.internal
    """
    settings = get_settings()
    url = settings.get('ollama_url')
    
    if url:
        return url
        
    return os.environ.get('OLLAMA_URL', 'http://host.docker.internal:11434')

def set_ollama_url(url: str) -> bool:
    """Guarda la URL de Ollama."""
    settings = get_settings()
    settings['ollama_url'] = url
    return save_settings(settings)
