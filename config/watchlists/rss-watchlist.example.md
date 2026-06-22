---
type: Pulse Watchlist
schema: pulse-watchlist
created: 2026-06-22
updated: 2026-06-22
tags: [pulse, watchlist, rss]
alias: []
version: 1.0
description: Example RSS watchlist showing the file format and the two feed dispatch classes. Replace or extend with your own curated feeds.
source_type: RSS
total_entries: 3
---

# RSS Watchlist

## 1.0 Purpose

Curated RSS/Atom/RDF feeds whose recent items the Pulse pipeline monitors on demand. Each feed is user-curated; the system never auto-discovers. The entries below are real public feeds used as illustrative examples; keep, replace, or extend them with your own. Consumed by `run-pulse` (via `research-crawl-rss`) to populate the brief, where cross-source repetition reads as salience.

## 2.0 Rules and Conventions

### 2.1 Authority

- `practitioner`, deep individual expertise; voice of one person.
- `executive`, leader of a recognized organization.
- `institutional`, systemic gravity beyond a single company.

Synthesis weight gradient: `institutional > executive > practitioner`. Pick the value that fits the source's actual reach, independent of personal affection.

### 2.2 Specialty

- One sentence, ~12 words target. Focus area + perspective.
- Skip biography, role title, employer, Entity Type and URL already carry those.

### 2.3 Entry Discipline

- Add when the source produces signal across your domains of interest.
- Drop when a source becomes noise; resequence the `#` column on remove.
- No auto-discovery; user-curated only.

### 2.4 Analytical Lens

- Cross-domain signal beats single-domain depth.
- Per-post substance matters more than posting cadence.
- First-hand insight beats commentary aggregation.

### 2.5 Source-Type Conventions

- Entity Type ∈ {Deep-Content Feed, News-Firehose Feed} carries the feed's **dispatch class**, not an entity kind. `Deep-Content Feed` = low-count / high-token (full bodies or show-notes); `News-Firehose Feed` = high-count / low-token (headlines/excerpts). `run-pulse`'s volume auto-scaler reads this column to bin feeds, the two classes load on different axes and never share a bin; news firehoses sub-shard by token estimate to a per-worker budget.
- URL is the raw feed URL (RSS, Atom, or RDF, `research-crawl-rss` parses all three via feedparser). Store the canonical feed URL; some hosts 308-normalize a trailing slash, store the normalized no-slash form.
- No domain column. Domain is assigned at L1 classify-time against your `config/profile.md` §3.0, uniform with the LinkedIn / email / X watchlists. A single feed's items can span domains, so per-item classification beats a per-feed label.
- Cross-source signal is owned by the brief-assembly layer: L1 workers preserve each source's framing without deduping; assembly reads repetition across sources as salience and surfaces how framings diverge. Overlapping firehose coverage is signal, not noise to collapse.
- Bot-gating is runtime/IP-specific; `research-crawl-rss` sends a browser User-Agent by default and classifies any 403 as `cloudflare-waf` (UA-defeatable) vs `cloudflare-js-challenge` (route elsewhere).

## 3.0 Watchlist Entries

| # | Name | Entity Type | URL | Specialty | Authority | Notes |
|---|------|-------------|-----|-----------|-----------|-------|
| 1 | Hacker News Front Page | News-Firehose Feed | https://hnrss.org/frontpage | Front-page startup/tech community signal across engineering and industry | institutional | Title + link |
| 2 | TechCrunch | News-Firehose Feed | https://techcrunch.com/feed/ | Startup funding, product launches, and tech-industry news | executive |n/a |
| 3 | Stratechery (free) | Deep-Content Feed | https://stratechery.com/feed/ | Tech strategy and business-model analysis of platforms and incumbents | practitioner | Free tier only |
