# Welcome to PyChase Wiki

**PyChase** is an advanced **Python duplicate code detector** and **code similarity tool** that hunts down structurally similar functions, methods, and classes across your codebase. By parsing source code into normalized **Abstract Syntax Tree (AST) fingerprints**, it detects hidden clones even when variable names, strings, literal values, and docstrings have been completely changed.

Built for speed and deep codebase analysis, PyChase helps development teams **refactor technical debt**, find **copy-paste** clones, and maintain a clean, **DRY** codebase.

## Quick Links

| Page | Description |
|---|---|
| [Getting Started](Getting-Started) | Install and run PyChase on your project |
| [CLI Reference](CLI-Reference) | Complete command-line options reference |
| [Configuration](Configuration) | Project configuration via pyproject.toml |
| [How It Works](How-It-Works) | AST normalization, MinHash, LSH explained |
| [Demo Test Suite](Demo-Test-Suite) | 14 progressive test files with results |
| [Comparison](Comparison-with-Other-Tools) | PyChase vs dry4python, jscpd, SonarQube, PMD CPD |
| [CI/CD & Workflows](CI-CD-Workflows) | GitHub Actions setup and automation |

## Key Features

- **AST-level analysis** — not tokens, not lines, full Python AST with normalization
- **Three clone types** — exact (Type-1), renamed (Type-2), modified (Type-3)
- **Multi-granularity** — functions, methods, and classes in one pass
- **MinHash + LSH** — near-linear scaling to 100k+ units
- **Multiple output formats** — text, JSON, CSV, HTML (interactive)
- **Zero dependencies** — pure Python, one `pip install`
