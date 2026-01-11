"""
Core module for question loading and parsing.
"""

import os
import re
from typing import List, Dict, Any


def load_questions_from_file(filepath: str) -> List[Dict[str, Any]]:
    """Load questions from a text file and return parsed question data.
    
    Args:
        filepath: Path to the questions file
        
    Returns:
        List of question dictionaries with 'question', 'options', and 'answer' keys
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is invalid
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo '{filepath}' no se encontró.")

    questions_data = []
    current_question = {}
    options = []
    
    # Compile regex patterns once for better performance
    option_pattern = re.compile(r'^[A-D][).]\s')
    question_number_pattern = re.compile(r'^\d+\.\s*')

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line_raw in enumerate(f, 1):
            line = line_raw.strip()
            
            if not line:  # Empty line - end of question block
                if current_question and options:
                    current_question['options'] = options
                    questions_data.append(current_question)
                    current_question, options = {}, []
                continue

            # Check line type
            if option_pattern.match(line):  # Option line
                if 'question' not in current_question:
                    raise ValueError(f"Opción detectada sin una pregunta previa en línea {line_num}.")
                options.append(line[3:].strip())
                
            elif line.startswith('ANSWER:'):  # Answer line
                if 'question' not in current_question:
                    raise ValueError(f"Respuesta detectada sin una pregunta previa en línea {line_num}.")
                try:
                    current_question['answer'] = line.split(':', 1)[1].strip()[0]
                except (IndexError, KeyError):
                    raise ValueError(f"Formato de ANSWER incorrecto en línea {line_num}: '{line_raw.strip()}'")
                    
            else:  # Question line
                # Save previous question if exists
                if current_question and options:
                    current_question['options'] = options
                    questions_data.append(current_question)
                
                # Clean question text
                question_text = question_number_pattern.sub('', line)
                current_question = {'question': question_text}
                options = []

    # Don't forget the last question
    if current_question and options:
        current_question['options'] = options
        questions_data.append(current_question)

    if not questions_data:
        raise ValueError("No se cargó ninguna pregunta. Verifica el formato del archivo.")

    return questions_data


def validate_questions(questions: List[Dict]) -> bool:
    """Validate question structure.
    
    Args:
        questions: List of question dictionaries
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    for i, q in enumerate(questions, 1):
        if 'question' not in q:
            raise ValueError(f"Pregunta {i} no tiene texto")
        if 'options' not in q or len(q['options']) < 2:
            raise ValueError(f"Pregunta {i} debe tener al menos 2 opciones")
        if 'answer' not in q:
            raise ValueError(f"Pregunta {i} no tiene respuesta")
        if q['answer'] not in 'ABCDEFGH':
            raise ValueError(f"Pregunta {i} tiene respuesta inválida: {q['answer']}")
    
    return True
