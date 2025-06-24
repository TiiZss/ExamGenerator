# 
# ______                      _____                           _             
#|  ____|                    / ____|                         | |            
#| |__  __  ____ _ _ __ ___ | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
#|  __| \ \/ / _` | '_ ` _ \| | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
#| |____ >  < (_| | | | | | | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
#|______/_/\_\__,_|_| |_| |_|\_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
#                                                                           
# by TiiZss v.6.20250624

import random
import re
import sys
import os
from typing import List, Dict, Tuple

def load_questions_from_file(filepath: str) -> List[Dict[str, any]]:
    """Load questions from a text file and return parsed question data."""
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

def generate_exam(exam_number: int, exam_name_prefix: str, all_questions: List[Dict], 
                 num_questions_per_exam: int) -> Tuple[str, str]:
    """Generate a single exam and its answer key."""
    exam_content = f"--- EXAMEN {exam_name_prefix} {exam_number} ---\n\n"
    answers_content = f"--- RESPUESTAS EXAMEN {exam_name_prefix} {exam_number} ---\n\n"

    # Select and shuffle questions
    num_to_select = min(num_questions_per_exam, len(all_questions))
    selected_questions = random.sample(all_questions, num_to_select)
    
    option_letters = ['A', 'B', 'C', 'D']

    for i, q_data in enumerate(selected_questions, 1):
        question_text = q_data["question"]
        original_options = q_data["options"]
        correct_answer_index = ord(q_data["answer"]) - ord('A')
        correct_answer_text = original_options[correct_answer_index]

        # Shuffle options and find new correct letter
        shuffled_options = random.sample(original_options, len(original_options))
        new_correct_letter = option_letters[shuffled_options.index(correct_answer_text)]

        # Build exam content
        exam_content += f"{i}. {question_text}\n"
        for j, option in enumerate(shuffled_options):
            exam_content += f"   {option_letters[j]}) {option}\n"
        exam_content += "\n"
        
        answers_content += f"{i}. {new_correct_letter})\n"
    
    return exam_content, answers_content

def validate_args(args: List[str]) -> Tuple[str, str, int, int]:
    """Validate and parse command line arguments."""
    if len(args) < 5:
        raise ValueError("Uso: python eg.py <archivo_preguntas.txt> <nombre_base> <num_examenes> <preguntas_por_examen>")
    
    questions_file = args[1]
    exam_prefix = args[2]
    
    try:
        num_exams = int(args[3])
        if num_exams <= 0:
            raise ValueError("El número de exámenes debe ser positivo.")
    except ValueError as e:
        raise ValueError(f"Número de exámenes inválido: {e}")
    
    try:
        questions_per_exam = int(args[4])
        if questions_per_exam <= 0:
            raise ValueError("El número de preguntas por examen debe ser positivo.")
    except ValueError as e:
        raise ValueError(f"Número de preguntas por examen inválido: {e}")
    
    return questions_file, exam_prefix, num_exams, questions_per_exam

def main():
    """Main execution function."""
    try:
        questions_file, exam_prefix, num_exams, questions_per_exam = validate_args(sys.argv)
        
        # Load questions
        questions_data = load_questions_from_file(questions_file)
        print(f"Cargadas {len(questions_data)} preguntas del archivo '{questions_file}'.")
        
        # Adjust questions per exam if necessary
        if questions_per_exam > len(questions_data):
            print(f"Advertencia: Solo hay {len(questions_data)} preguntas disponibles.")
            questions_per_exam = len(questions_data)

        # Generate exams
        for i in range(1, num_exams + 1):
            exam_content, answers_content = generate_exam(i, exam_prefix, questions_data, questions_per_exam)
            
            # Write files
            with open(f"examen_{exam_prefix}_{i}.txt", "w", encoding="utf-8") as f:
                f.write(exam_content)
            
            with open(f"respuestas_examen_{exam_prefix}_{i}.txt", "w", encoding="utf-8") as f:
                f.write(answers_content)

        print(f"Generados {num_exams} exámenes ({exam_prefix}) con {questions_per_exam} preguntas cada uno.")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
