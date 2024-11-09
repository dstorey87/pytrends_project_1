import json
import os

def save_data(filepath, data):
    """Save data to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to {filepath}: {e}")

def ensure_dir(directory):
    """Ensure a directory exists."""
    os.makedirs(directory, exist_ok=True)
