# Setup

From a clean clone to a first brief. Most of this is one-time.

## Prerequisites

- **[Claude Code](https://claude.com/claude-code)** (or another agent harness that runs `.claude/commands/` skills and supports MCP). You drive the pipeline by invoking `/run-pulse` inside it.
- **Node.js** — only to run the Apify MCP server via `npx` (the LinkedIn + X lanes). Skip if you run neither paid lane.
- **Python 3** with **`feedparser`** — only for the RSS lane: `pip install feedparser`. Skip if you run no RSS.
- **An Apify account + API token** — for LinkedIn + X. Get one at <https://console.apify.com/account/integrations>. Skip if you run neither.
- **A Gmail MCP server** — only for the email lane.

Nothing here is required for all four lanes at once. Run only the lanes you want; empty watchlists skip, and missing optional tooling just drops its lane.

## 1. Configure secrets and MCP servers

```bash
cp .env.example .env
cp .mcp.json.example .mcp.json
```

- **`.env`** — set `APIFY_TOKEN` to your token. This is the only secret the core needs. `.env` is gitignored.
- **`.mcp.json`** — declare the MCP servers your harness loads. The shipped example wires Apify via `npx @apify/actors-mcp-server` and reads `APIFY_TOKEN` from `.env`. Add a Gmail MCP server here if you want the email lane; configure it per your provider. `.mcp.json` is gitignored.

The crawl leaves call the `mcp__apify__*` tools (LinkedIn + X) and `mcp__claude_ai_Gmail__*` tools (email). `run-pulse` does a cheap namespace check before any paid dispatch: if Apify is missing while a paid lane is non-empty, it halts before spending; if Gmail is missing, it offers to drop email or reconnect. RSS needs no MCP — it shells out to `feedparser`.

## 2. Make the lens yours

```bash
cp config/profile.example.md config/profile.md
```

Edit `config/profile.md`. This is the single most important file: it is the lens the whole pipeline reads through. Define your north star, your **domain enum** (§3.0 — the keys the classifier tags against and the report sections are built from), and your lens filters (what to amplify, what to drop). The example is a generic AI/startup builder; replace all of it. See [`schemas/schema-pulse-profile.md`](../schemas/schema-pulse-profile.md) for the contract.

## 3. Curate your watchlists

```bash
for f in config/watchlists/*.example.md; do cp "$f" "${f%.example.md}.md"; done
```

Edit each `config/watchlists/{lane}-watchlist.md`. Replace the illustrative rows with your own curated sources. A lane whose watchlist is empty (or that you never copy from `.example`) is simply skipped. The format and per-lane rules are in [`schemas/schema-pulse-watchlist.md`](../schemas/schema-pulse-watchlist.md):

- **LinkedIn / X** — profile, company, or org URLs.
- **RSS** — raw feed URLs, each tagged deep-content or news-firehose (this drives the auto-scaler).
- **Email** — sender addresses you already receive newsletters from.

> You do not have to do steps 2 and 3 by hand. Open the repo in Claude Code and ask the agent to read `run-pulse.md` and help you build your profile and watchlists. The skills are written to be onboarded from.

## 4. First run

Open the repo in your agent and invoke:

```
/run-pulse
```

This runs a 1-day window over every non-empty lane. It will:

1. Read your profile + watchlists.
2. Crawl RSS first (free) to measure volume.
3. Show a plan with a **cost estimate** for the paid lanes and wait for your approval.
4. On approval, crawl the paid lanes, classify everything in parallel, and write the brief.

The brief lands at `output/reports/pulse-report-<date>/pulse-report-<date>.md`. `output/` is gitignored, so reports stay local unless you repoint `REPORTS_DIR` or un-ignore it.

Useful flags (all optional, all have defaults):

```
/run-pulse --days=7                 # wider window
/run-pulse --x-max-per-handle=10    # raise the per-handle post cap
/run-pulse --linkedin-max-posts=5   # raise the per-URL post cap
```

## Troubleshooting

- **"Apify MCP not connected"** — the namespace check failed before spending. Confirm `.mcp.json` loaded and `APIFY_TOKEN` is set, then re-run.
- **Email lane dropped** — the Gmail MCP was absent. Reconnect it at the approval gate, or proceed without email.
- **RSS feed failed** — usually a JS-challenge-gated feed or a transient network error. Remove the feed or retry. Store feed URLs in their 308-normalized (no-trailing-slash) form where the host redirects.
- **Want to keep briefs in git** — repoint `REPORTS_DIR` (in `run-pulse.md` Global References) outside `output/`, or adjust `.gitignore`.
