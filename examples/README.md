# Examples: the relevance seam

The core pipeline ends at a neutral signals brief. These are two self-contained, swappable implementations of what happens *next*: scoring that brief against a context you care about. They exist to prove the full loop without coupling the core to any one use case. **The core never imports them**: delete or replace them freely.

```
brief  +  your context   →   relevance logic   →   relevance artifact
(IN)      (here)              (here)                (output/relevance/)
```

Both consume the brief at `output/reports/pulse-report-<date>/pulse-report-<date>.md`. Neither modifies it.

## The two patterns

The only real decision in a relevance layer is fan-out, and the two examples show both ends of it:

| Example | Context | Pattern | When |
|---|---|---|---|
| [`portfolio-relevance/`](portfolio-relevance/) | one stock portfolio | **inline**: read brief + context in one pass, write the take directly | one or two contexts |
| [`project-relevance/`](project-relevance/) | several projects | **sub-agent per context**: one agent per project, in parallel, each in its own window | many contexts |

The sub-agent pattern reuses the same context-isolation lever the core uses: each per-context read happens in an isolated window, so your orchestrating thread never bloats. Reach for it once you have more than a couple of contexts.

## Running either one

Each folder has a `README.md` with a ready-to-paste prompt and a sample output, plus a `*.example.md` context file you swap for your own. Run a Pulse brief first (`/run-pulse`), then follow the example's README. Both write to `output/relevance/` (gitignored, like the rest of `output/`).

## Bringing your own context

A context object is just a markdown file describing what you want the brief scored against: a portfolio, a company's positioning, a research agenda, a job search, anything. Copy the closest example, replace its `*.example.md` with your real context, and adjust the prompt's output shape if you want something other than the recommended relevance artifact. The shape is in [`../docs/extending.md`](../docs/extending.md).
