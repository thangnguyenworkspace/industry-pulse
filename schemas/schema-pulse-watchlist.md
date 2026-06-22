---
type: Schema Definition
id: pulse-watchlist
version: 1.0
description: Anatomy of Pulse watchlist files — three-section body (Purpose / Rules and Conventions / Watchlist Entries), seven-column entry table, source-type-driven variation rules.
governs: Pulse watchlist files at config/watchlists/{source-type}-watchlist.md — curated, manually maintained lists of sources monitored by run-pulse. Ship as .example templates; copy to the working filename to activate.
applies_to: "config/watchlists/*-watchlist.md"
---

# Pulse Watchlist

## 1.0 YAML Header Fields

| Field | Type | Required | Default | Constraint |
|-------|------|----------|---------|------------|
| type | String | Yes | — | Always `Pulse Watchlist` |
| schema | String | Yes | — | Always `pulse-watchlist` |
| created | Date | Yes | — | YYYY-MM-DD |
| updated | Date | Yes | — | YYYY-MM-DD — updated on every edit |
| tags | List | Yes | [] | Minimum `[pulse, watchlist]` plus the source type tag (e.g., `linkedin`, `email`) |
| alias | List | Yes | [] | Alternative names |
| version | Number | Yes | 1.0 | Incremented on substantive changes to entries or shape |
| description | String | Yes | — | One-line summary of the watchlist's purpose |
| source_type | Enum | Yes | — | One of {LinkedIn, Email, X, RSS} per §3.2 Source Type |
| total_entries | Number | Yes | 0 | Count of rows in §3.0 Watchlist Entries; updated on add/remove |

## 2.0 Markdown Schema

The canonical structure all Pulse watchlist files follow.

````markdown
---
type: Pulse Watchlist
schema: pulse-watchlist
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [pulse, watchlist, <source-type-tag>]
alias: []
version: 1.0
description: <one-line summary>
source_type: <LinkedIn | Email | X | RSS>
total_entries: <integer>
---

# <Source Type> Watchlist

## 1.0 Purpose

<2-3 sentence statement of what this watchlist tracks, who consumes it (run-pulse), and the curation discipline (user-curated, no auto-discovery).>

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

<Optional per source type. LinkedIn watchlists declare Entity Type rules + URL format. Email watchlists declare sender-only filter rules. Future source types append here.>

## 3.0 Watchlist Entries

| # | Name | Entity Type | URL | Specialty | Authority | Notes |
|---|------|-------------|-----|-----------|-----------|-------|
| 1 | <entry name> | <per §3.3 Entity Type> | <per source_type — see §3.2> | <≤1 sentence per §2.2> | <practitioner \| executive \| institutional> | <free-text annotation or `—`> |
````

## 3.0 Field Definitions

### 3.1 Body Sections

| Field | Type | Required | Placeholder | Update Rule | Notes |
|-------|------|----------|-------------|-------------|-------|
| H1 Title | Heading | Yes | — | replace | Exactly one H1 line, format `# <Source Type> Watchlist`. |
| §1.0 Purpose | Markdown prose | Yes | `Purpose pending.` | replace | 2-3 sentences. What this watchlist tracks + consumer + curation discipline. |
| §2.0 Rules and Conventions | Sub-sectioned prose | Yes | — | replace | §2.1-§2.4 byte-identical across watchlists for consistency. §2.5 carries optional source-type rules. |
| §3.0 Watchlist Entries | Table | Yes | `(No entries yet.)` | additive-subtractive | Seven-column shape fixed across all source types. Column values vary per `source_type` per §3.2. Row count tracked by frontmatter `total_entries`. |

### 3.2 Source Type

**Purpose:** Top-level enum that drives column-value semantics + which Entity Type values are valid.

**Used by:** frontmatter `source_type` field; consumed by run-pulse to dispatch the right crawl primitive per file.

| Value | Meaning | URL Format | Entity Type values |
|---|---|---|---|
| LinkedIn | LinkedIn profiles, companies, channels, showcase pages monitored via `research-crawl-linkedin-posts`. | `https://www.linkedin.com/<path>` | Individual, Company, Channel |
| Email | Email senders monitored via `research-crawl-email` (Gmail MCP, sender-only filter). | Email address (e.g., `newsletter@example.com`) | Sender |
| X | X/Twitter accounts monitored via `research-crawl-x-posts` (search-mode, per-handle). | `https://x.com/<handle>` | Individual, Organization |
| RSS | RSS/Atom/RDF feeds monitored via `research-crawl-rss` (Python feedparser, per-feed cap + recency window). | Feed URL (e.g., `https://example.com/feed`) | Deep-Content Feed, News-Firehose Feed |

