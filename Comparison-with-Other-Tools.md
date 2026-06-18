# Comparison with Other Tools

## Overview

| Tool | Scope | Algorithm | Clone Types | Output |
|---|---|---|---|---|
| **PyChase** | Functions, methods, classes | MinHash+LSH, Jaccard | Type-1,2,3 | Text, JSON, CSV, HTML |
| **dry4python** | Functions only | Brute-force, Jaccard | Type-2 only | Text, JSON |
| **PMD CPD** | Cross-language | Karp-Rabin | Type-1,2 | Text, XML, CSV |
| **jscpd** | Cross-language (150+) | Token-based | Type-1,2 | Text, JSON, HTML |
| **SonarQube** | Cross-language | Custom AST matching | Type-1,2 | Web dashboard |
| **Duplo** | Lines only | Hash-based | Type-1 | Text |
| **Simian** | Lines/tokens | Hash-based | Type-1,2 | Text, XML |

## vs dry4python

| Dimension | dry4python | PyChase |
|---|---|---|
| Scope | Functions only | Functions, methods, classes |
| Algorithm | O(n²) brute-force | O(n) MinHash + LSH |
| Clone Types | Type-2 only | Type-1, Type-2, Type-3 |
| Output | Text, JSON | Text, JSON, CSV, HTML |
| AST Coverage | Basic | Full 3.10+ (match, async) |
| Setup | Zero deps | Zero deps |

## vs jscpd

| Dimension | jscpd | PyChase |
|---|---|---|
| Analysis | Token-based (shallow) | AST-based (structural) |
| Python Support | Generic tokenizer | Dedicated Python AST parser |
| Install | Requires Node.js | `pip install pychase` |
| Structural Similarity | ❌ | ✅ Normalized AST |
| Clone Grouping | Unstructured | Connected-component clusters |

## vs SonarQube

| Dimension | SonarQube | PyChase |
|---|---|---|
| Setup | Database + server + scanner | `pip install pychase` |
| Clone Detection | Basic heuristic | AST structural fingerprints |
| False Positive Control | Limited | Threshold + min-lines + min-nodes |
| Portability | Tied to server | Standalone CLI, any CI |
| Speed | Minutes (full pipeline) | Milliseconds |

## Why PyChase?

- ✅ **Python AST-level structural analysis** — not tokens, not lines
- ✅ **MinHash + LSH** — near-linear scaling to 100k+ units
- ✅ **Three clone types** — exact (Type-1), renamed (Type-2), modified (Type-3)
- ✅ **Multi-granularity** — functions + methods + classes
- ✅ **Interactive HTML reports** — collapsible groups, code previews
- ✅ **Zero external dependencies** — no JVM, no Node, no database
- ✅ **Python-first** — built specifically for Python AST
