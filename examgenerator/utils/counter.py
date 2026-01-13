
import json
import os
from pathlib import Path

STATS_FILE = Path('/app/config/stats.json')

def get_exam_count():
    """Get the total number of exams generated."""
    if not STATS_FILE.exists():
        return 0
    
    try:
        with open(STATS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('total_exams', 0)
    except Exception:
        return 0

def increment_exam_count(amount=1):
    """Increment the total number of exams generated."""
    current = get_exam_count()
    new_count = current + amount
    
    try:
        # Ensure dir exists
        STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(STATS_FILE, 'w') as f:
            json.dump({'total_exams': new_count}, f)
    except Exception as e:
        print(f"Error saving stats: {e}")
        
    return new_count
