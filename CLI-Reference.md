# CLI Reference

## Usage

```bash
pychase [options] [file-or-directory ...]
```

## Options

| Flag | Default | Description |
|---|---|---|
| `--threshold N` | 0.82 | Minimum similarity score (0.0–1.0). Lower = more matches |
| `--min-lines N` | 4 | Minimum source lines per code unit |
| `--min-nodes N` | 20 | Minimum normalized AST nodes |
| `--format F` | text | Output format: `text`, `json`, `csv`, `html` |
| `--json` | — | Short for `--format json` |
| `--text` | — | Short for `--format text` |
| `--output FILE` | — | Write output to file |
| `--exclude GLOB` | — | Exclude matching paths (repeatable) |
| `--shingle-size N` | 3 | AST k-shingle size |
| `--verbose` | — | Show scanning progress |

## Examples

```bash
# Scan current directory
pychase .

# Scan with JSON output for CI
pychase --json --threshold 0.85 ./src ./tests

# Generate HTML report
pychase --format html --output report.html .

# Exclude generated files
pychase --exclude '*/migrations/*' --exclude '*_pb2.py' .

# Relax thresholds for thorough discovery
pychase --threshold 0.6 --min-lines 3 --min-nodes 15 .
```

## Configuration

See [Configuration](Configuration) for pyproject.toml setup.
