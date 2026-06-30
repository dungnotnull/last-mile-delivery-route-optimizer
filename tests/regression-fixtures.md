# tests/regression-fixtures.md — Last-mile Delivery Route Optimizer

Regression test fixtures with expected inputs, outputs, and validation criteria for the 6 test scenarios.

## Regression Fixtures by Scenario

### Scenario 1: Multi-Vehicle Route Optimization

### Given (Input Data)
```json
{
  "scenario": "scenario_1_multi_vehicle",
  "description": "35 stops, 2 vans, morning delivery windows",
  "fleet": {
    "n_vehicles": 2,
    "vehicle_capacity_weight": 1000,
    "vehicle_capacity_volume": 20,
    "fuel_consumption_l_per_100km": 8.5
  },
  "depot": {
    "location": {"lat": 40.7128, "lon": -74.0060},
    "name": "NYC Distribution Center"
  },
  "stops": [
    {"id": 1, "location": {"lat": 40.7589, "lon": -73.9851}, "demand": 150, "earliest": "08:00", "latest": "10:00", "service_time": 10},
    {"id": 2, "location": {"lat": 40.7484, "lon": -73.9857}, "demand": 200, "earliest": "08:30", "latest": "10:30", "service_time": 15},
    {"id": 3, "location": {"lat": 40.7614, "lon": -73.9776}, "demand": 120, "earliest": "08:00", "latest": "10:00", "service_time": 8},
    {"id": 35, "location": {"lat": 40.7282, "lon": -73.7949}, "demand": 180, "earliest": "09:00", "latest": "11:00", "service_time": 12}
  ],
  "solver_settings": {
    "distance_strategy": "HAVERSINE",
    "solver_strategy": "METAHEURISTIC",
    "time_limit_seconds": 30
  }
}
```

### Expected Behavior (Harness Flow)
1. **Intake (sub-evaluation-framework-selector):**
   - Validates: 35 stops, 2 vehicles, capacity constraints, time windows present
   - Classification: CVRPTW (Capacitated Vehicle Routing with Time Windows)
   - Solver strategy: METAHEURISTIC (Google OR-Tools with Guided Local Search)
   - Complexity: MEDIUM (35 stops, 2 vehicles)

2. **Scoring (sub-scoring-engine):**
   - Builds 36×36 distance matrix (depot + 35 stops)
   - Solves using Google OR-Tools with capacity and time window constraints
   - Returns 2 routes with balanced stops and loads
   - Computes KPIs: total_distance, total_fuel, on_time_percentage

3. **Traffic Update (sub-traffic-feed-updater):**
   - Queries traffic APIs for route corridors
   - Applies traffic factors to sensitive legs
   - Re-optimizes if factor > 1.5 for tight-window routes

4. **Improvement Roadmap (sub-improvement-roadmap):**
   - Analyzes stem distance percentage
   - Identifies time window tightness
   - Recommends depot location or window relaxation improvements

5. **Quality Gates:**
   - Evidence gate: Every score cites framework (OR-Tools, CVRP formulation)
   - Framework gate: No ad-hoc criteria
   - Challenge gate: Devil's-advocate review completed

