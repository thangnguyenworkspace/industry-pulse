---
type: Schema Definition
id: pulse-report
version: 1.0
description: Defines the Pulse signals brief — the neutral, domain-first intelligence report run-pulse produces per invocation. Coverage strip + executive summary + per-domain pulse + cross-domain & cross-source patterns, with Title Sentence headlines, second-order analytical depth, cross-source signal synthesis (repetition = salience, framing divergence = insight), and provenance frontmatter tracking per-source-type crawl counts + lens consumed.
governs: Pulse signals brief files produced by run-pulse — one per invocation at output/reports/pulse-report-{YYYY-MM-DD}/pulse-report-{YYYY-MM-DD}.md.
applies_to: "output/reports/pulse-report-*/pulse-report-*.md"
---

# Pulse Report

This schema defines the **signals brief** — the neutral, forwardable intelligence report that the public Pulse pipeline produces and stops at. It is the public seam: relevance analysis, personalization, and delivery all sit downstream of this artifact and are left as extension points (see the repo README and `examples/`). The brief is written in neutral third-person and carries no personal or project-specific content by construction.

## 1.0 YAML Header Fields

| Field | Type | Required | Default | Constraint |
|-------|------|----------|---------|------------|
| type | String | Yes | — | Pulse Report |
| schema | String | Yes | — | pulse-report |
| created | Date | Yes | — | YYYY-MM-DD — report-creation date; matches `report_date`. |
| updated | Date | Yes | — | YYYY-MM-DD — matches `created` (reports are immutable post-write). |
| tags | List | Yes | [] | Minimum `[pulse, report]` plus the date tag (e.g., `2026-05-27`). |
| alias | List | Yes | [] | Alternative names. |
| version | Number | Yes | 1.0 | Always 1.0 (reports do not version). |
| description | String | Yes | — | One-line summary of the report's headline pattern. |
| report_date | Date | Yes | — | YYYY-MM-DD — date of the report. Matches the per-run folder + filename date. |
| days_window | Number | Yes | 1 | The `--days` value at invocation. |
| linkedin_source_count | Number | Yes | 0 | LinkedIn URLs crawled from watchlist. |
| linkedin_post_count | Number | Yes | 0 | Posts surfaced after Drop filter (Authored + Reposted + Mentioned). |
| email_sender_count | Number | Yes | 0 | Email senders crawled; 0 when email watchlist empty or skipped. |
| email_message_count | Number | Yes | 0 | Messages surfaced after Drop filter. |
| x_handle_count | Number | Yes | 0 | X handles crawled; 0 when X watchlist empty or skipped. |
| x_post_count | Number | Yes | 0 | X posts surfaced after Drop filter. |
| rss_feed_count | Number | Yes | 0 | RSS feeds crawled; 0 when RSS watchlist empty or skipped. |
| rss_item_count | Number | Yes | 0 | RSS items surfaced after Drop filter. |
| profile_version_consumed | Number | Yes | — | Profile `version:` value at read time. |

## 2.0 Markdown Schema

````markdown
---
type: Pulse Report
schema: pulse-report
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [pulse, report, YYYY-MM-DD]
alias: []
version: 1.0
description: <one-line summary of headline pattern>
report_date: YYYY-MM-DD
days_window: <integer>
linkedin_source_count: <integer>
linkedin_post_count: <integer>
email_sender_count: <integer>
email_message_count: <integer>
x_handle_count: <integer>
x_post_count: <integer>
rss_feed_count: <integer>
rss_item_count: <integer>
profile_version_consumed: <number>
---

# Pulse Report: YYYY-MM-DD

> **Today:** <total> signals · LinkedIn <n> · X <n> · RSS <n> · Email <n> · across <n> domains · <days_window>-day window

## 1.0 Executive Summary

- **<Title-Sentence headline naming a cross-domain or cross-source pattern of the day.>** <2-3 sentence neutral body>. *<metadata tail, e.g., "heaviest: §2.0 AI & Agent Systems" or "drives §3.0 Trend 1" or "across 6 sources, 3 source-types">*
- **<Title-Sentence headline.>** <2-3 sentence neutral body>. *<metadata tail>*
- **<Title-Sentence headline.>** <2-3 sentence neutral body>. *<metadata tail>*