### 3.3 Entity Type

**Purpose:** Sub-classification within a source type. Valid values constrained by `source_type` per §3.2.

**Used by:** §3.0 Watchlist Entries `Entity Type` column.

| Value | Meaning | Valid under source_type |
|---|---|---|
| Individual | Personal profile (one person). | LinkedIn, X |
| Company | LinkedIn company page. | LinkedIn |
| Channel | LinkedIn showcase or sub-channel page. | LinkedIn |
| Sender | Email sender address (one inbox-sender identity). | Email |
| Organization | Company / fund / lab account on X (one org identity). | X |
| Deep-Content Feed | Low-frequency, high-token full-content or show-notes feed; one dispatch bin. | RSS |
| News-Firehose Feed | High-churn, low-token headline/excerpt feed; volume-sharded dispatch bin. | RSS |

For `source_type: RSS`, the Entity Type value carries the feed's dispatch class — read by run-pulse's volume auto-scaler to bin feeds — rather than an entity kind. The two feed classes load on different axes: deep-content is low-count / high-token, news-firehose is high-count / low-token.

### 3.4 Authority

**Purpose:** Captures the source's reach gradient for synthesis weighting.

**Used by:** §3.0 Watchlist Entries `Authority` column; read by run-pulse at synthesis time.

| Value | Meaning |
|---|---|
| practitioner | Deep individual expertise; voice of one person (e.g., a researcher, an engineer, a domain KOL). |
| executive | Leader of a recognized organization (e.g., Fortune 500 CEO, partner at top-tier VC, founder of an established startup). |
| institutional | Systemic gravity beyond a single company (e.g., a category-defining institution itself, central bankers, heads of state). |

## 4.0 Notes

### 4.1 Writing Conventions

- **Entry names use the source's real display name.** For LinkedIn: profile or company display name as it appears on the page. For Email: the human-readable sender label or institution name, not the email handle.
- **§2.1-§2.4 are uniform across watchlists.** Copy the canonical text from the §2.0 template verbatim. Edits to those four sub-sections happen at the schema level, not per-file.
- **§2.5 Source-Type Conventions is per-watchlist.** Each watchlist populates §2.5 with source-type-specific rules (e.g., LinkedIn's Entity Type routing, Email's opt-out etiquette).

### 4.2 Presentation Rules

- **Column order is fixed.** The seven columns appear in the §3.0 template order across every file.
- **Entries are numbered sequentially.** The `#` column starts at 1 and increments by 1; no gaps after deletion (resequence on remove).
- **Sort order is curation order.** New entries append to the bottom by default. Bulk re-sort by Authority is allowed when the user re-curates; no automatic re-sort.

### 4.3 Edge Cases

- **`total_entries` divergence from row count.** Frontmatter `total_entries` must equal the row count in §3.0 Watchlist Entries. Divergence is non-conformant.
- **Entity Type / source_type mismatch.** An entry with Entity Type outside the §3.2 valid set for its file's `source_type` is non-conformant.
- **Empty watchlist.** A file with zero entries is valid (`total_entries: 0`, §3.0 shows the placeholder `(No entries yet.)` after the table header). A lane with an empty watchlist is skipped at run time.

### 4.4 Extension Procedure

Adding a new source type follows three steps:

1. Append a row to §3.2 Source Type with the new value, URL format, and valid Entity Type values.
2. Append rows to §3.3 Entity Type for any new entity classifications introduced.
3. Bump this schema's `version` and scaffold the new source type's watchlist file at `config/watchlists/{type}-watchlist.md`.

The seven-column entry table shape stays fixed; only value semantics vary per source type. §2.5 Source-Type Conventions carries any per-type rule additions.

### 4.5 Other Notes

- Four source types ship: LinkedIn + X (via Apify), Email (via Gmail MCP), RSS (via Python feedparser, no MCP). The seven-column entry table is shared across all four; only column-value semantics vary per `source_type` (§3.2). For RSS, the Entity Type column carries the feed's dispatch class, which run-pulse's volume auto-scaler reads to bin feeds.
- Watchlist files are read-only at run time — run-pulse never writes back. The user curates; the composer consumes.
