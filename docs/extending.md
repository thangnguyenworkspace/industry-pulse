# Extending

The core stops at the neutral signals brief. Everything that makes the output *yours* is an extension point. This guide covers the three you are most likely to reach for — the relevance seam, delivery, and a new source-type lane.

## The relevance seam

The brief is the contract between the reusable core and your layer. It is neutral and personal-free, so it is the natural input to a relevance step you implement.

```
brief  +  your context object   →   your relevance logic   →   a relevance artifact
(IN)      (portfolio, company,       (sub-agent or inline)       (per-context take +
           project, research…)                                    optional action)
```

- **IN** — the gated brief (markdown per `schema-pulse-report`) plus a *context object*. A context object is whatever you want the brief scored against: a stock portfolio, a company's positioning, a personal project, a startup thesis, a research area. The brief's patterns and per-domain analysis are finished; your layer *applies* them, it does not re-derive them.
- **PROCESS** — your relevance logic. Two patterns, picked by fan-out:
  - **Sub-agent per context** when you check several contexts in parallel. Each agent reads the brief plus one context and returns that context's take in its own isolated window. This is the same context-isolation lever the core uses — keep the per-context reading out of your orchestrating thread. See [`examples/project-relevance/`](../examples/project-relevance/).
  - **Inline** when you have one or two contexts. Read the brief plus the context in the main workflow and write the take directly. See [`examples/portfolio-relevance/`](../examples/portfolio-relevance/).
- **OUT** — a relevance artifact per context. The repo ships a recommended shape (`schema-pulse-project-relevance`: a few second-order relevance items, each carrying its source permalink, plus one suggested action) as a *shape, not a mandate* — emit whatever your downstream needs.

The two worked examples in [`examples/`](../examples/) are self-contained and swappable. The core never imports them, so delete or replace them freely.

### The recommended relevance artifact

If you want a starting shape, the per-context artifact that the internal system produced looked like this:

```markdown
## 1.0 Relevance Items
- **<what today's signal means for this context>.** <second-order implication>. <the non-obvious move or trade-off>. Hooks to: <which part of the context>. <source> · <permalink>

## 2.0 Suggested Action
- **<one concrete next move the signal implies>.** <source / pointer> · <permalink>
```

Two rules carried real weight: every relevance item keeps its **source permalink** (a take you cannot click through to is incomplete), and every item is a **second-order point** — what the signal *means* for this context and the move it implies, not a restatement of the brief's fact.

## Delivery

Delivery is yours, and the default already happened: the brief is written to disk. That is the out-of-box delivery, with no PDF, email, or notification dependency. Anything richer is an optional adapter you bolt on after the brief (or after a relevance artifact):

- **File** — the default. The brief (and any relevance artifact) is markdown on disk.
- **PDF** — render the markdown with your own toolchain (for example `pandoc`, plus a Mermaid renderer for the `§3.0` diagrams). Keep it a thin adapter, not a core dependency.
- **Email / notify / route** — push the brief or a relevance take to an inbox, a chat channel, or a queue. This is a few lines wrapping whatever transport you already use.

Keep adapters downstream of the artifact so the core stays dependency-free and runnable from a clean clone.

## Adding a new source-type lane

The four lanes share one shape, so a fifth (a forum, a Slack export, a podcast transcript feed) follows the existing pattern:

1. **Write a crawl leaf** as a pure primitive — it takes a source list, writes one markdown file per source into a dated `output/raw/{lane}/` subdir, and returns a compact summary. Spawn no sub-agents inside it; the caller owns isolation. Model it on `research-crawl-rss` (free backend) or `research-crawl-x-posts` (paid MCP backend).
2. **Extend the watchlist schema** — add your `source_type` value and any new `Entity Type` values to `schemas/schema-pulse-watchlist.md` (§3.2 / §3.3), then create `config/watchlists/{lane}-watchlist.md`. The seven-column entry table shape stays fixed.
3. **Wire it into `run-pulse`** — add the watchlist path to Global References, a read step, a bin in the auto-scaler (count-sharded like X/LinkedIn, or volume-binned like RSS), and a classifier worker prompt that reuses the shared classifier contract. The classifier contract and the tagged-output shape do not change — a new lane just feeds more tagged files into the same synthesis.

Because the synthesis reads *every* tagged file in the run, a new lane needs no synthesis changes — its items flow into the per-domain brief automatically.

## Retargeting the whole pipeline

You do not need new code to point Pulse at a different world. Rewrite `config/profile.md` — its domain enum and lens filters — and curate different watchlists, and the same pipeline produces a brief for a biotech investor, a policy analyst, or a hobbyist. The profile is the lens; everything else is plumbing.
