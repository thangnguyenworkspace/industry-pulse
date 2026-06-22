---
type: Pulse Watchlist
schema: pulse-watchlist
created: 2026-06-22
updated: 2026-06-22
tags: [pulse, watchlist, linkedin]
alias: []
version: 1.0
description: Example LinkedIn watchlist showing the file format. Replace the entries with your own curated profiles, companies, and channels.
source_type: LinkedIn
total_entries: 3
---

# LinkedIn Watchlist

## 1.0 Purpose

Curated list of LinkedIn profiles, companies, and channels whose new posts the Pulse pipeline monitors on demand. Each entry is user-curated; the system never auto-discovers. The entries below are illustrative examples showing the format; replace them with your own curated sources. Consumed by `run-pulse` to populate the brief.

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

- Entity Type ∈ {Individual, Company, Channel}. `Channel` is a LinkedIn showcase or sub-channel page (e.g., a product showcase under a parent company).
- URL format: `https://www.linkedin.com/<path>`. Use the canonical handle path (e.g., `/in/<handle>/`, `/company/<slug>/`, `/showcase/<slug>/`).
- Prefer real display names over handles. Update the name when the crawler's first pull reveals the actual LinkedIn display name.

## 3.0 Watchlist Entries

| # | Name | Entity Type | URL | Specialty | Authority | Notes |
|---|------|-------------|-----|-----------|-----------|-------|
| 1 | a16z | Company | https://www.linkedin.com/company/a16z/ | Multi-stage venture firm; broad content engine on tech, AI, and startups | institutional | Example org entry |
| 2 | OpenAI | Company | https://www.linkedin.com/company/openai/ | Frontier AI lab; product and research announcements | institutional | Example org entry |
| 3 | Example Practitioner | Individual | https://www.linkedin.com/in/your-handle-here/ | Replace with an individual whose posts you want to track | practitioner | Placeholder — swap in a real profile |
