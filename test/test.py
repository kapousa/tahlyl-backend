import re

range_string = "Normal: 0.5 - 1.2 mg/dL"

# Use regular expression to find the numerical values
match = re.search(r'(\d+\.?\d*) - (\d+\.?\d*)', range_string)

if match:
    min_value_str, max_value_str = match.groups()
    min_value = float(min_value_str)
    max_value = float(max_value_str)
    print(f"Minimum value: {min_value}")
    print(f"Maximum value: {max_value}")
else:
    print("Could not extract the range from the string.")