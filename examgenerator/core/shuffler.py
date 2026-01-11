"""
Shuffling utilities for exam generation.
"""

import random
from typing import List, Dict, Tuple


def shuffle_exam_questions(questions: List[Dict], seed: str) -> List[Dict]:
    """Shuffle questions for an exam using a deterministic seed.
    
    Args:
        questions: List of question dictionaries
        seed: Seed string for deterministic randomization
        
    Returns:
        Shuffled copy of questions list
    """
    random.seed(seed)
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return shuffled


def shuffle_question_options(question: Dict, option_letters: str = 'ABCD') -> Tuple[List[str], str]:
    """Shuffle options for a question and calculate new correct answer letter.
    
    Args:
        question: Question dictionary with 'options' and 'answer' keys
        option_letters: String of letters to use (default 'ABCD')
        
    Returns:
        Tuple of (shuffled_options, new_correct_letter)
    """
    correct_idx = option_letters.index(question['answer'])
    correct_answer_text = question['options'][correct_idx]
    
    shuffled_options = question['options'].copy()
    random.shuffle(shuffled_options)
    
    new_correct_letter = option_letters[shuffled_options.index(correct_answer_text)]
    
    return shuffled_options, new_correct_letter
