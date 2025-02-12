import re
import numpy as np

def extract_sql_query(response: str) -> str | None:
    pattern = r"```(?:sql)?\s*(.*?)\s*```"
    match = re.search(pattern, response, re.DOTALL)
    return match.group(1).strip() if match else None

def convert_numpy_arrays(data):
        if isinstance(data, dict):
            return {k: convert_numpy_arrays(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [convert_numpy_arrays(x) for x in data]
        elif isinstance(data, np.ndarray):
            return data.tolist()
        else:
            return data