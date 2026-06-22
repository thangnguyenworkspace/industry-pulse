---
type: Pulse Watchlist
schema: pulse-watchlist
created: 2026-06-22
updated: 2026-06-22
tags: [pulse, watchlist, x]
alias: []
version: 1.0
description: Example X/Twitter watchlist showing the file format. Replace the entries with your own curated accounts.
source_type: X
total_entries: 3
---

# X Watchlist

## 1.0 Purpose

Curated list of X/Twitter accounts whose recent posts the Pulse pipeline monitors on demand. Each entry is user-curated; the system never auto-discovers. The entries below are illustrative examples showing the format; replace them with your own curated sources. Consumed by `run-pulse` (via `research-crawl-x-posts`) to populate the brief.

## 2.0 Rules and Conventions

### 2.1 Authority

- `practitioner` — deep individual expertise; voice of one person.
- `executive` — leader of a recognized organization.
- `institutional` — systemic gravity beyond a single company.

Synthesis weight gradient: `institutional > executive > practitioner`. Pick the value that fits the source's actual reach, independent of personal affection.

### 2.2 Specialty

- One sentence, ~12 words target. Focus area + perspective.
- Skip biography, role title, employer — Entity Type and URL already carry those.

### 2.3 Entry Discipline

- Add when the source produces signal across your domains of interest.
- Drop when a source becomes noise; resequence the `#` column on remove.
- No auto-discovery; user-curated only.

### 2.4 Analytical Lens

- Cross-domain signal beats single-domain depth.
- Per-post substance matters more than posting cadence.
- First-hand insight beats commentary aggregation.

### 2.5 Source-Type Conventions

- Entity Type ∈ {Individual, Organization}. `Organization` is a company / fund / lab account (not a personal profile).
- URL format: `https://x.com/<handle>`. Store the canonical profile URL; `research-crawl-x-posts` extracts the bare handle and crawls via `from:<handle>` search terms.
- Prefer real display names over handles. Update the name when the crawler's first pull reveals the actual X display name.

## 3.0 Watchlist Entries

| # | Name | Entity Type | URL | Specialty | Authority | Notes |
|---|------|-------------|-----|-----------|-----------|-------|
| 1 | Anthropic | Organization | https://x.com/AnthropicAI | AI safety lab; Claude model family research and releases | institutional | Example org entry |
| 2 | OpenAI | Organization | https://x.com/OpenAI | Frontier AI lab; product and research announcements | institutional | Example org entry |
| 3 | Example Builder | Individual | https://x.com/your_handle_here | Replace with an individual whose posts you want to track | practitioner | Placeholder — swap in a real handle |
