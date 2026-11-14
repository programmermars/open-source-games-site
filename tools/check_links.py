"""Check every outside link the site points at, and catch hijacked domains.

Usage:
  python tools/check_links.py                    # compare against data/link-baseline.json
  python tools/check_links.py --update-baseline  # record where each link lands today
  python tools/check_links.py --summary FILE     # also write a Markdown report (GitHub step summary)

Fails (exit 1) when:
  - a link now lands on a different site than the baseline recorded (a likely takeover or move), or
  - a playable game's URL errors, or an embedded game's page now refuses to be framed.
Homepages that are merely down are reported as warnings, since sites flake.
Standard library only.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "data" / "link-baseline.json"
UA = "Mozilla/5.0 (compatible; open-source-games-site link checker; +https://github.com/programmermars/open-source-games-site)"
TWO_PART_SUFFIXES = {"co.uk", "org.uk", "ac.uk", "com.au", "co.jp", "com.br", "co.nz", "com.cn", "com.my"}


def site_of(url):
    host = (urlsplit(url).hostname or "").lower()
    parts = host.split(".")
    if len(parts) >= 3 and ".".join(parts[-2:]) in TWO_PART_SUFFIXES:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def collect():
    data = json.loads((ROOT / "data" / "games.json").read_text(encoding="utf-8"))
    play = json.loads((ROOT / "data" / "play.json").read_text(encoding="utf-8"))
    links = {}

    def walk(entries):
        for e in entries:
            if e.get("href"):
                links.setdefault(e["href"], {"kind": "homepage", "title": e["title"]})
            walk(e.get("children", []))

    for g in data["genres"]:
        walk(g["entries"])
        for s in g.get("subgroups", []):
            walk(s["entries"])
        for f in g["families"]:
            walk(f["entries"])
            for s in f["subgroups"]:
                walk(s["entries"])
    for pid, p in play.items():
        links[p["url"]] = {"kind": "play-" + p["mode"], "title": pid}
    return links


def frame_blocked(headers):
    xfo = (headers.get("X-Frame-Options") or "").lower()
    if "deny" in xfo or "sameorigin" in xfo:
        return f"X-Frame-Options: {xfo}"
    csp = (headers.get("Content-Security-Policy") or "").lower()
    for part in csp.split(";"):
        part = part.strip()
        if part.startswith("frame-ancestors") and "*" not in part.split()[1:]:
            return f"CSP {part}"
    return None


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return {"status": r.status, "final": r.geturl(), "headers": dict(r.headers)}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "final": e.geturl() or url, "headers": dict(e.headers or {})}
    except Exception as e:  # network errors, TLS errors, timeouts
        return {"status": None, "final": url, "headers": {}, "error": f"{type(e).__name__}: {e}"[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update-baseline", action="store_true")
    ap.add_argument("--summary")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    links = collect()
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = dict(zip(links, pool.map(fetch, links)))

    if args.update_baseline:
        base = {u: site_of(r["final"]) for u, r in results.items() if r["status"] and r["status"] < 400}
        BASELINE.write_text(json.dumps(base, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"baseline: {len(base)} of {len(links)} links recorded")
        return 0

    base = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
    failures, warnings = [], []
    for url, r in results.items():
        meta = links[url]
        landed = site_of(r["final"])
        expected = base.get(url)
        if expected and r["status"] and landed != expected:
            failures.append(f"{meta['title']}: {url} now lands on {r['final']} (was {expected})")
        is_play = meta["kind"].startswith("play")
        if not r["status"] or r["status"] >= 400:
            msg = f"{meta['title']}: {url} -> {r.get('error') or r['status']}"
            (failures if is_play else warnings).append(msg)
        if meta["kind"] == "play-embed" and r["status"] and r["status"] < 400:
            blocked = frame_blocked(r["headers"])
            if blocked:
                failures.append(f"{meta['title']}: {url} can no longer be embedded ({blocked}); switch it to \"tab\" in data/play.json")
        if not expected and r["status"] and r["status"] < 400:
            warnings.append(f"{meta['title']}: {url} has no baseline yet (lands on {landed})")

    lines = [f"## Link check: {len(links)} links", ""]
    lines += ["### Failures", ""] + [f"- {x}" for x in failures] if failures else ["No failures."]
    lines += ["", "### Warnings", ""] + [f"- {x}" for x in warnings] if warnings else ["", "No warnings."]
    report = "\n".join(lines) + "\n"
    print(report)
    if args.summary:
        with open(args.summary, "a", encoding="utf-8") as fh:
            fh.write(report)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
