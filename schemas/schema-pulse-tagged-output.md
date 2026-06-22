---
type: Schema Definition
id: pulse-tagged-output
version: 1.0
description: Defines the per-source-type tagged-signals file — one per source-type per run-pulse invocation, written by a classifier-tagger worker (classified + domain-tagged signal that preserves each source's framing), read by the brief-assembly layer for domain-first cross-source synthesis.
governs: Per-source-type tagged-signals files produced by run-pulse's classifier-tagger workers — one file per source-type per run at output/tagged/tagged-{YYYY-MM-DD}/{source-type}-tagged.md.
applies_to: "output/tagged/tagged-*/*-tagged.md"
---

# Pulse Tagged Output

## 1.0 YAML Header Fields

| Field | Type | Required | Default | Constraint |
|-------|------|----------|---------|------------|
| type | String | Yes | — | Pulse Tagged Output |
| schema | String | Yes | — | pulse-tagged-output |
| created | Date | Yes | — | YYYY-MM-DD — matches `tagged_date`. |
| updated | Date | Yes | — | YYYY-MM-DD — matches `created` (files are immutable per-run intermediates). |
| tags | List | Yes | [] | Minimum `[pulse, tagged]` plus the `source_type` and date tags. |
| alias | List | Yes | [] | Alternative names. |
| version | Number | Yes | 1.0 | Always 1.0 (per-run intermediates do not version). |
| description | String | Yes | — | One-line summary of the source-type + dominant domains tagged. |
| source_type | String | Yes | — | Enum §3.2 — the single source-type this file covers. File-level by path construction. |
| tagged_date | Date | Yes | — | YYYY-MM-DD — run date; matches the `tagged-{date}/` folder + filename suffix. |
| days_window | Number | Yes | 1 | The `--days` value at the invocation that produced the consumed raw. |
| source_count | Number | Yes | 0 | Source-instances crawled (handles / senders / feed-slugs) in the consumed raw. |
| item_count | Number | Yes | 0 | Items surviving the Drop filter (= §1.0 body items). |
| profile_version_consumed | Number | Yes | — | `config/profile.md` `version:` whose §3.0 Domain Interests enum the tagging ran against. |

## 2.0 Markdown Schema

```markdown
---
type: Pulse Tagged Output
schema: pulse-tagged-output
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [pulse, tagged, <source_type>, YYYY-MM-DD]
alias: []
version: 1.0
description: <one-line summary — source-type + dominant domains>
source_type: <linkedin | email | x | rss>
tagged_date: YYYY-MM-DD
days_window: <integer>
source_count: <integer>
item_count: <integer>
profile_version_consumed: <number>
---

# Pulse Tagged Output — <source_type> — YYYY-MM-DD

## 1.0 Tagged Signals

- **[<author_class>]** <source> · `<domain-key>`,`<domain-key>` · <YYYY-MM-DD> — <compact_summary: 1-3 sentences capturing this source's own framing — the angle it took + notable wording, not a flattened neutral fact; enough for synthesis to derive an implication and compare framings across sources, not the full raw item> ↳ <permalink>
- **[<author_class>]** <source> · `<domain-key>` · <YYYY-MM-DD> — <compact_summary> ↳ <permalink>
```

## 3.0 Field Definitions

### 3.1 Body Sections

| Field | Type | Required | Placeholder | Update Rule | Notes |
|-------|------|----------|-------------|-------------|-------|
| H1 Title | Heading | Yes | — | replace | Exactly one H1, format `# Pulse Tagged Output — {source_type} — YYYY-MM-DD`. |
| §1.0 Tagged Signals | Item bullets | Yes | `No items surfaced for {source_type} in {days_window}-day window.` | replace | Flat list of Drop-survivor items. Each bullet carries the six per-item fields: author_class (bracketed lead), source, domain_tags (backticked keys, comma-joined), date (the item's own timestamp — distinct from the file-level `tagged_date` run date), compact_summary, permalink. The brief-assembly layer re-organizes by domain at synthesis, so within-file order is not load-bearing (emission order, typically grouped by source). |

### 3.2 source_type

**Purpose:** The single source-type a tagged file covers. File-level (frontmatter), not per-item — each file is single-source-type by path construction (`{source-type}-tagged.md`).

**Used by:** frontmatter `source_type`; the `tags` list; the H1 title.

| Value | Meaning |
|-------|---------|
| linkedin | LinkedIn posts crawled via `research-crawl-linkedin-posts`. |
| email | Email messages crawled via `research-crawl-email`. |
| x | X/Twitter posts crawled via `research-crawl-x-posts`. |
| rss | RSS/Atom feed items crawled via `research-crawl-rss`. |

### 3.3 author_class

**Purpose:** Classification of each surviving item by authorship relation. The fourth verdict — Drop — is the exclusion class: Drop items never reach the file.

**Used by:** §1.0 Tagged Signals item bullets (bracketed lead).

| Value | Meaning |
|-------|---------|
| Authored | The watchlist source originated the item. |
| Reposted | The source reshared another author's item verbatim. |
| Mentioned | The source is referenced or quoted within an item authored by another. |

Drop (unrelated / promotional / affiliate / off-topic) is the exclusion verdict — those items never reach the file, so Drop is never a stored value.

### 3.4 domain_tags

**Purpose:** One or more of your domain keys tagging each item. The value+key vocabulary is owned by your profile (`config/profile.md` §3.0, governed by `schema-pulse-profile §3.2`); this schema references the keys by value. Multi-tag permitted — an item may carry more than one key.

**Used by:** §1.0 Tagged Signals item bullets (backticked, comma-joined keys).

The keys come from whatever domain set you declare in your profile — the classifier tags against those keys, not a fixed list. The example profile ships an AI/startup/GTM-centered set; yours may differ entirely. Cardinality, scope, and boundary/cross-routing rules are governed at `schema-pulse-profile §3.2` and your `config/profile.md` §3.0 (the runtime scope/boundary classifier contract). The profile is the single source of truth for the vocabulary.

## 4.0 Notes

### 4.1 Writing Conventions

No writing conventions. Classification judgment, compact-summary phrasing, and tagging discipline live in the producer skill body (run-pulse classifier-tagger worker prompt).

### 4.2 Presentation Rules

- One body section only: §1.0 Tagged Signals. The file is a flat tagged-signal list plus provenance frontmatter — no per-domain or per-source sub-sections (domain organization is owned downstream at brief assembly; this layer only classifies and tags).
- Each item bullet renders in field order: `[author_class]` → source → backticked domain keys (comma-joined, no spaces inside backticks) → date → ` — ` compact_summary → ` ↳ ` permalink.
- Domain keys render backticked and comma-joined: `` `ai-agent-systems`,`growth-gtm` ``. Use keys (§3.4), never the display values.
- compact_summary preserves the source's own framing — the angle it took and notable wording — not a flattened neutral restatement, so brief assembly can compare how different sources frame the same story. It stays a précis (enough for downstream synthesis to derive takeaway, implication, and why-it-matters), not the full raw item. The implication payload is added at brief assembly and is absent from this file by contract.
- No cross-source dedup at this layer. Each source's take is preserved as its own item, even when several sources cover the same event — repetition across sources is signal the brief-assembly layer reads as salience, and the differing framings are themselves the insight. Collapsing duplicates here would destroy that signal.
- Frontmatter field order follows §1.0 YAML Header Fields top-to-bottom.

### 4.3 Edge Cases

- **Empty / all-dropped run.** When a source-type yields zero surviving items, the file still writes: frontmatter `item_count: 0`, §1.0 carries the placeholder line. `source_count > 0` with `item_count: 0` distinguishes "crawled but everything Dropped" from "nothing crawled" (`source_count: 0`). The file stays a valid provenance record that the agent ran.
- **Partial crawl.** `source_count` counts successfully-crawled source-instances; sources that fail to crawl drop out, so `source_count` may sit below the watchlist size on a partial run.
- **Missing permalink.** When an item has no public URL (some email messages, or a repost whose original is gone), the `↳` segment carries the best available source-native reference (message-id, feed guid) rather than being omitted — the segment is always present, so downstream citation stays deterministic.
- **Multi-tag item.** An item spanning two domains carries both keys in its bullet; it renders once with both backticked keys, never duplicated per domain.
- **Multi-day window.** When `days_window > 1`, item dates may span several days; no per-day grouping inside §1.0.
- **source_type is file-level.** `source_type` lives in frontmatter only, never per item — each file is single-source-type by construction. The six other per-item fields (source, author_class, domain_tags, compact_summary, permalink, date) vary per bullet.

### 4.4 Other Notes

- This is a per-run intermediate, not a deliverable — the report (`schema-pulse-report`) is the product. The tagged-output files are kept for provenance and re-synthesis; `output/tagged/` is gitignored by default.
- The implication payload (takeaway / implication / why-it-matters) is generated at brief assembly by the synthesis layer and is intentionally absent from this classifier-tagger file — this layer only classifies authorship and tags domains, preserving each source's framing for cross-source comparison downstream.
