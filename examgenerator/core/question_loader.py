"""
Core module for question loading and parsing.
"""

import os
import re
from typing import List, Dict, Any, Union, TextIO
import io

def load_questions_from_stream(stream: TextIO) -> List[Dict[str, Union[str, List[str]]]]:
    """Load questions from a text stream (file-like object) and return parsed question data.
    
    Args:
        stream: Text stream (file-like object) containing questions
        
    Returns:
        List of question dictionaries
        
    Raises:
        ValueError: If format is invalid
    """
    questions_data: List[Dict[str, Any]] = []
    current_question: Dict[str, Any] = {}
    options: List[str] = []
    
    # Compile regex patterns once for better performance
    option_pattern = re.compile(r'^[A-D][).]\s')
    question_number_pattern = re.compile(r'^\d+\.\s*')

    # Ensure we are at the beginning
    if stream.seekable():
        stream.seek(0)
    
    for line_num, line_raw in enumerate(stream, 1):
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
                continue # Skip orphan options or raise error? Original raised error.
                # raise ValueError(f"Opción detectada sin una pregunta previa en línea {line_num}.")
            options.append(line[3:].strip())
            
        elif line.startswith('ANSWER:'):  # Answer line
            if 'question' not in current_question:
                continue
                # raise ValueError(f"Respuesta detectada sin una pregunta previa en línea {line_num}.")
            try:
                current_question['answer'] = line.split(':', 1)[1].strip()[0]
            except (IndexError, KeyError):
                pass 
                # raise ValueError(f"Formato de ANSWER incorrecto en línea {line_num}: '{line_raw.strip()}'")
                
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

def load_questions_from_file(filepath: str) -> List[Dict[str, Union[str, List[str]]]]:
    """Load questions from a text file (legacy wrapper)."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo '{filepath}' no se encontró.")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return load_questions_from_stream(f)

def validate_questions(questions: List[Dict]) -> bool:
    """Validate question structure."""
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
