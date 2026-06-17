import ast
import json
import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

# ── AST Normalization ──────────────────────────────────────────────────────────

_NORMALIZED = (
    ast.Name, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
    ast.Attribute, ast.arg, ast.keyword, ast.Constant,
    ast.Str, ast.Bytes, ast.Num, ast.NameConstant,
)


def _walk(node, depth=0):
    for child in ast.iter_child_nodes(node):
        yield from _walk(child, depth + 1)


def normalize(node):
    seq = []
    stack = [(node, 0)]
    while stack:
        n, d = stack.pop()
        name = type(n).__name__
        if isinstance(n, (ast.Constant,)):
            seq.append((d, name))
        elif isinstance(n, _NORMALIZED):
            seq.append((d, name))
        elif isinstance(n, (ast.operator, ast.cmpop, ast.boolop, ast.unaryop)):
            seq.append((d, type(n).__name__))
        elif isinstance(n, ast.expr_context):
            seq.append((d, name))
        else:
            seq.append((d, name))
        children = list(ast.iter_child_nodes(n))
        for c in reversed(children):
            stack.append((c, d + 1))
    return seq


def shingles(seq, k=3):
    seen = set()
    for i in range(len(seq) - k + 1):
        s = tuple(seq[i:i + k])
        seen.add(s)
    return frozenset(seen)


# ── MinHash ────────────────────────────────────────────────────────────────────

class MinHash:
    def __init__(self, num_perm=256, seed=42):
        self.num_perm = num_perm
        import random
        rng = random.Random(seed)
        self.a = rng.sample(range(1, 1 << 31), num_perm)
        self.b = rng.sample(range(0, 1 << 31), num_perm)
        self.mod = (1 << 32) - 1

    def sig(self, shs):
        sig = [self.mod] * self.num_perm
        for sh in shs:
            h = hash(sh) & self.mod
            if h == 0:
                h = 1
            for i in range(self.num_perm):
                v = (self.a[i] * h + self.b[i]) % self.mod
                if v < sig[i]:
                    sig[i] = v
        return tuple(sig)


# ── LSH ────────────────────────────────────────────────────────────────────────

class LSH:
    def __init__(self, bands=16, rows=16):
        self.bands = bands
        self.rows = rows
        self._buckets = [defaultdict(set) for _ in range(bands)]

    def index(self, key, sig):
        for b in range(self.bands):
            h = hash(sig[b * self.rows:(b + 1) * self.rows])
            self._buckets[b][h].add(key)

    def candidates(self):
        seen = set()
        for band in self._buckets:
            for bucket in band.values():
                items = sorted(bucket)
                for i in range(len(items)):
                    for j in range(i + 1, len(items)):
                        pair = (items[i], items[j])
                        if pair not in seen:
                            seen.add(pair)
                            yield pair


# ── Unit extraction ────────────────────────────────────────────────────────────

def _ignore_line(source, lineno):
    lines = source.splitlines()
    for i in range(max(0, lineno - 2), lineno):
        if i < len(lines) and "dry4python: ignore" in lines[i]:
            return True
    return False


def _extract(node, prefix, source, filepath, cfg):
    units = []
    stack = [(node, prefix)]
    while stack:
        n, pfx = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            qn = f"{pfx}.{n.name}" if pfx else n.name
            if _ignore_line(source, n.lineno):
                continue
            ns = normalize(n)
            sl = n.lineno
            el = n.end_lineno or sl
            nl = el - sl + 1
            if nl >= cfg.min_lines and len(ns) >= cfg.min_nodes:
                units.append({
                    "file": filepath, "qualname": qn,
                    "start_line": sl, "end_line": el,
                    "num_lines": nl, "num_nodes": len(ns),
                    "seq": ns,
                })
            continue
        if isinstance(n, ast.ClassDef):
            qn = f"{pfx}.{n.name}" if pfx else n.name
            ns = normalize(n)
            sl = n.lineno
            el = n.end_lineno or sl
            nl = el - sl + 1
            if nl >= cfg.min_lines and len(ns) >= cfg.min_nodes:
                units.append({
                    "file": filepath, "qualname": qn,
                    "start_line": sl, "end_line": el,
                    "num_lines": nl, "num_nodes": len(ns),
                    "seq": ns,
                })
            children = list(ast.iter_child_nodes(n))
            for c in reversed(children):
                stack.append((c, qn))
        else:
            for c in reversed(list(ast.iter_child_nodes(n))):
                stack.append((c, pfx))
    return units


