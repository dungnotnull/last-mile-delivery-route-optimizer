# PROJECT-detail.md — Last-mile Delivery Route Optimizer

## Executive Summary
This skill is a full Claude harness that turns fuel-minimizing last-mile routing with live traffic, time windows, and capacity constraints. It operates research-first: every material judgment is grounded in a named, citable framework and, where possible, a freshly retrieved source. It produces a professional-grade deliverable: a multi-dimensional score against the chosen framework plus a prioritized, effort/impact-ranked improvement roadmap.

## Problem Statement
Micro delivery operators plan routes by intuition, burning fuel and missing time windows. This skill formulates the delivery set as a capacitated vehicle-routing problem with time windows, produces optimized stop sequences, and continuously incorporates real-time traffic and weather to minimize fuel and lateness.

## Target Users & Use Cases
Primary users are practitioners and decision-makers in the **Science, Engineering & Industry** domain. Trigger examples:
1. Operator has 35 stops, 2 vans, and morning delivery windows; skill returns two balanced optimized routes.
2. A road closes mid-day; traffic-feed updater re-optimizes the affected route.
3. User wants to know if a third vehicle reduces total cost; skill compares fleet-size scenarios.
4. Stops have weight/volume limits; skill enforces capacity and rejects infeasible loads.
5. Customer demands a tighter time window; skill quantifies the mileage/fuel penalty.
6. User asks where to place a new micro-depot; skill evaluates candidate locations by stem mileage.

## Harness Architecture
```
/last-mile-delivery-route-optimizer (main.md harness)
  -> sub-evaluation-framework-selector              [intake / framing]
  -> sub-scoring-engine              [framework selection / risk-scope screen]
  -> knowledge refresh   [SECOND-KNOWLEDGE-BRAIN via knowledge_updater.py]
  -> sub-traffic-feed-updater              [multi-dimensional scoring]
  -> evidence + challenge gate
  -> improvement roadmap [prioritized, effort/impact]
  -> SYNTHESIZE          [final scored deliverable]
```

## Full Sub-Skill Catalog
### sub-evaluation-framework-selector
- **Purpose:** Frame the problem (single/multi-vehicle, capacity, time windows) and choose the solver strategy.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-scoring-engine
- **Purpose:** Build the distance/time matrix, solve the route set, and score it on fuel, distance, and on-time KPIs.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-traffic-feed-updater
- **Purpose:** Refresh real-time traffic/weather and re-optimize sensitive legs.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.
### sub-improvement-roadmap
- **Purpose:** Recommend structural improvements (depot location, time-window negotiation, fleet sizing) with impact estimates.
- **Inputs:** outputs of the prior stage + user-provided context.
- **Outputs:** structured findings passed to the next stage.
- **Tools:** WebSearch, WebFetch, Read, Write, Bash
- **Quality gate:** output is schema-valid, evidence-linked, and framework-grounded before the harness proceeds.

## Skill File Format Specification
Every skill file uses YAML frontmatter (`name`, `description`) followed by the required sections: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates. The main harness invokes sub-skills via the Skill tool in the order shown above.

## E2E Execution Flow
1. Parse the user request; if inputs are insufficient, `sub-evaluation-framework-selector` asks targeted intake questions.
2. `sub-scoring-engine` selects the governing framework(s) and screens scope/risk; branch to a refusal or disclaimer if out of scope.
3. Refresh knowledge if the brain is stale (>7 days) and WebSearch/WebFetch are available; otherwise degrade gracefully to internal knowledge with a stated limitation.
4. `sub-traffic-feed-updater` scores each dimension, citing evidence per claim.
5. Run the evidence/quality gate(s) and a devil's-advocate challenge pass.
6. Emit the scored report + roadmap in the Output Format below.

## SECOND-KNOWLEDGE-BRAIN Integration
- **Sources:** Google OR-Tools routing documentation; OSRM / OpenStreetMap routing engines and OSM data; ArXiv (math.OC, cs.DS) for vehicle-routing research; INRIX / TomTom traffic indices (public reports); Operations Research journals via Google Scholar
- **Crawl config:** see `tools/knowledge_updater.py` (ArXiv categories math.OC, cs.DS; domain queries seeded from the idea).
- **Append format:** date-stamped entries with Title, Authors, Year, Venue, DOI/URL, key finding, relevance note; deduplicated by URL/DOI hash.

## Supporting Tools Spec — knowledge_updater.py
- **Inputs:** search queries + source list (in-file config), optional `--since` date.
- **Outputs:** appended entries in `SECOND-KNOWLEDGE-BRAIN.md` + a run log.
- **Schedule:** weekly cron (graceful no-op when offline).

## Quality Gates
- **Evidence gate:** every material claim is traceable to a cited source or a prior step; prefer the highest evidence tier available.
- **Framework gate:** all scoring is grounded in the named frameworks below — never ad-hoc criteria.
- **Challenge gate:** a devil's-advocate pass has stress-tested the recommendation before it is shown.

## Test Scenarios
See `tests/test-scenarios.md` (>=5 concrete scenarios with expected harness behavior).

## Key Design Decisions
1. Framework-grounded scoring only — no ad-hoc rubrics.
2. Research-first with graceful degradation when offline.
3. Composable sub-skills (>=3) so cluster siblings can reuse them.
4. Deliverable is an artifact (scored report + roadmap), not a chat reply.
5. Evidence/quality gate enforced before any sensitive/regulated output.
