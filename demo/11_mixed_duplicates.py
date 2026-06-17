"""Mixed bag: some duplicates, some unique code — tests precision."""

def safe_divide(a, b):
    if b == 0:
        return None
    return a / b


def safe_subtract(a, b):
    if b == 0:
        return a
    return a - b


def unique_algorithm_one(x):
    """This function is unique — should not match anything."""
    result = 0
    for i in range(x):
        for j in range(i):
            result += i * j
    return result


def unique_algorithm_two(y):
    """Also unique — completely different structure."""
    seen = set()
    stack = [y]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(getattr(node, "children", []))
    return len(seen)


def fetch_and_cache(url, cache):
    if url in cache:
        return cache[url]
    data = fetch(url)
    cache[url] = data
    return data


def compute_and_cache(key, cache, compute_fn):
    if key in cache:
        return cache[key]
    data = compute_fn(key)
    cache[key] = data
    return data


def fetch(url):
    return f"data from {url}"
