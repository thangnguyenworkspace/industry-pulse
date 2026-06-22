---
type: Pulse Watchlist
schema: pulse-watchlist
created: 2026-06-22
updated: 2026-06-22
tags: [pulse, watchlist, email]
alias: []
version: 1.0
description: Example email watchlist showing the file format. Replace the placeholder senders with the real newsletter addresses you want to monitor.
source_type: Email
total_entries: 2
---

# Email Watchlist

## 1.0 Purpose

Curated list of email senders whose new messages the Pulse pipeline monitors on demand. Each entry is user-curated; the system never auto-discovers. The entries below are placeholders using `example.com` addresses; replace them with the real sender addresses you want to track. Consumed by `run-pulse` (via `research-crawl-email`, Gmail MCP) to populate the brief.

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

- Entity Type is always `Sender`. Email watchlists have one entity classification — the inbox-sender identity.
- URL is the literal email address (e.g., `newsletter@example.com`). Use the canonical sending address, not a reply-to alias.
- Prefer the human-readable sender label or institution name in the Name column, not the email handle (e.g., `Market News Daily` over `markets@example.com`).
- One entry per sending address. If an institution sends from multiple addresses, list each as a separate entry.

## 3.0 Watchlist Entries

| # | Name | Entity Type | URL | Specialty | Authority | Notes |
|---|------|-------------|-----|-----------|-----------|-------|
| 1 | Example AI Newsletter | Sender | ai-news@example.com | Curated roundup of AI research, model releases, and tooling launches | institutional | Placeholder — replace with a real sender address |
| 2 | Example Growth Newsletter | Sender | growth@example.com | SaaS marketing, growth, and positioning playbooks for founders and operators | practitioner | Placeholder — replace with a real sender address |
