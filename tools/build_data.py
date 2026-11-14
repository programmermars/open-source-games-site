"""Turn bobeff/open-source-games README.md into data/games.json.

Usage: python tools/build_data.py <path to upstream README.md> [<commit sha>]

Merges data/play.json (browser-playable games, keyed by entry id) and
data/zh.json (Chinese descriptions, keyed by entry id) when they exist.
Descriptions are converted to a small, escaped HTML subset: <a>, <cite>.
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = r"https?://(?:[^()\s]|\([^()\s]*\))+"
LINK = re.compile(r"\[([^\]]+)\]\((" + URL + r")\)")

# ---------------------------------------------------------------- inline markdown -> safe HTML

INLINE = re.compile(
    r"\[\[source\]\]\((?P<src>" + URL + r")\)"            # [[source]](url)
    r"|\*\[(?P<it>[^\]]+)\]\((?P<itu>" + URL + r")\)\*"     # *[Title](url)*
    r"|\[(?P<lt>[^\]]+)\]\((?P<lu>" + URL + r")\)"          # [text](url)
    r"|\*(?P<em>[^*\s][^*]*?)\*"                             # *text*
)


def a(href, text, cls=None):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{html.escape(href, quote=True)}">{html.escape(text)}</a>'


def inline_html(md):
    out, pos = [], 0
    for m in INLINE.finditer(md):
        out.append(html.escape(md[pos:m.start()]))
        if m.group("src"):
            out.append(
                f'<a class="osg-source" href="{html.escape(m.group("src"), quote=True)}">'
                '<span class="osg-source-bracket" aria-hidden="true">[</span>'
                '<span class="osg-source-word">source</span>'
                '<span class="osg-source-bracket" aria-hidden="true">]</span></a>'
            )
        elif m.group("it"):
            out.append(f'<cite class="osg-orig">{a(m.group("itu"), m.group("it"))}</cite>')
        elif m.group("lt"):
            out.append(a(m.group("lu"), m.group("lt")))
        else:
            out.append(f'<cite class="osg-orig">{html.escape(m.group("em"))}</cite>')
        pos = m.end()
    out.append(html.escape(md[pos:]))
    return "".join(out).strip()


def plain(md):
    t = re.sub(r"\s*\[\[source\]\]\(" + URL + r"\)", "", md)
    t = LINK.sub(lambda m: m.group(1), t)
    t = t.replace("**", "").replace("*", "")
    return re.sub(r"\s+", " ", t).strip()


# ---------------------------------------------------------------- slugs

def slug(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^\w\s-]", "", t.lower()).strip()
    return re.sub(r"[\s_]+", "-", t) or "x"


def gh_anchor(title):
    """GitHub's heading anchor: lowercase, drop punctuation, spaces to hyphens."""
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", title.lower()).strip())


# ---------------------------------------------------------------- lineage from description words

LINEAGE_RULES = [
    ("decompilation", r"\bdecompil\w*|\breverse[- ]engineer\w*"),
    ("re-implementation", r"\bre-?implement\w*|\brecreation\b|\breplacement engine\b|\bengine remake\b"),
    ("remake", r"\bremake\b|\bdemake\b"),
    ("clone", r"\bclone\b"),
    ("port", r"\bports?\b"),
]


def lineage(desc_plain):
    for kind, pat in LINEAGE_RULES:
        if re.search(pat, desc_plain, re.I):
            return kind
    return None


# ---------------------------------------------------------------- entry line parser

TAIL_SOURCE = re.compile(r"\s*\[\[source\]\]\((" + URL + r")\)\s*$")
TAIL_ROLE = re.compile(r"\s*\*\*(Engine|UI):\s*((?:(?!\*\*).)+)\*\*\s*$")
TAIL_BOLDLINK = re.compile(r"\s*\*\*\[([^\]]+)\]\((" + URL + r")\)\*\*\s*$")
HEAD_BOLD = re.compile(r"^\*\*(.+?)\*\*")
HEAD_LINK = re.compile(r"^\[([^\]]+)\]\((" + URL + r")\)")


def parse_entry(text):
    text = text.strip()
    m = HEAD_BOLD.match(text) or HEAD_LINK.match(text)
    if not m:
        return None
    if m.re is HEAD_LINK:
        title, href = m.group(1), m.group(2)
    else:
        inner = m.group(1)
        links = LINK.findall(inner)
        title = plain(inner)
        href = links[0][1] if len(links) == 1 else None
    title = title.rstrip(":").strip()
    rest = text[m.end():]

    # trailing tags, collected from the end
    tags = []
    while True:
        for kind, rx in (("src", TAIL_SOURCE), ("role", TAIL_ROLE), ("uses", TAIL_BOLDLINK)):
            mm = rx.search(rest)
            if mm:
                tags.append((kind, mm))
                rest = rest[:mm.start()]
                break
        else:
            break
    tags.reverse()

    sources, engines = [], []
    i = 0
    while i < len(tags):
        kind, mm = tags[i]
        nxt = tags[i + 1] if i + 1 < len(tags) else None
        if kind == "src":
            sources.append(mm.group(1))
        else:
            if kind == "role":
                role, body = mm.group(1), mm.group(2).strip()
                lm = LINK.fullmatch(body)
                name, ehref = (lm.group(1), lm.group(2)) if lm else (plain(body), None)
            else:
                role, name, ehref = "Uses", mm.group(1), mm.group(2)
            eng = {"kind": role, "name": name}
            if ehref:
                eng["href"] = ehref
            if nxt and nxt[0] == "src":
                eng["sourceHref"] = nxt[1].group(1)
                i += 1
            engines.append(eng)
        i += 1

    rest = rest.strip()
    if re.fullmatch(r"[-–]", rest):
        rest = ""
    desc_md = None
    dm = re.match(r"^[-–]\s+(.*)$", rest, re.S)
    if dm:
        desc_md = dm.group(1).strip()
    elif rest:
        # "**[Strategus](…)** Engine Games": words after the bold title belong to the title
        title = f"{title} {plain(rest)}".strip()

    entry = {"title": title}
    if href:
        entry["href"] = href
    if desc_md:
        entry["desc_md"] = desc_md
        entry["desc_html"] = inline_html(desc_md)
        lk = lineage(plain(desc_md))
        if lk:
            entry["lineage"] = lk
    if sources:
        entry["sources"] = sources
    if engines:
        entry["engines"] = engines
    return entry


