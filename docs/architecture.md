# Architecture

Pulse is a three-layer pipeline. Raw crawling, classification, and synthesis are separated so the heavy, parallelizable reading never touches the orchestrating thread, and so each layer has one job.

```
L0  Crawl leaves        pull raw posts per source type (pure primitives)
L1  Classifier workers  bucket + domain-tag each item, preserve framing  (parallel fan-out)
L3  Synthesis           the main thread writes one neutral signals brief
```

There is no L2. An intermediate per-domain synthesis layer was considered and dropped: the main thread synthesizes across domains directly from the tagged files, and the token math did not justify the extra hop. The layer numbers come from the internal design and are kept so the layers read consistently.

## L0: crawl leaves

Four leaves, one per source type, each a pure primitive: it owns its API mechanics and pitfalls and spawns no sub-agents of its own. The caller owns isolation.

| Lane | Leaf | Backend | Paid? |
|---|---|---|---|
| LinkedIn | `research-crawl-linkedin-posts` | Apify actor | Yes |
| X | `research-crawl-x-posts` | Apify actor (+ inline X-Article enrichment) | Yes |
| RSS | `research-crawl-rss` | Python `feedparser` via subprocess | No |
| Email | `research-crawl-email` | Gmail MCP | No |

Each leaf writes one markdown file per source into a dated `output/raw/{lane}/` subdir and returns a compact summary, not the raw bodies. The bodies stay on disk for the L1 workers to read, so a large crawl never inflates the main thread's context.

## L1: classifier workers

A fan-out of workers, each handling one slice of one lane. Every worker runs the same contract: classify each item as **Authored / Reposted / Mentioned / Drop**, drop anything matching the profile's drop criteria, then tag each survivor with one or more of *your* domain keys (from `config/profile.md` §3.0). Workers preserve each source's own framing in a short summary and never dedupe. Repetition across sources is signal, not noise. Each worker writes one tagged-output file (`schema-pulse-tagged-output`) and returns counts only.

Two worker shapes share that contract:

- **Crawl-and-classify** (LinkedIn, X, email): the worker invokes its leaf in-process on its source slice, so the Apify or Gmail raw dataset lands in the worker's context, not the main thread's, then classifies.
- **Classify-only** (RSS): the RSS raw is already on disk (see the auto-scaler below), so the worker just reads its assigned feed files and classifies.

### The auto-scaler

Worker counts are computed per run, never hard-coded, because volume varies. Each lane bins differently:

- **RSS: volume bins.** RSS is crawled first (it is free), which yields a real per-feed token estimate. Feeds are partitioned by dispatch class (deep-content vs news-firehose, they load on different axes), then greedily packed into bins so each bin stays under a per-worker token budget (`L1_TOKEN_BUDGET`, default 25k).
- **X + LinkedIn: count bins.** The paid lanes cannot free-probe volume, so they shard on the known watchlist count: `ceil(source_count / SOURCES_PER_WORKER)` bins (default 30 sources per worker), split into near-even contiguous slices.
- **Email: one worker.** Sender counts are small; email never shards.

If the total worker count exceeds the concurrency cap (`L1_CONCURRENCY_CAP`, default 14), the smallest bins merge until it fits, and the cap-hit is logged as a signal to raise the cap or split a watchlist. All workers dispatch in a single message so they run in parallel.

## L3: synthesis

The main thread reads every tagged file and writes one brief (`schema-pulse-report`): a coverage strip, an executive summary, a per-domain pulse, and a cross-domain & cross-source patterns section. This is the only layer that adds the implication payload (takeaway + implication + why-it-matters) that the tagged files omit by contract. This is the judgment pass.

The brief is written in neutral third-person and carries no personal or project content, which is what makes it the forwardable public artifact and the seam to your own layer. It then passes a QC gate: a dedicated sub-agent reviews it against a quality checklist and returns findings; the main thread (which holds the brief in context) applies the fixes and re-checks, looping until clean or three passes. Everything downstream stands on the brief, so the hard cross-thread reasoning finishes here.

## Cost discipline

Only LinkedIn and X cost money (Apify). Two rules keep spend bounded:

- **Per-source caps are the only enforceable limit.** Every crawl passes a per-URL / per-handle max (`--linkedin-max-posts`, `--x-max-per-handle`). Do not rely on any total-charge ceiling. Cap the per-source volume instead.
- **A cost estimate is shown before any paid dispatch.** The plan-and-confirm step prints an estimate and waits for approval; RSS and email have already run (free) by then, so you approve only the paid lanes. Realistic spend tends to run well under the worst-case estimate for short windows.

## Context isolation

The recurring lever: keep heavy reading out of the orchestrating thread. Leaves return summaries and write bodies to disk. Crawl-and-classify workers pull the raw dataset into their own window. The main thread holds only the tagged signal files plus the synthesis it is writing. The same lever is what you reuse downstream: run each relevance check in its own sub-agent so the per-context reading never bloats your orchestrator. See [extending.md](extending.md).
