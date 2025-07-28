from typing import List, Dict, Any


def get_unique_metric_names_from_list(data_list: List[Dict[str, Any]]) -> List[str]:
    """
    Extracts unique 'metric_name' values from a list of dictionaries.

    Args:
        data_list: A list of dictionaries, where each dictionary represents a metric
                   and is expected to have a 'metric_name' key.

    Returns:
        A list of unique metric names (strings) in arbitrary order.
        Returns an empty list if the input list is empty or no 'metric_name' keys are found.
    """
    unique_names = set()  # Use a set to automatically handle duplicates
    for item in data_list:
        if 'metric_name' in item:
            unique_names.add(item['metric_name'])

    # Convert the set back to a list before returning
    return list(unique_names)