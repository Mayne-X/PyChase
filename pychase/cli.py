import argparse
import fnmatch
import os
import sys
import glob
from pathlib import Path

from pychase.engine import find
from pychase.formatter import dispatch


class Config:
    def __init__(self):
        self.threshold = 0.82
        self.min_lines = 4
        self.min_nodes = 20
        self.format = "text"
        self.output = None
        self.exclude = []
        self.shingle_size = 3
        self.num_perm = 256
        self.num_bands = 16
        self.rows_per_band = 16
        self.paths = ["."]
        self.verbose = False

    @classmethod
    def from_pyproject(cls, path=None):
        cfg = cls()
        if path is None:
            path = cls._find_pyproject()
        if path and os.path.isfile(path):
            try:
                import tomllib
            except ImportError:
                try:
                    import tomli as tomllib
                except ImportError:
                    return cfg
            try:
                with open(path, "rb") as f:
                    data = tomllib.load(f)
                tool = data.get("tool", {}).get("pychase", {})
                for key, val in tool.items():
                    k = key.replace("-", "_")
                    if hasattr(cfg, k):
                        setattr(cfg, k, val)
                if tool.get("paths"):
                    cfg.paths = tool["paths"]
            except Exception:
                pass
        return cfg

    @staticmethod
    def _find_pyproject():
        cwd = os.getcwd()
        for parent in [cwd] + list(Path(cwd).parents):
            candidate = os.path.join(str(parent), "pyproject.toml")
            if os.path.isfile(candidate):
                return candidate
        return None


def _collect_files(paths, excludes):
    files = []
    seen = set()
    patterns = ["**/*.py"]
    for p in paths:
        if os.path.isfile(p):
            if p.endswith(".py"):
                files.append(p)
        elif os.path.isdir(p):
            for pat in patterns:
                for f in glob.glob(os.path.join(p, pat), recursive=True):
                    f = os.path.normpath(f)
                    if f.endswith(".py"):
                        files.append(f)
        else:
            for pat in patterns:
                for f in glob.glob(os.path.join(p, pat), recursive=True):
                    f = os.path.normpath(f)
                    if f.endswith(".py"):
                        files.append(f)

    # Remove duplicates
    files = list(dict.fromkeys(files))

    # Apply excludes
    if excludes:
        filtered = []
        for f in files:
            skip = False
            for ex in excludes:
                if fnmatch.fnmatch(f, ex) or fnmatch.fnmatch(os.path.basename(f), ex):
                    skip = True
                    break
            if not skip:
                filtered.append(f)
        files = filtered

    # Skip common dirs
    skip_dirs = {".git", ".venv", "venv", "__pycache__", "__pypackages__",
                 ".eggs", "migrations", "build", "dist", ".mypy_cache",
                 ".pytest_cache", ".tox", "node_modules", ".idea"}
    skip_patterns = ["*_pb2.py", "*_pb2_grpc.py", "*_generated.py"]
    filtered = []
    for f in files:
        parts = f.replace("\\", "/").split("/")
        if any(d in skip_dirs for d in parts):
            continue
        if any(fnmatch.fnmatch(os.path.basename(f), pat) for pat in skip_patterns):
            continue
        filtered.append(f)

    return sorted(filtered)


def main():
    cfg = Config.from_pyproject()

    parser = argparse.ArgumentParser(
        description="PyChase - chases down duplicate and structurally similar Python code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pychase .
  pychase src/foo.py src/bar.py
  pychase --json --threshold 0.9 ./src ./tests
  pychase --format html --output report.html .
  pychase --exclude '*/migrations/*' .
        """,
    )
    parser.add_argument("paths", nargs="*", default=None,
                        help="Files or directories to scan (default: .)")
    parser.add_argument("--threshold", type=float, default=cfg.threshold,
                        help=f"Minimum similarity score (default: {cfg.threshold})")
    parser.add_argument("--min-lines", type=int, default=cfg.min_lines,
                        help=f"Minimum source lines per function (default: {cfg.min_lines})")
    parser.add_argument("--min-nodes", type=int, default=cfg.min_nodes,
                        help=f"Minimum normalized AST nodes (default: {cfg.min_nodes})")
    parser.add_argument("--format", choices=["text", "json", "csv", "html"],
                        default=cfg.format,
                        help=f"Output format (default: {cfg.format})")
    parser.add_argument("--json", action="store_true", default=False,
                        help="Short for --format json")
    parser.add_argument("--text", action="store_true", default=False,
                        help="Short for --format text")
    parser.add_argument("--output", "-o", default=None,
                        help="Write output to file (implies --format html for .html)")
    parser.add_argument("--exclude", action="append", default=[],
                        help="Exclude paths matching glob (can be repeated)")
    parser.add_argument("--shingle-size", type=int, default=cfg.shingle_size,
                        help=f"AST shingle size (default: {cfg.shingle_size})")
    parser.add_argument("--verbose", "-v", action="store_true", default=False,
                        help="Verbose output")

    args = parser.parse_args()

    # Merge config: CLI overrides pyproject.toml
    cfg.threshold = args.threshold
    cfg.min_lines = args.min_lines
    cfg.min_nodes = args.min_nodes
    cfg.shingle_size = args.shingle_size
    cfg.verbose = args.verbose

    if args.json:
        cfg.format = "json"
    elif args.text:
        cfg.format = "text"
    else:
        cfg.format = args.format
    if args.output:
        cfg.output = args.output
        if args.output.endswith(".html") and not args.format:
            cfg.format = "html"

    if args.exclude:
        cfg.exclude = (cfg.exclude or []) + args.exclude

    if args.paths:
        cfg.paths = args.paths

    files = _collect_files(cfg.paths, cfg.exclude)

    if cfg.verbose:
        print(f"Scanning {len(files)} files...", file=sys.stderr)

    if not files:
        print("No Python files found.")
        return

    result = find(files, cfg)

    if cfg.verbose:
        units = result["total_units"]
        pairs = len(result["pairs"])
        groups = len(result["groups"])
        print(f"Found {units} units, {pairs} candidate pairs, {groups} groups", file=sys.stderr)

    dispatch(result, cfg.format, output=cfg.output)


if __name__ == "__main__":
    main()
