"""
Directory and file management utilities.
"""

import os
import re


def sanitize_folder_name(name: str) -> str:
    """Sanitize a folder name to remove invalid characters.
    
    Args:
        name: Raw folder name
        
    Returns:
        Sanitized folder name safe for all filesystems
    """
    return re.sub(r'[<>:"/\\|?*]', '_', name)


def create_output_directory(exam_prefix: str) -> str:
    """Create output directory for exams.
    
    Args:
        exam_prefix: Prefix for exam (e.g., "Parcial", "Final")
        
    Returns:
        Path to created directory
    """
    folder_name = f"Examenes_{sanitize_folder_name(exam_prefix)}"
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    return folder_name
