#!/usr/bin/env python3
"""rss-ingest.py: feedparser engine for the /research-crawl-rss leaf.

Pure primitive: fetch N RSS/Atom/RDF feeds, apply per-feed maxItems cap + recency window,
write one markdown file per feed, and emit a JSON manifest (per-feed counts + token estimates)
to stdout for the dispatcher's volume-driven auto-scaler.

No Agent spawn. stdlib urllib for fetch (browser-like UA) + feedparser for parsing.

Robustness features: est_tokens tallies the EMITTED post-strip/post-truncation payload
incl. titles/links/metadata; HTML stripped before truncation; bozo + content-type +
empty-body surfaced in manifest; 403 / Cloudflare-challenge classified; --max-body-chars
flag + boundary-aware truncation; no md written when emitted==0; body_source recorded;
dateless-drop surfaced + deterministic fallback.

Usage:
  rss-ingest.py --feeds-file feeds.tsv --days 1 --max-items 15 --out-dir ./out
  rss-ingest.py --url https://news.ycombinator.com/rss --name hackernews --days 2 --out-dir ./out
feeds-file lines: name<TAB>url[<TAB>domain]   (blank lines / # comments ignored)
"""
import argparse, json, sys, os, gzip, io, time, re, html
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
import urllib.request, urllib.error
import calendar
import feedparser

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")  # load-bearing default; do not strip

# Cloudflare / WAF challenge markers
JS_CHALLENGE_MARKERS = ("just a moment", "challenges.cloudflare.com", "cf-browser-verification",
                        "_cf_chl_opt", "enable javascript and cookies to continue")
WAF_DENY_MARKERS = ("access denied", "you have been blocked", "attention required")

class _Stripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, d):
        self.parts.append(d)
    def text(self):
        return "".join(self.parts)

def strip_html(s):
    """tags → gone, entities → unescaped, whitespace collapsed. Tolerant of malformed HTML."""
    if not s:
        return ""
    try:
        p = _Stripper(); p.feed(s); p.close()
        out = p.text()
    except Exception:
        out = re.sub(r"<[^>]+>", " ", s)
    out = html.unescape(out)
    return re.sub(r"[ \t]*\n[ \t]*", "\n", re.sub(r"[ \t]+", " ", out)).strip()

def slugify(s):
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")[:50] or "feed"

def boundary_trunc(text, limit):
    """cut on a sentence/paragraph boundary at or before limit (fallback: hard cut)."""
    if len(text) <= limit:
        return text
    window = text[:limit]
    for sep in ("\n\n", ". ", "\n", " "):
        idx = window.rfind(sep)
        if idx >= int(limit * 0.6):
            return window[:idx + len(sep)].rstrip()
    return window.rstrip()

