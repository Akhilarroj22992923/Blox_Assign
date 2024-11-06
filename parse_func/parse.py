import json
from decimal import Decimal

def parse_json(file_path):
    """
    Parses a JSON file into a Python object with arbitrary precision for integers
    and floating points using Decimal.
    """
    def parse_decimal(obj):
        if isinstance(obj, list):
            return [parse_decimal(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: parse_decimal(value) for key, value in obj.items()}
        elif isinstance(obj, (float, int)):
            return Decimal(str(obj))  # Ensures arbitrary precision
        return obj

    # Load JSON data from the file with custom decimal handling
    with open(file_path, 'r') as file:
        parsed_data = json.load(file, parse_float=Decimal, parse_int=Decimal)
    
    return parse_decimal(parsed_data)

# Example usage
if __name__ == "__main__":
    # parsed_object = parse_json("../string.json")
    parsed_object = parse_json("C:/Users/rasika sikaMANI/Downloads/Blox_Assign/string.json")

    print(parsed_object)
