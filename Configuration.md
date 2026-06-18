# Configuration

PyChase can be configured via `pyproject.toml` in your project root:

```toml
[tool.pychase]
threshold = 0.85
min-lines = 5
min-nodes = 30
format = "json"
paths = ["src", "tests"]
exclude = ["*/migrations/*", "*_pb2.py"]
```

## Configuration Rules

| Key | Default | Description |
|---|---|---|
| `threshold` | 0.82 | Minimum similarity score |
| `min-lines` | 4 | Minimum source lines per unit |
| `min-nodes` | 20 | Minimum normalized AST nodes |
| `format` | "text" | Output format |
| `paths` | ["."] | Files/directories to scan |
| `exclude` | [] | Glob patterns to exclude |
| `shingle-size` | 3 | AST k-shingle size |

## Precedence

Command-line arguments override pyproject.toml values. `--exclude` patterns are appended to configured excludes.

## Ignoring Code

```python
# pychase: ignore        — skip next function or entire file (line 1)
# pychase: ignore-file   — skip the entire file from any line
```