### Expected Output Structure
```json
{
  "executive_summary": {
    "verdict": "FEASIBLE_SOLUTION",
    "total_distance_km": 145.8,
    "total_fuel_liters": 12.4,
    "on_time_percent": 94.3,
    "routes_generated": 2
  },
  "inputs_and_assumptions": {
    "problem_type": "CVRPTW",
    "n_stops": 35,
    "n_vehicles": 2,
    "distance_method": "HAVERSINE",
    "traffic_data": "HISTORICAL_PROFILES",
    "assumptions": [
      "Average speed 30 km/h urban",
      "Fuel consumption 8.5 L/100km",
      "Historical traffic patterns applied"
    ]
  },
  "multi_dimensional_score": {
    "fuel_efficiency": {
      "score": 7.2,
      "max_score": 10,
      "framework": "Lin et al. 2014 fuel modeling",
      "evidence": "Fuel = 145.8 km × 8.5 L/100km × 1.0 (traffic factor)",
      "interpretation": "Moderate fuel efficiency, improvement possible via route optimization"
    },
    "service_level": {
      "score": 9.4,
      "max_score": 10,
      "framework": "Kallehauge 2008 time window compliance",
      "evidence": "33 of 35 stops on time (94.3%), 2 stops marginally late (< 5 min)",
      "interpretation": "Excellent service level, minimal violations"
    },
    "load_balance": {
      "score": 8.5,
      "max_score": 10,
      "framework": "Uchoa et al. 2017 balance metrics",
      "evidence": "Vehicle 1: 82% utilization, Vehicle 2: 78% utilization, CV = 0.05",
      "interpretation": "Well-balanced routes, both vehicles optimally loaded"
    }
  },
  "findings": {
    "strengths": [
      "Both vehicles balanced in stops served (17-18 stops each)",
      "High on-time percentage (94.3%)",
      "Reasonable total distance for 35 stops"
    ],
    "risks": [
      "2 stops marginally late, may need departure time adjustment",
      "Stem distance is 28% of total (depot location suboptimal)"
    ],
    "gaps": [
      "No real-time traffic data, using historical patterns",
      "Fuel model assumes average conditions, no weather adjustment"
    ]
  },
  "improvement_roadmap": {
    "prioritized_actions": [
      {
        "priority": 1,
        "category": "OPERATIONAL",
        "title": "Adjust departure times to eliminate marginally late stops",
        "effort": "LOW",
        "impact": "HIGH",
        "estimated_fuel_savings_percent": 0,
        "estimated_on_time_improvement_percent": 5.7,
        "implementation_time_months": 0.5,
        "framework": "Service-level optimization"
      },
      {
        "priority": 2,
        "category": "DEPOT_LOCATION",
        "title": "Evaluate depot relocation to reduce stem distance",
        "effort": "MEDIUM",
        "impact": "HIGH",
        "estimated_fuel_savings_percent": 8,
        "estimated_on_time_improvement_percent": 0,
        "implementation_time_months": 6,
        "framework": "CVRP stem-mileage minimization"
      }
    ]
  },
  "sources_and_limitations": {
    "frameworks_cited": [
      "Toth & Vigo 2014 - VRP formulations",
      "Kallehauge 2008 - Time window handling",
      "Google OR-Tools Documentation - Routing solver",
      "Lin et al. 2014 - Fuel consumption modeling"
    ],
    "data_sources": [
      "Haversine distance calculation",
      "Historical traffic profiles (NYC Metro)"
    ],
    "limitations": [
      "No live traffic data, using historical patterns",
      "Weather conditions not factored",
      "Fuel model assumes constant consumption rate"
    ]
  }
}
```

### Pass Criteria
- ✓ All quality gates pass (evidence, framework, challenge)
- ✓ Every score cites its framework explicitly
- ✓ Roadmap items are effort/impact-ranked
- ✓ Output structure matches specification (6 sections)
- ✓ Solution is feasible (all constraints satisfied)

---

### Scenario 2: Dynamic Re-optimization for Road Closure

### Given (Input Data)
```json
{
  "scenario": "scenario_2_road_closure",
  "description": "Mid-day road closure requires route re-optimization",
  "initial_solution": {
    "routes": [
      {
        "vehicle_id": 1,
        "stop_sequence": [0, 5, 8, 12, 15, 0],
        "distance_km": 45.2,
        "travel_time_minutes": 78
      },
      {
        "vehicle_id": 2,
        "stop_sequence": [0, 3, 7, 11, 14, 0],
        "distance_km": 42.8,
        "travel_time_minutes": 74
      }
    ]
  },
  "incident": {
    "type": "ROAD_CLOSURE",
    "location": {"lat": 40.7589, "lon": -73.9851},
    "affected_legs": [
      {"vehicle": 1, "from_stop": 5, "to_stop": 8}
    ],
    "detour_factor": 2.3,
    "estimated_duration_hours": 4
  }
}
```

### Expected Behavior
1. **Traffic Feed Updater identifies incident:**
   - Flagged as CRITICAL sensitivity (tight time windows + high impact)
   - Traffic factor = 2.3 (230% of normal travel time)
   - Trigger automatic re-optimization

2. **Re-optimization executes:**
   - Update affected leg travel time in matrix
   - Re-solve with updated times (10-second timeout for responsiveness)
   - Extract alternative routes avoiding closure

3. **Quality validation:**
   - New routes satisfy all time windows (or flag violations)
   - Delta vs. original computed (distance, time, fuel)
   - Alert generated for dispatcher attention

