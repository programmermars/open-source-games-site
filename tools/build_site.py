"""Render public/ from data/games.json and design/tokens.json.

Usage: python tools/build_site.py
Writes public/index.html, public/assets/tokens.css, public/assets/osg.css, public/_headers.
public/assets/site.css, boot.js and app.js are hand-written and not touched.
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
CJK = '"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans SC", "Noto Sans CJK SC"'


def esc(s):
    return html.escape(str(s), quote=True)


def bi(zh, en):
    if zh is None or zh == en:
        return esc(en)
    return f'<span class="l-zh" lang="zh-CN">{esc(zh)}</span><span class="l-en" lang="en">{esc(en)}</span>'


def bi_html(zh_html, en_html):
    if not zh_html:
        return en_html
    return f'<span class="l-zh" lang="zh-CN">{zh_html}</span><span class="l-en" lang="en">{en_html}</span>'


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def strip_md(md):
    md = re.sub(r"\[\[source\]\]\([^)]*\)", "", md)
    md = re.sub(r"\[([^\]]+)\]\((?:[^()\s]|\([^()\s]*\))+\)", r"\1", md)
    return md.replace("*", "")


# ---------------------------------------------------------------- tokens.css

def tokens_css():
    t = json.loads((ROOT / "design" / "tokens.json").read_text(encoding="utf-8"))
    themes = [th["id"] for th in t["color"]["themes"]]
    first = themes[0]

    def val(v):
        m = re.fullmatch(r"\{(.+)\}", v)
        return f"var(--{m.group(1)})" if m else v

    per = {th: [] for th in themes}
    for fam in ("color", "shadow"):
        for tok in t[fam]["tokens"]:
            v = tok["value"]
            if isinstance(v, str):
                v = {first: v}
            for th in themes:
                if th in v:
                    per[th].append(f"  --{tok['name']}: {val(v[th])};")
    rest = []
    for fam in ("spacing", "radius", "border", "layout"):
        for tok in t[fam]["tokens"]:
            v = str(tok["value"])
            rest.append(f"  --{tok['name']}: {v};")
    fams = dict(t["type"]["families"])
    fams["sans"] = fams["sans"].replace(", sans-serif", f", {CJK}, sans-serif")
    for k, v in fams.items():
        rest.append(f"  --font-{k}: {v};")
    dark = "\n".join("  " + line for line in per["dark"])
    return (
        f"/* Open Source Games tokens, generated from design/tokens.json by tools/build_site.py */\n"
        f":root {{\n" + "\n".join(per[first]) + "\n" + "\n".join(rest) + "\n}\n"
        f'@media (prefers-color-scheme: dark) {{\n  :root:not([data-theme="light"]) {{\n{dark}\n    color-scheme: dark;\n  }}\n}}\n'
        f':root[data-theme="dark"] {{\n' + "\n".join(per["dark"]) + "\n  color-scheme: dark;\n}\n"
    )


# ---------------------------------------------------------------- strings

UI = {
    "title": ("开源游戏合集", "Open source games"),
    "intro": (
        "精选开源游戏，以及商业经典游戏的开源重制。能在浏览器里直接玩的排在最前面。",
        "A list of open-source video games and open-source remakes of commercial games. The ones you can play in your browser come first.",
    ),
    "credit": ("清单来自", "List from"),
    "play_h": ("浏览器即玩", "Play in your browser"),
    "play_embed": ("▶ 开始玩", "▶ Play here"),
    "play_tab": ("新标签打开 ↗", "Open in new tab ↗"),
    "play_sm": ("▶ 玩", "▶ Play"),
    "unofficial": ("非官方", "Unofficial"),
    "account": ("需注册", "Account needed"),
    "keyboard": ("键盘", "Keyboard"),
    "mouse": ("鼠标", "Mouse"),
    "touch": ("触屏", "Touch"),
    "search": ("搜索游戏、引擎或原作", "Search games, engines, originals"),
    "only": ("只看能直接玩的", "Only browser-playable"),
    "toc": ("目录", "Table of contents"),
    "supported": ("支持的游戏", "Supported games"),
    "source": ("源码", "source"),
    "Engine": ("引擎", "Engine"),
    "UI": ("界面", "UI"),
    "Uses": ("使用", "Uses"),
    "port": ("移植", "port"),
    "re-implementation": ("重新实现", "re-implementation"),
    "remake": ("重制", "remake"),
    "clone": ("复刻", "clone"),
    "decompilation": ("反编译", "decompilation"),
    "playing": ("正在玩", "Now playing"),
    "fullscreen": ("全屏", "Fullscreen"),
    "newtab": ("新标签打开 ↗", "Open in new tab ↗"),
    "close": ("关闭", "Close"),
    "served": ("游戏由此网站提供：", "Served by "),
    "foot1": (
        "游戏版权归各自作者所有。本站只链接或内嵌各游戏自己托管的网页版，不托管任何游戏文件。",
        "Every game belongs to its authors. This site only links to or embeds the browser versions they host, and hosts no game files.",
    ),
    "foot2": ("清单数据", "List data"),
    "free": (
        "这是一个免费、非商业的网站：不收费、没有广告、不收集个人数据。由 programmermars 维护。",
        "A free, non-commercial website: no fees, no ads, no personal data collected. Maintained by programmermars.",
    ),
    "privacy": ("隐私政策", "Privacy"),
    "terms": ("使用条款", "Terms of use"),
    "credits": ("致谢与许可", "Credits & licenses"),
    "code": ("本站源代码", "Source code"),
    "home": ("← 开源游戏合集", "← Open source games"),
    "effective": ("生效日期：", "Effective "),
    "sitecode": ("本站代码", "Site code"),
    "skip": ("跳到游戏目录", "Skip to the catalog"),
    "noscript": (
        "搜索、切换语言和主题、在本页内嵌游玩需要 JavaScript；所有链接仍可直接打开。",
        "Search, language and theme switches and in-page play need JavaScript; every link still works.",
    ),
}


def ui(key):
    zh, en = UI[key]
    return bi(zh, en)


def count_label(n, zh_unit):
    en = f"{n} entry" if n == 1 else f"{n} entries"
    return bi(f"{n} {zh_unit}", en)


# ---------------------------------------------------------------- pieces

def source_link(href):
    host = urlsplit(href).hostname or ""
    host = host[4:] if host.startswith("www.") else host
    host_html = f'<span class="osg-source-host">{esc(host)}</span>' if host and host != "github.com" else ""
    return (
        f'<a class="osg-source" href="{esc(href)}" title="Source code on {esc(host)}">'
        f'<span class="osg-source-bracket" aria-hidden="true">[</span>'
        f'<span class="osg-source-word">{ui("source")}</span>'
        f'<span class="osg-source-bracket" aria-hidden="true">]</span>{host_html}</a>'
    )


def engine_tag(e):
    name = (
        f'<a class="osg-engine-name" href="{esc(e["href"])}">{esc(e["name"])}</a>'
        if e.get("href") else f'<span class="osg-engine-name">{esc(e["name"])}</span>'
    )
    src = source_link(e["sourceHref"]) if e.get("sourceHref") else ""
    kind = ui(e["kind"]) if e["kind"] in UI else esc(e["kind"])
    return f'<span class="osg-engine"><span class="osg-engine-kind">{kind}</span>{name}{src}</span>'


def lineage_tag(kind):
    return f'<span class="osg-lineage" data-kind="{esc(kind)}">{ui(kind)}</span>'


def controls_label(ctrls):
    zh = " · ".join(UI[c][0] for c in ctrls)
    en = " · ".join(UI[c][1] for c in ctrls)
    return bi(zh, en)


def play_button(eid, p, small=False):
    cls = "osg-play" + (" osg-play--sm" if small else "") + (" osg-play--tab" if p["mode"] == "tab" else "")
    if small:
        label = ui("play_sm") if p["mode"] == "embed" else bi("玩 ↗", "Play ↗")
    else:
        label = ui("play_embed") if p["mode"] == "embed" else ui("play_tab")
    data = f' data-play-id="{esc(eid)}"' if p["mode"] == "embed" else ""
    return f'<a class="{cls}" href="{esc(p["url"])}" target="_blank" rel="noopener"{data}>{label}</a>'


def entry_html(e, ctx, nested=False):
    title = (
        f'<a class="osg-entry-title" href="{esc(e["href"])}">{esc(e["title"])}</a>'
        if e.get("href") else f'<span class="osg-entry-title">{esc(e["title"])}</span>'
    )
    head = [title]
    if e.get("lineage"):
        head.append(lineage_tag(e["lineage"]))
    if e.get("play"):
        head.append(play_button(e["id"], e["play"], small=True))
    parts = [f'<div class="osg-entry-head">{"".join(head)}</div>']
    if e.get("desc_html"):
        parts.append(f'<p class="osg-entry-desc">{bi_html(e.get("desc_zh_html"), e["desc_html"])}</p>')
    meta = [source_link(s) for s in e.get("sources", [])] + [engine_tag(x) for x in e.get("engines", [])]
    if meta:
        parts.append(f'<div class="osg-entry-meta">{"".join(meta)}</div>')
    if e.get("supports"):
        items = "".join(
            f'<li><cite class="osg-orig"><a href="{esc(s["href"])}">{esc(s["title"])}</a></cite></li>' for s in e["supports"]
        )
        parts.append(f'<div class="osg-entry-supports"><span class="osg-entry-supports-label">{ui("supported")}</span><ul>{items}</ul></div>')
    if e.get("children"):
        kids = "".join(entry_html(c, ctx, nested=True) for c in e["children"])
        parts.append(f'<ul class="osg-entries osg-entries--nested">{kids}</ul>')

    search = " ".join(
        [e["title"], strip_md(e.get("desc_md", "")), strip_md(e.get("desc_zh_md", ""))]
        + [x["name"] for x in e.get("engines", [])]
        + [s["title"] for s in e.get("supports", [])]
        + ctx
    )
    attrs = f' id="g-{esc(e["id"])}" data-search="{esc(norm(search))}"'
    if e.get("play"):
        attrs += ' data-play="1"'
    return f'<li class="osg-entry"{attrs}>{"".join(parts)}</li>'


def entry_list(entries, ctx):
    if not entries:
        return ""
    return f'<ul class="osg-entries">{"".join(entry_html(e, ctx) for e in entries)}</ul>'


def genre_html(g, hz):
    gid = g["id"]
    gtitle_zh = hz.get(g["title"])
    ctx = [g["title"], gtitle_zh or ""]
    body = [entry_list(g["entries"], ctx)]
    for s in g.get("subgroups", []):
        body.append(f'<div class="osg-group"><h4 class="osg-subgroup">{bi(hz.get(s["title"]), s["title"])}</h4>{entry_list(s["entries"], ctx)}</div>')
    for f in g["families"]:
        fctx = ctx + [f["title"], hz.get(f["title"], "")]
        inner = [f'<h3 class="osg-family">{bi_html(esc(hz[f["title"]]) if hz.get(f["title"]) else "", f["title_html"])}</h3>']
        inner.append(entry_list(f["entries"], fctx))
        for s in f["subgroups"]:
            inner.append(f'<div class="osg-group"><h4 class="osg-subgroup">{bi(hz.get(s["title"]), s["title"])}</h4>{entry_list(s["entries"], fctx)}</div>')
        body.append(f'<div class="osg-group osg-group--family">{"".join(inner)}</div>')
    return (
        f'<section class="osg-genre" id="{esc(gid)}" aria-labelledby="{esc(gid)}-h">'
        f'<header class="osg-genre-head"><h2 class="osg-genre-title" id="{esc(gid)}-h"><a href="#{esc(gid)}">{bi(gtitle_zh, g["title"])}</a></h2>'
        f'<span class="osg-genre-count">{count_label(g["count"], "个")}</span></header>'
        f'{"".join(body)}</section>'
    )


def toc_html(genres, hz):
    items = "".join(
        f'<li class="osg-toc-item"><a class="osg-toc-link" href="#{esc(g["id"])}">'
        f'<span class="osg-toc-name">{bi(hz.get(g["title"]), g["title"])}</span>'
        f'<span class="osg-toc-dots" aria-hidden="true"></span>'
        f'<span class="osg-toc-count">{g["count"]}</span></a></li>'
        for g in genres
    )
    return (
        f'<nav class="osg-toc" aria-labelledby="toc-title"><p class="osg-toc-title" id="toc-title">{ui("toc")}</p>'
        f'<ol class="osg-toc-list">{items}</ol></nav>'
    )


def all_entries(genres):
    def walk(lst):
        for e in lst:
            yield e
            yield from walk(e.get("children", []))
    for g in genres:
        yield from walk(g["entries"])
        for s in g.get("subgroups", []):
            yield from walk(s["entries"])
        for f in g["families"]:
            yield from walk(f["entries"])
            for s in f["subgroups"]:
                yield from walk(s["entries"])


def play_section(playable):
    playable = sorted(
        playable,
        key=lambda e: (e["play"]["mode"] != "embed", bool(e["play"].get("account")), bool(e["play"].get("unofficial")), e["title"].lower()),
    )
    rows = []
    for e in playable:
        p = e["play"]
        tags = []
        if p.get("unofficial"):
            tags.append(f'<span class="osg-lineage">{ui("unofficial")}</span>')
        if p.get("account"):
            tags.append(f'<span class="osg-lineage">{ui("account")}</span>')
        title = (
            f'<a class="osg-entry-title" href="{esc(e["href"])}">{esc(e["title"])}</a>'
            if e.get("href") else f'<span class="osg-entry-title">{esc(e["title"])}</span>'
        )
        desc = f'<p class="osg-entry-desc">{bi_html(e.get("desc_zh_html"), e["desc_html"])}</p>' if e.get("desc_html") else ""
        note = f'<p class="play-note"><span class="play-controls">{controls_label(p["controls"])}</span>{bi(p["note"]["zh"], p["note"]["en"])}</p>'
        rows.append(
            f'<li class="play-row" data-id="{esc(e["id"])}"><div class="play-info">'
            f'<div class="osg-entry-head">{title}{"".join(tags)}</div>{desc}{note}</div>'
            f'<div class="play-actions">{play_button(e["id"], p)}</div></li>'
        )
    n = len(playable)
    return (
        f'<section class="osg-genre play" id="play" aria-labelledby="play-h">'
        f'<header class="osg-genre-head"><h2 class="osg-genre-title" id="play-h"><a href="#play">{ui("play_h")}</a></h2>'
        f'<span class="osg-genre-count">{bi(f"{n} 款", f"{n} games")}</span></header>'
        f'<ul class="play-list">{"".join(rows)}</ul></section>'
    )


HEAD = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0000aa">
<link rel="icon" href="{b}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{b}assets/fonts.css?v={v}">
<link rel="stylesheet" href="{b}assets/tokens.css?v={v}">
<link rel="stylesheet" href="{b}assets/osg.css?v={v}">
<link rel="stylesheet" href="{b}assets/site.css?v={v}">
<script src="{b}assets/boot.js?v={v}"></script>
<script src="{b}assets/app.js?v={v}" defer></script>
</head>
<body class="osg-root">
<a class="skip" href="#{skip_to}">{skip}</a>
<div class="page">
<div class="topbar">
<p class="topbar-credit">{left}</p>
<div class="topbar-tools">
<button type="button" class="tool" id="lang-toggle" hidden><span class="l-zh" lang="en">English</span><span class="l-en" lang="zh-CN">中文</span></button>
<button type="button" class="tool" id="theme-toggle" hidden></button>
</div>
</div>
"""