# ---------------------------------------------------------------- document walk

def build(readme_text, commit):
    lines = readme_text.splitlines()
    genres, genre, family, subgroup = [], None, None, None
    last_top, last_entry, in_supports = None, None, False
    ids = {}

    def new_id(title):
        base = slug(title)
        n = ids.get(base, 0) + 1
        ids[base] = n
        return base if n == 1 else f"{base}-{n}"

    def container():
        if subgroup is not None:
            return subgroup["entries"]
        if family is not None:
            return family["entries"]
        return genre["entries"]

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("## "):
            title = line[3:].strip()
            family = subgroup = last_top = last_entry = None
            in_supports = False
            if title.lower() == "table of contents":
                genre = None
                continue
            genre = {"id": gh_anchor(title), "title": title, "entries": [], "families": []}
            genres.append(genre)
            continue
        if genre is None:
            continue
        if line.startswith("### "):
            md = line[4:].strip().strip("*").strip()
            family = {"title": plain(md), "title_html": inline_html(md), "entries": [], "subgroups": []}
            genre["families"].append(family)
            subgroup = last_top = last_entry = None
            in_supports = False
            continue
        if line.startswith("#### "):
            md = line[5:].strip().strip("*").strip()
            subgroup = {"title": plain(md), "entries": []}
            (family["subgroups"] if family else genre.setdefault("subgroups", [])).append(subgroup)
            last_top = last_entry = None
            in_supports = False
            continue
        if not line.strip():
            continue
        if re.match(r"^\s*\*\*Supported games:\*\*\s*$", line):
            in_supports = True
            continue
        m = re.match(r"^(\s*)- (.*)$", line)
        if m:
            indent, body = len(m.group(1)), m.group(2)
            if indent >= 2 and in_supports and last_top is not None:
                lm = LINK.search(body)
                if lm:
                    last_top.setdefault("supports", []).append({"title": lm.group(1), "href": lm.group(2)})
                continue
            entry = parse_entry(body)
            if entry is None:
                continue
            entry["id"] = new_id(entry["title"])
            if indent >= 2 and last_top is not None:
                last_top.setdefault("children", []).append(entry)
            else:
                container().append(entry)
                last_top = entry
                in_supports = False
            last_entry = entry
            continue
    return genres


def reparse_wrapped(readme_text):
    """Join wrapped list items onto one line before parsing."""
    out = []
    for line in readme_text.splitlines():
        s = line.rstrip()
        is_struct = (not s.strip()) or s.lstrip().startswith(("- ", "#", "**Supported")) or s.startswith("  **")
        if not is_struct and out and out[-1].strip() and re.match(r"^\s*- ", out[-1]):
            out[-1] = out[-1] + " " + s.strip()
        else:
            out.append(s)
    return "\n".join(out)


def count_top(genre):
    n = len(genre["entries"])
    for f in genre["families"]:
        n += len(f["entries"]) + sum(len(s["entries"]) for s in f["subgroups"])
    n += sum(len(s["entries"]) for s in genre.get("subgroups", []))
    return n


def walk(genres):
    for g in genres:
        lists = [g["entries"]] + [s["entries"] for s in g.get("subgroups", [])]
        for f in g["families"]:
            lists.append(f["entries"])
            lists += [s["entries"] for s in f["subgroups"]]
        for lst in lists:
            for e in lst:
                yield e
                for c in e.get("children", []):
                    yield c


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    readme = Path(sys.argv[1]).read_text(encoding="utf-8")
    commit = sys.argv[2] if len(sys.argv) > 2 else ""
    genres = build(reparse_wrapped(readme), commit)

    play = {}
    zh = {}
    pp, zp = ROOT / "data" / "play.json", ROOT / "data" / "zh.json"
    if pp.exists():
        play = json.loads(pp.read_text(encoding="utf-8"))
    if zp.exists():
        zh = json.loads(zp.read_text(encoding="utf-8"))

    seen_play = set()
    total = 0
    for e in walk(genres):
        total += 1
        if e["id"] in play:
            e["play"] = play[e["id"]]
            seen_play.add(e["id"])
        zmd = zh.get("entries", {}).get(e["id"])
        if zmd and e.get("desc_md"):
            e["desc_zh_md"] = zmd
            e["desc_zh_html"] = inline_html(zmd)
        e.pop("_cont", None)
    for g in genres:
        g["count"] = count_top(g)

    extra_ids = set()
    xp = ROOT / "data" / "extra.json"
    if xp.exists():
        extra_ids = {x["id"] for x in json.loads(xp.read_text(encoding="utf-8"))["entries"]}
    missing = sorted(set(play) - seen_play - extra_ids)
    if missing:
        print("play.json ids not found in the list:", ", ".join(missing), file=sys.stderr)

    data = {
        "source": {"repo": "bobeff/open-source-games", "commit": commit, "license": "CC0-1.0"},
        "headings_zh": zh.get("headings", {}),
        "genres": genres,
    }
    out = ROOT / "data" / "games.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(genres)} genres, {total} entries, {len(seen_play)} playable -> {out}")


if __name__ == "__main__":
    main()