def fetch(url, ua, timeout=30):
    """Return (status, bytes, content_type, error). Browser-like UA; identity encoding to dodge gzip surprises."""
    req = urllib.request.Request(url, headers={
        "User-Agent": ua,
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
        "Accept-Encoding": "identity",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                data = gzip.GzipFile(fileobj=io.BytesIO(data)).read()
            return r.status, data, (r.headers.get("Content-Type") or "").split(";")[0].strip().lower(), None
    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read()
        except Exception:
            pass
        return e.code, body, (e.headers.get("Content-Type", "").split(";")[0].strip().lower() if e.headers else ""), f"HTTPError {e.code} {e.reason}"
    except Exception as e:
        return 0, b"", "", f"{type(e).__name__}: {e}"

def classify_gate(status, data):
    """distinguish UA-solvable WAF deny from unsolvable JS challenge."""
    low = data[:4000].decode("utf-8", "ignore").lower() if data else ""
    if any(m in low for m in JS_CHALLENGE_MARKERS):
        return "gated:cloudflare-js-challenge"
    if status == 403 or any(m in low for m in WAF_DENY_MARKERS):
        return "gated:cloudflare-waf"
    return None

def entry_dt(e):
    st = e.get("published_parsed") or e.get("updated_parsed")
    if st:
        return datetime.fromtimestamp(calendar.timegm(st), tz=timezone.utc)
    return None

def entry_content(e):
    """return (text, source); content:encoded/atom content if present, else summary/description."""
    if e.get("content"):
        vals = [c.get("value", "") for c in e["content"] if c.get("value")]
        if vals:
            return max(vals, key=len), "content"
    s = e.get("summary", "") or ""
    return s, ("summary" if s else "none")

def process_feed(name, url, domain, days, max_items, max_body, ua, out_dir, now):
    status, data, ctype, err = fetch(url, ua)
    rec = {"name": name, "url": url, "domain": domain, "http_status": status, "content_type": ctype,
           "feed_type": None, "bozo": None, "bozo_exception": None, "gated": None,
           "items_total": 0, "items_in_window": 0, "items_emitted": 0, "full_items": 0,
           "body_sources": {}, "est_tokens": 0, "latest_item": None,
           "no_date_items": 0, "items_dropped_dateless": 0, "error": err, "out_file": None}

    gate = classify_gate(status, data)
    if gate:
        rec["gated"] = gate
        rec["error"] = rec["error"] or gate
        return rec
    if err:
        return rec
    if not data or len(data) < 40:                           # empty/near-empty 200
        rec["error"] = f"empty body (HTTP {status})"
        return rec

    fp = feedparser.parse(data)
    rec["feed_type"] = fp.get("version") or None
    rec["bozo"] = bool(fp.bozo)                              # surface bozo regardless of entries
    if fp.bozo:
        rec["bozo_exception"] = str(getattr(fp, "bozo_exception", ""))[:200]
    if not fp.entries:
        # distinguish non-feed HTML from a genuinely empty feed
        if ctype and "html" in ctype:
            rec["error"] = f"not a feed (got {ctype})"
        elif fp.bozo:
            rec["error"] = f"unparseable: {rec['bozo_exception']}"
        else:
            rec["error"] = "feed has zero entries"
        return rec

    entries = fp.entries
    rec["items_total"] = len(entries)
    cutoff = now - timedelta(days=days)
    enriched = [(entry_dt(e), e) for e in entries]
    in_window = [(dt, e) for dt, e in enriched if dt and dt >= cutoff]
    undated = [(dt, e) for dt, e in enriched if dt is None]
    rec["items_in_window"] = len(in_window)
    rec["no_date_items"] = len(undated)
    pool = sorted(in_window, key=lambda x: x[0], reverse=True)
    if not pool and undated:
        pool = undated                                       # dateless fallback (feed order; documented)
    elif in_window and undated:
        rec["items_dropped_dateless"] = len(undated)         # surface silently-dropped undated items
    pool = pool[:max_items]                                  # per-feed cap
    rec["items_emitted"] = len(pool)
    all_dt = [dt for dt, _ in enriched if dt]
    if all_dt:
        rec["latest_item"] = max(all_dt).isoformat()

    if not pool:                                             # no empty-shell md
        rec["error"] = rec["error"] or "no items in window"
        return rec

    slug = slugify(name)
    path = os.path.join(out_dir, f"{slug}.md")
    os.makedirs(out_dir, exist_ok=True)
    payload_chars = 0
    lines = [f"# {name}",
             f"<!-- url:{url} domain:{domain} type:{rec['feed_type']} fetched:{now.isoformat()} "
             f"window_days:{days} cap:{max_items} max_body:{max_body} -->", ""]
    for dt, e in pool:
        raw, src = entry_content(e)
        rec["body_sources"][src] = rec["body_sources"].get(src, 0) + 1
        body = boundary_trunc(strip_html(raw), max_body)     # strip HTML before truncation
        if len(body) > 1500:
            rec["full_items"] += 1
        block = [f"## {e.get('title','(no title)')}",
                 f"- link: {e.get('link','')}",
                 f"- published: {dt.isoformat() if dt else '(no date)'}"]
        if e.get("author"):
            block.append(f"- author: {e.get('author')}")
        block += ["", body if body else "(no body content)", ""]
        lines += block
        payload_chars += sum(len(x) for x in block)          # tally EMITTED payload incl. metadata
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    rec["out_file"] = path
    rec["est_tokens"] = int(payload_chars / 4)               # post-strip/post-truncation, full payload
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feeds-file")
    ap.add_argument("--url"); ap.add_argument("--name", default="feed"); ap.add_argument("--domain", default="")
    ap.add_argument("--days", type=int, default=1)
    ap.add_argument("--max-items", type=int, default=15)
    ap.add_argument("--max-body-chars", type=int, default=8000)
    ap.add_argument("--out-dir", default="./rss-out")
    ap.add_argument("--user-agent", default=UA)
    args = ap.parse_args()

    feeds = []
    if args.feeds_file:
        for ln in open(args.feeds_file, encoding="utf-8"):
            ln = ln.rstrip("\n")
            if not ln.strip() or ln.lstrip().startswith("#"):
                continue
            parts = ln.split("\t")
            feeds.append((parts[0], parts[1], parts[2] if len(parts) > 2 else ""))
    elif args.url:
        feeds.append((args.name, args.url, args.domain))
    else:
        print("ERROR: pass --feeds-file or --url", file=sys.stderr); sys.exit(2)

    now = datetime.now(timezone.utc)
    t0 = time.time()
    records = [process_feed(n, u, d, args.days, args.max_items, args.max_body_chars,
                            args.user_agent, args.out_dir, now)
               for n, u, d in feeds]
    manifest = {
        "fetched_at": now.isoformat(), "window_days": args.days,
        "max_items_per_feed": args.max_items, "max_body_chars": args.max_body_chars,
        "out_dir": args.out_dir, "elapsed_sec": round(time.time() - t0, 1),
        "feeds": records,
        "totals": {
            "feeds": len(records),
            "ok": sum(1 for r in records if not r["error"]),
            "errored": sum(1 for r in records if r["error"]),
            "gated": sum(1 for r in records if r["gated"]),
            "bozo_recovered": sum(1 for r in records if r["bozo"] and r["items_emitted"] > 0),
            "items_emitted": sum(r["items_emitted"] for r in records),
            "est_tokens": sum(r["est_tokens"] for r in records),
        },
    }
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
