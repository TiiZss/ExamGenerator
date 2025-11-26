<<<<<<< HEAD
# 
# ______                      _____                           _             
#|  ____|                    / ____|                         | |            
#| |__  __  ____ _ _ __ ___ | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
#|  __| \ \/ / _` | '_ ` _ \| | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
#| |____ >  < (_| | | | | | | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
#|______/_/\_\__,_|_| |_| |_|\_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
#                                                                           
# by TiiZss v.9.20251125

import random
import re
import sys
import os
import csv
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

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

def create_output_directory(exam_prefix: str) -> str:
    """Create output directory for exam files."""
    # Clean the exam prefix to make it a valid directory name
    safe_prefix = re.sub(r'[<>:"/\\|?*]', '_', exam_prefix)
    output_dir = f"Examenes_{safe_prefix}"
    
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Creada carpeta: {output_dir}")
    else:
        print(f"Usando carpeta existente: {output_dir}")
    
    return output_dir

def calculate_exam_time(num_questions: int, minutes_per_question: float = 1.0) -> str:
    """Calculate exam time based on number of questions."""
    total_minutes = int(num_questions * minutes_per_question)
    
    if total_minutes < 60:
        return f"{total_minutes} minutos"
    else:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        if minutes > 0:
            return f"{hours} hora{'s' if hours > 1 else ''} y {minutes} minutos"
        else:
            return f"{hours} hora{'s' if hours > 1 else ''}"

