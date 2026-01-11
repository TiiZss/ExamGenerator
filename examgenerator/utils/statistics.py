"""
Generador de estadísticas para exámenes.
"""

from typing import List, Dict, Any
from collections import Counter
from ..utils.logging_config import get_logger

logger = get_logger('statistics')


def generate_exam_statistics(all_exam_data: List[Dict]) -> Dict[str, Any]:
    """
    Genera estadísticas detalladas sobre los exámenes generados.
    
    Args:
        all_exam_data: Lista de datos de todos los exámenes
    
    Returns:
        Diccionario con estadísticas
    """
    if not all_exam_data:
        return {}
    
    stats = {
        'total_exams': len(all_exam_data),
        'total_questions': 0,
        'answer_distribution': {},
        'question_reuse': Counter(),
        'warnings': []
    }
    
    # Contar respuestas y uso de preguntas
    all_answers = []
    for exam in all_exam_data:
        answers = exam.get('answers', [])
        stats['total_questions'] += len(answers)
        all_answers.extend(answers)
        
        # Contar reutilización de preguntas
        for question in exam.get('questions', []):
            q_text = question.get('question', '')[:50]  # Primeros 50 caracteres como ID
            stats['question_reuse'][q_text] += 1
    
    # Calcular distribución de respuestas
    answer_counts = Counter(all_answers)
    total_answers = len(all_answers)
    
    if total_answers > 0:
        for letter in sorted(answer_counts.keys()):
            count = answer_counts[letter]
            percentage = (count / total_answers) * 100
            stats['answer_distribution'][letter] = {
                'count': count,
                'percentage': round(percentage, 2)
            }
        
        # Detectar desbalance
        percentages = [d['percentage'] for d in stats['answer_distribution'].values()]
        if percentages:
            min_pct, max_pct = min(percentages), max(percentages)
            if min_pct < 15 or max_pct > 35:
                stats['warnings'].append(
                    "Distribución de respuestas desbalanceada. "
                    f"Rango: {min_pct:.1f}% - {max_pct:.1f}%"
                )
    
    # Analizar reutilización
    reuse_values = list(stats['question_reuse'].values())
    if reuse_values:
        max_reuse = max(reuse_values)
        avg_reuse = sum(reuse_values) / len(reuse_values)
        stats['question_reuse_stats'] = {
            'max_times_used': max_reuse,
            'avg_times_used': round(avg_reuse, 2),
            'unique_questions': len(stats['question_reuse'])
        }
    
    logger.debug(f"Estadísticas generadas para {stats['total_exams']} exámenes")
    return stats


def print_statistics(stats: Dict[str, Any]):
    """
    Imprime estadísticas de forma visual.
    
    Args:
        stats: Diccionario con estadísticas
    """
    if not stats:
        return
    
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DE GENERACIÓN")
    print("="*60)
    
    print(f"\n📝 Resumen:")
    print(f"  • Total de exámenes: {stats['total_exams']}")
    print(f"  • Total de preguntas: {stats['total_questions']}")
    
    if 'question_reuse_stats' in stats:
        print(f"\n🔄 Reutilización de preguntas:")
        print(f"  • Preguntas únicas: {stats['question_reuse_stats']['unique_questions']}")
        print(f"  • Uso promedio: {stats['question_reuse_stats']['avg_times_used']:.1f} veces")
        print(f"  • Uso máximo: {stats['question_reuse_stats']['max_times_used']} veces")
    
    if stats['answer_distribution']:
        print(f"\n📈 Distribución de respuestas correctas:")
        for letter, data in sorted(stats['answer_distribution'].items()):
            bar_length = int(data['percentage'] / 2)  # Escala a 50 caracteres max
            bar = '█' * bar_length
            print(f"  {letter}) {bar:<25} {data['percentage']:5.1f}% ({data['count']} preguntas)")
    
    # Mostrar advertencias
    if stats['warnings']:
        print(f"\n⚠️  ADVERTENCIAS:")
        for warning in stats['warnings']:
            print(f"  • {warning}")
    
    print("="*60 + "\n")


def save_statistics_to_file(stats: Dict[str, Any], output_dir: str):
    """
    Guarda estadísticas en un archivo JSON.
    
    Args:
        stats: Diccionario con estadísticas
        output_dir: Directorio de salida
    """
    import json
    from pathlib import Path
    from datetime import datetime
    
    stats_file = Path(output_dir) / "statistics.json"
    
    # Agregar metadata
    stats['generated_at'] = datetime.now().isoformat()
    
    # Convertir Counter a dict para JSON
    if 'question_reuse' in stats:
        stats['question_reuse'] = dict(stats['question_reuse'])
    
    try:
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        logger.info(f"Estadísticas guardadas en: {stats_file}")
    except Exception as e:
        logger.error(f"Error guardando estadísticas: {e}")
