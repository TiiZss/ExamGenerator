"""
CSV exporter for exam answers.
"""

import os
import csv
from typing import List, Dict


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
