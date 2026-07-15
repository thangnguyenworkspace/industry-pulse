# AGENTS.md

Entry point for an agent operating or ingesting this repository. This is the single canonical agent-instruction file; [CLAUDE.md](CLAUDE.md) imports it, so the two cannot drift. Edit this file, never CLAUDE.md. The human entry point is [README.md](README.md).

## What this is

industry-pulse is a watchlist-driven intelligence pipeline you run on demand. It crawls LinkedIn, X, RSS, and email, classifies and domain-tags every post in parallel against a profile you define, and writes one neutral, cited signals brief per run. The brief names nothing personal, so it stays forwardable; the relevance-and-delivery layer that scores a brief against your own context attaches at a documented seam and is not part of this repo. It is a frozen snapshot: the agent's job here is orientation, not modification.

## Architecture

Three layers kept apart so the heavy reading never lands in the thread doing synthesis: pure-primitive crawl leaves, a parallel classify-and-tag fan-out, and a single-threaded synthesis pass that writes the brief. The full design, including the volume-aware auto-scaler and the context-isolation discipline, is the canonical statement in [docs/architecture.md](docs/architecture.md).

## How to navigate

| Path | What it is | Read it when |
|---|---|---|
| `README.md` | Human entry point: thesis, quickstart, design decisions | Orienting to what the project is and how to run it |
| `docs/architecture.md` | The three layers, the auto-scaler, cost discipline, context isolation | You need the full mechanics behind a run |
| `.claude/skills/run-pulse/SKILL.md` | The orchestrator, top-to-bottom with every path and decision spelled out | Tracing or changing how a run is sequenced |
| `.claude/skills/research-crawl-*/SKILL.md` | The four crawl leaves (LinkedIn, X, RSS, email), one pure primitive each | Working on a single source lane |
| `config/` | The lens you supply: `profile.example.md` + `watchlists/*.example.md` | Setting up or changing what the pipeline reads through |
| `schemas/` | Markdown contracts for every file the pipeline reads or writes | Checking or changing a file's shape |
| `docs/setup.md` | Clean-clone-to-first-brief setup, MCP servers included | Onboarding a fresh clone |
| `docs/extending.md` | The relevance seam, delivery adapters, adding a source lane | Building your own relevance or delivery layer |
| `scripts/rss-ingest.py` | The one standalone executable: the feedparser engine the RSS leaf calls | Running or debugging the RSS lane outside the harness |

## Run it

The full pipeline runs inside Claude Code, where the skills are slash commands. First-run setup copies the example config and adds one secret:

```
cp .env.example .env                 # add APIFY_TOKEN (needed only for the paid lanes)
cp .mcp.json.example .mcp.json       # configure Apify, plus Gmail for the email lane
cp config/profile.example.md config/profile.md                 # make the lens yours
for f in config/watchlists/*.example.md; do cp "$f" "${f%.example.md}.md"; done   # then curate
```

Then open the repo in Claude Code and run:

```
/run-pulse           # 1-day window across every non-empty lane
/run-pulse --days=7  # a wider weekly compression run
```

The brief lands in `output/reports/pulse-report-<date>/`. Full setup, including the MCP servers, is in `docs/setup.md`.

One component runs standalone, no harness, anywhere Python 3 with `feedparser` is installed:

```
python3 scripts/rss-ingest.py --url https://news.ycombinator.com/rss --name hackernews --days 2 --out-dir ./out
```

## Boundaries

| Scope | Paths |
|---|---|
| Safe to modify | `docs/**`, `examples/**`, `config/*.example.md`, `config/watchlists/*.example.md` |
| Ask first | `scripts/rss-ingest.py`, `.claude/skills/**`, `schemas/**` |
| Never touch | `.env`, `.mcp.json`, `config/profile.md`, `config/watchlists/*-watchlist.md`, `output/**` |

The values above are rendered from `repo-manifest.json` `boundaries`; the manifest owns them. The never-touch paths are the private lens and secrets that are gitignored and never shipped.

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
- **Artifact type:** `app`, not `skill-package`. The `.claude/skills/` bundle is this app's implementation, run only inside its own pipeline; it is not published as versioned, independently-pinnable capabilities with trigger evals, so the skill-package obligations (a capabilities index, per-skill evals) do not apply. The type is a deliberate choice, not an omission.
- **Build provenance:** built with Claude Code. MIT licensed. `CLAUDE.md` is an import shim over this file, not separately maintained content.
- **Deliberately withheld:** the private relevance-and-delivery layer (how briefs get scored and routed) and the real profile and watchlists. Only `*.example` configs ship. This is by design: the reusable core is the published part, the personal layer is not.
- **Known limitation:** the pipeline executes only inside Claude Code, since the skills are slash commands. On another harness the `SKILL.md` files read as prose but do not run. `scripts/rss-ingest.py` is the one piece that runs anywhere Python does.
