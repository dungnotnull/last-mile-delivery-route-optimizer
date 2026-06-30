# SCORING-SCHEMA.md — Standardized Scoring for Science & Industry Cluster

This document defines the standardized scoring schema used across the science-industry cluster for consistent evaluation and reporting.

## Scoring Philosophy

All cluster skills use a **framework-grounded, evidence-based** scoring approach:
- Every score cites a specific framework or research source
- Scores are computed using transparent formulas
- Evidence is explicitly tiered by quality
- Scores include interpretation and context

## Universal Scoring Structure

### Basic Score Object

```json
{
  "dimension_name": {
    "score": number,              // 0-10 scale
    "max_score": 10,              // Always 10 for consistency
    "framework": "citation",      // Source framework/research
    "evidence": "explanation",   // How score computed
    "interpretation": "string",   // What this score means
    "benchmark": number,          // Industry benchmark (if available)
    "percentile": number          // Performance vs. benchmark (if available)
  }
}
```

### Score Interpretation Guide

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| 9.0-10.0 | Excellent | Maintain current practices |
| 7.5-9.0 | Good | Minor improvements possible |
| 6.0-7.5 | Satisfactory | Moderate improvements needed |
| 4.0-6.0 | Fair | Significant improvements needed |
| 0-4.0 | Poor | Major improvements required |

## Standard Scoring Dimensions

### 1. Efficiency Score

**Purpose:** Measure resource utilization and cost efficiency.

**Framework Sources:**
- Operations Research textbooks (Toth & Vigo, 2014)
- Industry productivity benchmarks
- Domain-specific efficiency standards

**Computation Methods:**

**For Routing/Logistics:**
```
efficiency_score = 10 × (ideal_distance / actual_distance)
where ideal_distance is lower bound (e.g., MST approximation)
```

**For Production:**
```
efficiency_score = 10 × (actual_utilization / target_utilization)
where target_utilization is typically 85%
```

**Evidence Requirements:**
- Cite specific efficiency benchmark
- Reference comparison methodology
- State assumptions (e.g., "ideal_distance computed via MST")

### 2. Service Level Score

**Purpose:** Measure on-time delivery and customer satisfaction.

**Framework Sources:**
- Service-level agreement (SLA) standards
- Queuing theory (Kleinrock, 1975)
- Customer satisfaction research

**Computation Methods:**

**For Time Windows:**
```
service_score = 10 × (on_time_stops / total_stops)
where on_time means arrival_time ≤ latest_time + grace_period
```

**For General Service:**
```
service_score = 10 × (1 - tardiness_rate)
where tardiness_rate = late_deliveries / total_deliveries
```

**Evidence Requirements:**
- Cite SLA standard or industry benchmark
- Define grace period if used
- State what constitutes "late"

### 3. Robustness Score

**Purpose:** Measure resilience to disruptions and variance.

**Framework Sources:**
- Robust optimization literature (Bertsimas & Sim, 2004)
- Reliability engineering standards
- Risk management frameworks

**Computation Methods:**

**For Route Robustness:**
```
robustness_score = 10 × (1 - disruption_probability)
where disruption_probability estimated from traffic/weather variance
```

**For General Robustness:**
```
robustness_score = 10 × (redundancy_level / target_redundancy)
where redundancy_level = backup_resources / total_resources
```

**Evidence Requirements:**
- Cite robust optimization framework
- State disruption scenarios considered
- Quantify variance sources

### 4. Flexibility Score

**Purpose:** Measure adaptability to changes and reconfiguration speed.

**Framework Sources:**
- Flexible manufacturing systems research
- Agile operations frameworks
- Change management standards

**Computation Methods:**

**For Reconfiguration Flexibility:**
```
flexibility_score = 10 × (1 / reconfiguration_time_hours)
normalized to [0, 10] range
```

**For General Flexibility:**
```
flexibility_score = 10 × (adaptable_operations / total_operations)
where adaptable_operations can be reassigned without penalty
```

**Evidence Requirements:**
- Cite flexibility research source
- Define reconfiguration scenarios
- State time measurement methodology

### 5. Sustainability Score

**Purpose:** Measure environmental impact and energy efficiency.

**Framework Sources:**
- Green OR research (Lin et al., 2014)
- Carbon footprint standards (ISO 14064)
- Energy efficiency benchmarks

**Computation Methods:**

**For Fuel/Energy:**
```
sustainability_score = 10 × (baseline_emissions / actual_emissions)
where baseline_emissions are from industry standards
```

**For General Sustainability:**
```
sustainability_score = 10 × (renewable_ratio / target_ratio)
where renewable_ratio = renewable_energy / total_energy
```

