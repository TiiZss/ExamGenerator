"""
TXT exporter for exam answers and exams.
"""

import os
from datetime import datetime
from typing import List, Dict


def create_answers_txt(all_exam_data: List[Dict], exam_prefix: str, output_dir: str, minutes_per_question: float = 1.0) -> None:
    """Create a TXT file with all exam answers (transposed layout)."""
    # Import time calculation function
    from ..core.time_calculator import calculate_exam_time
    
    max_questions = max(len(exam_data['answers']) for exam_data in all_exam_data)
    
    txt_content = f"RESPUESTAS DE EXÁMENES - {exam_prefix}\n"
    txt_content += "=" * 50 + "\n\n"
    
    # Create header
    header = "Examen".ljust(12)
    for i in range(1, max_questions + 1):
        header += f"P{i}".ljust(4)
    txt_content += header + "\n"
    txt_content += "-" * len(header) + "\n"
    
    # Add exam data
    for exam_data in all_exam_data:
        row = f"Examen {exam_data['exam_number']}".ljust(12)
        for question_idx in range(max_questions):
            if question_idx < len(exam_data['answers']):
                answer = exam_data['answers'][question_idx]
            else:
                answer = "-"
            row += answer.ljust(4)
        txt_content += row + "\n"
    
    # Add exam info
    txt_content += "\n" + "=" * 50 + "\n"
    txt_content += "INFORMACIÓN DEL EXAMEN\n"
    txt_content += "=" * 50 + "\n"
    txt_content += f"Nombre del examen: {exam_prefix}\n"
    txt_content += f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
    txt_content += f"Número de exámenes: {len(all_exam_data)}\n"
    txt_content += f"Preguntas por examen: {max_questions}\n"
    txt_content += f"Tiempo estimado: {calculate_exam_time(max_questions, minutes_per_question)}\n"
    
    # Write TXT file
    txt_filename = os.path.join(output_dir, f"respuestas_{exam_prefix}_completas.txt")
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    
    print(f"Archivo TXT creado: {txt_filename}")


def create_exam_txt(exam_content: str, exam_prefix: str, exam_number: int, output_dir: str) -> None:
    """Save exam as TXT file.
    
    Args:
        exam_content: Formatted exam content
        exam_prefix: Exam prefix (e.g., "Parcial", "Final")
        exam_number: Exam number
        output_dir: Output directory path
    """
    txt_filename = os.path.join(output_dir, f"examen_{exam_prefix}_{exam_number}.txt")
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(exam_content)
    print(f"Examen TXT creado: {txt_filename}")
