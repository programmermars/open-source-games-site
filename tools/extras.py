"""Games this site adds beyond the upstream list (data/extra.json).

build_site.py and check_links.py call merge() after loading data/games.json, so a rebuild of
games.json from the upstream README never drops them. Each entry names the genre it joins and
is marked "extra": true, so pages can say it was added here.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load():
    p = ROOT / "data" / "extra.json"
    return json.loads(p.read_text(encoding="utf-8"))["entries"] if p.exists() else []


def merge(data):
    """Add data/extra.json entries (with their data/play.json record) to data's genres in place."""
    extras = load()
    if not extras:
        return []
    play = json.loads((ROOT / "data" / "play.json").read_text(encoding="utf-8"))
    genres = {g["id"]: g for g in data["genres"]}
    added = []
    for x in extras:
        g = genres[x["genre"]]
        e = {
            "title": x["title"],
            "href": x["href"],
            "desc_md": x["desc_en"],
            "desc_html": html.escape(x["desc_en"], quote=False),
            "desc_zh_md": x["desc_zh"],
            "desc_zh_html": html.escape(x["desc_zh"], quote=False),
            "sources": x["sources"],
            "id": x["id"],
            "extra": True,
        }
        if x["id"] in play:
            e["play"] = play[x["id"]]
        g["entries"].append(e)
        g["count"] = g.get("count", 0) + 1
        added.append(e)
    return added
