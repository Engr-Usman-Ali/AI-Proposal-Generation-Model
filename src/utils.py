# src/utils.py
import json
import os

def save_json(data, filename):
    """Save dictionary or list as JSON file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def append_text(text, filename):
    """Append proposal text to a .txt file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n\n" + "="*80 + "\n\n")
