# Demo Test Suite

The `demo/` directory contains **14 progressively complex test files** that showcase all detection capabilities:

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
| 10 | `10_nested_blocks.py` | Nested fns, comprehensions | 9-12 | 1.000 |
| 11 | `11_mixed_duplicates.py` | Dupes + unique code | 6 | 0.971 |
| 12 | `12_edge_cases.py` | Tiny functions (1-2 lines) | 1-2 | (below threshold) |
| 13 | `13_unique_code.py` | No duplicates | — | (none expected) |
| 14 | `14_big_compare.py` | Large-scale (50+ lines) | 17-37 | 0.680-1.000 |

## Run the Demo

```bash
# Comprehensive scan
pychase --threshold 0.55 --min-lines 2 --min-nodes 10 demo/

# Default scan
pychase --threshold 0.7 demo/

# HTML report
pychase --format html --output demo_report.html demo/
```

## Sample Results (threshold 0.55)

```
PyChase found 24 duplicate groups (29 pairs) across 69 units

DUPLICATE score=1.000
  demo/01_exact_clones.py:3-5 greet_english
  demo/01_exact_clones.py:8-10 greet_spanish

DUPLICATE score=0.971
  demo/11_mixed_duplicates.py:37-42 fetch_and_cache
  demo/11_mixed_duplicates.py:45-50 compute_and_cache

DUPLICATE score=0.952
  demo/14_big_compare.py:9-27 generate_monthly_report_standard
  demo/14_big_compare.py:30-48 generate_weekly_report_standard
```
