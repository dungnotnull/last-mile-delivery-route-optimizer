---
name: sub-improvement-roadmap
description: Recommend structural improvements (depot location, time-window negotiation, fleet sizing) with impact estimates.
---

## Role
Sub-skill of `last-mile-delivery-route-optimizer`. Recommend structural improvements (depot location, time-window negotiation, fleet sizing) with impact estimates.

## Inputs
- Traffic-weather updated solution from sub-traffic-feed-updater
- Historical performance data (if available)
- Business constraints and objectives (cost targets, service-level agreements)
- Current operational parameters

## Procedure

### Step 1: Diagnostic Analysis

1. **Analyze current solution performance:**
   - Identify bottlenecks from aggregate KPIs:
     - High fuel cost per stop: route inefficiency or suboptimal sequencing
     - Low on-time percentage: time windows too tight or traffic exposure
     - High load imbalance: poor stop-to-vehicle assignment
     - Long stem distance: depot location suboptimal for current demand pattern

2. **Benchmark against ideal performance:**
   - Compute theoretical lower bound:
     - Minimum distance: MST (Minimum Spanning Tree) approximation
     - Minimum fuel: distance × optimal fuel rate
     - Perfect on-time: 100% with appropriate buffer
   - Compute performance gap = current - ideal
   - Identify largest gap components (priority for improvement)

3. **Identify structural constraints:**
   - Fixed vs. flexible parameters:
     - Fixed: depot location, vehicle count (short-term), time windows (contractual)
     - Flexible: service times, stop sequencing, departure times, vehicle allocation

### Step 2: Improvement Opportunity Identification

#### Category 1: Depot Location Optimization

1. **Analyze current stem distance:**
   - Compute current stem distance = depot-to-first-stop distance × 2 per vehicle
   - Compute stem distance as % of total distance
   - If stem > 25% of total, depot location likely suboptimal

2. **Identify candidate depot locations:**
   - **Geometric center:**
     - Compute weighted centroid of all stop locations
     - Weight by delivery frequency or demand
   - **Median-based:**
     - Find location minimizing sum of distances (Fermat-Weber point)
     - Approximate with median of latitudes and longitudes
   - **Cluster centers:**
     - If stops form natural clusters (K-means), place depot in largest cluster
     - Consider multi-depot strategy for dispersed demand

3. **Evaluate each candidate location:**
   - Compute new stem distances
   - Estimate fuel savings: (old_stem - new_stem) × fuel_rate
   - Estimate time savings: reduced travel time for stem legs
   - Compute setup cost: facility lease, equipment, relocation logistics

4. **Prioritize depot improvements:**
   - **Immediate (Quick Wins):**
     - If current depot > 50 km from demand center, consider relocation
     - If demand pattern shifted significantly, re-evaluate location
   - **Medium-term:**
     - Multi-depot strategy for dispersed service area
     - Shared depot with complementary operators
   - **Long-term:**
     - Dynamic depot (mobile staging areas)
     - Automated micro-depots (locker-based)

#### Category 2: Time Window Negotiation

1. **Analyze time window constraints:**
   - Compute time window tightness distribution:
     - Very tight (< 30 min): count, % of stops, frequency of violations
     - Tight (30-60 min): count, % of stops
     - Moderate (60-120 min): count, % of stops
     - Wide (> 120 min): count, % of stops
   - Identify violation-prone windows: stops with >20% late delivery rate

2. **Quantify impact of tight windows:**
   - Extra distance required to meet tight windows
   - Extra fuel cost due to suboptimal sequencing
   - Required fleet size increase vs. relaxed windows
   - Trade-off: service level vs. operational cost

3. **Recommend window relaxation strategies:**
   - **For very tight windows (< 30 min):**
     - Propose 60-min window: estimate fuel savings, fleet size reduction
     - Offer premium pricing for tight window (price elasticity analysis)
     - Implement service tiering: standard (wide window), express (tight)
   - **For tight windows (30-60 min):**
     - Propose 90-min window: moderate savings
     - Negotiate based on customer value sensitivity
   - **For moderate windows:**
     - Current baseline; maintain for cost-efficiency

