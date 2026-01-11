"""
Main exam generation logic.
"""

import random
from typing import List, Dict, Tuple
from .shuffler import shuffle_question_options


def generate_exam(
    questions: List[Dict],
    num_questions: int,
    seed: str,
    option_letters: str = 'ABCD'
) -> Tuple[List[Dict], Dict[int, str]]:
    """Generate a single exam with shuffled questions and options.
    
    Args:
        questions: List of all available questions
        num_questions: Number of questions to include in exam
        seed: Seed for deterministic randomization
        option_letters: Letters to use for options (default 'ABCD')
        
    Returns:
        Tuple of (exam_questions, answers_dict)
        - exam_questions: List of questions with shuffled options
        - answers_dict: Dictionary mapping question_number -> correct_letter
    """
    random.seed(seed)
    
    # Select random questions
    selected_questions = random.sample(questions, min(num_questions, len(questions)))
    
    # Shuffle each question's options
    exam_questions = []
    answers = {}
    
    for idx, question in enumerate(selected_questions, 1):
        shuffled_options, new_correct_letter = shuffle_question_options(question, option_letters)
        
        exam_questions.append({
            'number': idx,
            'question': question['question'],
            'options': shuffled_options,
            'original_answer': question['answer']
        })
        
        answers[idx] = new_correct_letter
    
    return exam_questions, answers
