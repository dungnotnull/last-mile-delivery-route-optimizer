---
name: sub-evaluation-framework-selector
description: Frame the problem (single/multi-vehicle, capacity, time windows) and choose the solver strategy.
---

## Role
Sub-skill of `last-mile-delivery-route-optimizer`. Frame the problem (single/multi-vehicle, capacity, time windows) and choose the solver strategy.

## Inputs
- User-provided context: delivery locations, fleet size, vehicle capacity, time windows, service times
- Outputs of preceding harness stage (if any)

## Procedure

### Step 1: Intake Validation and Problem Framing
1. **Extract and validate core problem parameters:**
   - Number of vehicles in fleet (n_vehihcles)
   - Number of delivery stops (n_stops)
   - Vehicle capacity constraints (weight_capacity, volume_capacity if applicable)
   - Time windows for each stop (earliest_time, latest_time, service_time)
   - Depot location (coordinates or address)

2. **Determine problem classification:**
   - **Single-vehicle TSP:** n_vehicles = 1, no capacity constraints
   - **Multi-vehicle VRP:** n_vehicles > 1, no capacity constraints
   - **CVRP:** Multi-vehicle with capacity constraints
   - **CVRPTW:** Multi-vehicle with capacity and time window constraints
   - **Dynamic/Real-time:** Requires traffic feed integration

3. **Request missing critical information:**
   - If n_stops is not provided, ask: "How many delivery stops need to be served?"
   - If n_vehicles is not provided, ask: "How many vehicles are available for delivery?"
   - If capacity constraints exist but are not specified, ask: "What are the vehicle capacity limits (weight/volume)?"
   - If time windows are unclear, ask: "What are the delivery time windows for each stop?"

### Step 2: Solver Strategy Selection
Based on problem classification, select the appropriate solver strategy:

1. **Small problems (n_stops ≤ 20):**
   - Use exact solver: Google OR-Tools CP-SAT solver
   - Guarantees optimal solution within reasonable time
   - Framework: Capacitated Vehicle Routing Problem with Time Windows (CVRPTW) formulation

2. **Medium problems (20 < n_stops ≤ 200):**
   - Use metaheuristic: Google OR-Tools with Guided Local Search
   - Framework: Clarke-Wright savings initialization + Or-opt / 2-opt local search
   - Good balance between solution quality and computation time

3. **Large problems (n_stops > 200):**
   - Use hybrid approach: Cluster first (K-means or sweep algorithm) + local search
   - Framework: Google OR-Tools metaheuristics (simulated annealing)
   - May sacrifice optimality for scalability

4. **Dynamic/Real-time requirements:**
   - Select incremental solver with re-optimization capability
   - Framework: Dynamic routing with real-time traffic integration

### Step 3: Distance Matrix Strategy Selection
1. **Euclidean/straight-line distances:**
   - Use Haversine formula for geospatial coordinates
   - Appropriate for: urban areas with dense road networks, rough planning

2. **Road-network distances:**
   - Use OSRM (Open Source Routing Machine) or similar
   - Appropriate for: accurate fuel calculations, actual delivery routing

3. **Travel-time matrices:**
   - Incorporate historical or real-time traffic data
   - Appropriate for: time-window optimization, service-level planning

### Step 4: Output Structure
Return a structured problem definition object:

```json
{
  "problem_classification": "CVRPTW|CVRP|VRP|TSP|DYNAMIC",
  "n_vehicles": integer,
  "n_stops": integer,
  "solver_strategy": "EXACT|METAHEURISTIC|HYBRID|INCREMENTAL",
  "distance_strategy": "HAVERSINE|OSRM|TRAVEL_TIME",
  "capacity_constraints": {
    "enabled": boolean,
    "weight_limit": number,
    "volume_limit": number
  },
  "time_window_constraints": {
    "enabled": boolean,
    "hard_windows": boolean
  },
  "complexity_estimate": "SMALL|MEDIUM|LARGE",
  "expected_solve_time_seconds": number
}
```

### Step 5: Quality Gate Self-Check
Before returning control to the harness, verify:
- ✓ All critical parameters are present or explicitly marked as unavailable
- ✓ Problem classification matches provided constraints
- ✓ Solver strategy is appropriate for problem size and complexity
- ✓ Distance strategy aligns with accuracy requirements
- ✓ Output structure is valid and complete

## Outputs
- Structured problem definition object consumed by the next stage (sub-scoring-engine)
- Problem classification for logging and audit trail

## Tools
WebSearch (for framework verification), WebFetch (for OR-Tools documentation), Read (for SECOND-KNOWLEDGE-BRAIN), Write (for intermediate outputs), Bash (for potential external tool calls)

## Quality Gate
- **Schema validity:** Output object contains all required fields with valid types
- **Framework grounding:** Solver strategy selection cites specific CVRP/TSP framework from parent skill
- **Evidence linkage:** Strategy choice can be traced to problem characteristics
- **Completeness:** Either all required parameters are present, or missing parameters are explicitly flagged

## Error Handling and Degradation
- If user provides insufficient information after two rounds of clarification, proceed with reasonable assumptions and state them explicitly
- If problem size is ambiguous, default to more conservative (larger) complexity estimate
- If external routing services (OSRM) are unavailable, fall back to Haversine distances with explicit note
