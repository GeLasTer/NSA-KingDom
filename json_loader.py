import json
from user import User
from graph import Graph

class JSONLoader:

    @staticmethod
    def load_from_file(filepath):
    
        # =====================================================
        # Read file
        # =====================================================
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filepath} not found!")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format!")

        # =====================================================
        # Initial validation
        # =====================================================
        if 'users' not in data or 'relations' not in data:
            raise ValueError("Dataset must contain 'users' and 'relations' keys!")

        if not isinstance(data['users'], list) or not isinstance(data['relations'], list):
            raise ValueError("'users' and 'relations' must be lists!")

       

        