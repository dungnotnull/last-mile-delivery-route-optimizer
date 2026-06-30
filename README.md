# Last-Mile Delivery Route Optimizer

[![Status: Production-Ready](https://img.shields.io/badge/status-production--ready-success)](https://github.com/dungnotnull/last-mile-delivery-route-optimizer)
[![Version: 1.0.0](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/dungnotnull/last-mile-delivery-route-optimizer/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Cluster: Science & Industry](https://img.shields.io/badge/cluster-science--&--industry-orange)](CLUSTER-INTEGRATION.md)

> A production-grade AI-powered route optimization system that minimizes fuel consumption while meeting time windows, capacity constraints, and real-time traffic conditions.

## Overview

The Last-Mile Delivery Route Optimizer is a comprehensive Claude AI skill that transforms delivery operations research into actionable intelligence. It formulates delivery sets as Capacitated Vehicle Routing Problems with Time Windows (CVRPTW), produces optimized stop sequences, and continuously incorporates real-time traffic and weather data to minimize fuel and lateness.

### Key Features

- **Framework-Grounded Optimization**: Every decision cites established operations research frameworks
- **Multi-Objective Scoring**: Balances fuel efficiency, service levels, and operational constraints
- **Real-Time Adaptation**: Integrates live traffic and weather data for dynamic re-optimization
- **Capacity Management**: Enforces weight and volume constraints across heterogeneous fleets
- **Strategic Insights**: Generates improvement roadmaps with effort-impact analysis
- **Self-Improving**: Automated knowledge pipeline continuously updates with latest research

### Use Cases

- Micro delivery operators planning daily routes for 1-50 vehicles
- Dynamic re-optimization when road closures or traffic incidents occur
- Fleet sizing analysis to determine optimal vehicle count
- Depot location evaluation to minimize stem mileage
- Time window negotiation to quantify service-level vs. cost trade-offs

## Architecture

The system operates as a research-first AI harness with four specialized sub-skills:

```
Intake → Framework Selection → Scoring Engine → Traffic Updater → Improvement Roadmap → Synthesis
```

### Sub-Skills

1. **sub-evaluation-framework-selector**: Frames the problem and selects solver strategy
2. **sub-scoring-engine**: Builds distance matrices, solves routes, computes KPIs
3. **sub-traffic-feed-updater**: Incorporates real-time conditions and re-optimizes
4. **sub-improvement-roadmap**: Recommends structural improvements with impact estimates

### Governing Frameworks

- Capacitated Vehicle Routing Problem with Time Windows (CVRPTW)
- Clarke-Wright savings & Or-opt/2-opt local search heuristics
- Google OR-Tools metaheuristics (Guided Local Search, Simulated Annealing)
- Haversine/road-network distance and travel-time matrices
- Fuel/emission cost modeling per route
- Service-level (on-time) and stem-mileage KPIs

## Installation

### Prerequisites

- Python 3.8 or higher
- Claude AI with skill support
- (Optional) Google Maps API, TomTom API, or OSRM instance for real-time routing

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dungnotnull/last-mile-delivery-route-optimizer.git
cd last-mile-delivery-route-optimizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the skill in your Claude AI environment.

## Usage

### Basic Example

Provide delivery requirements and let the optimizer generate routes:

**Input:**
- 35 delivery stops across NYC metro area
- 2 delivery vans with 1000 kg capacity each
- Morning delivery windows (8 AM - 12 PM)
- Current depot location

**Output:**
- 2 optimized routes with balanced stops
- Fuel consumption: 12.4 liters
- On-time percentage: 94.3%
- Total distance: 145.8 km
- Improvement roadmap with prioritized recommendations

### Advanced Features

**Real-Time Re-optimization:**
- Traffic incidents automatically trigger re-optimization
- Sensitive routes identified and prioritized
- Alternative routes computed when factors exceed thresholds

**Scenario Analysis:**
- Compare fleet sizes (1, 2, 3 vehicles)
- Evaluate time window tightness impacts
- Assess depot location alternatives
- Quantify capacity constraint violations

## Documentation

### Core Documentation

- **PROJECT-detail.md**: Complete technical specification
- **CLAUDE.md**: Behavioral guidelines for AI implementation
- **PROJECT-DEVELOPMENT-PHASE-TRACKING.md**: Development phase completion status

### Integration Documentation

- **CLUSTER-INTEGRATION.md**: Cluster-wide sub-skill sharing and reuse
- **SCORING-SCHEMA.md**: Standardized scoring methodology for science-industry cluster

### Knowledge Base

- **SECOND-KNOWLEDGE-BRAIN.md**: Self-improving domain knowledge with 10+ foundational research papers
- Continuously updated via automated knowledge pipeline

### Testing

- **tests/test-scenarios.md**: 6 comprehensive test scenarios
- **tests/regression-fixtures.md**: Expected outputs and validation criteria
- **tests/validate_tests.py**: Automated validation script

## Research & Frameworks

### Foundational Papers

The system grounds all decisions in established operations research:

1. **Toth & Vigo (2014)** - The Vehicle Routing Problem
2. **Gendreau & Potvin (2010)** - Local Search in Combinatorial Optimization
3. **Google OR-Tools Documentation** - Production-grade routing library
4. **Kallehauge (2008)** - Time Window Constrained Routing
5. **Lin et al. (2014)** - Green Vehicle Routing and fuel modeling

### Evidence Quality

All scoring uses explicit evidence tiers:
- Tier 1: Systematic Reviews
- Tier 2: RCT/Benchmarks
- Tier 3: Field Studies
- Tier 4: Expert Consensus
- Tier 5: Vendor Documentation

## Quality Assurance

### Quality Gates

Every output passes three quality gates:

1. **Evidence Gate**: Every claim cites a specific source
2. **Framework Gate**: All scoring uses named frameworks
3. **Challenge Gate**: Devil's-advocate review completed

### Test Coverage

- 6 comprehensive test scenarios covering all major use cases
- Regression fixtures with expected outputs
- Automated validation with 100% pass rate

## Development Status

**Version:** 1.0.0 (Production-Ready)

**All Phases Complete:**
- Phase 0: Research & Skill Architecture
- Phase 1: Core Sub-Skills (4 sub-skills)
- Phase 2: Main Harness + Quality Gates
- Phase 3: SECOND-KNOWLEDGE-BRAIN Pipeline
- Phase 4: Testing & Validation
- Phase 5: Integration & Cross-Skill Wiring

## Cluster Integration

This skill is part of the Science & Industry cluster and shares sub-skills with:

- Potential: supply-chain-optimizer
- Potential: production-scheduler
- Potential: warehouse-layout-optimizer

Shared sub-skills available for cluster-wide reuse:
- sub-evaluation-framework-selector
- sub-scoring-engine
- sub-traffic-feed-updater
- sub-improvement-roadmap

## Contributing

We welcome contributions! Please see our contribution guidelines:

1. Fork the repository
2. Create a feature branch
3. Follow the CLAUDE.md guidelines for code quality
4. Ensure tests pass: `python tests/validate_tests.py`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google OR-Tools team for the exceptional routing library
- Operations research community for foundational frameworks
- Claude AI for the harness architecture

## Citation

If you use this work in your research, please cite:

```bibtex
@software{last_mile_route_optimizer,
  title={Last-Mile Delivery Route Optimizer},
  author={Dung},
  year={2026},
  version={1.0.0},
  url={https://github.com/dungnotnull/last-mile-delivery-route-optimizer}
}
```

## Contact

- Repository: https://github.com/dungnotnull/last-mile-delivery-route-optimizer
- Issues: https://github.com/dungnotnull/last-mile-delivery-route-optimizer/issues

---

**Built with research-first principles and production-grade standards.**

Optimizing last-mile delivery through rigorous operations research and AI-powered intelligence.
