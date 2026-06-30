# tests/test-scenarios.md — Last-mile Delivery Route Optimizer

Scenario-based tests for the `last-mile-delivery-route-optimizer` harness. Each scenario asserts the harness flow,
framework-grounded scoring, gate enforcement, and deliverable shape.

### Scenario 1
- **Given:** Operator has 35 stops, 2 vans, and morning delivery windows; skill returns two balanced optimized routes.
- **Expected harness behavior:** intake confirms inputs → framework selected → `sub-traffic-feed-updater` scores against the named frameworks → evidence + challenge gate passed → scored report + prioritized roadmap emitted with citations.
- **Pass criteria:** all quality gates pass; every score cites its framework; roadmap items are effort/impact-ranked.
### Scenario 2
- **Given:** A road closes mid-day; traffic-feed updater re-optimizes the affected route.
- **Expected harness behavior:** intake confirms inputs → framework selected → `sub-traffic-feed-updater` scores against the named frameworks → evidence + challenge gate passed → scored report + prioritized roadmap emitted with citations.
- **Pass criteria:** all quality gates pass; every score cites its framework; roadmap items are effort/impact-ranked.
### Scenario 3
- **Given:** User wants to know if a third vehicle reduces total cost; skill compares fleet-size scenarios.
- **Expected harness behavior:** intake confirms inputs → framework selected → `sub-traffic-feed-updater` scores against the named frameworks → evidence + challenge gate passed → scored report + prioritized roadmap emitted with citations.
- **Pass criteria:** all quality gates pass; every score cites its framework; roadmap items are effort/impact-ranked.
### Scenario 4
- **Given:** Stops have weight/volume limits; skill enforces capacity and rejects infeasible loads.
- **Expected harness behavior:** intake confirms inputs → framework selected → `sub-traffic-feed-updater` scores against the named frameworks → evidence + challenge gate passed → scored report + prioritized roadmap emitted with citations.
- **Pass criteria:** all quality gates pass; every score cites its framework; roadmap items are effort/impact-ranked.
### Scenario 5
- **Given:** Customer demands a tighter time window; skill quantifies the mileage/fuel penalty.
- **Expected harness behavior:** intake confirms inputs → framework selected → `sub-traffic-feed-updater` scores against the named frameworks → evidence + challenge gate passed → scored report + prioritized roadmap emitted with citations.
- **Pass criteria:** all quality gates pass; every score cites its framework; roadmap items are effort/impact-ranked.
### Scenario 6
- **Given:** User asks where to place a new micro-depot; skill evaluates candidate locations by stem mileage.
- **Expected harness behavior:** intake confirms inputs → framework selected → `sub-traffic-feed-updater` scores against the named frameworks → evidence + challenge gate passed → scored report + prioritized roadmap emitted with citations.
- **Pass criteria:** all quality gates pass; every score cites its framework; roadmap items are effort/impact-ranked.

## Cross-cutting checks
- **Graceful degradation:** with WebSearch/WebFetch disabled, the harness still produces a deliverable and explicitly states the knowledge-currency limitation.
- **Refusal/scope:** out-of-scope or unsafe requests are refused or redirected.
- **Determinism of structure:** every run yields the six (or seven) Output-Format sections.