## 2.0 Per-Domain Pulse

### <Domain display name — from your profile §3.0 domain enum>

<2-3 sentence neutral intro: why this domain is surfacing now.>

- **<takeaway>.** <implication>. <why-it-matters>. <source inline tag(s); when corroborated across multiple sources, list them and append a terse spread cue, e.g., `via @swyx · via Stratechery · across 5 sources`> · <permalink(s)>
- **<takeaway>.** <implication>. <why-it-matters>. <source inline tag> · <permalink>

### <Next domain by item-density>

- ...

## 3.0 Cross-Domain & Cross-Source Patterns

### <Emerging cross-domain trend, or a cross-source convergence>

**<Title-Sentence claim naming the trend or the cross-source story.>** <Evidence — 2-3 sentences citing convergent sources by name + permalink where useful. Cross-domain trend: sources across two or more §2.0 domains. Cross-source convergence: the multiple sources (and source-types) carrying one story, with explicit attention to how their framings diverge.> <Implication — 1-2 sentences naming what the pattern signals.>

```mermaid
<Conditional per trend; minimum 2 across §3.0. Include when the trend has natural visual mapping (cross-domain convergence topology, layer stack, framing-divergence spread). Use `<br/>` for line breaks inside node labels; never `\n`.>
```

### <Next trend or convergence>

<...>
````

## 3.0 Field Definitions

### 3.1 Body Sections

| Field | Type | Required | Placeholder | Update Rule | Notes |
|-------|------|----------|-------------|-------------|-------|
| H1 Title | Heading | Yes | — | replace | Exactly one H1, format `# Pulse Report: YYYY-MM-DD`. |
| Coverage Strip | Blockquote | Yes | — | replace | One blockquote line directly under the H1, before §1.0, derived from the frontmatter survivor counts: `> **Today:** {total} signals · LinkedIn {n} · X {n} · RSS {n} · Email {n} · across {n} domains · {days_window}-day window`. Omit any source-type term whose count is 0. Surfaces the run's breadth before the reader dives; not a heading, so it does not affect section numbering. |
| §1.0 Executive Summary | Headline bullets | Yes | `No headline patterns surfaced for this run.` | replace | 3-5 scannable bullets covering the run's heaviest cross-domain and cross-source patterns. Each bullet pairs a bold Title-Sentence headline lead with a 2-3 sentence neutral body and an italicized metadata-tail cue (domain in §2.0, trend reference in §3.0, or source-spread such as `across 6 sources`). Stories corroborated across many sources weight toward the top — source-spread is salience. Reader scans the Title Sentences in ≤30 seconds and decides where to dive. |
| §2.0 Per-Domain Pulse | Per-domain bullets | Yes | `No items surfaced in {days_window}-day window.` | replace | Cross-source signal organized by domain. Synthesis unit: per-domain. H3 sub-sections name each domain from your profile §3.0 enum; each H3 weaves LinkedIn + email + X + RSS items into one cross-source narrative. H3 domains order by item-count (heaviest first); empty domains do not render, thin domains sort to the bottom. Each item carries takeaway + implication + why-it-matters + source inline tag + permalink, with varied depth — marquee items in each cluster developed with genuine second-order analysis, supporting items kept tight; no fixed sentence cap, but every item earns its length with a non-obvious point rather than a fact-dump. When a story is corroborated across multiple sources, the item lists the corroborating sources and appends a terse source-spread cue (`across N sources`); the full framing-divergence analysis lives in §3.0. Corroborating items are never collapsed in a way that hides the spread. When a domain carries ≥6 items, group its bullets under bold thematic sub-labels named in the intro so the reader scans the cluster shape before the items; thin domains stay flat. |
| §3.0 Cross-Domain & Cross-Source Patterns | Trend prose (+ minimum 2 Mermaid) | Yes | `No cross-domain or cross-source patterns surfaced in {days_window}-day window.` | replace | Convergence, emerging trends, and shifts spanning two or more §2.0 domains, OR a single story corroborated across multiple sources/source-types (a single-domain cross-source convergence qualifies — the axis does not require cross-domain span). Synthesis unit: per-emerging-trend or per-cross-source-convergence. H3 sub-sections name each trend; each body follows a three-part structure — bold Title-Sentence claim lead → 2-3 sentences evidence (for a cross-source convergence, this is where how each source frames the story is analyzed) → 1-2 sentences implication. Per-trend cap ~400 words. Minimum 2 Mermaid diagrams required across §3.0 trends — pick the 2 with strongest topology fit (cross-domain convergence-flow, layer-stack, framing-divergence spread); skip categorical / contrast / thesis-type trends. |