**Evidence Requirements:**
- Cite sustainability framework or standard
- Reference emission factors or energy data
- State comparison baseline

## Evidence Tier System

### Tier Definitions

| Tier | Description | Examples |
|------|-------------|----------|
| 1 (Highest) | Systematic Review | Cochrane reviews, meta-analyses |
| 2 | RCT/Benchmark | Peer-reviewed experiments, standard benchmarks |
| 3 | Cohort/Field Study | Industry case studies, operational data |
| 4 | Expert Consensus | INFORMS guidelines, expert panels |
| 5 (Lowest) | Blog/Vendor | Vendor whitepapers, blog posts |

### Evidence Citation Format

```json
{
  "evidence_tier": 1-5,
  "source_type": "SYSTEMATIC_REVIEW|RCT|FIELD_STUDY|EXPERT_CONSENSUS|BLOG",
  "citation": "Author et al., Year, Venue",
  "doi": "https://doi.org/...",
  "retrieved_date": "YYYY-MM-DD"
}
```

### Evidence Quality Rules

1. **Prefer higher tiers:** Always cite the highest available evidence tier
2. **Be specific:** Cite specific papers/reports, not generic fields
3. **Date stamps:** Include retrieval dates for web sources
4. **Transparency:** State when using lower-tier evidence

## Aggregated Score Computation

### Overall Score

When computing an overall score from multiple dimensions:

**Weighted Average:**
```json
{
  "overall_score": {
    "score": number,
    "max_score": 10,
    "composition": {
      "efficiency": {"weight": 0.3, "score": 7.5},
      "service_level": {"weight": 0.4, "score": 8.2},
      "robustness": {"weight": 0.2, "score": 6.8},
      "flexibility": {"weight": 0.05, "score": 7.0},
      "sustainability": {"weight": 0.05, "score": 8.5}
    },
    "framework": "Multi-attribute utility analysis (Keeney & Raiffa, 1976)"
  }
}
```

**Weight Selection Principles:**
- Weights sum to 1.0
- Reflect business priorities (stated in assumptions)
- Default: efficiency 0.3, service 0.4, robustness 0.2, flexibility 0.05, sustainability 0.05
- Document rationale for non-default weights

## Quality Assurance

### Score Validation Checklist

Before emitting a score, verify:
- [ ] Score is between 0 and 10
- [ ] Framework citation is explicit and correct
- [ ] Evidence tier is stated
- [ ] Computation formula is documented
- [ ] Interpretation explains what score means
- [ ] Benchmark is provided if available
- [ ] Assumptions are stated

### Common Scoring Errors to Avoid

1. **Ad-hoc scoring:** "This looks like a 7" → Must cite framework and formula
2. **Missing evidence:** "Score is 8" → Must cite source
3. **Unclear interpretation:** "Score 8.5" → Must explain what 8.5 means
4. **Inconsistent scales:** Mixing 0-10 with 0-100 → Always use 0-10
5. **Hidden assumptions:** Not stating baseline or comparison method

## Implementation Examples

### Example 1: Routing Efficiency

```json
{
  "fuel_efficiency": {
    "score": 7.2,
    "max_score": 10,
    "framework": "Lin et al. 2014 fuel consumption modeling",
    "evidence": "Fuel = 145.8 km × 8.5 L/100km × 1.0 (traffic factor). Score = 10 × (130 / 145.8) = 8.9, adjusted to 7.2 for traffic variance.",
    "interpretation": "Moderate fuel efficiency. 12% above ideal distance due to urban routing and time window constraints.",
    "benchmark": 8.5,
    "percentile": 65,
    "evidence_tier": 2,
    "source_type": "FIELD_STUDY",
    "citation": "Lin et al., 2014, Transportation Research Part D",
    "doi": "https://doi.org/10.1016/j.trd.2014.05.003"
  }
}
```

### Example 2: Service Level

```json
{
  "service_level": {
    "score": 9.4,
    "max_score": 10,
    "framework": "Kallehauge 2008 time window compliance",
    "evidence": "33 of 35 stops on time (94.3%), 2 stops marginally late (< 5 min grace period). Score = 10 × 0.943 = 9.43.",
    "interpretation": "Excellent service level. Minor lateness within acceptable grace period.",
    "benchmark": 9.0,
    "percentile": 80,
    "evidence_tier": 3,
    "source_type": "FIELD_STUDY",
    "citation": "Kallehauge, 2008, Transportation Science",
    "doi": "https://doi.org/10.1287/trsc.1080.0222"
  }
}
```

---

**Schema Version:** 1.0
**Last Updated:** 2026-06-30
**Maintainer:** Science & Industry Cluster
**Status:** Production-ready, approved for cluster-wide use
