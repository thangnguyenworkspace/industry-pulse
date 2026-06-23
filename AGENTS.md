# AGENTS.md

## What this is

industry-pulse is a watchlist-driven intelligence pipeline you run on demand. It crawls LinkedIn, X, RSS, and email, classifies and domain-tags every post in parallel against a profile you define, and writes one neutral, cited signals brief per run. The brief names nothing personal, so it stays forwardable; the relevance-and-delivery layer that scores a brief against your own context attaches at a documented seam and is not part of this repo. The pipeline is built as Claude Code Agent Skills plus one standalone Python helper. This file orients an agent reading the repo cold: the project produces a brief, it is not a hosted service.

## Architecture

Three layers, kept apart so the heavy reading never lands in the thread doing synthesis:

- **Crawl leaves** (`.claude/skills/research-crawl-*`): four pure-primitive crawlers, one per source (LinkedIn, X, RSS, email). RSS runs free up front to size the run; the paid lanes (LinkedIn and X, via Apify) run only after a cost gate you approve.
- **Classify and tag**: a fan-out of parallel workers buckets each item (authored, reposted, mentioned, or dropped) and domain-tags it against the profile, keeping each source's own framing intact.
- **Synthesis**: the main thread reads every tagged file and writes one neutral signals brief, reading repetition across sources as salience and disagreement as insight.

The reusable core ends at the brief. The private relevance-and-delivery layer attaches across "the seam" and does not ship; two worked stand-ins live in `examples/`. Full mechanics, including the volume-aware auto-scaler and the context-isolation discipline, are in `docs/architecture.md`.

## How to navigate

Read `README.md` first, then `docs/architecture.md`, then `.claude/skills/run-pulse/SKILL.md` (the orchestrator). The layout:

- `.claude/skills/`: the pipeline itself. `run-pulse/` orchestrates; `research-crawl-{linkedin-posts,x-posts,rss,email}/` are the four crawl leaves. Each is a `SKILL.md` that reads top to bottom with every path and decision spelled out.
- `config/`: the lens you supply. `profile.example.md` (north star, domains, filters) and `watchlists/*-watchlist.example.md` (curated sources per lane).
- `schemas/`: the markdown contracts for every file the pipeline reads or writes (`schema-pulse-profile`, `-watchlist`, `-tagged-output`, `-report`). Each carries `id`, `version`, `governs`, and `applies_to`.
- `docs/`: `architecture.md`, `setup.md` (clean clone to first brief), `extending.md` (the seam, delivery adapters, adding a lane).
- `examples/`: two self-contained relevance implementations at the seam (`portfolio-relevance/`, `project-relevance/`). The core never imports them.
- `scripts/rss-ingest.py`: the single standalone executable, the feedparser engine the RSS leaf calls.
- `output/`: generated briefs and intermediates. Gitignored and regenerable per run.

## Run it

The full pipeline runs inside Claude Code, where the skills are slash commands. First-run setup copies the example config and adds one secret:

```
cp .env.example .env                 # add APIFY_TOKEN (needed only for the paid lanes)
cp .mcp.json.example .mcp.json       # Apify, plus Gmail for the email lane
cp config/profile.example.md config/profile.md
for f in config/watchlists/*.example.md; do cp "$f" "${f%.example.md}.md"; done
```

Then open the repo in Claude Code and run:

```
/run-pulse            # 1-day window across every non-empty lane
/run-pulse --days=7   # wider weekly compression run
```

The brief lands in `output/reports/pulse-report-<date>/`. Full setup, including the MCP servers, is in `docs/setup.md`.

One component runs standalone, no harness, anywhere Python 3 with `feedparser` is installed:

```
python3 scripts/rss-ingest.py --url https://news.ycombinator.com/rss --name hackernews --days 2 --out-dir ./out
```

## Conventions

Rules that hold across the repo, stated so they are checkable:

- **Path-driven config, no hidden loader.** Every path the pipeline reads or writes is declared in the `### Global References` block at the top of each skill. That block is the whole configuration surface.
- **`*.example` for everything you supply.** The real `.env`, `.mcp.json`, and `config/*.md` are gitignored; onboarding is `cp`. Never commit the real ones.
- **Markdown is the interchange format.** Skills, schemas, docs, and output are markdown; `scripts/rss-ingest.py` is the only executable code.
- **Schemas are contracts.** Each `schemas/*.md` carries `id`, `version`, `governs`, and `applies_to`; an artifact maps to its schema through the `applies_to` glob.
- **Generated output is disposable.** Everything under `output/` is gitignored and regenerable; only `output/.gitkeep` is tracked.
- **The core never imports `examples/`.** The relevance seam is a hard boundary; the examples sit downstream of it and are safe to delete or replace.

## Status & provenance

- **Maturity:** stable snapshot. A point-in-time release of a system run privately, complete as shipped. Not actively maintained; issues and pull requests are not watched.
- **Build provenance:** built with Claude Code. MIT licensed.
- **Deliberately withheld:** the private relevance-and-delivery layer (how briefs get scored and routed) and the real profile and watchlists. Only `*.example` configs ship. This is by design: the reusable core is the published part, the personal layer is not.
- **Known limitation:** the pipeline executes only inside Claude Code, since the skills are slash commands. On another harness the `SKILL.md` files read as prose but do not run. `scripts/rss-ingest.py` is the one piece that runs anywhere Python does.
