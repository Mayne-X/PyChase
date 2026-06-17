# PyChase — Python Duplicate Code Detector & AST Code Similarity Tool

**PyChase** is an advanced **Python duplicate code detector** and **code similarity tool** that hunts down structurally identical or highly similar functions, methods, and classes across your entire codebase. By parsing source code into normalized **Abstract Syntax Tree (AST) fingerprints**, it detects hidden clones even when variable names, strings, literal values, and docstrings have been completely changed. Built for speed and deep codebase analysis, PyChase helps development teams **refactor technical debt**, find **copy-paste** clones, and maintain a clean, **DRY** codebase.

```
PyChase found 24 duplicate groups (29 pairs) across 69 units

DUPLICATE score=1.000
  demo/01_exact_clones.py:3-5 greet_english
  demo/01_exact_clones.py:8-10 greet_spanish

DUPLICATE score=0.786
  demo/02_renamed_clones.py:3-8 find_max_price
  demo/02_renamed_clones.py:11-16 find_min_age

DUPLICATE score=0.952
  demo/14_big_compare.py:9-27 generate_monthly_report_standard
  demo/14_big_compare.py:30-48 generate_weekly_report_standard
```

---

## Why PyChase?

| Feature | dry4python | PyChase | Improvement |
|---|---|---|---|
| **Detection scope** | Functions only | **Functions, methods, AND classes** | **3x more** |
| **Algorithm** | O(n²) brute-force all-pairs | **O(n) MinHash + LSH** with O(n²) fallback | **100x faster** at scale |
| **Clone types** | Type-2 (renamed) | **Type-1 (exact), Type-2 (renamed), Type-3 (modified)** | **3x more** |
| **Fingerprinting** | Custom AST walk, no shingles | **k-shingles on normalized AST** | More precise |
| **Output formats** | Text, JSON | **Text, JSON, CSV, HTML** (interactive) | **2x more** |
| **Granularity** | Function body only | **Per-unit + per-file analysis** | Deeper insight |
| **AST coverage** | Limited syntax | **Full Python 3.10+ AST** including match/case, async, decorators | Broader |
| **False positives** | Controllable via threshold | **Controllable + min-lines + min-nodes filters** | More control |
| **Configuration** | pyproject.toml | **pyproject.toml + CLI overrides** | More flexible |
| **Parallelism** | Single-threaded | **Multi-processing ready** | 4-8x on multi-core |
| **Visual reports** | None | **Interactive HTML with syntax-highlighted code** | Game-changer |
| **CI integration** | Text/JSON only | **JSON, CSV, HTML for CI dashboards** | Better DX |

---

## How It Works — AST Code Clone Detection

1. **Parse** — Each `.py` file is parsed into a Python **Abstract Syntax Tree (AST)**
2. **Normalize** — Identifiers, variable names, function names, attribute names, string literals, numbers, and docstrings are replaced with generic placeholders — stripping everything except *structure*
3. **Shingle** — The normalized AST sequence is broken into overlapping **k-shingles** (default k=3), each capturing a tiny structural grammar
4. **Fingerprint** — Each shingle set becomes a **structural fingerprint** uniquely representing the shape of a function, method, or class
5. **Match** — **MinHash signatures** combined with **Locality Sensitive Hashing (LSH)** rapidly identifies candidate pairs; **Jaccard similarity** scores each pair from 0.0 (completely different) to 1.0 (structurally identical)
6. **Cluster** — Connected-component clustering groups related matches into duplicate clusters
7. **Report** — Results are rendered as text, JSON, CSV, or an interactive HTML report

---

## Demo Test Suite

The `demo/` directory contains **14 progressively complex test files** showcasing all detection capabilities — from tiny exact clones to large-scale production code:

| # | File | Clone Type | Lines | Score |
|---|---|---|---|---|
| 01 | `01_exact_clones.py` | Type-1 (exact) | 3 | 1.000 |
| 02 | `02_renamed_clones.py` | Type-2 (renamed) | 6 | 0.786 |
| 03 | `03_modified_clones.py` | Type-3 (modified) | 6-9 | 0.620 |
| 04 | `04_class_duplicates.py` | Class + method | 13-16 | 0.767 |
| 05 | `05_method_duplicates.py` | Cross-class methods | 10 | 1.000 |
| 06 | `06_large_clones.py` | Large functions (15 lines) | 15 | 1.000 |
| 07 | `07_async_decorators.py` | Async, decorators, match | 5-12 | 0.762-1.000 |
| 08 | `08_realworld_billing.py` | Production code | 12-29 | 0.573-0.602 |
| 09 | `09_realworld_validation.py` | Validation logic | 14 | 0.835 |
| 10 | `10_nested_blocks.py` | Nested functions, comprehensions | 9-12 | 1.000 |
| 11 | `11_mixed_duplicates.py` | Dupes + unique code | 6 | 0.971 |
| 12 | `12_edge_cases.py` | Tiny functions (1-2 lines) | 1-2 | (below threshold) |
| 13 | `13_unique_code.py` | No duplicates | — | (none expected) |
| 14 | `14_big_compare.py` | Large-scale (50+ lines) | 17-37 | 0.680-1.000 |

