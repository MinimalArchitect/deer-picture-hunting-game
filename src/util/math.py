def clip(value, min_value, max_value):
    """Clip a value to a range"""
    return max(min_value, min(value, max_value))
