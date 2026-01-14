import math

def make_json_safe(value):
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
    return value
