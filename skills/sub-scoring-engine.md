---
name: sub-scoring-engine
description: Build the distance/time matrix, solve the route set, and score it on fuel, distance, and on-time KPIs.
---

## Role
Sub-skill of `last-mile-delivery-route-optimizer`. Build the distance/time matrix, solve the route set, and score it on fuel, distance, and on-time KPIs.

## Inputs
- Problem definition object from sub-evaluation-framework-selector
- Delivery location data (coordinates or addresses)
- Vehicle specifications (fuel consumption rates, capacity limits)
- Time window requirements (earliest_time, latest_time, service_time)
- Demand data (weight, volume for each stop)

## Procedure

### Step 1: Distance/Time Matrix Construction

#### For Haversine distance strategy:
1. **Parse coordinates:** Extract latitude/longitude for depot and all stops
2. **Compute pairwise distances:**
   - Use Haversine formula: 
     ```
     a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
     c = 2 ⋅ atan2(√a, √(1−a))
     d = R ⋅ c
     ```
   - Earth radius R = 6,371 km
   - Result: symmetric distance matrix in kilometers
3. **Estimate travel times:** 
   - Base: distance / average_speed (default 30 km/h urban)
   - Adjust for traffic: apply congestion factor if available

#### For OSRM road-network strategy:
1. **Build OSRM API calls:**
   - Base URL: `http://router.project-osrm.org/table/v1/driving/`
   - Format: `lon1,lat1;lon2,lat2;...`
   - Parameters: `sources=0&destinations=all` for each origin
2. **Parse OSRM response:**
   - Extract `durations` (travel time in seconds)
   - Extract `distances` (road network distance in meters)
3. **Construct matrices:**
   - Travel-time matrix: seconds → convert to minutes
   - Distance matrix: meters → convert to kilometers
4. **Handle failures gracefully:**
   - If OSRM unavailable, fall back to Haversine with explicit note
   - Log fallback event for audit trail

#### For travel-time matrix strategy:
1. **Incorporate real-time traffic:**
   - Source: sub-traffic-feed-updater traffic indices
   - Apply speed adjustments per road segment
2. **Compute time-dependent matrices:**
   - Peak vs. off-peak travel times
   - Use conservative (peak) estimates for planning

### Step 2: Route Optimization Execution

#### Google OR-Tools Implementation Pattern:
1. **Create RoutingIndexManager:**
   - num_locations = n_stops + 1 (depot)
   - num_vehicles = from problem definition
   - depot node index = 0 (first location)

2. **Create RoutingModel:**
   - Initialize with manager
   - Set transit callback: returns distance/time between nodes

3. **Define cost function:**
   - Base: arc cost (distance or travel time)
   - Add penalty for:
     - Soft time window violations (per minute late penalty)
     - Load imbalance between vehicles
     - Excess vehicle usage

4. **Add constraints:**
   - **Capacity constraints:**
     - Use AddDimensionWithCapacity for cumulative demand
     - Set vehicle capacity limits
     - Slack for minor violations if soft constraints
   - **Time window constraints:**
     - AddDimension with time horizon
     - Set time windows per node (depot + stops)
     - Set penalty coefficient for violations

5. **Set search parameters:**
   - For EXACT: use default CP-SAT solver
   - For METAHEURISTIC: 
     - `first_solution_strategy = AUTOMATIC`
     - `local_search_metaheuristic = GUIDED_LOCAL_SEARCH`
     - `time_limit_ms = 30000` (30 seconds default)
   - For HYBRID:
     - Pre-cluster with sweep or K-means
     - Solve each cluster independently
     - Merge with 2-opt inter-cluster improvements

6. **Execute solve:**
   - Call routing.SolveWithParameters(search_parameters)
   - Monitor solve time and iterations

### Step 3: Solution Extraction and Validation

1. **Extract routes:**
   - For each vehicle: extract node sequence from solution
   - Compute route statistics: total distance, total time, load per vehicle
   - Identify depot-to-depot loops

2. **Validate constraints:**
   - Check capacity: cumulative demand ≤ vehicle capacity for all vehicles
   - Check time windows: arrival_time ∈ [earliest, latest] for all stops
   - Check all stops visited: every node appears exactly once across all routes
   - Check depot start/end: each route begins and ends at depot

3. **Flag violations:**
   - Log any constraint violations with severity (minor/moderate/severe)
   - Count: n_capacity_violations, n_time_window_violations, n_unserved_stops

### Step 4: KPI Computation

