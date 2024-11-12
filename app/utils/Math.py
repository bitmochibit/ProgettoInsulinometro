def clamp(value, min_val, max_val):
    if value <= min_val:
        return min_val
    elif value >= max_val:
        return max_val

    return value