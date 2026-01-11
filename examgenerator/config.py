"""
Configuration management for ExamGenerator.
"""

import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class Config:
    """Configuration manager for ExamGenerator."""
    
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        """Singleton pattern - only one config instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration."""
        if not self._config:  # Load only once
            self.load_config()
    
    def load_config(self, config_path: Optional[str] = None):
        """Load configuration from YAML file.
        
        Args:
            config_path: Optional path to config file. If None, uses default locations.
        """
        if config_path is None:
            # Try default locations
            possible_paths = [
                Path('config.yaml'),
                Path('examgenerator') / 'config.yaml',
                Path.home() / '.examgenerator' / 'config.yaml',
            ]
            
            for path in possible_paths:
                if path.exists():
                    config_path = str(path)
                    break
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
                print(f"Configuración cargada desde: {config_path}")
            except Exception as e:
                print(f"Error al cargar configuración: {e}")
                self._load_defaults()
        else:
            print("Usando configuración por defecto")
            self._load_defaults()
    
    def _load_defaults(self):
        """Load default configuration values."""
        self._config = {
            'exam': {
                'default_time_per_question': 1,
                'option_letters': 'ABCD',
                'default_export_format': 'txt',
                'default_answers_format': 'txt'
            },
            'output': {
                'directory_prefix': 'Examenes_',
                'create_date_folders': False,
                'date_format': '%Y-%m-%d'
            },
            'docx': {
                'default_template': '',
                'fonts': {
                    'title_size': 16,
                    'question_size': 11,
                    'option_size': 10
                },
                'spacing': {
                    'title_after': 12,
                    'question_before': 6,
                    'question_after': 3,
                    'option_after': 2
                }
            },
            'ai': {
                'default_engine': 'gemini',
                'gemini': {
                    'default_model': 'gemini-1.5-flash',
                    'temperature': 0.7,
                    'timeout': 60
                },
                'ollama': {
                    'default_model': 'llama2',
                    'url': 'http://localhost:11434',
                    'timeout': 300,
                    'auto_start': True
                },
                'default_num_questions': 10,
                'default_language': 'español'
            },
            'logging': {
                'enabled': True,
                'level': 'INFO',
                'log_file': 'examgenerator.log',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'date_format': '%Y-%m-%d %H:%M:%S'
            },
            'validation': {
                'min_questions_per_exam': 1,
                'max_questions_per_exam': 100,
                'min_options': 2,
                'max_options': 8,
                'require_question_numbers': False
            },
            'performance': {
                'parallel_processing': False,
                'max_workers': 4,
                'cache_enabled': False,
                'cache_dir': '.cache'
            },
            'web': {
                'enabled': True,
                'host': '127.0.0.1',
                'port': 5000,
                'debug': False,
                'secret_key': 'change-this-secret-key-in-production'
            },
            'export': {
                'excel': {
                    'include_info': True,
                    'freeze_header': True
                },
                'html': {
                    'interactive': True,
                    'theme': 'light'
                },
                'csv': {
                    'delimiter': ',',
                    'quotechar': '"'
                }
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.
        
        Args:
            key: Configuration key in dot notation (e.g., 'exam.default_time_per_question')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
            
        Examples:
            >>> config = Config()
            >>> config.get('exam.default_time_per_question')
            1
            >>> config.get('ai.gemini.default_model')
            'gemini-1.5-flash'
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation.
        
        Args:
            key: Configuration key in dot notation
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, config_path: str = 'config.yaml'):
        """Save current configuration to YAML file.
        
        Args:
            config_path: Path to save configuration file
        """
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"Configuración guardada en: {config_path}")
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
    
    def reload(self, config_path: Optional[str] = None):
        """Reload configuration from file.
        
        Args:
            config_path: Optional path to config file
        """
        self._config = {}
        self.load_config(config_path)
    
    @property
    def all(self) -> Dict[str, Any]:
        """Get all configuration as dictionary."""
        return self._config.copy()


# Global config instance
config = Config()