### Expected Output (Route Update)
```json
{
  "traffic_weather_summary": {
    "query_timestamp": "2026-06-30T14:30:00Z",
    "data_sources": ["TomTom Traffic API", "Historical Profiles"],
    "coverage_percent": 100,
    "overall_congestion_level": "SEVERE"
  },
  "route_updates": [
    {
      "vehicle_id": 1,
      "reoptimized": true,
      "traffic_factor": 2.3,
      "weather_factor": 1.0,
      "combined_factor": 2.3,
      "sensitive_legs": [
        {
          "leg_index": 1,
          "from_stop": 5,
          "to_stop": 8,
          "original_time_minutes": 12,
          "updated_time_minutes": 28,
          "factor": 2.3,
          "sensitivity": "CRITICAL"
        }
      ],
      "delta_vs_original": {
        "distance_km_change": +5.2,
        "time_minutes_change": +18,
        "fuel_liters_change": +0.6,
        "new_time_window_violations": 1
      }
    }
  ],
  "alerts": [
    {
      "severity": "CRITICAL",
      "type": "TRAFFIC",
      "route_id": 1,
      "message": "Road closure on Leg 5→8 causing 230% travel time increase. Re-optimized with detour.",
      "recommended_action": "Monitor stop 8 delivery, now at risk of being 15 minutes late. Notify customer."
    }
  ]
}
```

### Pass Criteria
- ✓ Re-optimization triggered for combined_factor ≥ 1.5
- ✓ Sensitive leg identified as CRITICAL
- ✓ Alert generated with recommended action
- ✓ Delta computed correctly
- ✓ Framework cited (TomTom traffic, dynamic routing)

---

### Scenario 3: Fleet Size Comparison

### Given (Input Data)
```json
{
  "scenario": "scenario_3_fleet_sizing",
  "description": "Compare 2-vehicle vs 3-vehicle fleet for same stops",
  "base_case": {
    "n_vehicles": 2,
    "n_stops": 40,
    "vehicle_capacity": 1000
  },
  "comparison_cases": [
    {"n_vehicles": 3, "n_stops": 40, "vehicle_capacity": 1000},
    {"n_vehicles": 1, "n_stops": 40, "vehicle_capacity": 2000}
  ]
}
```

### Expected Behavior
1. **Solve each scenario:**
   - 1-vehicle: Single TSP route with large capacity
   - 2-vehicle: Base case (balanced routes)
   - 3-vehicle: More routes, shorter each

2. **Compute cost trade-offs:**
   - Fixed cost per vehicle: $200/day
   - Variable cost: $1.50/km fuel
   - Total cost = fixed + variable

3. **Service level comparison:**
   - On-time percentage by scenario
   - Average delivery time
   - Flexibility to disruptions

### Expected Output (Comparison Summary)
```json
{
  "fleet_comparison": {
    "scenarios": [
      {
        "n_vehicles": 1,
        "total_distance_km": 182.5,
        "total_fuel_liters": 15.5,
        "total_cost_usd": 233,
        "on_time_percent": 88.5,
        "flexibility_score": 2,
        "utilization_percent": 92
      },
      {
        "n_vehicles": 2,
        "total_distance_km": 156.2,
        "total_fuel_liters": 13.3,
        "total_cost_usd": 400,
        "on_time_percent": 94.3,
        "flexibility_score": 6,
        "utilization_percent": 80
      },
      {
        "n_vehicles": 3,
        "total_distance_km": 168.8,
        "total_fuel_liters": 14.3,
        "total_cost_usd": 653,
        "on_time_percent": 96.8,
        "flexibility_score": 9,
        "utilization_percent": 62
      }
    ],
    "recommendation": {
      "optimal_fleet_size": 2,
      "rationale": "Balances cost efficiency ($400) with high service level (94.3% on-time). 3-vehicle improves service by 2.5% but costs 63% more.",
      "framework": "Fleet sizing cost-benefit analysis (Toth & Vigo 2014)"
    }
  }
}
```

### Pass Criteria
- ✓ All fleet sizes evaluated
- ✓ Cost breakdown includes fixed and variable components
- ✓ Service level metrics computed for each scenario
- ✓ Optimal fleet size recommended with explicit rationale
- ✓ Framework cited (VRP fleet sizing literature)

---

### Scenario 4: Capacity Constraint Enforcement

### Given (Input Data)
```json
{
  "scenario": "scenario_4_capacity_constraints",
  "description": "Enforce weight/volume limits, reject infeasible loads",
  "fleet": {
    "n_vehicles": 3,
    "weight_capacity": 500,
    "volume_capacity": 10
  },
  "stops": [
    {"id": 1, "demand_weight": 200, "demand_volume": 5, "location": {"lat": 40.75, "lon": -73.98}},
    {"id": 2, "demand_weight": 350, "demand_volume": 8, "location": {"lat": 40.76, "lon": -73.97}},
    {"id": 3, "demand_weight": 450, "demand_volume": 12, "location": {"lat": 40.74, "lon": -73.99}}
  ]
}
```

