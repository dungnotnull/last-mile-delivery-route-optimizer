#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_tests.py — Validate test scenarios and regression fixtures for last-mile-delivery-route-optimizer.

This script validates that:
1. All 6 test scenarios are properly documented
2. Expected outputs are complete
3. Pass criteria are clearly defined
4. Regression fixtures match the output schema

Usage:
    python tests/validate_tests.py              # Validate all scenarios
    python tests/validate_tests.py --scenario 1  # Validate specific scenario
"""
import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Paths
TEST_DIR = Path(__file__).parent
PROJECT_ROOT = TEST_DIR.parent
SCENARIOS_FILE = TEST_DIR / "test-scenarios.md"
FIXTURES_FILE = TEST_DIR / "regression-fixtures.md"
MAIN_SKILL = PROJECT_ROOT / "skills" / "main.md"

# Expected output sections (from main.md)
EXPECTED_SECTIONS = [
    "executive_summary",
    "inputs_and_assumptions",
    "multi_dimensional_score",
    "findings",
    "improvement_roadmap",
    "sources_and_limitations"
]

# Test scenarios
SCENARIOS = [
    {"id": 1, "name": "Multi-vehicle route optimization", "file_key": "scenario_1"},
    {"id": 2, "name": "Dynamic re-optimization for road closure", "file_key": "scenario_2"},
    {"id": 3, "name": "Fleet size comparison", "file_key": "scenario_3"},
    {"id": 4, "name": "Capacity constraint enforcement", "file_key": "scenario_4"},
    {"id": 5, "name": "Time window tightness impact", "file_key": "scenario_5"},
    {"id": 6, "name": "Depot location evaluation", "file_key": "scenario_6"}
]


def read_file(file_path: Path) -> str:
    """Read file contents with error handling."""
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"[error] Failed to read {file_path}: {e}")
        return ""


def validate_scenario_documentation(content: str, scenario_id: int) -> Tuple[bool, List[str]]:
    """Validate that a scenario is documented in test-scenarios.md."""
    issues = []

    # Check if scenario section exists
    scenario_header = f"### Scenario {scenario_id}"
    if scenario_header not in content:
        issues.append(f"Scenario {scenario_id} not found in test-scenarios.md")
        return False, issues

    # Extract scenario content
    lines = content.split("\n")
    scenario_start = lines.index(scenario_header)
    scenario_end = scenario_start + 20  # Check next 20 lines

    scenario_content = "\n".join(lines[scenario_start:scenario_end])

    # Validate required elements
    required_elements = [
        "**Given:**",
        "**Expected harness behavior:**",
        "**Pass criteria:**"
    ]

    for element in required_elements:
        if element not in scenario_content:
            issues.append(f"Scenario {scenario_id} missing '{element}'")

    # Check pass criteria content
    if "**Pass criteria:**" in scenario_content:
        pass_criteria = scenario_content.split("**Pass criteria:**")[1].split("\n")[0]
        if "quality gates pass" not in pass_criteria.lower():
            issues.append(f"Scenario {scenario_id} pass criteria don't mention quality gates")

    return len(issues) == 0, issues


def validate_fixture_structure(content: str, scenario_id: int) -> Tuple[bool, List[str]]:
    """Validate that a scenario has regression fixtures defined."""
    issues = []
    scenario_key = SCENARIOS[scenario_id - 1]["file_key"]

    # Check if scenario section exists in fixtures
    scenario_header = f"### Scenario {scenario_id}:"
    if scenario_header not in content:
        issues.append(f"Scenario {scenario_id} fixtures not found in regression-fixtures.md")
        return False, issues

    # Extract scenario content
    lines = content.split("\n")
    scenario_start = None
    for i, line in enumerate(lines):
        if scenario_header in line:
            scenario_start = i
            break

    if scenario_start is None:
        issues.append(f"Scenario {scenario_id} not found in regression-fixtures.md")
        return False, issues

    # Find next scenario or end of file
    scenario_end = len(lines)
    for i in range(scenario_start + 1, len(lines)):
        if lines[i].startswith("### Scenario ") and ":" in lines[i]:
            scenario_end = i
            break

    scenario_content = "\n".join(lines[scenario_start:scenario_end])

    # Validate required sections
    required_sections = [
        "### Given (Input Data)",
        "### Expected Behavior",
        "### Expected Output",
        "### Pass Criteria"
    ]

    for section in required_sections:
        if section not in scenario_content:
            issues.append(f"Scenario {scenario_id} fixtures missing '{section}'")

    # Validate JSON structure in Given section
    if "### Given (Input Data)" in scenario_content:
        given_section = scenario_content.split("### Given (Input Data)")[1].split("###")[0]
        if "```json" not in given_section:
            issues.append(f"Scenario {scenario_id} Given section missing JSON code block")
        else:
            # Validate JSON is well-formed
            json_start = given_section.find("{")
            json_end = given_section.rfind("}") + 1
            if json_start > 0 and json_end > json_start:
                json_str = given_section[json_start:json_end]
                try:
                    json.loads(json_str)
                except json.JSONDecodeError as e:
                    issues.append(f"Scenario {scenario_id} Given section has invalid JSON: {e}")

    # Validate Expected Output has required sections
    # Note: Scenario 1 is the full end-to-end test with all 6 sections
    # Scenarios 2-6 are specialized tests with focused outputs
    if "### Expected Output" in scenario_content:
        output_section = scenario_content.split("### Expected Output")[1].split("###")[0]
        # Only validate full sections for scenario 1
        if scenario_id == 1:
            for expected_section in EXPECTED_SECTIONS:
                if expected_section not in output_section:
                    issues.append(f"Scenario {scenario_id} Expected Output missing '{expected_section}'")
        else:
            # For specialized scenarios, just check they have some output structure
            if not output_section.strip():
                issues.append(f"Scenario {scenario_id} Expected Output section is empty")
            elif "```json" not in output_section and "```" not in output_section:
                issues.append(f"Scenario {scenario_id} Expected Output missing code block")

    return len(issues) == 0, issues


def validate_cross_cutting_criteria(content: str) -> Tuple[bool, List[str]]:
    """Validate that cross-cutting validation criteria are defined."""
    issues = []

    required_sections = [
        "## Cross-Cutting Validation Criteria",
        "### Schema Validation",
        "### Framework Grounding",
        "### Quality Gates",
        "### Degradation Behavior",
        "### Determinism of Structure"
    ]

    for section in required_sections:
        if section not in content:
            issues.append(f"Regression fixtures missing '{section}'")

    # Validate Test Execution Protocol section
    if "## Test Execution Protocol" not in content:
        issues.append("Regression fixtures missing Test Execution Protocol")

    return len(issues) == 0, issues


def validate_output_schema() -> Tuple[bool, List[str]]:
    """Validate that main.md defines the expected output schema."""
    issues = []
    content = read_file(MAIN_SKILL)

    if not content:
        issues.append("Cannot read main.md")
        return False, issues

    # Check Output Format section
    if "## Output Format" not in content:
        issues.append("main.md missing Output Format section")

    # Validate expected sections are mentioned
    output_section_start = content.find("## Output Format")
    if output_section_start > 0:
        output_content = content[output_section_start:output_section_start + 2000]
        for section in EXPECTED_SECTIONS:
            if section not in output_content:
                issues.append(f"main.md Output Format missing '{section}'")

    return len(issues) == 0, issues


def run_validation(scenario_id: int = None) -> Tuple[bool, Dict[str, List[str]]]:
    """Run validation for all or specific scenario(s)."""
    all_results = {}
    overall_valid = True

    print(f"[info] Starting test scenario validation...")

    # Validate main.md output schema
    schema_valid, schema_issues = validate_output_schema()
    all_results["main_schema"] = schema_issues
    if not schema_valid:
        overall_valid = False
        print(f"[fail] main.md output schema validation failed")
        for issue in schema_issues:
            print(f"  - {issue}")

    # Read scenario and fixture files
    scenarios_content = read_file(SCENARIOS_FILE)
    fixtures_content = read_file(FIXTURES_FILE)

    if not scenarios_content:
        all_results["scenarios_file"] = ["Cannot read test-scenarios.md"]
        overall_valid = False
    if not fixtures_content:
        all_results["fixtures_file"] = ["Cannot read regression-fixtures.md"]
        overall_valid = False

    if not scenarios_content or not fixtures_content:
        return overall_valid, all_results

    # Validate each scenario
    scenarios_to_validate = [scenario_id] if scenario_id else range(1, 7)

    for sid in scenarios_to_validate:
        scenario_results = []

        # Validate documentation
        doc_valid, doc_issues = validate_scenario_documentation(scenarios_content, sid)
        scenario_results.extend(doc_issues)

        # Validate fixtures
        fix_valid, fix_issues = validate_fixture_structure(fixtures_content, sid)
        scenario_results.extend(fix_issues)

        all_results[f"scenario_{sid}"] = scenario_results

        if not (doc_valid and fix_valid):
            overall_valid = False
            print(f"[fail] Scenario {sid} validation failed")
            for issue in scenario_results:
                print(f"  - {issue}")
        else:
            print(f"[pass] Scenario {sid} validated successfully")

    # Validate cross-cutting criteria
    cross_valid, cross_issues = validate_cross_cutting_criteria(fixtures_content)
    all_results["cross_cutting"] = cross_issues
    if not cross_valid:
        overall_valid = False
        print(f"[fail] Cross-cutting criteria validation failed")
        for issue in cross_issues:
            print(f"  - {issue}")
    else:
        print(f"[pass] Cross-cutting criteria validated")

    return overall_valid, all_results


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Validate test scenarios and regression fixtures'
    )
    parser.add_argument('--scenario', type=int, choices=range(1, 7),
                       help='Specific scenario to validate (1-6)')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    args = parser.parse_args()

    print(f"[info] Last-mile Delivery Route Optimizer - Test Validation")
    print(f"[info] Validating scenarios: Scenario {args.scenario}" if args.scenario else "[info] Validating all scenarios")
    print()

    valid, results = run_validation(args.scenario)

    print()
    if valid:
        print(f"[ok] All validation checks passed")
        print(f"[info] Test scenarios are ready for execution")
        return 0
    else:
        print(f"[fail] Validation failed with {sum(len(v) for v in results.values())} issues")
        print(f"[info] See output above for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
