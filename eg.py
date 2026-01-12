#!/usr/bin/env python3
"""
ExamGenerator - Generador avanzado de exámenes aleatorios
Version 12.0 - Arquitectura Modular

Genera exámenes únicos con preguntas y respuestas barajadas.
Exporta a TXT, DOCX, Excel, CSV, HTML.
"""

import os
import sys
import random
from typing import List, Dict, Tuple, Optional

# Import from modular architecture
from examgenerator.core import (
    load_questions_from_file,
    validate_questions,
    create_output_directory,
    calculate_exam_time,
    generate_exam
)
from examgenerator.exporters import (
    create_exam_txt,
    create_exam_docx,
    create_answers_txt,
    create_answers_excel,
    create_answers_csv,
    create_answers_html
)


def validate_args(args: List[str]) -> Tuple[str, str, int, int, str, Optional[str], str, float]:
    """Validate and parse command line arguments.
    
    Args:
        args: Command line arguments (sys.argv)
        
    Returns:
        Tuple of (questions_file, exam_prefix, num_exams, questions_per_exam, 
                  export_format, template_path, answers_format, minutes_per_question)
                  
    Raises:
        ValueError: If arguments are invalid
    """
    if len(args) < 5:
        print("Uso: python eg.py <archivo_preguntas> <prefijo_examen> <num_examenes> <preguntas_por_examen> [formato] [plantilla] [formato_respuestas] [minutos_por_pregunta]")
        print("\nArgumentos:")
        print("  archivo_preguntas      : Archivo .txt con las preguntas")
        print("  prefijo_examen         : Prefijo para los exámenes (ej: Parcial, Final)")
        print("  num_examenes           : Cantidad de exámenes a generar")
        print("  preguntas_por_examen   : Número de preguntas por examen")
        print("  [formato]              : Formato de salida (txt, docx, both) - por defecto: txt")
        print("  [plantilla]            : Archivo de plantilla DOCX (opcional)")
        print("  [formato_respuestas]   : Formato del archivo de respuestas (xlsx, csv, txt, html) - por defecto: xlsx")
        print("  [minutos_por_pregunta] : Minutos asignados por pregunta (puede ser decimal) - por defecto: 1")
        print("\nEjemplos:")
        print("  python eg.py preguntas.txt Parcial 3 10")
        print("  python eg.py preguntas.txt Final 5 20 both")
        print("  python eg.py preguntas.txt Parcial 2 15 docx plantilla.docx xlsx")
        raise ValueError("Argumentos insuficientes.")
    
    questions_file = args[1]
    if not os.path.exists(questions_file):
        raise FileNotFoundError(f"El archivo '{questions_file}' no se encontró.")
    
    exam_prefix = args[2]
    
    try:
        num_exams = int(args[3])
        if num_exams <= 0:
            raise ValueError("El número de exámenes debe ser mayor que 0.")
    except ValueError:
        raise ValueError("El número de exámenes debe ser un número entero positivo.")
    
    try:
        questions_per_exam = int(args[4])
        if questions_per_exam <= 0:
            raise ValueError("El número de preguntas por examen debe ser mayor que 0.")
    except ValueError:
        raise ValueError("El número de preguntas por examen debe ser un número entero positivo.")
    
    # Optional format parameter
    export_format = args[5].lower() if len(args) > 5 else 'txt'
    if export_format not in ['txt', 'docx', 'both']:
        raise ValueError("Formato debe ser: txt, docx o both")
    
    # Optional template parameter
    template_path = args[6] if len(args) > 6 else None
    if template_path and not os.path.exists(template_path):
        raise ValueError(f"El archivo de plantilla '{template_path}' no se encontró.")
    
    # Optional answers format parameter
    answers_format = args[7].lower() if len(args) > 7 else 'xlsx'
    if answers_format not in ['xlsx', 'csv', 'txt', 'html']:
        raise ValueError("Formato de respuestas debe ser: xlsx, csv, txt o html")

    # Optional minutes per question (positional 8)
    try:
        minutes_per_question = float(args[8]) if len(args) > 8 else 1.0
        if minutes_per_question <= 0:
            raise ValueError
    except ValueError:
        raise ValueError("Los minutos por pregunta deben ser un número positivo (puede ser decimal).")
    
    return (
        questions_file,
        exam_prefix,
        num_exams,
        questions_per_exam,
        export_format,
        template_path,
        answers_format,
        minutes_per_question,
    )