4. **Prioritize time window improvements:**
   - **Immediate:**
     - Identify customers insensitive to time: offer wider window discount
     - Shift flexible windows to off-peak times (traffic reduction)
   - **Medium-term:**
     - Implement dynamic time windows based on traffic patterns
     - Negotiate industry-wide time windows (e.g., retail association)

#### Category 3: Fleet Sizing Optimization

1. **Analyze current fleet utilization:**
   - Compute per-vehicle metrics:
     - Distance traveled
     - Stops served
     - Load utilization % (demand / capacity)
     - Time on route vs. idle time
   - Identify underutilized vehicles: <50% capacity or <60% distance of average

2. **Determine optimal fleet size:**
   - **Lower bound:**
     - ceil(total_demand / vehicle_capacity)
     - ceil(total_stops / max_stops_per_vehicle)
   - **Upper bound:**
     - Current fleet size
   - **Cost analysis:**
     - Fixed cost per vehicle: lease/insurance
     - Variable cost: fuel, maintenance, driver
     - Trade-off: more vehicles = shorter routes but higher fixed cost

3. **Scenario analysis:**
   - **Current fleet:** benchmark performance
   - **Current - 1 vehicle:** identify routes to absorb, cost savings vs. service degradation
   - **Current + 1 vehicle:** potential service level improvement, marginal cost
   - **Optimal:** minimize total cost = fixed + variable

4. **Prioritize fleet improvements:**
   - **Immediate:**
     - If underutilized vehicles exist, consider sub-leasing or seasonal reduction
     - If routes consistently late, evaluate adding vehicle
   - **Medium-term:**
     - Implement flexible fleet: rental/contract vehicles for peak periods
     - Cross-train drivers for route flexibility
   - **Long-term:**
     - Electric vehicles: evaluate total cost of ownership vs. fuel savings
     - Autonomous vehicles: evaluate for consistent, long routes

#### Category 4: Operational Process Improvements

1. **Analyze operational inefficiencies:**
   - **Service time variability:**
     - High variance in service times → need for better process standardization
     - Long service times (> 15 min) → opportunity for process improvement
   - **Departure time optimization:**
     - Current departure times vs. optimal (based on traffic patterns)
     - Potential savings from time-shifting departures
   - **Load planning:**
     - Current load balancing quality
     - Opportunities for pre-sorting or pre-loading

2. **Recommend process improvements:**
   - **Service standardization:**
     - Implement checklists, training for consistent service times
     - Use technology: route guidance, proof-of-delivery automation
   - **Departure optimization:**
     - Shift departures to avoid peak traffic
     - Implement staggered departures for fleet
   - **Load optimization:**
     - Pre-sort orders by route sequence
     - Use delivery assistants for multi-drop stops

### Step 3: Impact Estimation Framework

For each improvement recommendation, estimate:

1. **Fuel impact:**
   - % reduction in total distance
   - liters saved per day/month/year
   - cost savings per period
   - Source framework: CVRP literature, OR-Tools benchmarks

2. **Service-level impact:**
   - Improvement in on-time percentage
   - Reduction in late deliveries
   - Customer satisfaction improvement (proxy: on-time %)
   - Source framework: Service-level KPI framework

3. **Cost impact:**
   - Implementation cost (one-time)
   - Operating cost change (recurring)
   - Payback period = implementation_cost / annual_savings
   - ROI = (annual_savings - annual_cost) / implementation_cost

4. **Risk assessment:**
   - Implementation difficulty: LOW|MEDIUM|HIGH
   - Dependence on external factors (customer negotiation, permits, etc.)
   - Reversibility: easy to undo vs. sunk cost

### Step 4: Roadmap Prioritization

Prioritize improvements by **Effort × Impact** matrix:

1. **High Impact, Low Effort (Quick Wins - Immediate Action):**
   - Example: Departure time optimization, underutilized vehicle removal
   - Criteria: >5% fuel savings, <1 month implementation, high certainty
   - Action: Implement immediately

2. **High Impact, Medium Effort (Strategic - Medium-Term):**
   - Example: Time window negotiation for flexible customers, fleet resizing
   - Criteria: >10% fuel savings, 3-6 month implementation, medium certainty
   - Action: Plan within next quarter