FOOT = """<footer class="foot">
<p class="foot-free">{free}</p>
<p>{foot1}</p>
<nav class="foot-links" aria-label="Site"><a href="{b}privacy/">{privacy}</a><a href="{b}terms/">{terms}</a><a href="{b}credits/">{credits}</a><a href="{repo}">{code}</a></nav>
<p>{foot2} <a href="https://github.com/bobeff/open-source-games/tree/{commit}">bobeff/open-source-games@{commit_short}</a> · CC0 1.0 · {sitecode} MIT</p>
</footer>
</div>
"""

INDEX_BODY = """<header class="osg-header">
<h1 class="osg-header-title">{title}</h1>
<p class="osg-header-intro">{intro}</p>
</header>
<noscript><p class="noscript">{noscript}</p></noscript>
{play}
<div class="finder" role="search">
<label class="finder-label" for="q">{search}</label>
<div class="finder-row">
<input class="finder-input" id="q" type="search" autocomplete="off" spellcheck="false">
<label class="finder-check" for="only-play"><input type="checkbox" id="only-play">{only}</label>
</div>
<p class="finder-count" id="count" aria-live="polite"></p>
</div>
{toc}
<main id="catalog" class="catalog" tabindex="-1">
{genres}
</main>
"""

PLAYER = """<dialog class="player" id="player" aria-labelledby="player-title">
<div class="player-bar">
<p class="player-kicker">{playing}</p>
<h2 class="player-title" id="player-title"></h2>
<div class="player-tools">
<button type="button" class="tool" data-act="fullscreen">{fullscreen}</button>
<a class="tool" data-act="newtab" href="#" target="_blank" rel="noopener">{newtab}</a>
<button type="button" class="tool" data-act="close">{close}</button>
</div>
</div>
<div class="player-stage"><iframe id="player-frame" title="" allow="fullscreen; autoplay; gamepad; clipboard-write" sandbox="allow-scripts allow-same-origin allow-pointer-lock allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-orientation-lock" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
<p class="player-foot">{served}<span id="player-host"></span><span class="player-controls" id="player-controls"></span></p>
</dialog>
<script type="application/json" id="play-data">{play_json}</script>
"""