### Expected Behavior
1. **Feasibility check:**
   - Stop 3 demand (450 kg, 12 m³) exceeds vehicle capacity (500 kg, 10 m³)
   - Total demand = 1000 kg, 25 m³
   - Fleet capacity = 1500 kg, 30 m³ (feasible)
   - Individual stop feasibility: Stop 3 volume > vehicle volume (INFEASIBLE for single-stop route)

2. **Solution approach:**
   - Flag infeasible assignment (cannot serve Stop 3 alone)
   - If split delivery allowed: split Stop 3 into multiple vehicles
   - If split delivery not allowed: REJECT or request larger vehicle

### Expected Output (Capacity Analysis)
```json
{
  "feasibility_analysis": {
    "overall_feasible": true,
    "fleet_utilization": {
      "total_demand_weight": 1000,
      "fleet_capacity_weight": 1500,
      "weight_utilization_percent": 66.7,
      "total_demand_volume": 25,
      "fleet_capacity_volume": 30,
      "volume_utilization_percent": 83.3
    },
    "infeasible_stops": [
      {
        "stop_id": 3,
        "reason": "VOLUME_EXCEEDS_VEHICLE",
        "demand_volume": 12,
        "vehicle_capacity": 10,
        "feasible_with_split": true,
        "recommended_action": "Split delivery across 2 vehicles or use larger vehicle"
      }
    ]
  },
  "solution_approach": "SPLIT_DELIVERY",
  "framework": "Capacitated VRP with split deliveries (Toth & Vigo 2014, Chapter 6)"
}
```

### Pass Criteria
- ✓ Capacity constraints enforced
- ✓ Infeasible assignments flagged
- ✓ Clear recommendations provided
- ✓ Framework cited (CVRP with split deliveries)
- ✓ Degradation note if split not allowed

---

### Scenario 5: Time Window Tightness Impact

### Given (Input Data)
```json
{
  "scenario": "scenario_5_time_windows",
  "description": "Quantify fuel/mileage penalty for tighter time windows",
  "base_case": {
    "time_window_width_minutes": 120
  },
  "tight_window_cases": [
    {"time_window_width_minutes": 60},
    {"time_window_width_minutes": 30}
  ]
}
```

### Expected Behavior
1. **Solve each time window scenario:**
   - Wide (120 min): Flexible sequencing, optimal distance
   - Moderate (60 min): Some constraint, minor distance increase
   - Tight (30 min): Highly constrained, significant distance increase

2. **Quantify penalties:**
   - Extra distance per 30-minute reduction
   - Extra fuel cost
   - Trade-off: service level vs. cost

### Expected Output (Time Window Analysis)
```json
{
  "time_window_impact": {
    "scenarios": [
      {
        "window_width_minutes": 120,
        "total_distance_km": 145.2,
        "total_fuel_liters": 12.3,
        "on_time_percent": 98.5,
        "fuel_cost_usd": 18.45
      },
      {
        "window_width_minutes": 60,
        "total_distance_km": 158.7,
        "total_fuel_liters": 13.5,
        "on_time_percent": 96.2,
        "fuel_cost_usd": 20.25
      },
      {
        "window_width_minutes": 30,
        "total_distance_km": 182.5,
        "total_fuel_liters": 15.5,
        "on_time_percent": 92.8,
        "fuel_cost_usd": 23.25
      }
    ],
    "penalty_analysis": {
      "distance_increase_per_30min_reduction": {
        "60→30": 23.8,
        "120→60": 13.5
      },
      "fuel_cost_increase_per_30min_reduction_usd": {
        "60→30": 3.00,
        "120→60": 1.80
      },
      "framework": "Time window sensitivity analysis (Kallehauge 2008)"
    }
  }
}
```

### Pass Criteria
- ✓ All time window scenarios evaluated
- ✓ Penalty quantified per 30-minute reduction
- ✓ Fuel cost increase computed
- ✓ Service level trade-off documented
- ✓ Framework cited (time window literature)

---

### Scenario 6: Depot Location Evaluation