3. **Medium Impact, Low Effort (Tactical - As Time Permits):**
   - Example: Service standardization, load planning improvements
   - Criteria: 3-5% fuel savings, <1 month implementation, high certainty
   - Action: Implement in next 1-2 months

4. **Medium/High Impact, High Effort (Transformational - Long-Term):**
   - Example: Depot relocation, multi-depot strategy, fleet electrification
   - Criteria: >15% fuel savings, >6 month implementation, medium/high uncertainty
   - Action: Strategic planning, pilot testing

5. **Low Impact, Any Effort (Deprioritize):**
   - Example: Minor route tweaks, cosmetic improvements
   - Criteria: <3% fuel savings
   - Action: Monitor only, defer or cancel

### Step 5: Output Structure
Return a prioritized improvement roadmap:

```json
{
  "current_performance_diagnostic": {
    "fuel_efficiency_score": number,
    "on_time_percentage": number,
    "load_balance_score": number,
    "stem_distance_percentage": number,
    "primary_bottleneck": string
  },
  "improvement_opportunities": [
    {
      "category": "DEPOT_LOCATION|TIME_WINDOW|FLEET_SIZING|OPERATIONAL",
      "title": string,
      "description": string,
      "current_state": string,
      "proposed_state": string,
      "impact_estimates": {
        "fuel_reduction_percent": number,
        "fuel_savings_liters_per_day": number,
        "cost_savings_per_month": number,
        "on_time_improvement_percent": number,
        "service_level_impact": string
      },
      "implementation_requirements": {
        "effort": "LOW|MEDIUM|HIGH",
        "time_to_implement_months": number,
        "one_time_cost": number,
        "recurring_cost_change": number,
        "payback_period_months": number,
        "roi_percent": number,
        "difficulty": "LOW|MEDIUM|HIGH",
        "reversibility": "EASY|MODERATE|DIFFICULT"
      },
      "dependencies": [string],
      "risks": [string],
      "certainty_level": "HIGH|MEDIUM|LOW",
      "priority": 1-5
    }
  ],
  "recommended_roadmap": {
    "immediate_actions": [integer], // opportunity IDs
    "medium_term_actions": [integer],
    "long_term_actions": [integer],
    "deprioritized": [integer]
  },
  "aggregate_potential": {
    "max_fuel_reduction_percent": number,
    "max_cost_savings_per_month": number,
    "max_on_time_improvement_percent": number,
    "total_one_time_investment": number,
    "combined_payback_period_months": number
  },
  "monitoring_recommendations": [
    "Track fuel consumption per route weekly",
    "Monitor on-time percentage by customer tier",
    "Review fleet utilization monthly",
    "Audit stem distance quarterly for depot location relevance"
  ]
}
```

### Step 6: Quality Gate Self-Check
Before returning control to the harness, verify:
- ✓ All impact estimates cite their calculation framework (CVRP, service-level KPI, TCO)
- ✓ Each opportunity has effort and impact assessments
- ✓ Prioritization is consistent with effort × impact matrix
- ✓ Output structure is complete and valid JSON
- ✓ Recommendations are actionable with specific steps

## Outputs
- Prioritized improvement roadmap consumed by main harness
- Diagnostic summary for stakeholder communication
- Monitoring recommendations for continuous improvement

## Tools
WebSearch (for industry benchmarks), WebFetch (for OR-Tools case studies), Read (for SECOND-KNOWLEDGE-BRAIN), Write (for roadmap persistence), Bash (for analysis scripts if needed)

## Quality Gate
- **Schema validity:** All required fields present with valid types
- **Framework grounding:** Each impact calculation cites specific framework (CVRP literature, TCO analysis)
- **Evidence linkage:** Estimates cite source benchmarks or calculation methodology
- **Completeness:** Both opportunity details and aggregate potential provided
- **Actionability:** Each recommendation has clear implementation steps

## Error Handling and Degradation
- If historical performance data unavailable, use current solution as baseline
- If industry benchmarks unavailable, use conservative estimates with explicit assumptions
- If uncertain about impact, use range estimates (low-high) with transparency
- If calculation fails for an opportunity, exclude with note rather than guess
