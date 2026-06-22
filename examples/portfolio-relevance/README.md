# Portfolio relevance (inline pattern)

Score a Pulse brief against a stock portfolio in a single pass. One context, so no fan-out: read the brief plus the portfolio and write the take directly. This is the simplest shape a relevance layer takes.

- **IN**: the brief at `output/reports/pulse-report-<date>/pulse-report-<date>.md` + [`portfolio.example.md`](portfolio.example.md).
- **OUT**: `output/relevance/portfolio-<date>.md`, one relevance item per affected holding plus a suggested action.

## Run it

Run a brief first (`/run-pulse`). Then paste this to your agent, substituting today's date:

```
Read these two files:
  - output/reports/pulse-report-<date>/pulse-report-<date>.md   (the signals brief)
  - examples/portfolio-relevance/portfolio.example.md           (the portfolio)

For each holding, decide whether anything in the brief changes, confirms, or
threatens its thesis. Skip holdings with no relevant signal, silence is fine.

Write output/relevance/portfolio-<date>.md:

  # Portfolio Relevance: <date>

  ## 1.0 Relevance Items
  - **<holding>: <what the signal means for this thesis>.** <second-order
    implication, what it changes, not just what happened>. <the move it implies
    or the risk to watch>. <source> · <permalink>

  ## 2.0 Suggested Action
  - **<the single highest-leverage move the day implies for this portfolio>.**
    <source / pointer> · <permalink>

Rules: every item keeps its source permalink from the brief. Every item is a
second-order point (what it means for the holding), never a restatement of the
brief's fact. If no holding has signal, write the file with a one-line
"No portfolio-relevant signal today." under §1.0 and skip §2.0.
```

## What you get (sample)

```markdown
# Portfolio Relevance: 2026-06-22

## 1.0 Relevance Items
- **NVDA: a second frontier lab signaling in-house silicon is a slow-burn demand risk, not a today risk.** The brief's cross-source convergence on custom-accelerator announcements matters less for near-term compute demand than for the 2027+ pricing power the thesis leans on. Watch whether hyperscaler capex guidance moves with it. via @<handle> · across 4 sources · https://...
- **Fintech: stablecoin-regulation movement is the confirming signal the rails thesis wanted.** A concrete licensing step lowers the regulatory tail risk that has capped the position. It strengthens the case to hold, not yet to add. via <feed> · https://...

## 2.0 Suggested Action
- **Re-check the AI-infra holding's exposure to in-house-silicon substitution before the next earnings window.** drives §3.0 Trend 1 · https://...
```

## Make it yours

Replace `portfolio.example.md` with your real holdings (or point the prompt at a different context file), and change the output shape if you want something other than the recommended relevance artifact. To check several portfolios or several context types at once, use the [sub-agent pattern](../project-relevance/) instead.
