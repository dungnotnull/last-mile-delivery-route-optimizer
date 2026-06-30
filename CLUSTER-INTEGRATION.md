# CLUSTER-INTEGRATION.md — Science & Industry Cluster Integration

This document defines the integration points, shared sub-skills, and standardized scoring schema for the `last-mile-delivery-route-optimizer` skill within the science-industry cluster.

## Cluster Context

The `last-mile-delivery-route-optimizer` belongs to the **science-industry** cluster, which includes skills related to operations research, logistics optimization, and industrial engineering.

### Cluster Skills (Siblings)
- `last-mile-delivery-route-optimizer` — Fuel-minimizing delivery routing with time windows
- Other potential cluster skills: supply-chain-optimizer, production-scheduler, warehouse-layout-optimizer

## Shared Sub-Skills

The following sub-skills from `last-mile-delivery-route-optimizer` are designed for reuse across the cluster:

### 1. sub-evaluation-framework-selector

**Purpose:** Frame the problem and choose the solver strategy based on problem characteristics.

**Reusable for:** Any operations research problem that requires selecting between exact solvers and heuristics based on problem size and complexity.

**Input Schema:**
```json
{
  "problem_parameters": {
    "n_entities": integer,           // Number of items to schedule/route
    "n_resources": integer,          // Number of vehicles/machines/agents
    "constraints": {
      "capacity": boolean,           // Capacity constraints present
      "temporal": boolean,          // Time windows/sequencing constraints
      "spatial": boolean            // Distance/location constraints
    },
    "objectives": [string]          // List of objectives (e.g., ["minimize_distance", "maximize_utilization"])
  }
}
```

**Output Schema:**
```json
{
  "problem_classification": string,     // Problem type (CVRPTW, TSP, JSP, etc.)
  "solver_strategy": string,            // EXACT, METAHEURISTIC, HYBRID
  "complexity_estimate": string,        // SMALL, MEDIUM, LARGE
  "expected_solve_time_seconds": number
}
```

**Integration Points:**
- Supply-chain-optimizer: Select between MILP and heuristic for network design
- Production-scheduler: Choose between exact scheduling and dispatch rules
- Warehouse-layout-optimizer: Decide between full enumeration and constructive heuristics

### 2. sub-scoring-engine

**Purpose:** Build matrices, solve the optimization problem, and score on KPIs.

**Reusable for:** Any optimization problem that requires building a cost/time matrix, solving with constraints, and computing multi-objective scores.

**Input Schema:**
```json
{
  "problem_definition": object,     // From sub-evaluation-framework-selector
  "entity_data": [object],          // Items to optimize (stops, jobs, items)
  "resource_data": [object],        // Resources (vehicles, machines, bins)
  "constraints": object,            // Constraint definitions
  "objective_weights": object       // Weights for multi-objective optimization
}
```

**Output Schema:**
```json
{
  "solution_status": string,
  "assignments": [object],          // Resource-to-entity assignments
  "aggregate_kpis": object,         // Total cost, time, utilization
  "balance_metrics": object,        // Load balance across resources
  "constraint_violations": object
}
```

**Integration Points:**
- Supply-chain-optimizer: Score facility location and network design solutions
- Production-scheduler: Score job-machine assignments with makespan and tardiness
- Warehouse-layout-optimizer: Score storage location assignments

### 3. sub-traffic-feed-updater

**Purpose:** Refresh real-time conditions and re-optimize sensitive components.

**Reusable for:** Any dynamic optimization problem where external conditions (demand, traffic, machine status) change and require re-optimization.

**Input Schema:**
```json
{
  "initial_solution": object,
  "current_conditions": object,     // Traffic, demand changes, machine status
  "sensitivity_analysis": object     // Which solution components are sensitive
}
```

**Output Schema:**
```json
{
  "updated_solution": object,
  "sensitive_components": [object],
  "delta_vs_initial": object,
  "alerts": [object]
}
```

**Integration Points:**
- Supply-chain-optimizer: Handle demand surges, supplier disruptions
- Production-scheduler: Handle machine breakdowns, urgent job insertions
- Warehouse-layout-optimizer: Handle demand pattern changes

### 4. sub-improvement-roadmap

**Purpose:** Recommend structural improvements with impact estimates.

**Reusable for:** Any optimization problem where structural changes (capacity, location, parameters) can improve performance.

**Input Schema:**
```json
{
  "current_solution": object,
  "performance_bottlenecks": object,
  "business_constraints": object,
  "improvement_categories": [string]  // CAPACITY, LOCATION, PARAMETER, PROCESS
}
```

**Output Schema:**
```json
{
  "improvement_opportunities": [
    {
      "category": string,
      "title": string,
      "impact_estimates": object,
      "implementation_requirements": object
    }
  ],
  "recommended_roadmap": object
}
```

**Integration Points:**
- Supply-chain-optimizer: Recommend facility locations, capacity expansions
- Production-scheduler: Recommend capacity additions, buffer sizing
- Warehouse-layout-optimizer: Recommend zone reconfigurations, automation investments

## Standardized Scoring Schema

### Scoring Dimensions

