"""Nested functions and comprehensions — tests depth handling."""

def process_dataframe_a(df):
    results = []
    for col in df.columns:
        if col.startswith("feature_"):
            values = [x * 2 for x in df[col] if x is not None]
            mean = sum(values) / len(values) if values else 0
            std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5 if values else 0
            results.append({"col": col, "mean": mean, "std": std})
    return results


def process_dataframe_b(df):
    results = []
    for col in df.columns:
        if col.startswith("metric_"):
            values = [x * 2 for x in df[col] if x is not None]
            mean = sum(values) / len(values) if values else 0
            std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5 if values else 0
            results.append({"col": col, "mean": mean, "std": std})
    return results


def outer_function_one(data):
    def inner_transform(item):
        return {"key": item.id, "value": item.data * 2}

    def inner_filter(item):
        return item.active and item.data > 0

    results = []
    for item in data:
        if inner_filter(item):
            results.append(inner_transform(item))
    return results


def outer_function_two(records):
    def inner_map(rec):
        return {"key": rec.uid, "value": rec.payload * 2}

    def inner_filter(rec):
        return rec.enabled and rec.payload > 0

    results = []
    for rec in records:
        if inner_filter(rec):
            results.append(inner_map(rec))
    return results
