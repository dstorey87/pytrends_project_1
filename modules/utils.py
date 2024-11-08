# File: modules/utils.py

import json
import os
import pandas as pd

def load_data(filepath):
    """
    Load data from a JSON file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict or list: Data loaded from the file.
    """
    with open(filepath, "r") as file:
        return json.load(file)

def save_data(filepath, data):
    """
    Save data to a JSON file.

    Args:
        filepath (str): Path to save the file.
        data (dict or list): Data to save.
    """
    def default_converter(o):
        if isinstance(o, pd.Timestamp):
            return o.isoformat()  # Convert Timestamp to ISO 8601 string
        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4, default=default_converter)