### Given (Input Data)
```json
{
  "scenario": "scenario_6_depot_location",
  "description": "Evaluate candidate depot locations by stem mileage",
  "current_depot": {"lat": 40.7128, "lon": -74.0060, "name": "Manhattan"},
  "candidate_locations": [
    {"lat": 40.7589, "lon": -73.9851, "name": "Upper East Side"},
    {"lat": 40.6892, "lon": -74.0445, "name": "Bay Ridge"},
    {"lat": 40.7484, "lon": -73.9857, "name": "Midtown"}
  ],
  "stops": [
    {"id": 1, "location": {"lat": 40.7589, "lon": -73.9851}},
    {"id": 2, "location": {"lat": 40.7484, "lon": -73.9857}},
    {"id": 30, "location": {"lat": 40.7282, "lon": -73.7949}}
  ]
}
```

### Expected Behavior
1. **Compute stem distance for each candidate:**
   - Stem = sum of depot-to-first-stop distances × 2 for all vehicles
   - Current depot stem distance (baseline)
   - Each candidate stem distance

2. **Evaluate cost-benefit:**
   - Fuel savings from reduced stem
   - One-time relocation cost
   - Payback period

3. **Rank candidates:**
   - By stem distance reduction
   - By total cost improvement
   - By feasibility (availability, cost)

### Expected Output (Depot Location Analysis)
```json
{
  "depot_location_evaluation": {
    "current_depot": {
      "name": "Manhattan",
      "stem_distance_km": 38.5,
      "stem_percent_of_total": 26.4
    },
    "candidates": [
      {
        "name": "Midtown",
        "stem_distance_km": 28.2,
        "stem_reduction_km": 10.3,
        "fuel_savings_liters_per_day": 0.9,
        "fuel_savings_usd_per_month": 40.5,
        "relocation_cost_usd": 150000,
        "payback_period_months": 3704,
        "feasibility": "HIGH"
      },
      {
        "name": "Upper East Side",
        "stem_distance_km": 32.8,
        "stem_reduction_km": 5.7,
        "fuel_savings_liters_per_day": 0.5,
        "fuel_savings_usd_per_month": 22.5,
        "relocation_cost_usd": 120000,
        "payback_period_months": 5333,
        "feasibility": "MEDIUM"
      }
    ],
    "recommendation": {
      "optimal_location": "Midtown",
      "rationale": "Reduces stem distance by 26.8%, saving $40.50/month in fuel. However, payback period is very long (3704 months). Consider only if other strategic factors apply.",
      "framework": "Stem-mileage minimization (CVRP depot location literature)"
    }
  }
}
```

### Pass Criteria
- ✓ All candidate locations evaluated
- ✓ Stem distance computed for each
- - Fuel savings estimated correctly
- ✓ Payback period calculated
- ✓ Recommendation includes strategic considerations
- ✓ Framework cited (CVRP depot location)

---

## Cross-Cutting Validation Criteria

### Schema Validation
All scenario outputs must validate against the output schema in `skills/main.md`:
- ✓ executive_summary present
- ✓ inputs_and_assumptions present
- ✓ multi_dimensional_score present
- ✓ findings present
- ✓ improvement_roadmap present
- ✓ sources_and_limitations present

### Framework Grounding
- ✓ Every score cites a specific framework from the parent skill
- ✓ No ad-hoc criteria appear
- ✓ Evidence tier is stated for each claim

### Quality Gates
- ✓ Evidence gate: All claims cite sources
- ✓ Framework gate: All scoring uses named frameworks
- ✓ Challenge gate: Devil's-advocate review completed

### Degradation Behavior
- ✓ With WebSearch/WebFetch disabled, harness produces deliverable with limitation stated
- ✓ With traffic APIs unavailable, historical patterns used with explicit note
- ✓ With solver timeout, best solution found returned with warning

### Determinism of Structure
- ✓ Every run yields the 6 Output-Format sections
- ✓ Consistent field naming across runs
- ✓ Repeatable results for same inputs (given same solver version)

## Test Execution Protocol

To execute regression tests:

1. **Run harness for each scenario:**
   ```bash
   # Scenario 1
   python -m skills.main --scenario tests/regression-fixtures.json --case scenario_1_multi_vehicle

   # Repeat for scenarios 2-6
   ```

2. **Validate outputs:**
   - Compare structure against expected output in this file
   - Verify all pass criteria are met
   - Check framework citations are present
   - Confirm quality gates pass

3. **Document deviations:**
   - If output differs from expected, document reason
   - Update expected output if behavior change is intentional
   - Flag as regression test failure if unintentional

## Maintenance Notes

- Update this file when:
  - New scenarios added
  - Expected behavior changes (intentional)
  - New frameworks added to parent skill
  - Output schema modified

- Last updated: 2026-06-30
- Version: 1.0
- Maintainer: Last-mile Delivery Route Optimizer harness
