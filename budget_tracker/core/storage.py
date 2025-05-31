import json
from pathlib import Path

DATA_FILE = Path("data/transactions.json")

# Ensure data file exists
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]")

def load_data():
    """Load transactions from JSON file."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(data):
    """Write transactions to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)