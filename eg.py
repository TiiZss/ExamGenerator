# 
# ______                      _____                           _             
#|  ____|                    / ____|                         | |            
#| |__  __  ____ _ _ __ ___ | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
#|  __| \ \/ / _` | '_ ` _ \| | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
#| |____ >  < (_| | | | | | | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
#|______/_/\_\__,_|_| |_| |_|\_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
#                                                                           
# by TiiZss v.5.20250613

import random
import re
import sys
import os

def load_questions_from_file(filepath):
    questions_data = []
    current_question = {}
    options = []
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo '{filepath}' no se encontró.")

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line_num, line_raw in enumerate(lines):
        line = line_raw.strip()
        
        if not line: # Empty line signifies end of a question block
            if current_question and options:
                current_question['options'] = options
                questions_data.append(current_question)
                current_question = {} # Reset for next question
                options = [] # Reset options
            continue

        # Check if it's an option or an answer line
        is_option = re.match(r'^[A-D][).]\s', line)
        is_answer = line.startswith('ANSWER:')

        if is_option: # It's an option
            if 'question' not in current_question:
                raise ValueError(f"Opción detectada sin una pregunta previa en línea {line_num + 1}. Revisa tu archivo de preguntas.")
            options.append(line[3:].strip()) 
        elif is_answer: # It's the answer
            if 'question' not in current_question:
                raise ValueError(f"Respuesta detectada sin una pregunta previa en línea {line_num + 1}. Revisa tu archivo de preguntas.")
            try:
                current_question['answer'] = line.split(':')[1].strip()[0] 
            except IndexError:
                raise ValueError(f"Formato de ANSWER incorrecto en línea {line_num + 1}: '{line_raw.strip()}'. Debe ser 'ANSWER: X)'")
        else: # If it's not an option, not an answer, and not blank, it must be a question
            if current_question and options: # Save previous question if exists
                current_question['options'] = options
                questions_data.append(current_question)
            
            # Initialize a new question
            if re.match(r'^\d+\.\s*', line):
                question_text = re.sub(r'^\d+\.\s*', '', line)
            else:
                question_text = line
            
            current_question = {'question': question_text}
            options = [] # Ensure options are empty for the new question

    if current_question and options:
        current_question['options'] = options
        questions_data.append(current_question)

    if not questions_data:
        raise ValueError("No se cargó ninguna pregunta. El archivo podría estar vacío o con formato completamente incorrecto.")

    return questions_data

def generate_exam(exam_number, exam_name_prefix, all_questions, num_questions_per_exam):
    # Modificación aquí: Usa exam_name_prefix
    exam_content = f"--- EXAMEN {exam_name_prefix} {exam_number} ---\n\n"
    answers_content = f"--- RESPUESTAS EXAMEN {exam_name_prefix} {exam_number} ---\n\n"

    # Select a random subset of questions for this exam
    if num_questions_per_exam > len(all_questions):
        print(f"Advertencia: El número de preguntas por examen ({num_questions_per_exam}) es mayor que el total de preguntas disponibles ({len(all_questions)}). Se usarán todas las preguntas disponibles.")
        selected_questions = random.sample(all_questions, len(all_questions))
    else:
        selected_questions = random.sample(all_questions, num_questions_per_exam)

    random.shuffle(selected_questions) # Shuffle in place

    for i, q_data in enumerate(selected_questions):
        question_text = q_data["question"]
        original_options = list(q_data["options"])
        
        correct_answer_text = original_options[ord(q_data["answer"]) - ord('A')]

        shuffled_options = random.sample(original_options, len(original_options))

        exam_content += f"{i + 1}. {question_text}\n"
        
        option_letters = ['A', 'B', 'C', 'D']
        new_correct_letter = ''
        for j, option in enumerate(shuffled_options):
            exam_content += f"   {option_letters[j]}) {option}\n"
            if option == correct_answer_text:
                new_correct_letter = option_letters[j]
        exam_content += "\n"
        answers_content += f"{i + 1}. {new_correct_letter})\n"
    
    return exam_content, answers_content

# --- Main execution ---
if __name__ == "__main__":
    if len(sys.argv) < 5: # Now we expect 4 arguments
        print("Uso: python generador_examenes.py <ruta_del_archivo_de_preguntas.txt> <nombre_base_examen> <numero_total_de_examenes> <numero_de_preguntas_por_examen>")
        print("Ejemplo: python generador_examenes.py preguntas.txt SOC 30 20")
        sys.exit(1) # Exit with an error code

    questions_file_path = sys.argv[1] # 1st argument
    exam_name_prefix = sys.argv[2] # 2nd argument
    
    try:
        num_exams = int(sys.argv[3]) # 3rd argument
        if num_exams <= 0:
            print("Error: El número total de exámenes debe ser un entero positivo.")
            sys.exit(1)
    except ValueError:
        print("Error: El número total de exámenes debe ser un valor numérico entero.")
        sys.exit(1)

    try:
        num_questions_per_exam = int(sys.argv[4]) # 4th argument
        if num_questions_per_exam <= 0:
            print("Error: El número de preguntas por examen debe ser un entero positivo.")
            sys.exit(1)
    except ValueError:
        print("Error: El número de preguntas por examen debe ser un valor numérico entero.")
        sys.exit(1)

    try:
        questions_data = load_questions_from_file(questions_file_path)
        if not questions_data:
            print(f"Error: No se pudieron cargar preguntas del archivo '{questions_file_path}'. Asegúrate de que el formato sea correcto.")
        else:
            print(f"Se cargaron {len(questions_data)} preguntas del archivo '{questions_file_path}'.")
            
            if num_questions_per_exam > len(questions_data):
                print(f"Advertencia: Se solicitó {num_questions_per_exam} preguntas por examen, pero solo hay {len(questions_data)} disponibles. Se usarán todas las preguntas disponibles en cada examen.")
                num_questions_per_exam = len(questions_data)

            for i in range(1, num_exams + 1):
                exam, answers = generate_exam(i, exam_name_prefix, questions_data, num_questions_per_exam)
                
                with open(f"examen_{exam_name_prefix}_{i}.txt", "w", encoding="utf-8") as f:
                    f.write(exam)
                
                with open(f"respuestas_examen_{exam_name_prefix}_{i}.txt", "w", encoding="utf-8") as f:
                    f.write(answers)

            print(f"Se han generado {num_exams} exámenes ({exam_name_prefix}), cada uno con {num_questions_per_exam} preguntas, y sus respectivas respuestas.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