def analyze_file(filepath, cfg):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception:
        return [], []

    lines = source.splitlines()
    if lines and "dry4python: ignore" in lines[0]:
        return [], []

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return [], []

    units = []
    for child in ast.iter_child_nodes(tree):
        units.extend(_extract(child, "", source, filepath, cfg))

    return units, source


# ── Similarity ─────────────────────────────────────────────────────────────────

def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ── Clustering ─────────────────────────────────────────────────────────────────

def cluster(pairs):
    adj = defaultdict(set)
    for i, p in enumerate(pairs):
        lk = (p["left"]["file"], p["left"]["qualname"], p["left"]["start_line"])
        rk = (p["right"]["file"], p["right"]["qualname"], p["right"]["start_line"])
        adj[lk].add(rk)
        adj[rk].add(lk)

    visited = set()
    groups = []

    for start in adj:
        if start in visited:
            continue
        q = [start]
        comp = set()
        while q:
            k = q.pop()
            if k in visited:
                continue
            visited.add(k)
            comp.add(k)
            q.extend(adj[k] - visited)

        gp = []
        for i, p in enumerate(pairs):
            lk = (p["left"]["file"], p["left"]["qualname"], p["left"]["start_line"])
            rk = (p["right"]["file"], p["right"]["qualname"], p["right"]["start_line"])
            if lk in comp or rk in comp:
                gp.append(i)

        if gp:
            avg = sum(pairs[i]["score"] for i in gp) / len(gp)
            locs = {}
            for i in gp:
                locs[json.dumps(pairs[i]["left"], sort_keys=True)] = pairs[i]["left"]
                locs[json.dumps(pairs[i]["right"], sort_keys=True)] = pairs[i]["right"]
            groups.append({"score": avg, "locations": list(locs.values()), "pairs": len(gp)})

    return groups


# ── Main ───────────────────────────────────────────────────────────────────────

def find(files, cfg):
    all_units = []
    sources = {}

    for fp in files:
        units, src = analyze_file(fp, cfg)
        if units:
            sources[fp] = src
            for u in units:
                shs = shingles(u["seq"], cfg.shingle_size)
                u["shingles"] = shs
                uid = (fp, u["qualname"], u["start_line"])
                all_units.append((uid, u))

    n = len(all_units)
    pairs = []

    # Use MinHash + LSH for large datasets; brute-force for small ones
    if n > 200:
        minh = MinHash(cfg.num_perm, 42)
        lsh = LSH(cfg.num_bands, cfg.rows_per_band)
        for uid, u in all_units:
            sig = minh.sig(u["shingles"])
            lsh.index(uid, sig)

        umap = dict(all_units)
        for uid_a, uid_b in lsh.candidates():
            ua = umap[uid_a]
            ub = umap[uid_b]
            score = jaccard(ua["shingles"], ub["shingles"])
            if score >= cfg.threshold:
                pairs.append({
                    "score": score,
                    "left": {"file": ua["file"], "start_line": ua["start_line"],
                             "end_line": ua["end_line"], "qualname": ua["qualname"],
                             "nodes": ua["num_nodes"]},
                    "right": {"file": ub["file"], "start_line": ub["start_line"],
                              "end_line": ub["end_line"], "qualname": ub["qualname"],
                              "nodes": ub["num_nodes"]},
                })
    else:
        # Brute-force O(n^2) for small codebases
        for i in range(n):
            uid_a, ua = all_units[i]
            for j in range(i + 1, n):
                uid_b, ub = all_units[j]
                score = jaccard(ua["shingles"], ub["shingles"])
                if score >= cfg.threshold:
                    pairs.append({
                        "score": score,
                        "left": {"file": ua["file"], "start_line": ua["start_line"],
                                 "end_line": ua["end_line"], "qualname": ua["qualname"],
                                 "nodes": ua["num_nodes"]},
                        "right": {"file": ub["file"], "start_line": ub["start_line"],
                                  "end_line": ub["end_line"], "qualname": ub["qualname"],
                                  "nodes": ub["num_nodes"]},
                    })

    groups = cluster(pairs)

    return {
        "pairs": pairs,
        "groups": groups,
        "total_units": len(all_units),
        "sources": sources,
    }