SUB_BODY = """<header class="osg-header">
<h1 class="osg-header-title osg-header-title--sub">{title}</h1>
<p class="osg-header-intro">{effective}{date}</p>
</header>
<main id="main" class="prose" tabindex="-1">
<div class="l-zh" lang="zh-CN">{zh}</div>
<div class="l-en" lang="en">{en}</div>
</main>
"""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    data = json.loads((ROOT / "data" / "games.json").read_text(encoding="utf-8"))
    hz = data.get("headings_zh", {})
    genres = data["genres"]
    entries = list(all_entries(genres))
    playable = [e for e in entries if e.get("play")]

    play_data = {
        e["id"]: {
            "title": e["title"],
            "url": e["play"]["url"],
            "mode": e["play"]["mode"],
            "controls": {"zh": " · ".join(UI[c][0] for c in e["play"]["controls"]), "en": " · ".join(UI[c][1] for c in e["play"]["controls"])},
        }
        for e in playable
    }
    play_json = json.dumps(play_data, ensure_ascii=False).replace("<", "\\u003c")

    commit = data["source"].get("commit") or "main"
    desc = esc(UI["intro"][0] + " " + UI["intro"][1])

    def foot(b):
        return FOOT.format(
            b=b, free=ui("free"), foot1=ui("foot1"), privacy=ui("privacy"), terms=ui("terms"),
            credits=ui("credits"), code=ui("code"), repo=pages.REPO_URL, foot2=ui("foot2"),
            commit=esc(commit), commit_short=esc(commit[:7]), sitecode=ui("sitecode"),
        )

    import hashlib
    v = hashlib.sha1(b"".join(
        (PUB / "assets" / n).read_bytes() for n in ("site.css", "boot.js", "app.js")
    ) + (ROOT / "design" / "tokens.json").read_bytes() + (ROOT / "design" / "osg.css").read_bytes()).hexdigest()[:10]

    index = (
        HEAD.format(v=v, 
            title="开源游戏合集 · Open Source Games", desc=desc, b="", skip_to="catalog", skip=ui("skip"),
            left=f'{ui("credit")} <a href="https://github.com/bobeff/open-source-games">bobeff/open-source-games</a>',
        )
        + INDEX_BODY.format(
            title=ui("title"), intro=ui("intro"), noscript=ui("noscript"), play=play_section(playable),
            search=ui("search"), only=ui("only"), toc=toc_html(genres, hz),
            genres="\n".join(genre_html(g, hz) for g in genres),
        )
        + foot("")
        + PLAYER.format(
            playing=ui("playing"), fullscreen=ui("fullscreen"), newtab=ui("newtab"), close=ui("close"),
            served=ui("served"), play_json=play_json,
        )
        + "</body>\n</html>\n"
    )

    subpages = {
        "privacy": ("隐私政策 · Privacy", pages.privacy()),
        "terms": ("使用条款 · Terms of use", pages.terms()),
        "credits": ("致谢与许可 · Credits & licenses", pages.credits(esc, len(entries), commit[:7])),
    }
    sub_html = {}
    for key, (title, (zh, en)) in subpages.items():
        sub_html[key] = (
            HEAD.format(
                v=v, title=f"{title} · 开源游戏合集", desc=desc, b="../", skip_to="main", skip=ui("skip"),
                left=f'<a href="../">{ui("home")}</a>',
            )
            + SUB_BODY.format(title=ui(key), effective=ui("effective"), date=pages.EFFECTIVE, zh=zh, en=en)
            + foot("../")
            + "</body>\n</html>\n"
        )

    (PUB / "assets").mkdir(parents=True, exist_ok=True)
    (PUB / "index.html").write_text(index, encoding="utf-8", newline="\n")
    for key, doc in sub_html.items():
        (PUB / key).mkdir(exist_ok=True)
        (PUB / key / "index.html").write_text(doc, encoding="utf-8", newline="\n")
    (PUB / "assets" / "tokens.css").write_text(tokens_css(), encoding="utf-8", newline="\n")
    osg = (ROOT / "design" / "osg.css").read_text(encoding="utf-8")
    osg = re.sub(r"^@import url\([^)]*fonts\.googleapis[^)]*\);\s*", "/* Fonts are self-hosted: see fonts.css. */\n", osg)
    (PUB / "assets" / "osg.css").write_text(osg, encoding="utf-8", newline="\n")

    frames = sorted({f"{urlsplit(e['play']['url']).scheme}://{urlsplit(e['play']['url']).netloc}" for e in playable if e["play"]["mode"] == "embed"})
    csp = "; ".join([
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self'",
        "font-src 'self'",
        "img-src 'self' data:",
        "frame-src " + " ".join(frames),
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
        "frame-ancestors 'self'",
    ])
    headers = (
        "/*\n"
        f"  Content-Security-Policy: {csp}\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n"
        "/assets/*\n"
        "  Cache-Control: public, max-age=3600\n"
    )
    (PUB / "_headers").write_text(headers, encoding="utf-8", newline="\n")
    print("pages: index, " + ", ".join(sub_html))
    print(f"{len(entries)} entries, {len(playable)} playable, {len(frames)} embeddable origins -> public/")


if __name__ == "__main__":
    main()