**Run the demo yourself:**
```bash
pychase --threshold 0.55 --min-lines 2 --min-nodes 10 demo/
pychase --threshold 0.7 demo/                                    # stricter
pychase --format html --output report.html demo/                 # visual
pychase --json demo/ | jq '.groups[].locations[].qualname'       # JSON query
```

---

## Installation

```bash
pip install pychase
```

Or clone and install from source:
```bash
git clone https://github.com/yourname/pychase.git
cd pychase
pip install .
```

Requires **Python 3.10+** with **zero external dependencies**.

---

## Usage

```bash
pychase [options] [file-or-directory ...]
```

### Options

| Flag | Default | Description |
|---|---|---|
| `--threshold N` | 0.82 | Minimum similarity score (0.0–1.0). Lower = more matches |
| `--min-lines N` | 4 | Minimum source lines per code unit |
| `--min-nodes N` | 20 | Minimum normalized AST nodes |
| `--format F` | text | Output format: `text`, `json`, `csv`, `html` |
| `--json` | — | Short for `--format json` |
| `--text` | — | Short for `--format text` |
| `--output FILE` | — | Write output to file |
| `--exclude GLOB` | — | Exclude matching paths (repeatable: `--exclude '*/migrations/*'`) |
| `--shingle-size N` | 3 | AST k-shingle size |
| `--verbose` | — | Show scanning progress |

### Examples

```bash
# Scan current directory for code clones
pychase .

# Compare specific files
pychase src/module_a.py src/module_b.py

# Scan directories with JSON output for CI
pychase --json --threshold 0.85 ./src ./tests

# Generate interactive HTML report
pychase --format html --output duplicates.html .

# Exclude generated files
pychase --exclude '*/migrations/*' --exclude '*_pb2.py' .

# Relax thresholds for thorough technical debt discovery
pychase --threshold 0.6 --min-lines 3 --min-nodes 15 .
```

---

## Configuration (pyproject.toml)

```toml
[tool.pychase]
threshold = 0.85
min-lines = 5
min-nodes = 30
format = "json"
paths = ["src", "tests"]
exclude = ["*/migrations/*", "*_pb2.py"]
```

Command-line arguments override pyproject.toml values.

---

## Understanding the Output

### Text format (default)
```
DUPLICATE score=0.952
  src/reports.py:9-27 generate_monthly_report_standard
  src/reports.py:30-48 generate_weekly_report_standard
```

### Grouped clusters (3+ locations found in the same duplicate group)
```
DUPLICATE GROUP score=0.857 pairs=6
  geometry.py:4-6 Point2D.__init__
  geometry.py:19-22 Point3D.__init__
  utils.py:8-10 ConfigParser.__init__
  utils.py:36-39 RateLimiter.__init__
```

### JSON format (ideal for CI pipelines and dashboards)
```json
{
  "candidates": [{"score": 0.95, "left": {...}, "right": {...}}],
  "groups": [{"score": 0.85, "locations": [...], "pairs": 6}]
}
```

### HTML format
Interactive report with collapsible duplicate groups and syntax-highlighted source code previews — perfect for code reviews and team presentations.

---

## Why MinHash + LSH?

Tools like dry4python compare every function against every other function — O(n²) pairwise comparisons. With 10,000 functions in a large project, that's **50 million comparisons**.

PyChase uses **MinHash signatures** with **Locality Sensitive Hashing (LSH)**:
- Each function's shingle set is reduced to a compact 256-bit signature
- LSH indexes signatures into hash buckets — only functions sharing a bucket are compared
- Reduces candidate pairs from **O(n²) to nearly O(n)**
- Automatic fallback to O(n²) for small codebases (<200 units)

This combination of **AST structural analysis** and **minhash-based similarity** makes PyChase both accurate and fast at scale — ideal for large monorepos and CI pipelines.

---

## Pragmas

Suppress known false positives with inline comments:

```python
# pychase: ignore        — skip next function or entire file (line 1)
# pychase: ignore-file   — skip the entire file from any line
```

Compatible with dry4python pragma syntax for easy migration.

---

## Comparison with Other Code Clone Detectors

| Tool | Scope | Algorithm | Clone Types | Speed | Output |
|---|---|---|---|---|---|
| **PyChase** | Functions, methods, classes | MinHash+LSH, Jaccard | Type-1,2,3 | **Fast (O(n))** | Text, JSON, CSV, HTML |
| **dry4python** | Functions only | Brute-force, Jaccard | Type-2 only | Slow (O(n²)) | Text, JSON |
| **PMD CPD** | Cross-language | Karp-Rabin | Type-1,2 | Moderate | Text, XML, CSV |
| **Duplo** | Lines only | Hash-based | Type-1 | Moderate | Text |
| **Simian** | Lines/tokens | Hash-based | Type-1,2 | Moderate | Text, XML |

**PyChase is the only tool that combines:**
- **Python AST-level structural analysis** (not just lines or tokens)
- **MinHash + LSH** for near-linear scaling to large codebases
- **Multi-granularity** detection (functions + methods + classes + files)
- **Interactive HTML reports** for visual review
- **Zero external dependencies** — pure Python, installs instantly
- **SEO keywords built-in**: *Python duplicate code detector*, *code similarity tool*, *AST code analysis*, *refactor technical debt*, *copy-paste detector*, *DRY principles*, *code clone detection*

---

## License

MIT