#### Fuel Cost Scoring:
1. **Base fuel consumption:**
   - Formula: `fuel_liters = distance_km × liters_per_100km / 100`
   - Default: 8.5 L/100km for light commercial vehicle
   - Adjust for load: +5% per 50% capacity utilization

2. **Traffic penalty:**
   - Factor from sub-traffic-feed-updater (if available)
   - Range: 1.0 (free flow) to 2.5 (severe congestion)

3. **Total fuel cost:**
   - `fuel_cost = total_fuel_liters × fuel_price_per_liter`
   - Default fuel price: $1.50/L (adjust per region if known)

#### Distance Scoring:
1. **Total distance:** sum of all route distances
2. **Stem distance:** total distance from depot to first stop × 2
3. **On-route distance:** total - stem distance
4. **Distance per stop:** total_distance / n_stops

#### Service-Level (On-Time) Scoring:
1. **Time window compliance:**
   - `% on_time = (n_stops - n_late_arrivals) / n_stops × 100`
   - Late arrival: arrival_time > latest_time
   - Grace period: 5 minutes (configurable)

2. **Lateness distribution:**
   - Average lateness: sum(max(0, arrival - latest)) / n_stops
   - Maximum lateness: worst single-stop lateness
   - Severe lateness count: arrivals > 15 minutes late

#### Load Balance Scoring:
1. **Vehicle utilization:**
   - Load per vehicle: sum of demands served
   - Utilization %: (vehicle_load / vehicle_capacity) × 100
   - Standard deviation of utilization across fleet

2. **Distance balance:**
   - Distance per vehicle
   - Range: max_vehicle_distance - min_vehicle_distance
   - Coefficient of variation: std_dev / mean

### Step 5: Output Structure
Return a comprehensive solution score object:

```json
{
  "solution_status": "OPTIMAL|FEASIBLE|INFEASIBLE|UNSOLVED",
  "routes": [
    {
      "vehicle_id": integer,
      "stop_sequence": [integer, ...],
      "distance_km": number,
      "travel_time_minutes": number,
      "fuel_liters": number,
      "load_utilization_percent": number,
      "time_window_violations": integer
    }
  ],
  "aggregate_kpis": {
    "total_distance_km": number,
    "total_fuel_liters": number,
    "total_fuel_cost": number,
    "total_travel_time_minutes": number,
    "stem_distance_km": number,
    "on_time_percent": number,
    "late_arrivals_count": integer,
    "average_lateness_minutes": number,
    "max_lateness_minutes": number
  },
  "balance_metrics": {
    "vehicle_distance_stddev": number,
    "vehicle_load_stddev": number,
    "vehicle_distance_cv": number
  },
  "constraint_violations": {
    "capacity_violations": integer,
    "time_window_violations": integer,
    "unserved_stops": integer
  },
  "solve_metadata": {
    "solver_strategy_used": string,
    "solve_time_seconds": number,
    "iterations": integer,
    "objective_value": number
  }
}
```

### Step 6: Quality Gate Self-Check
Before returning control to the harness, verify:
- ✓ Distance/time matrix is valid (no infinite or NaN values)
- ✓ All stops are assigned to routes
- ✓ Solution status is clearly stated (OPTIMAL/FEASIBLE/INFEASIBLE)
- ✓ All KPIs are computed and within reasonable bounds
- ✓ Output structure is complete and valid JSON
- ✓ Framework citations are present (OR-Tools, CVRP formulation)

## Outputs
- Comprehensive solution score object consumed by the next stage (sub-traffic-feed-updater)
- Individual route details for operational use
- Aggregate KPIs for management reporting

## Tools
WebSearch (for framework documentation), WebFetch (for OR-Tools API reference), Read (for SECOND-KNOWLEDGE-BRAIN), Write (for solution persistence), Bash (for potential external solver calls)

## Quality Gate
- **Schema validity:** All required fields present with valid numeric/array types
- **Framework grounding:** Solution method cites Google OR-Tools and CVRP framework explicitly
- **Evidence linkage:** Each KPI calculation references its formula/framework
- **Completeness:** Both aggregate KPIs and per-vehicle details provided
- **Logical consistency:** Total KPIs equal sum of individual route KPIs

## Error Handling and Degradation
- If solver fails to find feasible solution, return INFEASIBLE status with diagnostic details (constraint violations, infeasibility proof if available)
- If solve timeout occurs, return best solution found with warning about solution quality
- If distance matrix construction fails, fall back to next available strategy (OSRM → Haversine) with explicit degradation note
- If KPI computation fails (e.g., missing fuel consumption rate), use sensible defaults with explicit assumptions stated
