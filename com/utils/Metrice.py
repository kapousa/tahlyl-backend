import json
import re


def extract_min_max(range_string: str) -> dict:
    # Use regular expression to find the numerical values
    match = re.search(r'(\d+\.?\d*) - (\d+\.?\d*)', range_string)
    if match:
        min_value_str, max_value_str = match.groups()
        min_value = float(min_value_str)
        max_value = float(max_value_str)
        return {"min": min_value, "max": max_value}
    else:
        return {"min": "Undefined", "max": "Undefined"}


def matric_string_to_dict(input_string):
    """
    Converts a string representing a dictionary of blood test results
    into a list of dictionaries, where each inner dictionary has a "name" key
    derived from the original top-level keys.

    Args:
        input_string: A string representing a dictionary.

    Returns:
        A string representing a list of dictionaries in the desired format,
        or None if the input string is not a valid dictionary.
    """
    try:
        data = json.loads(input_string.strip("'"))  # Remove surrounding quotes and parse
        output_list = []
        for name, values in data.items():
            values["name"] = name
            output_list.append(values)
        return output_list  # Return the Python list directly
    except json.JSONDecodeError:
        return None
