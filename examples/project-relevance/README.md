# Project relevance (sub-agent-per-context pattern)

Score a Pulse brief against several projects at once, one sub-agent per project, in parallel. Each agent reads the brief plus one project block in its own isolated window and returns that project's take. This is the pattern to reach for whenever you have more than a couple of contexts — it keeps the per-context reading out of your orchestrating thread, the same lever the core pipeline uses.

- **IN** — the brief at `output/reports/pulse-report-<date>/pulse-report-<date>.md` + [`projects.example.md`](projects.example.md) (one block per project).
- **OUT** — `output/relevance/<project-slug>-<date>.md` per *relevant* project. A project with no relevant signal writes no file and just reports "not relevant."

## Run it

Run a brief first (`/run-pulse`). Then paste this orchestration prompt to your agent, substituting today's date:

```
Read examples/project-relevance/projects.example.md and split it into its
project blocks (one per H2). For EACH project block, spawn one sub-agent IN A
SINGLE MESSAGE (parallel), each with this prompt:

  Read output/reports/pulse-report-<date>/pulse-report-<date>.md (the brief)
  and this project block:
  <paste the one project block>

  Decide whether today's brief carries signal that matters to THIS project,
  using its "Signal that matters" line. If nothing is relevant, return
  {"project":"<slug>","relevant":false} and write no file.

  If something is relevant, write output/relevance/<slug>-<date>.md:

    # Project Relevance: <slug>, <date>
    ## 1.0 Relevance Items
    - **<what the signal means for this project>.** <second-order implication>.
      <the non-obvious move or trade-off>. Hooks to: <which part of the project>.
      <source> · <permalink>
    ## 2.0 Suggested Action
    - **<one concrete next move the signal implies>.** <source / pointer> · <permalink>

  Rules: every item keeps its source permalink. Every item is a second-order
  point for this project, not a restatement of the brief. Return
  {"project":"<slug>","relevant":true,"path":"<the file path>"}.

Collect the returns and print a one-line summary per project (relevant + path,
or not relevant).
```

## What you get (sample)

Orchestrator summary:

```
acme-agent-platform     relevant     output/relevance/acme-agent-platform-2026-06-22.md
northwind-gtm-service    relevant     output/relevance/northwind-gtm-service-2026-06-22.md
sidebet-research         not relevant —
```

One relevance file (`acme-agent-platform-2026-06-22.md`):

```markdown
# Project Relevance: acme-agent-platform, 2026-06-22

## 1.0 Relevance Items
- **A well-funded eval/observability launch just narrowed your differentiation window.** The brief's agent-infra convergence shows the eval layer consolidating faster than the orchestration layer, so "orchestration + eval" as one platform is a shrinking wedge. The move is to decide whether eval is your moat or a buy-vs-build integration. Hooks to: the eval layer. via @<handle> · across 3 sources · https://...

## 2.0 Suggested Action
- **Pressure-test the eval-as-moat assumption against the launch before the next build cycle.** drives §3.0 Trend 1 · https://...
```

## Make it yours

Replace `projects.example.md` with your own project blocks — the fan-out scales to however many you list. Each block's "Signal that matters" line is what its sub-agent filters on, so make it specific. Swap the output shape if your downstream (a notification, a routed message, a digest) wants something other than the recommended relevance artifact.