def create_answers_excel(all_exam_data: List[Dict], exam_prefix: str, output_dir: str) -> None:
    """Create a single Excel file with all exam answers (transposed layout)."""
    try:
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("Error: Para exportar a Excel necesitas instalar openpyxl:")
        print("pip install openpyxl")
        return

    # Create workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Respuestas {exam_prefix}"
    
    # Define styles
    header_font = Font(bold=True, size=12, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    exam_font = Font(bold=True, size=11)
    exam_fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")
    
    answer_alignment = Alignment(horizontal="center", vertical="center")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Find maximum number of questions across all exams
    max_questions = max(len(exam_data['answers']) for exam_data in all_exam_data)
    
    # Set up headers (TRANSPOSED: Examen in rows, Questions in columns)
    headers = ["Examen"]
    for i in range(1, max_questions + 1):
        headers.append(f"P{i}")
    
    # Write headers
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border
    
    # Write exam data (TRANSPOSED: each row is an exam)
    for exam_idx, exam_data in enumerate(all_exam_data):
        row = exam_idx + 2
        
        # Exam name
        cell = ws.cell(row=row, column=1, value=f"Examen {exam_data['exam_number']}")
        cell.font = exam_font
        cell.fill = exam_fill
        cell.alignment = answer_alignment
        cell.border = thin_border
        
        # Answers for each question
        for question_idx in range(max_questions):
            col = question_idx + 2
            if question_idx < len(exam_data['answers']):
                answer = exam_data['answers'][question_idx]
                cell = ws.cell(row=row, column=col, value=answer)
            else:
                cell = ws.cell(row=row, column=col, value="-")
            
            cell.alignment = answer_alignment
            cell.border = thin_border
    
    # Add exam info at the bottom
    info_start_row = len(all_exam_data) + 4
    
    # Exam details header
    cell = ws.cell(row=info_start_row, column=1, value="Información de Exámenes")
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    
    # Merge cells for the header
    ws.merge_cells(start_row=info_start_row, start_column=1, 
                  end_row=info_start_row, end_column=len(headers))
    
    # Exam details
    details = [
        ("Nombre del examen:", exam_prefix),
        ("Fecha de generación:", datetime.now().strftime("%d/%m/%Y %H:%M")),
        ("Número total de exámenes:", str(len(all_exam_data))),
        ("Preguntas por examen:", str(max_questions)),
        ("Tiempo estimado:", calculate_exam_time(max_questions))
    ]
    
    for i, (label, value) in enumerate(details):
        row = info_start_row + i + 1
        
        # Label
        cell = ws.cell(row=row, column=1, value=label)
        cell.font = exam_font
        cell.border = thin_border
        
        # Value
        cell = ws.cell(row=row, column=2, value=value)
        cell.border = thin_border
    
    # Auto-adjust column widths
    for col in range(1, len(headers) + 1):
        column_letter = get_column_letter(col)
        if col == 1:
            ws.column_dimensions[column_letter].width = 15
        else:
            ws.column_dimensions[column_letter].width = 8
    
    # Save the workbook
    excel_filename = os.path.join(output_dir, f"respuestas_{exam_prefix}_completas.xlsx")
    wb.save(excel_filename)
    print(f"Archivo Excel creado: {excel_filename}")

def create_answers_csv(all_exam_data: List[Dict], exam_prefix: str, output_dir: str) -> None:
    """Create a CSV file with all exam answers (transposed layout)."""
    max_questions = max(len(exam_data['answers']) for exam_data in all_exam_data)
    
    # Prepare headers
    headers = ["Examen"]
    for i in range(1, max_questions + 1):
        headers.append(f"P{i}")
    
    # Prepare data
    rows = [headers]
    for exam_data in all_exam_data:
        row = [f"Examen {exam_data['exam_number']}"]
        for question_idx in range(max_questions):
            if question_idx < len(exam_data['answers']):
                row.append(exam_data['answers'][question_idx])
            else:
                row.append("-")
        rows.append(row)
    
    # Write CSV file
    csv_filename = os.path.join(output_dir, f"respuestas_{exam_prefix}_completas.csv")
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    
    print(f"Archivo CSV creado: {csv_filename}")

def create_answers_html(all_exam_data: List[Dict], exam_prefix: str, output_dir: str) -> None:
    """Create an HTML file with all exam answers (transposed layout)."""
    max_questions = max(len(exam_data['answers']) for exam_data in all_exam_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Respuestas - {exam_prefix}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
        }}
        th {{
            background-color: #4472C4;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f0f0f0;
        }}
        .exam-cell {{
            background-color: #D9E2F3 !important;
            font-weight: bold;
        }}
        .info-section {{
            margin-top: 30px;
            padding: 15px;
            background-color: #f8f9fa;
            border-left: 4px solid #4472C4;
        }}
        .info-section h3 {{
            margin-top: 0;
            color: #4472C4;
        }}
        .info-item {{
            margin: 8px 0;
        }}
        .info-label {{
            font-weight: bold;
            display: inline-block;
            width: 180px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Respuestas de Exámenes - {exam_prefix}</h1>
        
        <table>
            <thead>
                <tr>
                    <th>Examen</th>"""
    
    # Add question headers
    for i in range(1, max_questions + 1):
        html_content += f"<th>P{i}</th>"
    
    html_content += """
                </tr>
            </thead>
            <tbody>"""
    
    # Add exam data rows
    for exam_data in all_exam_data:
        html_content += f"""
                <tr>
                    <td class="exam-cell">Examen {exam_data['exam_number']}</td>"""
        
        for question_idx in range(max_questions):
            if question_idx < len(exam_data['answers']):
                answer = exam_data['answers'][question_idx]
            else:
                answer = "-"
            html_content += f"<td>{answer}</td>"
        
        html_content += "</tr>"
    
    html_content += f"""
            </tbody>
        </table>
        
        <div class="info-section">
            <h3>Información del Examen</h3>
            <div class="info-item">
                <span class="info-label">Nombre del examen:</span>
                {exam_prefix}
            </div>
            <div class="info-item">
                <span class="info-label">Fecha de generación:</span>
                {datetime.now().strftime("%d/%m/%Y %H:%M")}
            </div>
            <div class="info-item">
                <span class="info-label">Número de exámenes:</span>
                {len(all_exam_data)}
            </div>
            <div class="info-item">
                <span class="info-label">Preguntas por examen:</span>
                {max_questions}
            </div>
            <div class="info-item">
                <span class="info-label">Tiempo estimado:</span>
                {calculate_exam_time(max_questions)}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # Write HTML file
    html_filename = os.path.join(output_dir, f"respuestas_{exam_prefix}_completas.html")
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Archivo HTML creado: {html_filename}")

def create_answers_txt(all_exam_data: List[Dict], exam_prefix: str, output_dir: str) -> None:
    """Create a TXT file with all exam answers (transposed layout)."""
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
    txt_content += f"Tiempo estimado: {calculate_exam_time(max_questions)}\n"
    
    # Write TXT file
    txt_filename = os.path.join(output_dir, f"respuestas_{exam_prefix}_completas.txt")
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    
    print(f"Archivo TXT creado: {txt_filename}")

def create_docx_document(title: str, template_path: Optional[str] = None) -> Document:
    """Create a new DOCX document with custom styles or from template."""
    if template_path and os.path.exists(template_path):
        # Load from template
        doc = Document(template_path)
        print(f"Usando plantilla: {template_path}")
    else:
        # Create new document with default styles
        doc = Document()
        
        # Configure document styles
        styles = doc.styles
        
        # Title style
        if 'Custom Title' not in [style.name for style in styles]:
            title_style = styles.add_style('Custom Title', WD_STYLE_TYPE.PARAGRAPH)
            title_style.font.size = Pt(16)
            title_style.font.bold = True
            title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            title_style.paragraph_format.space_after = Pt(12)
        
        # Question style
        if 'Question' not in [style.name for style in styles]:
            question_style = styles.add_style('Question', WD_STYLE_TYPE.PARAGRAPH)
            question_style.font.size = Pt(11)
            question_style.font.bold = True
            question_style.paragraph_format.space_before = Pt(6)
            question_style.paragraph_format.space_after = Pt(3)
        
        # Option style
        if 'Option' not in [style.name for style in styles]:
            option_style = styles.add_style('Option', WD_STYLE_TYPE.PARAGRAPH)
            option_style.font.size = Pt(10)
            option_style.paragraph_format.left_indent = Inches(0.5)
            option_style.paragraph_format.space_after = Pt(2)
    
    return doc

def replace_placeholders(doc: Document, exam_prefix: str, exam_number: int, num_questions: int):
    """Replace placeholders in the template document."""
    now = datetime.now()
    
    # Spanish month names
    months_es = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    # Calculate exam time
    exam_time = calculate_exam_time(num_questions)
    exam_time_minutes = int(num_questions * 1.0)  # Default: 1 minute per question
    
    replacements = {
        '{{EXAM_NAME}}': f"{exam_prefix}",
        '{{EXAM_NUMBER}}': str(exam_number),
        '{{EXAM_TITLE}}': f"EXAMEN {exam_prefix} {exam_number}",
        '{{DATE}}': now.strftime("%d/%m/%Y"),
        '{{FULL_DATE}}': now.strftime("%d de %B de %Y"),
        '{{DAY}}': str(now.day),
        '{{MONTH}}': months_es[now.month],
        '{{MONTH_NUM}}': f"{now.month:02d}",
        '{{YEAR}}': str(now.year),
        '{{COURSE}}': exam_prefix,
        '{{TODAY}}': now.strftime("%d/%m/%Y"),
        '{{MONTH_YEAR}}': f"{months_es[now.month]} {now.year}",
        '{{NUM_QUESTIONS}}': str(num_questions),
        '{{EXAM_TIME}}': exam_time,
        '{{EXAM_TIME_MINUTES}}': str(exam_time_minutes),
        '{{TIME}}': exam_time,
        '{{DURATION}}': exam_time
    }
    
    # Replace in paragraphs
    for paragraph in doc.paragraphs:
        for placeholder, replacement in replacements.items():
            if placeholder in paragraph.text:
                for run in paragraph.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, replacement)
    
    # Replace in tables (if any)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for placeholder, replacement in replacements.items():
                        if placeholder in paragraph.text:
                            for run in paragraph.runs:
                                if placeholder in run.text:
                                    run.text = run.text.replace(placeholder, replacement)

def find_content_insertion_point(doc: Document) -> Optional[int]:
    """Find where to insert exam content in the template."""
    content_markers = ['{{CONTENT}}', '{{QUESTIONS}}', '{{EXAM_CONTENT}}']
    
    for i, paragraph in enumerate(doc.paragraphs):
        for marker in content_markers:
            if marker in paragraph.text:
                # Remove the marker
                paragraph.text = ""
                return i
    
    # If no marker found, insert after the first paragraph or at the end
    return len(doc.paragraphs) if len(doc.paragraphs) > 0 else 0

def save_exam_as_docx(exam_content: str, answers_content: str, exam_prefix: str, exam_number: int, 
                     selected_questions: List[Dict], output_dir: str, template_path: Optional[str] = None) -> None:
    """Save exam and answers as DOCX files."""
    option_letters = ['A', 'B', 'C', 'D']
    num_questions = len(selected_questions)
    
    # Create exam document
    exam_doc = create_docx_document(f"EXAMEN {exam_prefix} {exam_number}", template_path)
    
    # Replace placeholders in template
    replace_placeholders(exam_doc, exam_prefix, exam_number, num_questions)
    
    # Find insertion point for content
    insertion_point = find_content_insertion_point(exam_doc)
    
    # If no template or no insertion point found, add title
    if not template_path or insertion_point == 0:
        title_para = exam_doc.add_paragraph(f"EXAMEN {exam_prefix} {exam_number}")
        try:
            title_para.style = 'Custom Title'
        except KeyError:
            # Style doesn't exist, apply manual formatting
            title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in title_para.runs:
                run.font.size = Pt(16)
                run.font.bold = True
    
    # Add questions
    for i, q_data in enumerate(selected_questions, 1):
        question_text = q_data["question"]
        original_options = q_data["options"]
        correct_answer_index = ord(q_data["answer"]) - ord('A')
        correct_answer_text = original_options[correct_answer_index]

        # Shuffle options
        shuffled_options = random.sample(original_options, len(original_options))
        
        # Add question
        question_para = exam_doc.add_paragraph(f"{i}. {question_text}")
        try:
            question_para.style = 'Question'
        except KeyError:
            # Style doesn't exist, apply manual formatting
            for run in question_para.runs:
                run.font.bold = True
                run.font.size = Pt(11)
        
        # Add options
        for j, option in enumerate(shuffled_options):
            option_para = exam_doc.add_paragraph(f"{option_letters[j]}) {option}")
            try:
                option_para.style = 'Option'
            except KeyError:
                # Style doesn't exist, apply manual formatting
                option_para.paragraph_format.left_indent = Inches(0.5)
                for run in option_para.runs:
                    run.font.size = Pt(10)
        
        # Add some space after each question
        exam_doc.add_paragraph()
    
    # Save exam document
    exam_doc.save(os.path.join(output_dir, f"examen_{exam_prefix}_{exam_number}.docx"))

def generate_exam(exam_number: int, exam_name_prefix: str, all_questions: List[Dict], 
                 num_questions_per_exam: int, export_format: str = 'txt') -> Tuple[str, str, List[Dict], List[str]]:
    """Generate a single exam and its answer key."""
    exam_content = f"--- EXAMEN {exam_name_prefix} {exam_number} ---\n\n"
    answers_content = f"--- RESPUESTAS EXAMEN {exam_name_prefix} {exam_number} ---\n\n"

    # Select and shuffle questions
    num_to_select = min(num_questions_per_exam, len(all_questions))
    selected_questions = random.sample(all_questions, num_to_select)
    
    option_letters = ['A', 'B', 'C', 'D']
    exam_answers = []

    for i, q_data in enumerate(selected_questions, 1):
        question_text = q_data["question"]
        original_options = q_data["options"]
        correct_answer_index = ord(q_data["answer"]) - ord('A')
        correct_answer_text = original_options[correct_answer_index]

        # Shuffle options and find new correct letter
        shuffled_options = random.sample(original_options, len(original_options))
        new_correct_letter = option_letters[shuffled_options.index(correct_answer_text)]
        exam_answers.append(new_correct_letter)

        # Build exam content (for txt format)
        exam_content += f"{i}. {question_text}\n"
        for j, option in enumerate(shuffled_options):
            exam_content += f"   {option_letters[j]}) {option}\n"
        exam_content += "\n"
        
        answers_content += f"{i}. {new_correct_letter})\n"
    
    return exam_content, answers_content, selected_questions, exam_answers

def validate_args(args: List[str]) -> Tuple[str, str, int, int, str, Optional[str], str]:
    """Validate and parse command line arguments."""
    if len(args) < 5:
        raise ValueError("Uso: python eg.py <archivo_preguntas.txt> <nombre_base> <num_examenes> <preguntas_por_examen> [formato: txt|docx|both] [plantilla.docx] [respuestas: xlsx|csv|txt|html]")
    
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
    
    return questions_file, exam_prefix, num_exams, questions_per_exam, export_format, template_path, answers_format

def main():
    """Main execution function."""
    try:
        questions_file, exam_prefix, num_exams, questions_per_exam, export_format, template_path, answers_format = validate_args(sys.argv)
        
        # Check if python-docx is available for docx export
        if export_format in ['docx', 'both']:
            try:
                from docx import Document
            except ImportError:
                print("Error: Para exportar a DOCX necesitas instalar python-docx:")
                print("pip install python-docx")
                sys.exit(1)
        
        # Create output directory
        output_dir = create_output_directory(exam_prefix)
        
        # Load questions
        questions_data = load_questions_from_file(questions_file)
        print(f"Cargadas {len(questions_data)} preguntas del archivo '{questions_file}'.")
        
        # Adjust questions per exam if necessary
        if questions_per_exam > len(questions_data):
            print(f"Advertencia: Solo hay {len(questions_data)} preguntas disponibles.")
            questions_per_exam = len(questions_data)

        # Calculate and show exam time
        exam_time = calculate_exam_time(questions_per_exam)
        print(f"Tiempo estimado por examen: {exam_time}")

        # Store all exam data for answer files
        all_exam_data = []

        # Generate exams
        for i in range(1, num_exams + 1):
            # Set random seed for consistent shuffling across formats
            random.seed(f"{exam_prefix}_{i}")
            
            exam_content, answers_content, selected_questions, exam_answers = generate_exam(
                i, exam_prefix, questions_data, questions_per_exam, export_format
            )
            
            # Store exam data for answer files
            all_exam_data.append({
                'exam_number': i,
                'answers': exam_answers,
                'questions': selected_questions
            })
            
            # Export based on selected format
            if export_format in ['txt', 'both']:
                # Write TXT files in the output directory
                exam_file_path = os.path.join(output_dir, f"examen_{exam_prefix}_{i}.txt")
                with open(exam_file_path, "w", encoding="utf-8") as f:
                    f.write(exam_content)
                
                answers_file_path = os.path.join(output_dir, f"respuestas_examen_{exam_prefix}_{i}.txt")
                with open(answers_file_path, "w", encoding="utf-8") as f:
                    f.write(answers_content)
            
            if export_format in ['docx', 'both']:
                # Reset random seed to ensure same shuffling
                random.seed(f"{exam_prefix}_{i}")
                # Regenerate to ensure same shuffling
                _, _, selected_questions, _ = generate_exam(
                    i, exam_prefix, questions_data, questions_per_exam, export_format
                )
                save_exam_as_docx(exam_content, answers_content, exam_prefix, i, selected_questions, output_dir, template_path)

        # Create answer file in selected format
        if answers_format == 'xlsx':
            create_answers_excel(all_exam_data, exam_prefix, output_dir)
        elif answers_format == 'csv':
            create_answers_csv(all_exam_data, exam_prefix, output_dir)
        elif answers_format == 'html':
            create_answers_html(all_exam_data, exam_prefix, output_dir)
        elif answers_format == 'txt':
            create_answers_txt(all_exam_data, exam_prefix, output_dir)

        format_msg = {
            'txt': 'TXT',
            'docx': 'DOCX', 
            'both': 'TXT y DOCX'
        }
        
        template_msg = f" usando plantilla '{template_path}'" if template_path else ""
        print(f"Generados {num_exams} exámenes ({exam_prefix}) con {questions_per_exam} preguntas cada uno en formato {format_msg[export_format]}{template_msg}.")
        print(f"Archivos guardados en la carpeta: {output_dir}")
        print(f"Archivo de respuestas creado en formato: {answers_format.upper()}")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
=======
# 
# ______                      _____                           _             
#|  ____|                    / ____|                         | |            
#| |__  __  ____ _ _ __ ___ | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
#|  __| \ \/ / _` | '_ ` _ \| | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
#| |____ >  < (_| | | | | | | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
#|______/_/\_\__,_|_| |_| |_|\_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
#                                                                           
# by TiiZss v.9.20251125

import random
import re
import sys
import os
import csv
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

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

def create_output_directory(exam_prefix: str) -> str:
    """Create output directory for exam files."""
    # Clean the exam prefix to make it a valid directory name
    safe_prefix = re.sub(r'[<>:"/\\|?*]', '_', exam_prefix)
    output_dir = f"Examenes_{safe_prefix}"
    
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Creada carpeta: {output_dir}")
    else:
        print(f"Usando carpeta existente: {output_dir}")
    
    return output_dir

def calculate_exam_time(num_questions: int, minutes_per_question: float = 1.0) -> str:
    """Calculate exam time based on number of questions."""
    total_minutes = int(num_questions * minutes_per_question)
    
    if total_minutes < 60:
        return f"{total_minutes} minutos"
    else:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        if minutes > 0:
            return f"{hours} hora{'s' if hours > 1 else ''} y {minutes} minutos"
        else:
            return f"{hours} hora{'s' if hours > 1 else ''}"

def create_answers_excel(all_exam_data: List[Dict], exam_prefix: str, output_dir: str) -> None:
    """Create a single Excel file with all exam answers (transposed layout)."""
    try:
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("Error: Para exportar a Excel necesitas instalar openpyxl:")
        print("pip install openpyxl")
        return

    # Create workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Respuestas {exam_prefix}"
    
    # Define styles
    header_font = Font(bold=True, size=12, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    exam_font = Font(bold=True, size=11)
    exam_fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")
    
    answer_alignment = Alignment(horizontal="center", vertical="center")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Find maximum number of questions across all exams
    max_questions = max(len(exam_data['answers']) for exam_data in all_exam_data)
    
    # Set up headers (TRANSPOSED: Examen in rows, Questions in columns)
    headers = ["Examen"]
    for i in range(1, max_questions + 1):
        headers.append(f"P{i}")
    
    # Write headers
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border
    
    # Write exam data (TRANSPOSED: each row is an exam)
    for exam_idx, exam_data in enumerate(all_exam_data):
        row = exam_idx + 2
        
        # Exam name
        cell = ws.cell(row=row, column=1, value=f"Examen {exam_data['exam_number']}")
        cell.font = exam_font
        cell.fill = exam_fill
        cell.alignment = answer_alignment
        cell.border = thin_border
        
        # Answers for each question
        for question_idx in range(max_questions):
            col = question_idx + 2
            if question_idx < len(exam_data['answers']):
                answer = exam_data['answers'][question_idx]
                cell = ws.cell(row=row, column=col, value=answer)
            else:
                cell = ws.cell(row=row, column=col, value="-")
            
            cell.alignment = answer_alignment
            cell.border = thin_border
    
    # Add exam info at the bottom
    info_start_row = len(all_exam_data) + 4
    
    # Exam details header
    cell = ws.cell(row=info_start_row, column=1, value="Información de Exámenes")
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    
    # Merge cells for the header
    ws.merge_cells(start_row=info_start_row, start_column=1, 
                  end_row=info_start_row, end_column=len(headers))
    
    # Exam details
    details = [
        ("Nombre del examen:", exam_prefix),
        ("Fecha de generación:", datetime.now().strftime("%d/%m/%Y %H:%M")),
        ("Número total de exámenes:", str(len(all_exam_data))),
        ("Preguntas por examen:", str(max_questions)),
        ("Tiempo estimado:", calculate_exam_time(max_questions))
    ]
    
    for i, (label, value) in enumerate(details):
        row = info_start_row + i + 1
        
        # Label
        cell = ws.cell(row=row, column=1, value=label)
        cell.font = exam_font
        cell.border = thin_border
        
        # Value
        cell = ws.cell(row=row, column=2, value=value)
        cell.border = thin_border
    
    # Auto-adjust column widths
    for col in range(1, len(headers) + 1):
        column_letter = get_column_letter(col)
        if col == 1:
            ws.column_dimensions[column_letter].width = 15
        else:
            ws.column_dimensions[column_letter].width = 8
    
    # Save the workbook
    excel_filename = os.path.join(output_dir, f"respuestas_{exam_prefix}_completas.xlsx")
    wb.save(excel_filename)
    print(f"Archivo Excel creado: {excel_filename}")

def create_answers_csv(all_exam_data: List[Dict], exam_prefix: str, output_dir: str) -> None:
    """Create a CSV file with all exam answers (transposed layout)."""
    max_questions = max(len(exam_data['answers']) for exam_data in all_exam_data)
    
    # Prepare headers
    headers = ["Examen"]
    for i in range(1, max_questions + 1):
        headers.append(f"P{i}")
    
    # Prepare data
    rows = [headers]
    for exam_data in all_exam_data:
        row = [f"Examen {exam_data['exam_number']}"]
        for question_idx in range(max_questions):
            if question_idx < len(exam_data['answers']):
                row.append(exam_data['answers'][question_idx])
            else:
                row.append("-")
        rows.append(row)
    
    # Write CSV file
    csv_filename = os.path.join(output_dir, f"respuestas_{exam_prefix}_completas.csv")
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    
    print(f"Archivo CSV creado: {csv_filename}")

def create_answers_html(all_exam_data: List[Dict], exam_prefix: str, output_dir: str) -> None:
    """Create an HTML file with all exam answers (transposed layout)."""
    max_questions = max(len(exam_data['answers']) for exam_data in all_exam_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Respuestas - {exam_prefix}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
        }}
        th {{
            background-color: #4472C4;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f0f0f0;
        }}
        .exam-cell {{
            background-color: #D9E2F3 !important;
            font-weight: bold;
        }}
        .info-section {{
            margin-top: 30px;
            padding: 15px;
            background-color: #f8f9fa;
            border-left: 4px solid #4472C4;
        }}
        .info-section h3 {{
            margin-top: 0;
            color: #4472C4;
        }}
        .info-item {{
            margin: 8px 0;
        }}
        .info-label {{
            font-weight: bold;
            display: inline-block;
            width: 180px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Respuestas de Exámenes - {exam_prefix}</h1>
        
        <table>
            <thead>
                <tr>
                    <th>Examen</th>"""
    
    # Add question headers
    for i in range(1, max_questions + 1):
        html_content += f"<th>P{i}</th>"
    
    html_content += """
                </tr>
            </thead>
            <tbody>"""
    
    # Add exam data rows
    for exam_data in all_exam_data:
        html_content += f"""
                <tr>
                    <td class="exam-cell">Examen {exam_data['exam_number']}</td>"""
        
        for question_idx in range(max_questions):
            if question_idx < len(exam_data['answers']):
                answer = exam_data['answers'][question_idx]
            else:
                answer = "-"
            html_content += f"<td>{answer}</td>"
        
        html_content += "</tr>"
    
    html_content += f"""
            </tbody>
        </table>
        
        <div class="info-section">
            <h3>Información del Examen</h3>
            <div class="info-item">
                <span class="info-label">Nombre del examen:</span>
                {exam_prefix}
            </div>
            <div class="info-item">
                <span class="info-label">Fecha de generación:</span>
                {datetime.now().strftime("%d/%m/%Y %H:%M")}
            </div>
            <div class="info-item">
                <span class="info-label">Número de exámenes:</span>
                {len(all_exam_data)}
            </div>
            <div class="info-item">
                <span class="info-label">Preguntas por examen:</span>
                {max_questions}
            </div>
            <div class="info-item">
                <span class="info-label">Tiempo estimado:</span>
                {calculate_exam_time(max_questions)}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # Write HTML file
    html_filename = os.path.join(output_dir, f"respuestas_{exam_prefix}_completas.html")
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Archivo HTML creado: {html_filename}")

def create_answers_txt(all_exam_data: List[Dict], exam_prefix: str, output_dir: str) -> None:
    """Create a TXT file with all exam answers (transposed layout)."""
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
    txt_content += f"Tiempo estimado: {calculate_exam_time(max_questions)}\n"
    
    # Write TXT file
    txt_filename = os.path.join(output_dir, f"respuestas_{exam_prefix}_completas.txt")
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    
    print(f"Archivo TXT creado: {txt_filename}")

def create_docx_document(title: str, template_path: Optional[str] = None) -> Document:
    """Create a new DOCX document with custom styles or from template."""
    if template_path and os.path.exists(template_path):
        # Load from template
        doc = Document(template_path)
        print(f"Usando plantilla: {template_path}")
    else:
        # Create new document with default styles
        doc = Document()
        
        # Configure document styles
        styles = doc.styles
        
        # Title style
        if 'Custom Title' not in [style.name for style in styles]:
            title_style = styles.add_style('Custom Title', WD_STYLE_TYPE.PARAGRAPH)
            title_style.font.size = Pt(16)
            title_style.font.bold = True
            title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            title_style.paragraph_format.space_after = Pt(12)
        
        # Question style
        if 'Question' not in [style.name for style in styles]:
            question_style = styles.add_style('Question', WD_STYLE_TYPE.PARAGRAPH)
            question_style.font.size = Pt(11)
            question_style.font.bold = True
            question_style.paragraph_format.space_before = Pt(6)
            question_style.paragraph_format.space_after = Pt(3)
        
        # Option style
        if 'Option' not in [style.name for style in styles]:
            option_style = styles.add_style('Option', WD_STYLE_TYPE.PARAGRAPH)
            option_style.font.size = Pt(10)
            option_style.paragraph_format.left_indent = Inches(0.5)
            option_style.paragraph_format.space_after = Pt(2)
    
    return doc

def replace_placeholders(doc: Document, exam_prefix: str, exam_number: int, num_questions: int):
    """Replace placeholders in the template document."""
    now = datetime.now()
    
    # Spanish month names
    months_es = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    # Calculate exam time
    exam_time = calculate_exam_time(num_questions)
    exam_time_minutes = int(num_questions * 1.0)  # Default: 1 minute per question
    
    replacements = {
        '{{EXAM_NAME}}': f"{exam_prefix}",
        '{{EXAM_NUMBER}}': str(exam_number),
        '{{EXAM_TITLE}}': f"EXAMEN {exam_prefix} {exam_number}",
        '{{DATE}}': now.strftime("%d/%m/%Y"),
        '{{FULL_DATE}}': now.strftime("%d de %B de %Y"),
        '{{DAY}}': str(now.day),
        '{{MONTH}}': months_es[now.month],
        '{{MONTH_NUM}}': f"{now.month:02d}",
        '{{YEAR}}': str(now.year),
        '{{COURSE}}': exam_prefix,
        '{{TODAY}}': now.strftime("%d/%m/%Y"),
        '{{MONTH_YEAR}}': f"{months_es[now.month]} {now.year}",
        '{{NUM_QUESTIONS}}': str(num_questions),
        '{{EXAM_TIME}}': exam_time,
        '{{EXAM_TIME_MINUTES}}': str(exam_time_minutes),
        '{{TIME}}': exam_time,
        '{{DURATION}}': exam_time
    }
    
    # Replace in paragraphs
    for paragraph in doc.paragraphs:
        for placeholder, replacement in replacements.items():
            if placeholder in paragraph.text:
                for run in paragraph.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, replacement)
    
    # Replace in tables (if any)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for placeholder, replacement in replacements.items():
                        if placeholder in paragraph.text:
                            for run in paragraph.runs:
                                if placeholder in run.text:
                                    run.text = run.text.replace(placeholder, replacement)

def find_content_insertion_point(doc: Document) -> Optional[int]:
    """Find where to insert exam content in the template."""
    content_markers = ['{{CONTENT}}', '{{QUESTIONS}}', '{{EXAM_CONTENT}}']
    
    for i, paragraph in enumerate(doc.paragraphs):
        for marker in content_markers:
            if marker in paragraph.text:
                # Remove the marker
                paragraph.text = ""
                return i
    
    # If no marker found, insert after the first paragraph or at the end
    return len(doc.paragraphs) if len(doc.paragraphs) > 0 else 0

def save_exam_as_docx(exam_content: str, answers_content: str, exam_prefix: str, exam_number: int, 
                     selected_questions: List[Dict], output_dir: str, template_path: Optional[str] = None) -> None:
    """Save exam and answers as DOCX files."""
    option_letters = ['A', 'B', 'C', 'D']
    num_questions = len(selected_questions)
    
    # Create exam document
    exam_doc = create_docx_document(f"EXAMEN {exam_prefix} {exam_number}", template_path)
    
    # Replace placeholders in template
    replace_placeholders(exam_doc, exam_prefix, exam_number, num_questions)
    
    # Find insertion point for content
    insertion_point = find_content_insertion_point(exam_doc)
    
    # If no template or no insertion point found, add title
    if not template_path or insertion_point == 0:
        title_para = exam_doc.add_paragraph(f"EXAMEN {exam_prefix} {exam_number}")
        try:
            title_para.style = 'Custom Title'
        except KeyError:
            # Style doesn't exist, apply manual formatting
            title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in title_para.runs:
                run.font.size = Pt(16)
                run.font.bold = True
    
    # Add questions
    for i, q_data in enumerate(selected_questions, 1):
        question_text = q_data["question"]
        original_options = q_data["options"]
        correct_answer_index = ord(q_data["answer"]) - ord('A')
        correct_answer_text = original_options[correct_answer_index]

        # Shuffle options
        shuffled_options = random.sample(original_options, len(original_options))
        
        # Add question
        question_para = exam_doc.add_paragraph(f"{i}. {question_text}")
        try:
            question_para.style = 'Question'
        except KeyError:
            # Style doesn't exist, apply manual formatting
            for run in question_para.runs:
                run.font.bold = True
                run.font.size = Pt(11)
        
        # Add options
        for j, option in enumerate(shuffled_options):
            option_para = exam_doc.add_paragraph(f"{option_letters[j]}) {option}")
            try:
                option_para.style = 'Option'
            except KeyError:
                # Style doesn't exist, apply manual formatting
                option_para.paragraph_format.left_indent = Inches(0.5)
                for run in option_para.runs:
                    run.font.size = Pt(10)
        
        # Add some space after each question
        exam_doc.add_paragraph()
    
    # Save exam document
    exam_doc.save(os.path.join(output_dir, f"examen_{exam_prefix}_{exam_number}.docx"))

def generate_exam(exam_number: int, exam_name_prefix: str, all_questions: List[Dict], 
                 num_questions_per_exam: int, export_format: str = 'txt') -> Tuple[str, str, List[Dict], List[str]]:
    """Generate a single exam and its answer key."""
    exam_content = f"--- EXAMEN {exam_name_prefix} {exam_number} ---\n\n"
    answers_content = f"--- RESPUESTAS EXAMEN {exam_name_prefix} {exam_number} ---\n\n"

    # Select and shuffle questions
    num_to_select = min(num_questions_per_exam, len(all_questions))
    selected_questions = random.sample(all_questions, num_to_select)
    
    option_letters = ['A', 'B', 'C', 'D']
    exam_answers = []

    for i, q_data in enumerate(selected_questions, 1):
        question_text = q_data["question"]
        original_options = q_data["options"]
        correct_answer_index = ord(q_data["answer"]) - ord('A')
        correct_answer_text = original_options[correct_answer_index]

        # Shuffle options and find new correct letter
        shuffled_options = random.sample(original_options, len(original_options))
        new_correct_letter = option_letters[shuffled_options.index(correct_answer_text)]
        exam_answers.append(new_correct_letter)

        # Build exam content (for txt format)
        exam_content += f"{i}. {question_text}\n"
        for j, option in enumerate(shuffled_options):
            exam_content += f"   {option_letters[j]}) {option}\n"
        exam_content += "\n"
        
        answers_content += f"{i}. {new_correct_letter})\n"
    
    return exam_content, answers_content, selected_questions, exam_answers

def validate_args(args: List[str]) -> Tuple[str, str, int, int, str, Optional[str], str]:
    """Validate and parse command line arguments."""
    if len(args) < 5:
        raise ValueError("Uso: python eg.py <archivo_preguntas.txt> <nombre_base> <num_examenes> <preguntas_por_examen> [formato: txt|docx|both] [plantilla.docx] [respuestas: xlsx|csv|txt|html]")
    
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
    
    return questions_file, exam_prefix, num_exams, questions_per_exam, export_format, template_path, answers_format

def main():
    """Main execution function."""
    try:
        questions_file, exam_prefix, num_exams, questions_per_exam, export_format, template_path, answers_format = validate_args(sys.argv)
        
        # Check if python-docx is available for docx export
        if export_format in ['docx', 'both']:
            try:
                from docx import Document
            except ImportError:
                print("Error: Para exportar a DOCX necesitas instalar python-docx:")
                print("pip install python-docx")
                sys.exit(1)
        
        # Create output directory
        output_dir = create_output_directory(exam_prefix)
        
        # Load questions
        questions_data = load_questions_from_file(questions_file)
        print(f"Cargadas {len(questions_data)} preguntas del archivo '{questions_file}'.")
        
        # Adjust questions per exam if necessary
        if questions_per_exam > len(questions_data):
            print(f"Advertencia: Solo hay {len(questions_data)} preguntas disponibles.")
            questions_per_exam = len(questions_data)

        # Calculate and show exam time
        exam_time = calculate_exam_time(questions_per_exam)
        print(f"Tiempo estimado por examen: {exam_time}")

        # Store all exam data for answer files
        all_exam_data = []

        # Generate exams
        for i in range(1, num_exams + 1):
            # Set random seed for consistent shuffling across formats
            random.seed(f"{exam_prefix}_{i}")
            
            exam_content, answers_content, selected_questions, exam_answers = generate_exam(
                i, exam_prefix, questions_data, questions_per_exam, export_format
            )
            
            # Store exam data for answer files
            all_exam_data.append({
                'exam_number': i,
                'answers': exam_answers,
                'questions': selected_questions
            })
            
            # Export based on selected format
            if export_format in ['txt', 'both']:
                # Write TXT files in the output directory
                exam_file_path = os.path.join(output_dir, f"examen_{exam_prefix}_{i}.txt")
                with open(exam_file_path, "w", encoding="utf-8") as f:
                    f.write(exam_content)
                
                answers_file_path = os.path.join(output_dir, f"respuestas_examen_{exam_prefix}_{i}.txt")
                with open(answers_file_path, "w", encoding="utf-8") as f:
                    f.write(answers_content)
            
            if export_format in ['docx', 'both']:
                # Reset random seed to ensure same shuffling
                random.seed(f"{exam_prefix}_{i}")
                # Regenerate to ensure same shuffling
                _, _, selected_questions, _ = generate_exam(
                    i, exam_prefix, questions_data, questions_per_exam, export_format
                )
                save_exam_as_docx(exam_content, answers_content, exam_prefix, i, selected_questions, output_dir, template_path)

        # Create answer file in selected format
        if answers_format == 'xlsx':
            create_answers_excel(all_exam_data, exam_prefix, output_dir)
        elif answers_format == 'csv':
            create_answers_csv(all_exam_data, exam_prefix, output_dir)
        elif answers_format == 'html':
            create_answers_html(all_exam_data, exam_prefix, output_dir)
        elif answers_format == 'txt':
            create_answers_txt(all_exam_data, exam_prefix, output_dir)

        format_msg = {
            'txt': 'TXT',
            'docx': 'DOCX', 
            'both': 'TXT y DOCX'
        }
        
        template_msg = f" usando plantilla '{template_path}'" if template_path else ""
        print(f"Generados {num_exams} exámenes ({exam_prefix}) con {questions_per_exam} preguntas cada uno en formato {format_msg[export_format]}{template_msg}.")
        print(f"Archivos guardados en la carpeta: {output_dir}")
        print(f"Archivo de respuestas creado en formato: {answers_format.upper()}")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
>>>>>>> da6a17fb926a5a85bd4d383ef80408fcec706452
    main()