# How It Works

PyChase uses a multi-stage pipeline to detect structurally similar Python code:

## 1. Parse

Each `.py` file is parsed into a Python **Abstract Syntax Tree (AST)** using the standard `ast` module.

## 2. Normalize

Identifiers, variable names, function names, attribute names, string literals, numbers, and docstrings are replaced with generic placeholders. This strips away everything except the **structural shape** of the code.

Example — both functions produce the **same normalized AST**:

```python
def calculate_total(items, rate):
    subtotal = 0
    for item in items:
        subtotal += item.price
    tax = subtotal * rate
    return subtotal + tax

def compute_sum(products, factor):
    result = 0
    for product in products:
        result += product.cost
    fee = result * factor
    return result + fee
```

## 3. Shingle

The normalized AST node sequence is broken into overlapping **k-shingles** (default k=3):

```
(FunctionDef, arguments, arg) → (arguments, arg, Add) → (arg, Add, Name) → ...
```

Each shingle captures a tiny piece of structural grammar.

## 4. Fingerprint

The set of all shingles becomes a **structural fingerprint** — a unique identifier for the shape of a function, method, or class.

## 5. Match

**MinHash signatures** compress each fingerprint into a compact 256-bit signature. **Locality Sensitive Hashing (LSH)** indexes these signatures into buckets. Only units in the same bucket need to be compared — reducing candidate pairs from O(n²) to nearly O(n).

Each candidate pair receives a **Jaccard similarity score** (0.0 to 1.0) based on shared shingles vs total shingles.

## 6. Cluster

Connected-component clustering groups related matches. A group of 4 related functions appears once in the report rather than 6 separate pairwise entries.

## 7. Report

Results are rendered as text, JSON, CSV, or an interactive HTML report with collapsible groups and syntax-highlighted code previews.
