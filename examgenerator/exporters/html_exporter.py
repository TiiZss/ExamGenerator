"""
HTML exporter for exam answers.
"""

import os
from datetime import datetime
from typing import List, Dict


def create_answers_html(all_exam_data: List[Dict], exam_prefix: str, output_dir: str) -> None:
    """Create an HTML file with all exam answers (transposed layout)."""
    # Import time calculation function
    from ..core.time_calculator import calculate_exam_time
    
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