def main_generate(
    questions_file: str,
    exam_prefix: str,
    num_exams: int,
    num_questions: int,
    export_format: str = 'txt',
    template_path: Optional[str] = None,
    answers_format: str = 'xlsx',
    minutes_per_question: float = 1.0
) -> str:
    """Main generation function (callable from CLI).
    
    Args:
        questions_file: Path to questions file
        exam_prefix: Exam prefix (e.g., "Parcial", "Final")
        num_exams: Number of exams to generate
        num_questions: Questions per exam
        export_format: Export format ('txt', 'docx', 'both')
        template_path: Optional DOCX template path
        answers_format: Answers format ('xlsx', 'csv', 'txt', 'html')
        minutes_per_question: Minutes assigned per question (can be decimal)
        
    Returns:
        Output directory path
        
    Raises:
        Various exceptions for validation errors
    """
    # Check if python-docx is available for docx export
    if export_format in ['docx', 'both']:
        try:
            from docx import Document
        except ImportError:
            print("Error: Para exportar a DOCX necesitas instalar python-docx:")
            print("uv add python-docx")
            raise ImportError("python-docx not installed")
    
    # Create output directory
    output_dir = create_output_directory(exam_prefix)
    
    # Load and validate questions
    questions_data = load_questions_from_file(questions_file)
    validate_questions(questions_data)
    print(f"Cargadas {len(questions_data)} preguntas del archivo '{questions_file}'.")
    
    # Adjust questions per exam if necessary
    if num_questions > len(questions_data):
        print(f"Advertencia: Solo hay {len(questions_data)} preguntas disponibles.")
        num_questions = len(questions_data)

    # Calculate and show exam time
    exam_time = calculate_exam_time(num_questions, minutes_per_question)
    print(f"Tiempo estimado por examen: {exam_time} (minutos por pregunta: {minutes_per_question})")

    # Store all exam data for answer files
    all_exam_data = []

    # Generate exams
    for i in range(1, num_exams + 1):
        # Set deterministic random seed for consistent shuffling
        seed = f"{exam_prefix}_{i}"
        
        # Generate exam
        exam_questions, exam_answers = generate_exam(
            questions_data,
            num_questions,
            seed
        )
        
        # Store exam data for consolidated answer file
        all_exam_data.append({
            'exam_number': i,
            'answers': list(exam_answers.values()),
            'questions': exam_questions
        })
        
        # Create exam content for TXT export
        exam_content = f"--- EXAMEN {exam_prefix} {i} ---\n\n"
        option_letters = ['A', 'B', 'C', 'D']
        
        for q in exam_questions:
            exam_content += f"{q['number']}. {q['question']}\n"
            for j, option in enumerate(q['options']):
                exam_content += f"   {option_letters[j]}) {option}\n"
            exam_content += "\n"
        
        # Export based on selected format
        if export_format in ['txt', 'both']:
            create_exam_txt(exam_content, exam_prefix, i, output_dir)
            
            # Individual answers file
            answers_content = f"--- RESPUESTAS EXAMEN {exam_prefix} {i} ---\n\n"
            for q_num, answer in exam_answers.items():
                answers_content += f"{q_num}. {answer})\n"
            
            answers_file_path = os.path.join(output_dir, f"respuestas_examen_{exam_prefix}_{i}.txt")
            with open(answers_file_path, 'w', encoding='utf-8') as f:
                f.write(answers_content)
        
        if export_format in ['docx', 'both']:
            create_exam_docx(
                exam_prefix,
                i,
                exam_questions,
                output_dir,
                template_path,
                minutes_per_question,
            )

    # Create consolidated answer file in selected format
    if answers_format == 'xlsx':
        create_answers_excel(all_exam_data, exam_prefix, output_dir, minutes_per_question)
    elif answers_format == 'csv':
        create_answers_csv(all_exam_data, exam_prefix, output_dir)
    elif answers_format == 'html':
        create_answers_html(all_exam_data, exam_prefix, output_dir, minutes_per_question)
    elif answers_format == 'txt':
        create_answers_txt(all_exam_data, exam_prefix, output_dir, minutes_per_question)

    format_msg = {
        'txt': 'TXT',
        'docx': 'DOCX', 
        'both': 'TXT y DOCX'
    }
    
    template_msg = f" usando plantilla '{template_path}'" if template_path else ""
    print(f"Generados {num_exams} exámenes ({exam_prefix}) con {num_questions} preguntas cada uno en formato {format_msg[export_format]}{template_msg}.")
    print(f"Archivos guardados en la carpeta: {output_dir}")
    print(f"Archivo de respuestas creado en formato: {answers_format.upper()}")
    
    return output_dir


def main():
    """Main execution function for CLI."""
    try:
        questions_file, exam_prefix, num_exams, questions_per_exam, export_format, template_path, answers_format, minutes_per_question = validate_args(sys.argv)
        
        main_generate(
            questions_file=questions_file,
            exam_prefix=exam_prefix,
            num_exams=num_exams,
            num_questions=questions_per_exam,
            export_format=export_format,
            template_path=template_path,
            answers_format=answers_format,
            minutes_per_question=minutes_per_question
        )

    except (FileNotFoundError, ValueError, ImportError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
