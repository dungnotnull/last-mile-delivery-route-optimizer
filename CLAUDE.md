# CLAUDE.md — Last-mile Delivery Route Optimizer

**Skill slug:** `last-mile-delivery-route-optimizer`
**Source idea:** #173 (Vietnamese backlog `ideas.md`)
**Cluster:** science-industry — Science, Engineering & Industry
**Tagline:** Fuel-minimizing last-mile routing with live traffic, time windows, and capacity constraints.
**Current phase:** Phase 4 — Testing & Validation (initial build complete)

## Problem This Skill Solves
Micro delivery operators plan routes by intuition, burning fuel and missing time windows. This skill formulates the delivery set as a capacitated vehicle-routing problem with time windows, produces optimized stop sequences, and continuously incorporates real-time traffic and weather to minimize fuel and lateness.

## Harness Flow (Summary)
1. **Intake** → `sub-evaluation-framework-selector` gathers inputs and frames the problem.
2. **Screen / select** → `sub-scoring-engine` selects the governing framework and screens risk/scope.
3. **Score / analyze** → `sub-traffic-feed-updater` produces a multi-dimensional score against named frameworks.
4. **Knowledge refresh** → optional `tools/knowledge_updater.py` run keeps SECOND-KNOWLEDGE-BRAIN.md current.
5. **Gate** → quality / evidence gates must pass.
6. **Synthesize** → main harness emits the scored deliverable + prioritized improvement roadmap.

## Sub-skills
- `skills/sub-evaluation-framework-selector.md` — Frame the problem (single/multi-vehicle, capacity, time windows) and choose the solver strategy.
- `skills/sub-scoring-engine.md` — Build the distance/time matrix, solve the route set, and score it on fuel, distance, and on-time KPIs.
- `skills/sub-traffic-feed-updater.md` — Refresh real-time traffic/weather and re-optimize sensitive legs.
- `skills/sub-improvement-roadmap.md` — Recommend structural improvements (depot location, time-window negotiation, fleet sizing) with impact estimates.

## Tools Required
WebSearch, WebFetch, Read, Write, Bash

## Knowledge Sources (for crawl + reasoning)
- Google OR-Tools routing documentation
- OSRM / OpenStreetMap routing engines and OSM data
- ArXiv (math.OC, cs.DS) for vehicle-routing research
- INRIX / TomTom traffic indices (public reports)
- Operations Research journals via Google Scholar

## Supporting Python Tools
- `tools/knowledge_updater.py` — crawl4ai + WebSearch pipeline that fetches latest papers/reports from the domain sources above, scores by recency + relevance, deduplicates by URL/DOI hash, and appends to `SECOND-KNOWLEDGE-BRAIN.md`. Recommended schedule: weekly cron.

## Active Development Tasks
- [x] Scaffold all required deliverables
- [x] Define >=3 sub-skills with quality gates
- [x] Ground scoring in named world-renowned frameworks
- [x] Wire knowledge_updater crawl sources
- [ ] Expand SECOND-KNOWLEDGE-BRAIN with first live crawl batch
- [ ] Add regression fixtures from the test scenarios

## Reference Docs (this folder)
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving knowledge base
- `skills/main.md` — harness entry point
