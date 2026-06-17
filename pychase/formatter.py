import json
import html
import os

# ── Text ───────────────────────────────────────────────────────────────────────

def format_text(result):
    lines = []
    groups = result.get("groups", [])
    pairs = result.get("pairs", [])
    lines.append(f"PyChase found {len(groups)} duplicate groups ({len(pairs)} pairs) across {result['total_units']} units")
    lines.append("")

    for g in groups:
        locs = g["locations"]
        score = g["score"]
        if g["pairs"] > 1:
            lines.append(f"DUPLICATE GROUP score={score:.3f} pairs={g['pairs']}")
            for loc in locs:
                lines.append(f"  {loc['file']}:{loc['start_line']}-{loc['end_line']} {loc['qualname']}")
        else:
            lines.append(f"DUPLICATE score={score:.3f}")
            for loc in locs:
                lines.append(f"  {loc['file']}:{loc['start_line']}-{loc['end_line']} {loc['qualname']}")
        lines.append("")

    return "\n".join(lines)


def print_text(result):
    print(format_text(result))


# ── JSON ───────────────────────────────────────────────────────────────────────

def format_json(result):
    out = {
        "candidates": result["pairs"],
        "groups": result["groups"],
    }
    return json.dumps(out, indent=2)


def print_json(result):
    print(format_json(result))


# ── CSV ───────────────────────────────────────────────────────────────────────

def format_csv(result):
    lines = ["file_a,start_a,end_a,name_a,file_b,start_b,end_b,name_b,score"]
    for p in result["pairs"]:
        l, r = p["left"], p["right"]
        lines.append(f"{l['file']},{l['start_line']},{l['end_line']},{l['qualname']},"
                     f"{r['file']},{r['start_line']},{r['end_line']},{r['qualname']},{p['score']:.4f}")
    return "\n".join(lines)


def print_csv(result):
    print(format_csv(result))


# ── HTML ──────────────────────────────────────────────────────────────────────

HTML_TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PyChase Report</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 24px; }}
h1 {{ font-size: 24px; margin-bottom: 8px; }}
.summary {{ color: #8b949e; margin-bottom: 24px; font-size: 14px; }}
.group {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; margin-bottom: 16px; overflow: hidden; }}
.group-header {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; cursor: pointer; user-select: none; }}
.group-header:hover {{ background: #1c2128; }}
.score {{ color: #58a6ff; font-weight: 600; font-size: 18px; }}
.badge {{ background: #21262d; color: #8b949e; padding: 2px 8px; border-radius: 12px; font-size: 12px; }}
.group-body {{ display: none; border-top: 1px solid #30363d; }}
.group-body.open {{ display: block; }}
.location {{ display: flex; padding: 8px 16px; border-bottom: 1px solid #21262d; }}
.location:last-child {{ border-bottom: none; }}
.location-meta {{ min-width: 280px; flex-shrink: 0; }}
.location-file {{ color: #58a6ff; font-size: 13px; }}
.location-range {{ color: #8b949e; font-size: 12px; }}
.location-name {{ color: #d2a8ff; font-size: 13px; margin-top: 2px; }}
.code {{ flex: 1; background: #0d1117; border-radius: 4px; padding: 8px; overflow-x: auto; font-family: 'JetBrains Mono', 'Consolas', monospace; font-size: 12px; line-height: 1.5; max-height: 300px; overflow-y: auto; }}
.code .hl {{ background: #1f6feb33; }}
.pair-detail {{ margin: 4px 16px 8px; }}
.pair-meta {{ color: #8b949e; font-size: 12px; margin-bottom: 4px; }}
</style>
</head>
<body>
<h1>PyChase Report</h1>
<p class="summary">{num_groups} duplicate groups ({num_pairs} pairs) from {num_units} units</p>
{group_html}
<script>
document.querySelectorAll('.group-header').forEach(h => {{
h.addEventListener('click', () => {{
const body = h.nextElementSibling;
body.classList.toggle('open');
}});
}});
</script>
</body>
</html>"""

GROUP_TPL = """<div class="group">
<div class="group-header">
<span class="score">{score:.3f}</span>
<span class="badge">{count_lbl} &middot; {pairs_lbl}</span>
</div>
<div class="group-body">
{location_html}
</div>
</div>"""

LOCATION_TPL = """<div class="location">
<div class="location-meta">
<div class="location-file">{file}</div>
<div class="location-range">lines {start_line}-{end_line}</div>
<div class="location-name">{qualname}</div>
</div>
</div>"""

DETAIL_TPL = """<div class="pair-detail">
<div class="pair-meta">score: {score:.4f} &middot; nodes: {lnodes} &harr; {rnodes}</div>
</div>"""


def _read_lines(filepath, start, end):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return "".join(lines[start - 1:end])
    except Exception:
        return ""


def format_html(result):
    groups = result.get("groups", [])
    pairs = result.get("pairs", [])
    sources = result.get("sources", {})

    group_html = ""
    for g in groups:
        locs = g["locations"]
        loc_html = ""
        for loc in locs:
            code_html = ""
            fp = loc["file"]
            if fp in sources:
                code = _read_lines(fp, loc["start_line"], loc["end_line"])
                code_html = f'<div class="code">{html.escape(code)}</div>'
            loc_html += LOCATION_TPL.format(**loc) + code_html
        if g["pairs"] == 2:
            loc_html += DETAIL_TPL.format(score=g["score"], lnodes=0, rnodes=0)
        c = len(locs)
        p = g["pairs"]
        count_lbl = f"{c} location{'s' if c != 1 else ''}"
        pairs_lbl = f"{p} pair{'s' if p != 1 else ''}"
        group_html += GROUP_TPL.format(
            score=g["score"], count_lbl=count_lbl, pairs_lbl=pairs_lbl,
            location_html=loc_html,
        )

    return HTML_TPL.format(
        num_groups=len(groups),
        num_pairs=len(pairs),
        num_units=result["total_units"],
        group_html=group_html,
    )


def print_html(result, output=None):
    html_str = format_html(result)
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(html_str)
        print(f"Wrote HTML report to {output}")
    else:
        print(html_str)


# ── Dispatch ───────────────────────────────────────────────────────────────────

FORMATTERS = {
    "text": print_text,
    "json": print_json,
    "csv": print_csv,
    "html": print_html,
}


def dispatch(result, fmt, output=None):
    fn = FORMATTERS.get(fmt, print_text)
    if fmt == "html" and output:
        fn(result, output=output)
    elif fmt == "html":
        fn(result)
    else:
        fn(result)
