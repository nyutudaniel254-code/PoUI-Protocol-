def min_max_normalize(values):
    min_v = min(values.values())
    max_v = max(values.values())
    if min_v == max_v:
        return {k: 1.0 for k in values}
    return {k: (v - min_v) / (max_v - min_v) for k, v in values.items()}