## 4.0 Notes

### 4.1 Writing Conventions

No writing conventions here. Tone, sentence structure, and synthesis style live in the producer skill body (run-pulse). The rules below are presentation rules read at authoring time.

### 4.2 Presentation Rules

- Section order is fixed: coverage strip → §1.0 → §2.0 → §3.0. Reader scans the coverage strip + executive summary first (≤30 seconds), then dives as relevance dictates: per-domain signal → cross-domain patterns.
- **Coverage strip.** A single blockquote line directly under the H1, before §1.0, derived from the frontmatter survivor counts. Omit any source-type term whose count is 0. Not a heading, so it does not change section numbering.
- Frontmatter field order follows §1.0 YAML Header Fields top-to-bottom.
- **Voice register: neutral third-person.** The brief is the forwardable public artifact — no second-person address, no reader-specific asides, no project content. State what the signal is and what it implies for the field, not for any one reader. Personalization (coach voice, "this matters for you because…") is an extension layer you add downstream of this brief, not part of it.
- **Analytical depth is the standard — second-order analysis, not summary.** Every item earns its place with a non-obvious point: a second-order effect (X happened, so the non-obvious consequence is Y), a hidden tension or trade-off, an incentive read (who benefits from a framing and what that reveals), a cross-item pattern (when several items are secretly one shift), or a contrarian / disconfirming angle. Surface what most readers skim past — the buried detail that is actually the point. Where the day allows, develop one connective idea across sections rather than listing many disconnected facts. Never explain the obvious.
- **No fact-dumping; write connected, flowing sentences.** Each bullet reads as developed reasoning with transitions, not a telegraphic "takeaway, implication, why" fragment. Every named entity earns its framing: when a company, product, person, or protocol is named, the item gives what it is, why it matters, and what trend it signals, never a bare name. The reader skims until something catches and then slows down, so each item must hold real substance to reward the slowdown.
- **Title Sentence convention.** Where a bolded lead-in opens a §1.0 bullet body or a §3.0 trend body, that lead is a Title Sentence — first letter of every word capitalized, ends with a period. Example: `**The Agentic-Commerce Protocol Race Just Got Real This Week.**` Title Sentences are scannable headlines the reader can skim alone. Sentence-case bold leads still apply at §2.0 per-item takeaways (these are item-level facts, not headline patterns).
- §1.0 Executive Summary bullets cap at five (target 3-5). Each renders as: Title Sentence (bold, Title Case) → 2-3 sentence neutral body → italicized metadata tail. The metadata tail uses one or more cue forms: heaviest domain (`heaviest: §2.0 AI & Agent Systems`), trend reference (`drives §3.0 Trend 1`), or source-spread (`across 6 sources`). Stories corroborated across many sources weight toward the top. A §1.0 bullet states the claim + (for a story that earns a full §3.0 trend) a `§3.0` pointer — it does not pre-build §3.0's source-by-source evidence; §1.0 is the headline altitude, §3.0 is the evidence build, and the two must not read as verbatim duplicates.
- §2.0 H3 domains are the domain axis — one H3 per domain from your profile §3.0 enum, ordered by item-count (heaviest first), thin domains sorting to the bottom. A domain with a single item still renders its H3; empty domains omit entirely. Each H3 with items opens with a 2-3 sentence neutral intro paragraph above the bullet list — context for why the domain is surfacing now. When a domain carries ≥6 items, group its bullets under bold thematic sub-labels named in the intro; thin domains stay flat. Vary the intro opening across domains — do not template every domain on "This was the heaviest domain…".
- §2.0 bullets carry varied depth, not a fixed cap: the marquee items in each cluster get genuine multi-sentence analysis (a second-order read — a hidden tension, an incentive, a buried detail — not a summary), while supporting items stay tight. Each bullet weaves whichever source-types carry the signal into the domain narrative and earns its length with a non-obvious point; the permalink carries the raw depth, the bullet carries the insight.
- §3.0 trends each follow the structure: H3 (sentence-case descriptive heading) → Title Sentence body opener → 2-3 paragraphs of argumentative prose covering (a) what the pattern is + who's carrying it (across which §2.0 domains for a cross-domain trend, or across which sources/source-types for a cross-source convergence — including how each source's framing differs), then (b) what the pattern signals for the field. Optional closing Title Sentence permitted. Per-trend cap ~400 words.
- **Cross-source signal.** Repetition across sources is salience, not redundancy: a story corroborated across many sources weights toward §1.0 and the top of its §2.0 domain, and surfaces with a terse source-spread cue (corroborating sources listed, never collapsed to hide the spread). When the corroborating sources frame the story differently, that divergence is first-class insight — give it full prose in §3.0 as a cross-source convergence (what the story is, who's carrying it, and specifically how each source's framing differs + what that tells you). Single-domain convergences (one story, many sources, same domain) are valid §3.0 trends — the cross-source axis does not require cross-domain span.
- §3.0 Mermaid diagrams require a minimum of 2 across trends. Pick the 2 trends with strongest topology fit (typically cross-domain convergence-flow trends, layer-stack trends); skip categorical / contrast / thesis-type trends — forced diagrams on thesis trends are worse than skip. When 3 or 4 trends genuinely fit, more is fine; the rule is a minimum, not an exact count.
- §3.0 Mermaid line breaks inside node labels use `<br/>`, never `\n`. Most renderers show `<br/>` cleanly and `\n` literally.
- Source inline tags within bullets use `via {author display name}` for LinkedIn, `via {sender email}` for email, `via {@handle}` for X, `via {feed display name}` for RSS; classification tags (e.g., `reposted {original author}`, `mentions {entity}`) append after the via clause.
- Permalinks render at the tail of each bullet, separated by ` · ` (middle dot with surrounding spaces).
- **No em dashes in the report.** The body carries zero literal `—`, in prose and in item separators alike; use commas, parentheses, colons, or sentence breaks instead. The producer skill enforces this at authoring and at a dedicated QC gate.
- Length serves comprehension, not a target. Depth and connective reasoning set the length, never a quota. The only firm rule is the floor: never compress a section to where ideas can't develop (no nuance, no example, no trade-off).