All cluster skills use a consistent 10-point scoring scale with explicit framework grounding:

```json
{
  "dimension_name": {
    "score": number,              // 0-10
    "max_score": 10,
    "framework": "citation",      // Framework source
    "evidence": "explanation",   // How score was computed
    "interpretation": "string"   // What this score means
  }
}
```

### Common Scoring Dimensions

1. **Efficiency:** Resource utilization, cost efficiency
   - Framework: Operations research textbooks, industry benchmarks

2. **Service Level:** On-time delivery, customer satisfaction
   - Framework: Service-level agreements, queuing theory

3. **Robustness:** Resilience to disruptions, variance tolerance
   - Framework: Robust optimization literature, reliability engineering

4. **Flexibility:** Adaptability to changes, reconfiguration speed
   - Framework: Flexible systems research, agile operations

5. **Sustainability:** Environmental impact, energy efficiency
   - Framework: Green OR, carbon footprint standards

### Evidence Tiers

All cluster skills use the same evidence tier hierarchy:
1. **Systematic Review:** Highest evidence
2. **Meta-Analysis**
3. **RCT/Benchmark**
4. **Cohort/Field Study**
5. **Expert Opinion**
6. **Blog/Vendor Whitepaper:** Lowest evidence

### Quality Gates

All cluster skills enforce the same quality gates:
1. **Evidence Gate:** Every claim cites a source
2. **Framework Gate:** All scoring uses named frameworks
3. **Challenge Gate:** Devil's-advocate review completed

## Integration Protocol

### For Cluster Skills Reusing Sub-Skills

1. **Reference the shared sub-skill:**
   ```markdown
   ## Sub-skills Available
   - `../last-mile-delivery-route-optimizer/skills/sub-scoring-engine.md` — Build matrices and solve optimization problems
   ```

2. **Adapt input/output schemas:**
   - Use the shared schema as a template
   - Extend with domain-specific fields
   - Maintain compatibility with shared core fields

3. **Cite the shared framework:**
   ```markdown
   ## Governing Frameworks
   - CVRP formulation (from `last-mile-delivery-route-optimizer`)
   - Domain-specific frameworks
   ```

### For New Cluster Skills

1. **Follow cluster conventions:**
   - Use the standardized scoring schema
   - Implement the 3 quality gates
   - Cite evidence tiers

2. **Design for sub-skill reuse:**
   - Identify which operations research sub-skills you need
   - Check if shared sub-skills exist
   - Reuse before creating new ones

3. **Document integration points:**
   - Create a CLUSTER-INTEGRATION.md file
   - Specify which sub-skills you're using/sharing
   - Define any schema extensions

## Cluster-Wide Benefits

### Code Reuse
- Shared validation logic (evidence, framework, challenge gates)
- Common scoring computation patterns
- Reusable matrix construction and solver selection

### Consistency
- Uniform output format across cluster
- Consistent quality standards
- Predictable skill behavior

### Maintenance
- Single source of truth for common operations
- Framework updates propagate to all skills
- Reduced duplication of effort

## Shared Knowledge Base

The cluster shares the `SECOND-KNOWLEDGE-BRAIN.md` approach:

### Common Knowledge Sources
- ArXiv: math.OC, cs.DS (operations research, algorithms)
- INFORMS journals: Operations Research, Management Science
- Domain-specific: Google OR-Tools, solver documentation

### Knowledge Update Protocol
- Weekly crawl of ArXiv categories
- Quarterly review of industry benchmarks
- Annual framework refresh

## Integration Status

### Current Cluster Members
- `last-mile-delivery-route-optimizer` — Completed, production-ready

### Potential Future Members
- `supply-chain-optimizer` — Design phase
- `production-scheduler` — Not started
- `warehouse-layout-optimizer` — Not started

### Shared Sub-Skill Availability
- ✅ sub-evaluation-framework-selector — Ready for reuse
- ✅ sub-scoring-engine — Ready for reuse
- ✅ sub-traffic-feed-updater — Ready for reuse
- ✅ sub-improvement-roadmap — Ready for reuse

## Maintenance Protocol

### When Updating Shared Sub-Skills

1. **Version the sub-skill:**
   - Increment version in frontmatter
   - Document breaking changes
   - Update CLUSTER-INTEGRATION.md

2. **Notify cluster members:**
   - Update cluster documentation
   - Tag dependent skills
   - Provide migration guide if needed

3. **Test compatibility:**
   - Verify existing integrations still work
   - Run regression tests
   - Update fixtures if needed

### When Adding New Cluster Skills

1. **Review existing shared sub-skills:**
   - Check if your needs are met
   - Reuse before creating new
   - Extend if needed (don't duplicate)

2. **Document your integration:**
   - Add to CLUSTER-INTEGRATION.md
   - Specify which sub-skills you use
   - Define any schema extensions

3. **Contribute back:**
   - If you create a generally useful sub-skill, consider sharing it
   - Document it for cluster reuse
   - Update this integration document

---

**Document Version:** 1.0
**Last Updated:** 2026-06-30
**Maintainer:** Last-mile Delivery Route Optimizer
**Cluster:** Science & Industry
