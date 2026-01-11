"""
Time calculation utilities for exams.
"""


def calculate_exam_time(num_questions: int, minutes_per_question: int = 1) -> str:
    """Calculate exam duration and return formatted string.
    
    Args:
        num_questions: Number of questions in exam
        minutes_per_question: Minutes allocated per question (default 1)
        
    Returns:
        Formatted time string in Spanish (e.g., "45 minutos", "1 hora y 30 minutos")
    """
    total_minutes = num_questions * minutes_per_question
    
    if total_minutes < 60:
        return f"{total_minutes} minutos"
    
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    if minutes == 0:
        hora_str = "hora" if hours == 1 else "horas"
        return f"{hours} {hora_str}"
    
    hora_str = "hora" if hours == 1 else "horas"
    return f"{hours} {hora_str} y {minutes} minutos"