### 4.3 Edge Cases

- **Empty section.** When a section surfaces zero items (quiet day, no headline patterns, no cross-domain patterns), render the section header and replace the body with the placeholder line from §3.1. Section header always present.
- **Empty source-type run.** Any source-type can contribute zero: its `{type}_*` counts set to 0 and items source entirely from the remaining types. Report stays valid (e.g., an email-light day with `x_post_count: 0` and `rss_item_count: 0`).
- **All-empty run.** When all four source-types return zero usable items, the report file still writes — all sections carry the placeholder line and every count is 0. Useful as a provenance record that the invocation ran.
- **Empty vs single-item domain.** In §2.0 a domain with zero items omits its H3 entirely; a domain with a single item still renders its H3 (the domain is the fixed axis from your profile enum).
- **Multi-day window aggregation.** When `days_window > 1`, the synthesis aggregates across the full window; per-item dates may span several days. No per-day grouping inside sections.
- **Thin-section check.** Length is comprehension-driven, so there is no hard band to police; the length check is qualitative — if a section reads as summary without analysis (no second-order point, no trade-off, no development), the producer skill warns that the section is thin and the user decides whether to deepen or accept.

### 4.4 The publishable seam

This brief is the boundary between the public pipeline and your own layer. Because it is neutral and personal-free by construction, it is forwardable as-is and is the natural input to a relevance step you implement yourself: take this brief plus a context object (a portfolio, a company, a project, a research area), run your own relevance logic, and emit whatever downstream artifact you want (a personalized digest, a notification, a routed message). The repo's `examples/` directory shows two worked relevance implementations that consume this brief; the core pipeline never depends on them.
