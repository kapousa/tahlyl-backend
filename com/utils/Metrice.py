import json
import re
import ast

def extract_min_max(range_string: str) -> dict:
    # Use regular expression to find the numerical values (e.g., "1.2 - 3.4")
    match = re.search(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', range_string)
    if match:
        min_value_str, max_value_str = match.groups()
        min_value = float(min_value_str)
        max_value = float(max_value_str)
        return {"min": min_value, "max": max_value}
    else:
        try:
            # Safely evaluate the string as a Python literal (dictionary)
            range_string_dict = ast.literal_eval(range_string)

            # Directly return the 'normal_range' dictionary for 'min'
            # and a fixed string for 'max' as per your request
            return {"min": str(range_string_dict.get("normal_range", "normal_range:?")), "max": "None"}

        except (ValueError, SyntaxError):
            # Handle cases where the string is not a valid Python literal or other parsing errors
            return {"min": "min:?", "max": "max:?"}



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
