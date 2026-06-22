---
type: Pulse Profile
schema: pulse-profile
created: 2026-06-22
updated: 2026-06-22
tags: [pulse, profile, lens]
alias: []
version: 1.0
description: Example founder-lens profile for an indie builder tracking the AI, startup, and go-to-market landscape. Replace the content with your own.
---

# Pulse Profile

> **This is an example.** Copy it to `config/profile.md` and rewrite every section to match your own direction, domains, and filters. The pipeline reads whatever you put here, so the quality of your brief depends on the quality of this lens.

## 1.0 North Star + Current Bets

North star: build and run a small, AI-native software company, one where AI is wired into the actual operations and product rather than bolted on afterward. The feed is read in service of that future: what it looks like, who is building it well, and what it takes to get there.

Current lean: near-term, go deep on one narrow problem at the intersection of AI and go-to-market and ship it to real users. Learning, reps, and a small public track record come before anything bigger. Stage: building the skill stack and watching the opportunity landscape, not yet committed to a single company shape.

## 2.0 Skill Targets

- AI craft — agent harnesses, orchestration, context management, multi-agent coordination.
- Go-to-market and growth — positioning, demand generation, sales motion, retention loops.
- Company building — early-stage operating, founder-driven culture, AI-native ops.
- Founder thinking — judgment under uncertainty, opportunity-sizing, narrative.
- Writing and distribution — building an audience as founder leverage.

## 3.0 Domain Interests

The domains where signal is welcome, as a keyed table. The L1 classifier tags each crawled item against these keys, and the report renders one section per domain. This example ships six; pick your own set (keep it small and stable). Items may carry more than one domain tag.

| # | Domain | Key | Scope | Boundary / cross-routing |
|---|--------|-----|-------|--------------------------|
| 1 | AI & Agent Systems | `ai-agent-systems` | Agent harnesses, orchestration, context engineering, workflow design, productivity infrastructure. | Tooling as a product/capability here; tooling applied to run a company → `ai-native-company`; AI as an industry-shaping force → `tech-landscape`. |
| 2 | AI-Native Company Building | `ai-native-company` | How AI-deeply-integrated companies are designed and run — leverage points, ops automation, team structure. | "How AI changes how the company operates" here; "the AI capability itself" → `ai-agent-systems`. |
| 3 | Growth & GTM Craft | `growth-gtm` | BD, sales motion, marketing systems, positioning, growth strategy — the operator layer. | "How to sell/acquire/retain" here; "what to build / is this a market" → `founder-startup`. |
| 4 | Founder & Startup Ecosystem | `founder-startup` | VC perspectives, founder advice, opportunity-sizing, judgment under uncertainty, emerging opportunity spaces. | Strategic "what/whether" here; tactical "how to execute growth" → `growth-gtm`. |
| 5 | Tech Landscape | `tech-landscape` | The broader technology industry and its direction — platform shifts, big-tech strategy, hardware, regulation, market structure. | Industry direction here; the AI capability/craft itself → `ai-agent-systems` (cross-tag when both). |
| 6 | FinTech & Future-of-Money | `fintech-money` | Payments, regulated crypto finance, DeFi, future-of-money. | Money-system signal here; broad economy/markets → drop or route to a `macro` domain if you add one. |

## 4.0 Lens Filters

**Relevance amplifiers**
- Applies to how AI-native companies are built and operated (design, leverage primitives).
- Increases personal leverage or productivity ceiling.
- Informs a decision you are actively making — opportunity reads, market reads, execution reads.
- Reveals where AI is being applied or where new opportunities are emerging.
- Surfaces shifts in growth craft, BD / sales practice, or marketing systems.

**Drop criteria**
- Unrelated affiliate marketing or promotional content.
- Off-topic personal posts (anniversaries, generic milestones, congratulatory chains).
- Recruiter spam or job-board reposts.
- Surface-level news without implication payload (e.g., "X launched Y" with no read on why it matters).

**Pattern-synthesis prompts**
- Convergence between AI tooling, orchestration craft, and how companies operate.
- Economic or platform shifts → emerging startup opportunity surfaces.
- Workflow-tooling changes → implications for company design.
- Where AI productivity gains land in the GTM / growth stack.
