---
type: Schema Definition
id: pulse-profile
version: 1.0
description: Defines the hand-authored Pulse profile file, durable, slow-evolving lens context that run-pulse reads as the personal-relevance filter and domain taxonomy for signal analysis.
governs: The Pulse profile file at config/profile.md, durable direction + lens criteria + the domain enum that run-pulse reads at every invocation. Hand-authored; no skill produces it. Ships as config/profile.example.md; copy to config/profile.md and edit to make it yours.
---

# Pulse Profile

## 1.0 YAML Header Fields

| Field | Type | Required | Default | Constraint |
|-------|------|----------|---------|------------|
| type | String | Yes |n/a | Pulse Profile |
| schema | String | Yes |n/a | pulse-profile |
| created | Date | Yes |n/a | YYYY-MM-DD |
| updated | Date | Yes |n/a | YYYY-MM-DD, advances on every edit (typos, phrasing, content). |
| tags | List | Yes | [] | Classification tags. |
| alias | List | Yes | [] | Alternative names. |
| version | Number | Yes | 1.0 | Advances on substantive direction shifts (a changed bet, a new or dropped domain, a new lens-filter category). Minor edits advance `updated:` only. |
| description | String | Yes |n/a | One-line summary of current direction. |

## 2.0 Markdown Schema

```markdown
---
type: Pulse Profile
schema: pulse-profile
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
alias: []
version: 1.0
description: <one-line summary of current direction>
---

# Pulse Profile

## 1.0 North Star + Current Bets

<2-3 short paragraphs. Lead with your one-line vision (north star), the thing the whole feed is read in service of. Follow with current direction bets, where attention is trained right now: the questions you're actively chasing, the stage you're at. Slow-evolving; not edited weekly.>

## 2.0 Skill Targets

<Bulleted list of skills or capabilities you want to deliberately develop. Each bullet is one area, optionally with a one-line note on why it matters. Ordered roughly by current priority. Items consolidate out as they're absorbed; items add in as your direction sharpens.>

## 3.0 Domain Interests

<Your domain enum, the set of domains where signal is welcome, rendered as a keyed table. This is the classifier contract: run-pulse's L1 classifier tags each crawled item against these keys, and the report's per-domain sections are built from them. Define your own domains; the keys you pick here are the keys the whole pipeline uses. Keep the set small and stable (changing it is a version-bump event); items may carry more than one domain tag.>

| # | Domain | Key | Scope | Boundary / cross-routing |
|---|--------|-----|-------|--------------------------|
| 1 | <Domain display name> | `<domain-key>` | <category-identity, the kind of content, not a checklist> | <what sits out / where adjacent content routes> |

## 4.0 Lens Filters

<Three sub-lists naming the operational filter applied to crawl output.

**Relevance amplifiers**: bulleted criteria that promote an item's relevance weight (e.g., "applies to how AI-native companies operate", "increases personal leverage", "informs a decision I'm actively making").

**Drop criteria**: bulleted criteria for exclusion regardless of source (e.g., promotional content, unrelated affiliate marketing, off-topic personal posts, anniversary congrats).

**Pattern-synthesis prompts**: bulleted cross-item connections the synthesis pass actively looks for (e.g., "convergence between AI tooling and growth craft", "shifts in how AI-native companies operate", "emerging leverage primitives").>
```

## 3.0 Field Definitions

### 3.1 Body Sections

| Field | Type | Required | Placeholder | Update Rule | Notes |
|-------|------|----------|-------------|-------------|-------|
| §1.0 North Star + Current Bets | Prose | Yes | Pending future use | replace | Your one-line vision + current direction hypotheses. Slow-evolving (months). |
| §2.0 Skill Targets | List | Yes | Pending future use | additive-subtractive | What to deliberately develop. Each bullet is one area, optionally annotated. |
| §3.0 Domain Interests | Table | Yes |n/a | replace | Your domain enum, as a keyed table. Dual-purpose, drives Layer 1 inclusion AND L1 classifier domain-tagging; the report's per-domain sections reference these keys. Keep it small and stable; changes are version-bump events. |
| §4.0 Lens Filters | List | Yes | Pending future use | additive-subtractive | Explicit relevance amplifiers, drop criteria, and pattern-synthesis prompts. Most operationally load-bearing section. |

### 3.2 Domain

**Purpose:** Your closed taxonomy of domain interests, the value+key vocabulary the L1 classifier tags against and the report's per-domain sections are built from. The keys are user-defined: pick a small, stable set that matches what you actually track. Per-domain scope + boundary/cross-routing rules live in the file's §3.0 (the runtime-read classifier contract).

**Used by:** §3.0 Domain Interests (the file carries the operational scope/boundary); the keys are referenced by `schema-pulse-tagged-output` (`domain_tags[]`) and `schema-pulse-report` (per-domain §2 sections).

The example profile (`config/profile.example.md`) ships an illustrative seven-domain set centered on AI, startups, and go-to-market. Replace it with your own, the pipeline reads whatever keys you declare here, so a finance analyst, a biotech founder, or a hobbyist would each define a different set.

Guidance, not a fixed list:
- **Keep cardinality small and stable** (≈4-8 domains). The classifier tags against this set on every run, and the report renders one section per domain; too many domains fragments the brief.
- **Use lowercase-hyphenated keys** (e.g., `ai-agent-systems`). The keys are the join across the profile, the tagged-output, and the report.
- **Changing the set is a `version` bump.** Add, remove, or rename a domain deliberately, not casually.
- **Multi-tagging is permitted**: an item may carry more than one domain key.

## 4.0 Notes

### 4.1 Writing Conventions

- Concise prose. Each section ≈100-150 words; total file ≤500 words, except §3.0 Domain Interests, which carries the keyed classification contract and runs denser by design. Token budget is load-bearing, run-pulse reads this file on every invocation, so bloat eats into crawl-output context.
- First-person voice acceptable in §1.0. §2.0 + §4.0 lean noun-phrase bulleted with optional one-line annotations; §3.0 is the keyed Domain enum table; avoid full-sentence padding.
- Terms used must resolve in the content space your watchlists cover, the file is an LLM-consumed lens, so jargon that nobody in your sources uses fails to filter.

### 4.2 Presentation Rules

- §1.0 precedes §2.0, §4.0 because vision shapes which skills, domains, and filters matter.
- §4.0 Lens Filters carries the most operational weight at synthesis time, relevance amplifiers + drop criteria + pattern prompts are read as direct instructions to the report-writing pass.

### 4.3 Edge Cases

- File is hand-authored only. No skill produces or updates it; you edit it manually as your direction shifts.
- Empty profile (all sections still placeholder), run-pulse proceeds but the personal-relevance lens is weakly differentiated from raw world signal.

### 4.4 Other Notes

- The §3.0 domain enum is the single source of truth for the domain vocabulary. `schema-pulse-tagged-output` and `schema-pulse-report` mirror the keys for local readability, but the profile is canonical, change a key here and update those references.
