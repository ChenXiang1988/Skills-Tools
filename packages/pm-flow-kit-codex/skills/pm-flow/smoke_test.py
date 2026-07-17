#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke test for pm-flow's default generated workflow."""

import os
import shutil
import subprocess
import sys
import tempfile
import json


SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.dirname(SKILL_DIR)
PACKAGE_DIR = os.path.dirname(SKILLS_DIR)
PM_PRD_DIR = os.path.join(SKILLS_DIR, "pm-prd")
PM_RESEARCH_DIR = os.path.join(SKILLS_DIR, "pm-research")
PM_REQUIREMENT_ANALYSIS_DIR = os.path.join(SKILLS_DIR, "pm-requirement-analysis")
PM_METRICS_DEFINITION_DIR = os.path.join(SKILLS_DIR, "pm-metrics-definition")
PM_BOUNDARY_DIR = os.path.join(SKILLS_DIR, "pm-boundary")
PM_HTML_PROTOTYPE_DIR = os.path.join(SKILLS_DIR, "pm-html-prototype")
PM_PROTOTYPE_REVIEW_DIR = os.path.join(SKILLS_DIR, "pm-prototype-review")
PM_REVIEW_DIR = os.path.join(SKILLS_DIR, "pm-review")
PM_CONTEXT_CONTRACT_DIR = os.path.join(SKILLS_DIR, "pm-context-contract")
PM_MERMAID_DIAGRAM_DIR = os.path.join(SKILLS_DIR, "pm-mermaid-diagram")
HUMANIZER_DIR = os.path.join(SKILLS_DIR, "humanizer")
CONTROLLER = os.path.join(SKILL_DIR, "controller.py")


def assert_skill_assets():
    required = [
        os.path.join(SKILL_DIR, "references", "context-confirmation.md"),
        os.path.join(SKILL_DIR, "references", "requirement-analysis.md"),
        os.path.join(SKILL_DIR, "references", "analysis-routing.md"),
        os.path.join(SKILL_DIR, "references", "source-error-severity.md"),
        os.path.join(SKILL_DIR, "stages", "context-confirmation", "template.md"),
        os.path.join(SKILL_DIR, "stages", "requirement-analysis", "template.md"),
        os.path.join(PACKAGE_DIR, "design-system", "README.md"),
        os.path.join(PACKAGE_DIR, "design-system", "PROVENANCE.md"),
        os.path.join(PACKAGE_DIR, "design-system", "DESIGN.md"),
        os.path.join(PACKAGE_DIR, "design-system", "tokens.css"),
        os.path.join(PACKAGE_DIR, "design-system", "components.html"),
        os.path.join(PACKAGE_DIR, "design-system", "pda", "DESIGN.md"),
        os.path.join(PACKAGE_DIR, "design-system", "pda", "tokens.css"),
        os.path.join(PACKAGE_DIR, "design-system", "pda", "components.html"),
        os.path.join(PM_RESEARCH_DIR, "SKILL.md"),
        os.path.join(PM_RESEARCH_DIR, "references", "research-method.md"),
        os.path.join(PM_RESEARCH_DIR, "assets", "templates", "research.md"),
        os.path.join(PM_RESEARCH_DIR, "agents", "openai.yaml"),
        os.path.join(PM_REQUIREMENT_ANALYSIS_DIR, "SKILL.md"),
        os.path.join(PM_REQUIREMENT_ANALYSIS_DIR, "references", "analysis-method.md"),
        os.path.join(PM_REQUIREMENT_ANALYSIS_DIR, "references", "artifact-management.md"),
        os.path.join(PM_REQUIREMENT_ANALYSIS_DIR, "assets", "templates", "requirement-analysis.md"),
        os.path.join(PM_REQUIREMENT_ANALYSIS_DIR, "assets", "templates", "scenario-catalog.md"),
        os.path.join(PM_REQUIREMENT_ANALYSIS_DIR, "assets", "templates", "use-cases.md"),
        os.path.join(PM_REQUIREMENT_ANALYSIS_DIR, "assets", "templates", "end-to-end-flow.md"),
        os.path.join(PM_REQUIREMENT_ANALYSIS_DIR, "assets", "templates", "artifact-plan.md"),
        os.path.join(PM_METRICS_DEFINITION_DIR, "SKILL.md"),
        os.path.join(PM_METRICS_DEFINITION_DIR, "references", "metrics-definition.md"),
        os.path.join(PM_METRICS_DEFINITION_DIR, "assets", "templates", "metrics-definition.md"),
        os.path.join(PM_BOUNDARY_DIR, "SKILL.md"),
        os.path.join(PM_BOUNDARY_DIR, "references", "boundary-method.md"),
        os.path.join(PM_BOUNDARY_DIR, "assets", "templates", "boundary.md"),
        os.path.join(PM_BOUNDARY_DIR, "agents", "openai.yaml"),
        os.path.join(PM_PRD_DIR, "SKILL.md"),
        os.path.join(PM_PRD_DIR, "references", "prd-sizing.md"),
        os.path.join(PM_PRD_DIR, "references", "prd-quality-checklist.md"),
        os.path.join(PM_PRD_DIR, "references", "diagram-guidelines.md"),
        os.path.join(PM_PRD_DIR, "templates", "l1-light-prd.md"),
        os.path.join(PM_PRD_DIR, "templates", "l2-standard-prd.md"),
        os.path.join(PM_PRD_DIR, "templates", "l3-deep-prd.md"),
        os.path.join(PM_HTML_PROTOTYPE_DIR, "SKILL.md"),
        os.path.join(PM_HTML_PROTOTYPE_DIR, "references", "ant-design-adapter.md"),
        os.path.join(PM_HTML_PROTOTYPE_DIR, "assets", "scaffold", "assets", "prototype.css"),
        os.path.join(PM_HTML_PROTOTYPE_DIR, "assets", "scaffold", "assets", "connect-lines.js"),
        os.path.join(PM_HTML_PROTOTYPE_DIR, "assets", "scaffold", "assets", "fonts", "DingTalk-JinBuTi.woff2"),
        os.path.join(PM_HTML_PROTOTYPE_DIR, "assets", "scaffold", "templates", "prototype-doc.html"),
        os.path.join(PM_PROTOTYPE_REVIEW_DIR, "SKILL.md"),
        os.path.join(PM_PROTOTYPE_REVIEW_DIR, "references", "review-prototype.md"),
        os.path.join(PM_PROTOTYPE_REVIEW_DIR, "assets", "review", "template-doc.html"),
        os.path.join(PM_REVIEW_DIR, "SKILL.md"),
        os.path.join(PM_REVIEW_DIR, "references", "review-method.md"),
        os.path.join(PM_REVIEW_DIR, "assets", "templates", "review.md"),
        os.path.join(PM_REVIEW_DIR, "agents", "openai.yaml"),
        os.path.join(PM_CONTEXT_CONTRACT_DIR, "SKILL.md"),
        os.path.join(PM_CONTEXT_CONTRACT_DIR, "references", "context-contract.md"),
        os.path.join(PM_CONTEXT_CONTRACT_DIR, "assets", "templates", "intake.md"),
        os.path.join(PM_CONTEXT_CONTRACT_DIR, "assets", "templates", "context-manifest.md"),
        os.path.join(PM_MERMAID_DIAGRAM_DIR, "SKILL.md"),
        os.path.join(PM_MERMAID_DIAGRAM_DIR, "references", "diagram-patterns.md"),
        os.path.join(os.path.dirname(SKILLS_DIR), "references", "pm-shared", "error-taxonomy.md"),
        os.path.join(os.path.dirname(SKILLS_DIR), "references", "pm-shared", "bad-output-examples.md"),
        os.path.join(HUMANIZER_DIR, "SKILL.md"),
    ]
    missing = [path for path in required if not os.path.exists(path)]
    if missing:
        raise SystemExit("missing skill asset: %s" % ", ".join(missing))

    with open(os.path.join(SKILL_DIR, "contract_config.json"), encoding="utf-8") as f:
        contract = f.read()
    contract_gates = [
        "pm-prd was used",
        "pm-research was used",
        "pm-boundary was used",
        "pm-review was used",
        "Opportunity, user, market, and metric analysis",
        "Key assumptions have been identified",
        "Acceptance criteria can be converted into test scenarios",
        "humanizer",
        "Design guidelines or component-library rules",
        "component library is specified",
        "pm-requirement-analysis",
        "scenario-catalog.md",
        "use-cases.md",
        "end-to-end-flow.md",
        "metrics-definition.md",
        "artifact-plan.md",
        "pm-metrics-definition",
        "use cases",
        "end-to-end flow",
        "requirement analysis",
        "Context intake",
        "Requirement analysis level",
        "artifact routing",
        "fixed full workflow",
        "premature technical stack choices",
        "pm-html-prototype",
        "duplicate-action",
        "subjective-only wording",
        "P1/P0 source errors",
        "Workspace root has been confirmed",
        "work stops until the human clarifies",
        "Knowledge-base path has been confirmed",
        "knowledge-base root, manifest, or confirmed source list",
    ]
    missing_gates = [gate for gate in contract_gates if gate not in contract]
    if missing_gates:
        raise SystemExit("contract_config.json is missing gate: %s" % ", ".join(missing_gates))


def run(args, cwd=None, expect_ok=True):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(args, cwd=cwd, text=True, capture_output=True, env=env)
    if expect_ok and proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        raise SystemExit("command failed: %s" % " ".join(args))
    if not expect_ok and proc.returncode == 0:
        print(proc.stdout)
        raise SystemExit("command unexpectedly passed: %s" % " ".join(args))
    return proc


def controller(root, *args, expect_ok=True):
    return run([sys.executable, CONTROLLER, *args, "--root", root], expect_ok=expect_ok)


def bind_no_knowledge_base(root):
    return controller(
        root,
        "knowledge",
        "bind",
        "--none",
        "--reason",
        "Smoke test confirms no external knowledge base is used.",
        "--confirm",
        "--by",
        "smoke",
    )


def copy_template(stage, root, target):
    src = os.path.join(SKILL_DIR, "stages", stage, "template.md")
    os.makedirs(os.path.dirname(os.path.join(root, target)) or root, exist_ok=True)
    shutil.copy2(src, os.path.join(root, target))


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_requirement_analysis(root, path="requirement_analysis.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# Requirement Analysis

- Project: Smoke
- Requirement: Smoke flow
- Analyst: smoke
- Date: 2026-07-16T00:00:00+08:00
- Input source: smoke test fixed input.
- Context citation conclusion: No external knowledge base; proceed from test input.

## 1. Original Request

- Original wording: Verify that pm-flow requires requirement analysis artifacts before advancing any stage.
- Source: local automated test.
- Related materials: context_confirmation.md, scenario-catalog.md, use-cases.md, end-to-end-flow.md, metrics-definition.md, artifact-plan.md.

## 2. Problem And Goal

- Is the original request a solution proposal? No.
- If yes, restated underlying problem: Not applicable.
- Problem to solve: Prevent agents from writing PRDs, prototypes, or review conclusions before understanding the requirement.
- Affected users or roles: product manager, business owner, agent using pm-flow-kit.
- Current pain: Short user requests can lead to outputs without scope, constraints, or acceptance lens.
- Impact if not solved: Stage gates cannot stop generic artifacts from advancing.
- Expected result: Every stage has requirement analysis, scenario catalog, and artifact plan before advancement.

## 3. Scope And Non-Scope

- Scope: Verify requirement analysis files, scenario catalog, and artifact plan exist and are confirmed.
- Non-scope: Do not verify real business PRD content quality.
- Client surfaces: No business frontend.
- Roles: product manager, business owner, agent.
- Dependencies: controller.py, validate.py, contract_config.json.

## 4. Confirmed Facts, Assumptions, And Open Questions

| Type | Content | Source | Handling |
|---|---|---|---|
| Confirmed fact | Global preflight is a required gate. | contract_config.json | Use as test fact. |
| Assumption | The smoke analysis content is enough for preflight. | smoke test | Use as test assumption. |
| Open question | None. | smoke test | No action. |

## 5. Requirement Analysis Level

- Level: A1 light clarification.
- Rationale: smoke test verifies gates and artifact presence only.
- PRD level recommendation: L1.

## 6. Assumptions And Risks

| Assumption or risk | Type | Impact | Confidence | Validation | Blocking |
|---|---|---|---|---|---|
| Global artifact gates can prevent generic output. | Deliverability | High | High | smoke test | No |

## 7. Success Criteria And Acceptance Lens

- Business success criteria: stage confirm fails before requirement analysis is confirmed.
- User success criteria: existing stage flow still passes after requirement analysis is confirmed.
- Primary metric: percentage of stage advancement attempts correctly blocked before preflight.
- Input metrics: number of confirmed first-circle artifacts.
- Guardrail metrics: zero downstream artifacts accepted before required preflight is confirmed.
- Observable acceptance lens: smoke test passes.
- Failure or exception lens: missing preflight artifacts or unconfirmed status fails validation.

## 8. Artifact Routing

| Artifact | Needed | Reason | Output path |
|---|---|---|---|
| Metrics definition | Yes | Verify metrics definition is part of first-circle preflight. | metrics-definition.md |
| Scenario catalog | Yes | Verify scenario coverage is part of first-circle preflight. | scenario-catalog.md |
| Use cases | Yes | Verify use case coverage is part of first-circle preflight. | use-cases.md |
| End-to-end flow | Yes | Verify flow coverage is part of first-circle preflight. | end-to-end-flow.md |
| PRD | Yes | Verify PRD stage artifact. | prd.md |
| Field dictionary | No | No fields in this test. | Not applicable |
| HTML prototype | Depends | iteration path requires it; micro and iteration-lite do not. | prototypes/*.html |
| Prototype review artifact | No | This test verifies review.md only. | Not applicable |
| Mermaid diagram | No | No complex branch in this test. | Not applicable |
| Test scenarios | No | Covered by smoke_test.py. | Not applicable |
| Delivery check | No | No code shipping in this test. | Not applicable |

## 9. Deferred Or Non-Applicable Decisions

- Artifacts explicitly not needed: Field dictionary, Mermaid diagram, test scenarios, and delivery check are not needed for this smoke test beyond automated test code.
- Technical stack constraints that are confirmed: Python controller only.
- Technical stack choices deferred because they do not affect the product boundary yet: frontend, backend, database, deployment.
- Export, review, or delivery artifacts deferred: export and delivery artifacts are not needed.

## 10. Source Error Check

- Source errors found: No.
- Highest severity: none.
- Error location: none.
- Correction conclusion: No source error found.
- Blocks downstream output: No.
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_scenario_catalog(root, path="scenario-catalog.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# Scenario Catalog

- Project: Smoke
- Requirement: Smoke flow
- Version: smoke
- Note: This file verifies the scenario catalog as shared input for PRD, prototype, and test work.

## Scenario Overview

| Scenario ID | Name | Role | Client surface | Priority | In scope |
|---|---|---|---|---|---|
| SCN-001 | Advance stage gate | Agent | CLI | High | Yes |

## Scenario Details

### SCN-001 Advance stage gate

- Role: Agent.
- Client surface: CLI.
- Trigger: any stage is confirmed, marked, or closed.
- Preconditions: .pm-flow/state.json has been initialized.
- User action: run controller.py confirm, mark, or close.
- System response: check whether context_confirmation.md, requirement_analysis.md, scenario-catalog.md, use-cases.md, end-to-end-flow.md, metrics-definition.md, and artifact-plan.md exist and are confirmed.
- Page or module: none.
- Fields: state.requirement_analysis.status, state.context.confirmation.status.
- Data source: .pm-flow/state.json and artifact files.
- Post-condition: advance stage when valid; return an error when invalid.
- State change: todo -> confirmed -> done -> closed.
- Permission: none.
- Exception cases: any missing or unconfirmed preflight artifact.
- Acceptance lens: smoke test fails before preflight and passes after preflight.
- Prototype coverage needed: no.
- Diagram coverage needed: no.
- Test scenario coverage needed: yes.

## Exception Scenarios

| Exception ID | Related scenario | Trigger | System behavior | User action | Acceptance lens |
|---|---|---|---|---|---|
| EX-001 | SCN-001 | Missing requirement analysis artifact | Block stage advancement | Complete and confirm artifacts | Command fails |

## Coverage Check

- [x] Every key role has a scenario.
- [x] Every relevant client surface has a scenario.
- [x] Every prototype-needed scenario names a page or module.
- [x] Every key field can be traced to a scenario.
- [x] Every state change has a precondition and post-condition.
- [x] Every exception has an acceptance lens.
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_use_cases(root, path="use-cases.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# Use Cases

## Use Case Index

| Use Case ID | Name | Actor | Goal | Related scenarios | Priority | In scope |
|---|---|---|---|---|---|---|
| UC-001 | Gate stage advancement | Agent | Advance only after required preflight exists | SCN-001 | High | Yes |

## UC-001 Gate stage advancement

- Actor: Agent.
- Goal: Advance a workflow stage only after required artifacts are present and confirmed.
- Client surface: CLI.
- Preconditions: .pm-flow/state.json exists; context confirmation and analysis bundle are available.
- Trigger: Agent runs confirm, mark, close, or validate.
- Main flow:
  1. Agent checks current stage status.
  2. Controller checks context confirmation.
  3. Controller checks requirement analysis bundle artifacts.
  4. Controller advances only when required files exist and analysis is confirmed.
- Alternate flow: If the current stage is skipped, the controller rejects advancement for that stage.
- Exception flow: If a required artifact is missing, the controller returns an error and keeps state unchanged.
- Post-condition: Stage status changes only after preflight is valid.
- Fields involved: requirement_analysis.status, context.confirmation.status, stages[*].status.
- Data source: .pm-flow/state.json and first-circle artifact files.
- Permission or policy: no special permission.
- Related metrics: MET-001, MET-002, MET-003.
- Acceptance lens: missing first-circle artifacts block advancement; completed artifacts allow advancement.
- Related PRD requirements: smoke PRD.
- Prototype coverage needed: no.

## Coverage Check

- [x] Every high-priority scenario maps to at least one use case.
- [x] Every use case has actor, goal, precondition, trigger, main flow, exception flow, and post-condition.
- [x] Every use case has an acceptance lens.
- [x] Fields and data sources can be traced to use cases.
- [x] Metrics affected by a use case are listed or marked not applicable.
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_end_to_end_flow(root, path="end-to-end-flow.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# End-To-End Flow

## 1. Flow Scope

- Requirement: Smoke flow.
- Flow owner: pm-flow controller.
- Start event: Agent starts a product workflow.
- End state: All path stages are closed.
- In-scope actors: Agent, product owner.
- In-scope systems: controller.py, validate.py, .pm-flow/state.json.
- Out-of-scope branches: real business delivery and production deployment.

## 2. Flow Summary

| Step | Actor or system | Client surface | Action | System response | State change | Data touched | Exception |
|---|---|---|---|---|---|---|---|
| 1 | Agent | CLI | init workflow | create state file | none -> todo | state.json | existing state blocks without force |
| 2 | Agent | CLI | confirm context | record context confirmation | context todo -> confirmed | context_confirmation.md | missing content blocks confirmation |
| 3 | Agent | CLI | confirm analysis bundle | record analysis confirmation | analysis todo -> confirmed | requirement_analysis.md and bundle | missing artifact blocks confirmation |
| 4 | Agent | CLI | advance stage | mark stage done and closed | todo -> confirmed -> done -> closed | stage artifacts | missing required artifact blocks advancement |

## 3. Decision Branches

| Branch ID | Decision point | Condition | Yes path | No path | Owner | Acceptance lens |
|---|---|---|---|---|---|---|
| BR-001 | Is first-circle preflight confirmed? | context and analysis bundle confirmed | allow stage advance | block and return error | controller | smoke test confirms both outcomes |

## 4. Handoffs

| From | To | Trigger | Payload or field set | SLA or timing | Failure behavior |
|---|---|---|---|---|---|
| Agent | Controller | command execution | root, stage, state | immediate | command exits non-zero |
| Controller | Validator | validate command | state and artifacts | immediate | validation reports errors |

## 5. Diagram Routing

- Standalone Mermaid diagram needed: no.
- Diagram type: not applicable.
- Default path: product/04-diagrams/main-flow.mmd.
- Non-applicability reason: this smoke test covers controller gates, not business flow visualization.

## 6. Coverage Check

- [x] Start and end are explicit.
- [x] Every actor and system handoff is named.
- [x] Branch conditions are explicit.
- [x] State changes and data touched are visible.
- [x] Exception paths are not summarized as generic error handling.
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_metrics_definition(root, path="metrics-definition.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# Metrics Definition

## 1. Metric Context

- Requirement: Smoke flow.
- Related requirement analysis: requirement_analysis.md.
- Related scenario catalog: scenario-catalog.md.
- Metric owner: product owner.
- Data owner: workflow owner.

## 2. Objectives

- Business objective: prevent uncontrolled downstream output before first-circle analysis is complete.
- User behavior objective: agent completes context and analysis bundle before PRD, prototype, or review work.
- Operational or compliance objective: no stage advancement before required artifacts exist.
- Non-applicable objective types and reasons: revenue and growth metrics are not applicable to this smoke test.

## 3. Metrics

| Metric ID | Name | Type | Formula | Unit | Baseline | Target or threshold | Data source | Owner |
|---|---|---|---|---|---|---|---|---|
| MET-001 | Correct preflight blocking rate | Primary success | blocked invalid advances / invalid advance attempts | percentage | unknown | 100% | smoke_test.py output | workflow owner |
| MET-002 | Confirmed first-circle artifact count | Input metric | count of confirmed first-circle artifacts | count | unknown | 7 | project files | workflow owner |
| MET-003 | False successful downstream advances | Guardrail metric | invalid advances accepted | count | unknown | 0 | controller output | workflow owner |

## 4. Collection And Interpretation

- Collection point: smoke test command output.
- Event or table source: smoke_test.py and controller.py exit codes.
- Attribution window: one test run.
- Segment cuts: default, context root, iteration-lite, mapped config.
- Reporting cadence: every plugin validation run.
- Decision rule: ship only when all smoke scenarios pass without warnings.
- Diagnostic checks before claiming impact:
  - Data quality: command exit codes and generated files are checked directly.
  - Cohort or segment cuts: default, context root, iteration-lite, mapped config.
  - Channel or version cuts: not applicable to smoke tests.
  - Seasonality or external events: not applicable to smoke tests.

## 5. Measurement Risks

| Risk | Impact | Handling |
|---|---|---|
| Smoke test verifies structure but not real product judgment | Medium | Forward-test real tasks separately |

## 6. Coverage Check

- [x] The primary metric measures an outcome, not just feature delivery.
- [x] Input metrics explain what user behavior should change.
- [x] Guardrail metrics protect quality, risk, cost, or compliance.
- [x] Unknown baselines are marked instead of invented.
- [x] Every metric has a source or an explicit source gap.
- [x] Exposure, page view, and click-count metrics are not treated as value moments unless justified.
- [x] Impact claims require data-quality, cohort, channel, version, segment, seasonality, or attribution checks.
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_artifact_plan(root, path="artifact-plan.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# Artifact Plan

- Project: Smoke
- Requirement: Smoke flow
- Directory standard source: pm-flow-kit built-in standard.
- Note: This file records artifacts required by this test.

## Artifact List

| Artifact | Needed | Default path | Actual path | Rationale | Non-applicability reason | Status |
|---|---|---|---|---|---|---|
| context_confirmation.md | Yes | context_confirmation.md | context_confirmation.md | Context intake | Not applicable | Done |
| requirement_analysis.md | Yes | requirement_analysis.md | requirement_analysis.md | Requirement analysis | Not applicable | Done |
| scenario-catalog.md | Yes | scenario-catalog.md | scenario-catalog.md | Scenario coverage input | Not applicable | Done |
| use-cases.md | Yes | use-cases.md | use-cases.md | Use case coverage input | Not applicable | Done |
| end-to-end-flow.md | Yes | end-to-end-flow.md | end-to-end-flow.md | End-to-end flow input | Not applicable | Done |
| metrics-definition.md | Yes | metrics-definition.md | metrics-definition.md | Success and guardrail metrics | Not applicable | Done |
| artifact-plan.md | Yes | artifact-plan.md | artifact-plan.md | Artifact management | Not applicable | Done |
| research.md | Depends | research.md | research.md | new-platform path verification | iteration, iteration-lite, and micro do not need it | Pending |
| boundary.md | Depends | boundary.md | boundary.md | boundary stage verification | micro does not need it | Pending |
| prd.md | Yes | prd.md | prd.md | PRD stage verification | Not applicable | Pending |
| prototypes/ | Depends | prototypes/ | prototypes/ | iteration path verification | micro/iteration-lite do not need it | Pending |
| review.md | Yes | review.md | review.md | review stage verification | Not applicable | Pending |

## Workspace Standard Gap

- Workspace-defined directories: none.
- Artifact types not covered but needed here: all use built-in default paths.
- Built-in default directories used: project-root defaults.

## Deferred Or Non-Applicable Decisions

- Unneeded artifacts and reasons: field dictionary, diagrams, export, and delivery checks are not needed for controller gate verification.
- Technical stack choices that are known constraints: Python controller and local filesystem only.
- Technical stack choices deferred because they do not affect the product boundary yet: frontend, backend, database, deployment, and cloud provider.
- Review/export/delivery artifacts deferred or rejected: export and delivery artifacts are rejected for this smoke test.

## Next Artifact Order

1. research.md when the current path includes research.
2. boundary.md when the current path includes boundary.
3. prototypes/ when the current path includes prototype.
4. prd.md
5. review.md
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_analysis_bundle(root, requirement_path="requirement_analysis.md",
                          scenario_path="scenario-catalog.md",
                          use_cases_path="use-cases.md",
                          flow_path="end-to-end-flow.md",
                          metrics_path="metrics-definition.md",
                          plan_path="artifact-plan.md"):
    write_requirement_analysis(root, requirement_path)
    write_scenario_catalog(root, scenario_path)
    write_use_cases(root, use_cases_path)
    write_end_to_end_flow(root, flow_path)
    write_metrics_definition(root, metrics_path)
    write_artifact_plan(root, plan_path)


def write_context_confirmation(root, path="context_confirmation.md", mode="none"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    if mode == "root":
        source_summary = "context / CONTEXT_MANIFEST.md / intake.md / context/core/glossary.md"
        no_context_reason = "Not applicable; this test provides a directory-style context root."
        applicable = "context/CONTEXT_MANIFEST.md, context/core/glossary.md"
    else:
        source_summary = "No external knowledge base; proceed from smoke test fixed input."
        no_context_reason = "This test does not provide an external knowledge base."
        applicable = "No external applicable source."
    content = """# Context Intake Confirmation

- Project: Smoke
- Requirement: Smoke flow
- Confirmed by: smoke
- Generated at: 2026-07-16T00:00:00+08:00

## 1. Context Mode

- Context mode: {mode}
- External knowledge base used: {use_kb}
- Reason if not used: {no_context_reason}

## 2. Knowledge-Base Entry Points

- Context root: {context_root}
- Manifest or index: {manifest}
- Intake: {intake}
- Other sources: {source_summary}

## 3. Applicable Sources

- Required sources: {applicable}
- Stage-specific sources: read by stage, not all at once.
- Applicable rules: MUST rules must be followed; FORBIDDEN rules must not be violated.
- Referenced design guidelines, component library, fonts, or frontend framework: not involved in this test.

## 4. Non-Applicable Sources

- Excluded sources: archived, sample, or unrelated sources.
- Reason: they do not affect smoke test gates.
- Archived or outdated materials: not used as facts.

## 5. Rule Strength And Conflicts

- MUST rules: stage advancement requires context confirmation and requirement analysis preflight.
- FORBIDDEN rules: do not read all context by default; do not write assumptions as facts.
- Conflicts: none.
- Resolution: no conflict; continue.

## 6. Citation Conclusion

- Is the context usable: usable.
- Preconditions for continuing: keep this confirmation; reconfirm if new knowledge-base sources are added.
- Sources that must be cited later: {applicable}
- Sources that must not be cited later: archived or unconfirmed sources.
""".format(
        mode=mode,
        use_kb="yes" if mode == "root" else "no",
        no_context_reason=no_context_reason,
        context_root="context" if mode == "root" else "None",
        manifest="context/CONTEXT_MANIFEST.md" if mode == "root" else "None",
        intake="intake.md" if mode == "root" else "None",
        source_summary=source_summary,
        applicable=applicable,
    )
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_research(root, path="research.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# Smoke Flow Research

## Context References

- Sources read for this stage: context_confirmation.md, requirement_analysis.md, metrics-definition.md.
- Applicable knowledge-base sources: none for the default smoke flow.
- Non-applicable sources: archived or unconfirmed materials.
- Conflicts found: none.
- Stage assumptions: smoke test input is enough to verify research-stage gates.

## Research Frame

- Research question: Can pm-flow-kit complete the new-platform research stage before boundary, prototype, PRD, and review?
- Opportunity: prevent agents from skipping early discovery context in larger product flows.
- Target users: product manager, business owner, agent using pm-flow-kit.
- Decision to support: whether the workflow can advance beyond research after minimum context is captured.
- Non-applicability reason for deeper market sizing: this smoke test validates workflow behavior, not market truth.

## Opportunity And User Context

| Area | Finding | Evidence | Confidence | Impact |
|---|---|---|---|---|
| Opportunity | Stage-specific research should exist before boundary decisions. | new-platform path includes research first. | High | High |
| User | Agents need explicit artifacts to avoid jumping to PRD. | controller gates require required artifacts. | High | High |
| Market | Not applicable to local controller smoke tests. | no external market data used. | High | Low |

## Competitor And Benchmark Notes

| Benchmark | Relevant behavior | Gap or lesson | Applicability |
|---|---|---|---|
| Structured stage-gate workflows | Early discovery artifacts precede scope decisions. | pm-flow should enforce the same sequence. | Applicable |
| Generic document generators | Can produce downstream docs without context. | pm-flow should block premature output. | Applicable |

## Metrics Context

- Primary metric reference: metrics-definition.md.
- Input metric reference: confirmed first-circle artifact count.
- Guardrail reference: zero invalid downstream advances.
- Metrics non-applicability: revenue and growth metrics are not applicable to this smoke test.

## Source Risk, Assumptions, And Open Questions

| Type | Item | Handling |
|---|---|---|
| Source risk | No external knowledge base is used. | Record the no-context reason and avoid invented facts. |
| Assumption | Local smoke content is enough for research-stage gate verification. | Accept for automated test only. |
| Open question | None for this smoke flow. | No action needed. |

## Research Conclusion

- Conclusion: research stage is complete enough to continue to boundary for a local smoke workflow.
- Carry-forward constraints: do not treat smoke findings as real market evidence.
- Downstream implication: boundary should define only the controller validation scope.

## Close Checklist

- [x] pm-research was used for research-stage analysis.
- [x] Opportunity, user, market, competitor, benchmark, and metric context are covered or marked not applicable.
- [x] Sources, exclusions, assumptions, risks, and open questions are explicit.
- [x] The output can support boundary-stage decisions.
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_boundary(root, path="boundary.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# Smoke Flow Boundary

## Context References

- Sources read for this stage: context_confirmation.md, requirement_analysis.md, scenario-catalog.md, use-cases.md, end-to-end-flow.md, research.md.
- Applicable rules: stage gates require completed artifacts before close.
- Conflicts found: none.
- Stage assumptions: this boundary applies only to local workflow validation.

## Boundary Summary

- Boundary decision: validate pm-flow stage gates and content checks only.
- In-scope outcome: completed artifacts allow progression through the selected path.
- Non-scope outcome: real production delivery, market sizing, and code shipping readiness are not covered.
- Primary user: agent using pm-flow-kit.
- Business owner: smoke test owner.

## Scope

| Item | In scope | Reason | Owner |
|---|---|---|---|
| Workspace binding | Yes | required before product work starts | controller |
| Knowledge-base binding | Yes | required before product work starts | controller |
| Stage artifacts | Yes | required for each stage gate | controller |
| PRD and review content checks | Yes | prevent empty templates from passing | validator |

## Non-Scope

| Item | Out of scope reason |
|---|---|
| Production app behavior | smoke test validates workflow only |
| Business-market analysis | no external market source is used |
| Real stakeholder approval | automated smoke test cannot replace human approval |

## Roles, Permissions, And Surfaces

- Roles: product owner, agent, workflow owner.
- Permissions: local filesystem access to the project workspace.
- Client surfaces: command line controller and generated markdown artifacts.
- System ownership: pm-flow owns `.pm-flow/state.json`; project owners own business artifacts.

## Constraints, Dependencies, And Risks

| Type | Item | Impact | Handling |
|---|---|---|---|
| Constraint | Workspace and knowledge-base binding must be confirmed. | High | status blocks until confirmed. |
| Dependency | context_confirmation.md and analysis bundle. | High | analyze must be confirmed first. |
| Risk | Structural checks are not deep semantic judgment. | Medium | require --checked human review at close. |

## Decisions

- Decision: the smoke boundary is limited to workflow and artifact validation.
- Decision: prototype review artifacts are not required unless the artifact plan asks for them.
- Decision: empty PRD and review templates must fail downstream gates.

## Close Checklist

- [x] pm-boundary was used for boundary-stage definition.
- [x] Scope and non-scope are explicit.
- [x] Roles, permissions, client surfaces, and system ownership are explicit.
- [x] Constraints, dependencies, assumptions, and risks are listed.
- [x] Decisions are clear enough for prototype, PRD, and review stages.
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_prd(root, path="prd.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# Smoke Flow PRD

## Context References

- Sources read for this stage: context_confirmation.md, requirement_analysis.md, scenario-catalog.md, use-cases.md, end-to-end-flow.md, metrics-definition.md.
- Applicable rules: first-circle analysis must be confirmed before downstream output.
- Conflicts found: none.
- Stage assumptions: smoke test inputs represent a low-risk controller workflow.
- No-context reason, if applicable: no external knowledge base is used for the default smoke flow.

## PRD Level Decision

- PRD level: L1
- Decision rationale:
  - Scope: verify controller gates for PRD stage advancement.
  - Affected roles and client surfaces: agent using the CLI.
  - State, permission, money, inventory, fulfillment, or data impact: state.json only.
  - Cross-system or cross-team impact: none.
  - Risk and uncertainty: low; checks are local filesystem checks.
- Template selected: l1-light-prd.md.

## Requirement Summary

- Background: pm-flow must not close downstream stages from empty artifacts.
- Goal: block incomplete PRD artifacts while allowing completed smoke PRDs.
- Scope: PRD stage validation for required content, artifact references, and acceptance criteria.
- Explicit non-scope: no production app, UI, or deployment behavior.
- Success criteria: empty PRD template fails; this completed PRD passes mark, close, and validate.
- Metrics referenced: metrics-definition.md.
- Scenario catalog referenced: scenario-catalog.md.
- Use cases referenced: use-cases.md.
- End-to-end flow referenced: end-to-end-flow.md.

## PRD Body

### 1. Summary

- Requirement: gate PRD stage content.
- Problem: file-only gates allow empty PRD templates to pass.
- Goal: require minimum completed PRD content.
- Metrics or non-applicability reason: metrics-definition.md defines smoke metrics.

### 2. Scope

- In scope: stage content validation for prd.md.
- Out of scope: deep semantic judgment of business quality.

### 3. Requirement

- User: agent using pm-flow-kit.
- Scenario: agent marks or closes the PRD stage.
- Use case: UC-001 Gate stage advancement.
- Rule: PRD stage artifact must contain explicit level, scope, acceptance criteria, and evidence references.
- Expected behavior: completed PRD passes; empty template fails.

### 4. Acceptance Criteria

- Given prd.md is an untouched template, when mark prd is run, then the command fails.
- Given prd.md contains this completed L1 content, when mark prd and close prd are run, then both commands succeed.
- Given validate is run after PRD is done or closed, then validator reports no PRD content errors.

### 5. Risks And Open Questions

- Risks: rules are structural and cannot replace human review.
- Open questions: none.
- Non-applicability notes: field dictionary and Mermaid diagrams are not applicable to this smoke PRD.

## Key Decisions

- Decision: smoke PRD uses L1 because the change is local to workflow validation.

## Close Checklist

- [x] pm-prd was used for PRD sizing and template selection.
- [x] PRD level and rationale are explicit.
- [x] The PRD satisfies the required sections for its level.
- [x] Terminology and roles are aligned to project sources when they exist.
- [x] Client surfaces and system ownership are explicit.
- [x] Metrics definition, scenario catalog, use cases, and end-to-end flow are referenced or marked not applicable.
- [x] Acceptance criteria and exception flows are included.
- [x] Required diagrams, field dictionary, and acceptance criteria are produced as companion artifacts or marked not applicable.
- [x] Open questions are not written as facts.
- [x] Key decisions are recorded in state.json.decisions.
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def write_review(root, path="review.md"):
    target = os.path.join(root, path)
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    content = """# Smoke Flow Review Notes

## Context References

- Sources read for this stage: requirement_analysis.md, scenario-catalog.md, use-cases.md, end-to-end-flow.md, metrics-definition.md, prd.md.
- Applicable rules: findings must be closed or explicitly recorded as unresolved.
- Conflicts found: none.
- Stage assumptions: review checks workflow gating, not production behavior.
- No-context reason, if applicable: no external knowledge base is used for this smoke flow.

## Independent Review

- Reviewer: smoke independent reviewer.
- Review checklist: reviews/review-audit.md.
- Review dimensions: product logic, feasibility, UX, terminology, artifact completeness.

## Findings And Resolution

| # | Finding | Severity | Resolution | Status |
|---|---|---|---|---|
| 1 | No blocking issue found in the smoke PRD and stage artifacts. | Low | Closed after smoke test verification. | Closed |

## Decision Check

- Are state.json.decisions complete? yes.
- Missing decisions: none.

## Conclusion

- Overall conclusion: Ready
- Remaining open issues: none.

## Close Checklist

- [x] Independent review was performed.
- [x] Findings are closed or explicitly recorded.
- [x] Decision records are complete.
- [x] All previous stages are closed.
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


def assert_design_system_snapshot(root, marker=None):
    tokens = os.path.join(root, "prototypes", "assets", "design-system", "tokens.css")
    if not os.path.isfile(tokens):
        raise SystemExit("prototype design-system/tokens.css was not generated")
    with open(tokens, encoding="utf-8") as f:
        content = f.read()
    if "--color-primary" not in content:
        raise SystemExit("prototype design-system/tokens.css is missing --color-primary")
    if marker and marker not in content:
        raise SystemExit("prototype design-system snapshot did not use project override")


def test_new_platform_flow():
    root = tempfile.mkdtemp(prefix="pm-flow-new-platform-")
    try:
        controller(root, "init", "new-platform", "--project", "Smoke", "--requirement",
                   "New platform flow", "--force")
        bind_no_knowledge_base(root)
        write_context_confirmation(root)
        controller(root, "context", "confirm", "--confirm", "--by", "smoke")
        write_analysis_bundle(root)
        controller(root, "analyze", "--confirm", "--by", "smoke")

        write_research(root, "research.md")
        controller(root, "confirm", "research", "--by", "smoke")
        controller(root, "mark", "research")
        controller(root, "close", "research", "--checked", "--by", "smoke")

        write_boundary(root, "boundary.md")
        controller(root, "confirm", "boundary", "--by", "smoke")
        controller(root, "mark", "boundary")
        controller(root, "close", "boundary", "--checked", "--by", "smoke")

        controller(root, "scaffold", "--name", "Smoke")
        assert_design_system_snapshot(root)
        run([sys.executable, os.path.join(root, "prototypes", "assets", "validate_prototype.py")], cwd=root)
        controller(root, "confirm", "prototype", "--by", "smoke")
        controller(root, "mark", "prototype")
        controller(root, "close", "prototype", "--checked", "--by", "smoke")

        write_prd(root, "prd.md")
        controller(root, "confirm", "prd", "--by", "smoke")
        controller(root, "decide", "prd", "--text", "New platform smoke decision", "--by", "smoke")
        controller(root, "mark", "prd")
        controller(root, "close", "prd", "--checked", "--by", "smoke")

        write_review(root, "review.md")
        controller(root, "confirm", "review", "--by", "smoke")
        controller(root, "mark", "review")
        controller(root, "close", "review", "--checked", "--by", "smoke")
        controller(root, "validate")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_default_flow():
    root = tempfile.mkdtemp(prefix="pm-flow-smoke-")
    try:
        controller(root, "init", "iteration", "--project", "Smoke", "--requirement", "Default flow", "--force")
        config = read_json(os.path.join(root, ".pm-flow", "project_config.json"))
        if config.get("workspace", {}).get("realpath") != os.path.realpath(os.path.abspath(root)):
            raise SystemExit("workspace binding was not initialized")
        if config.get("knowledge_base", {}).get("status") != "unconfirmed":
            raise SystemExit("knowledge base should require explicit confirmation when no context is provided")
        if config.get("workspace", {}).get("plugin_workdir") != ".pm-flow/work":
            raise SystemExit("workspace plugin workdir should default to .pm-flow/work")
        if not os.path.isdir(os.path.join(root, ".pm-flow", "work")):
            raise SystemExit("workspace plugin workdir was not created")
        controller(root, "status", expect_ok=False)
        bind_no_knowledge_base(root)
        kb_status = controller(root, "knowledge", "status", "--json")
        kb_payload = json.loads(kb_status.stdout)
        if kb_payload.get("mode") != "none" or kb_payload.get("mismatch") is not None:
            raise SystemExit("knowledge-base none binding failed")
        status = controller(root, "workspace", "status", "--json")
        status_payload = json.loads(status.stdout)
        if status_payload.get("mismatch") is not None:
            raise SystemExit("workspace status unexpectedly reports mismatch")
        controller(root, "scaffold", "--name", "Smoke")
        assert_design_system_snapshot(root)
        run([sys.executable, os.path.join(root, "prototypes", "assets", "validate_prototype.py")], cwd=root)
        controller(root, "validate")
        controller(root, "confirm", "boundary", "--by", "smoke", expect_ok=False)
        write_analysis_bundle(root)
        controller(root, "analyze", "--confirm", "--by", "smoke", expect_ok=False)
        write_context_confirmation(root)
        controller(root, "context", "confirm", "--confirm", "--by", "smoke")
        controller(root, "analyze", "--confirm", "--by", "smoke")

        write_boundary(root, "boundary.md")
        controller(root, "confirm", "boundary", "--by", "smoke")
        controller(root, "mark", "boundary")
        controller(root, "close", "boundary", expect_ok=False)
        controller(root, "close", "boundary", "--checked", "--by", "smoke")

        controller(root, "confirm", "prototype", "--by", "smoke")
        controller(root, "mark", "prototype")
        controller(root, "validate")
        controller(root, "close", "prototype", "--checked", "--by", "smoke")

        copy_template("prd", root, "prd.md")
        controller(root, "confirm", "prd", "--by", "smoke")
        controller(root, "decide", "prd", "--text", "Smoke test decision", "--by", "smoke")
        controller(root, "mark", "prd", expect_ok=False)
        controller(root, "validate", expect_ok=False)
        write_prd(root, "prd.md")
        controller(root, "mark", "prd")
        controller(root, "close", "prd", "--checked", "--by", "smoke")

        copy_template("review", root, "review.md")
        controller(root, "review", "review")
        controller(root, "confirm", "review", "--by", "smoke")
        controller(root, "mark", "review", expect_ok=False)
        controller(root, "validate", expect_ok=False)
        write_review(root, "review.md")
        controller(root, "mark", "review")
        controller(root, "close", "review", "--checked", "--by", "smoke")
        final_validation = controller(root, "validate")
        if "Warning:" in final_validation.stdout:
            print(final_validation.stdout)
            raise SystemExit("final validation emitted warnings")

        print("pm-flow smoke test passed")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_workspace_rebind():
    root = tempfile.mkdtemp(prefix="pm-flow-workspace-")
    try:
        controller(root, "init", "micro", "--project", "Smoke", "--requirement", "Workspace binding", "--force")
        bind_no_knowledge_base(root)
        config_path = os.path.join(root, ".pm-flow", "project_config.json")
        config = read_json(config_path)
        config["workspace"]["realpath"] = "/tmp/pm-flow-old-workspace"
        config["workspace"]["root"] = "/tmp/pm-flow-old-workspace"
        write_json(config_path, config)
        controller(root, "status", expect_ok=False)
        controller(root, "workspace", "status", "--json")
        controller(root, "workspace", "rebind", "--confirm", "--by", "smoke")
        rebound = read_json(config_path)
        if rebound.get("workspace", {}).get("realpath") != os.path.realpath(os.path.abspath(root)):
            raise SystemExit("workspace rebind did not update realpath")
        controller(root, "status")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_knowledge_rebind():
    root = tempfile.mkdtemp(prefix="pm-flow-knowledge-")
    try:
        knowledge_root = os.path.join(root, "knowledge")
        os.makedirs(knowledge_root, exist_ok=True)
        with open(os.path.join(knowledge_root, "CONTEXT_MANIFEST.md"), "w", encoding="utf-8") as f:
            f.write("# Context Manifest\n")
        controller(root, "init", "micro", "--project", "Smoke", "--requirement", "Knowledge binding",
                   "--context-root", "knowledge", "--force")
        config_path = os.path.join(root, ".pm-flow", "project_config.json")
        config = read_json(config_path)
        config["knowledge_base"]["realpath"] = "/tmp/pm-flow-old-knowledge"
        write_json(config_path, config)
        controller(root, "status", expect_ok=False)
        controller(root, "knowledge", "status", "--json")
        controller(root, "knowledge", "rebind", "--knowledge-root", knowledge_root, "--confirm", "--by", "smoke")
        rebound = read_json(config_path)
        if rebound.get("knowledge_base", {}).get("realpath") != os.path.realpath(os.path.abspath(knowledge_root)):
            raise SystemExit("knowledge rebind did not update realpath")
        controller(root, "status")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_knowledge_bind_boundary_change_requires_rebind():
    root = tempfile.mkdtemp(prefix="pm-flow-knowledge-boundary-")
    try:
        knowledge_root = os.path.join(root, "knowledge")
        os.makedirs(knowledge_root, exist_ok=True)
        with open(os.path.join(knowledge_root, "CONTEXT_MANIFEST.md"), "w", encoding="utf-8") as f:
            f.write("# Context Manifest\n")
        with open(os.path.join(knowledge_root, "INDEX.md"), "w", encoding="utf-8") as f:
            f.write("# Alternate Index\n")
        with open(os.path.join(knowledge_root, "source-a.md"), "w", encoding="utf-8") as f:
            f.write("# Source A\n")

        controller(root, "init", "micro", "--project", "Smoke", "--requirement", "Knowledge boundary",
                   "--context-root", "knowledge", "--force")
        controller(root, "knowledge", "bind", "--knowledge-root", "knowledge",
                   "--manifest", "INDEX.md", "--confirm", "--by", "smoke", expect_ok=False)
        controller(root, "knowledge", "rebind", "--knowledge-root", "knowledge",
                   "--manifest", "INDEX.md", "--confirm", "--by", "smoke")
        rebound = json.loads(controller(root, "knowledge", "status", "--json").stdout)
        if not rebound.get("manifest", "").endswith("INDEX.md"):
            raise SystemExit("knowledge rebind did not update manifest")

        controller(root, "knowledge", "bind", "--knowledge-root", "knowledge",
                   "--manifest", "INDEX.md", "--source", "source-a.md",
                   "--confirm", "--by", "smoke", expect_ok=False)

        none_root = tempfile.mkdtemp(prefix="pm-flow-knowledge-none-")
        try:
            controller(none_root, "init", "micro", "--project", "Smoke", "--requirement", "No KB",
                       "--force")
            bind_no_knowledge_base(none_root)
            controller(none_root, "knowledge", "bind", "--none", "--reason",
                       "Different no-knowledge-base reason.", "--confirm", "--by", "smoke",
                       expect_ok=False)
        finally:
            shutil.rmtree(none_root, ignore_errors=True)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_context_root():
    root = tempfile.mkdtemp(prefix="pm-flow-context-")
    try:
        context_root = os.path.join(root, "context")
        os.makedirs(os.path.join(context_root, "core"), exist_ok=True)
        with open(os.path.join(context_root, "CONTEXT_MANIFEST.md"), "w", encoding="utf-8") as f:
            f.write("# Context Manifest\n\n## Required Files\n- `core/glossary.md`\n")
        with open(os.path.join(context_root, "core", "glossary.md"), "w", encoding="utf-8") as f:
            f.write("# Glossary\n")
        with open(os.path.join(root, "intake.md"), "w", encoding="utf-8") as f:
            f.write("# Intake\n")

        controller(root, "init", "micro", "--project", "Smoke", "--requirement", "Context flow",
                   "--context-root", "context", "--intake", "intake.md", "--force")
        kb_payload = json.loads(controller(root, "knowledge", "status", "--json").stdout)
        if kb_payload.get("mode") != "root" or kb_payload.get("mismatch") is not None:
            raise SystemExit("context-root init did not bind a valid knowledge base")
        controller(root, "context", "validate")
        controller(root, "status", "--json")
        write_context_confirmation(root, mode="root")
        controller(root, "context", "confirm", "--confirm", "--by", "smoke")
        write_analysis_bundle(root)
        controller(root, "analyze", "--confirm", "--by", "smoke")
        write_prd(root, "prd.md")
        controller(root, "confirm", "prd", "--by", "smoke")
        controller(root, "decide", "prd", "--text", "Context smoke decision", "--by", "smoke")
        controller(root, "mark", "prd")
        controller(root, "close", "prd", "--checked", "--by", "smoke")
        write_review(root, "review.md")
        controller(root, "confirm", "review", "--by", "smoke")
        controller(root, "mark", "review")
        controller(root, "close", "review", "--checked", "--by", "smoke")
        controller(root, "validate")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_iteration_lite_flow():
    root = tempfile.mkdtemp(prefix="pm-flow-lite-")
    try:
        controller(root, "init", "iteration-lite", "--project", "Smoke", "--requirement", "Lite flow", "--force")
        bind_no_knowledge_base(root)
        write_context_confirmation(root)
        controller(root, "context", "confirm", "--confirm", "--by", "smoke")
        write_analysis_bundle(root)
        controller(root, "analyze", "--confirm", "--by", "smoke")
        write_boundary(root, "boundary.md")
        controller(root, "confirm", "boundary", "--by", "smoke")
        controller(root, "mark", "boundary")
        controller(root, "close", "boundary", "--checked", "--by", "smoke")
        write_prd(root, "prd.md")
        controller(root, "confirm", "prd", "--by", "smoke")
        controller(root, "decide", "prd", "--text", "Lite smoke decision", "--by", "smoke")
        controller(root, "mark", "prd")
        controller(root, "close", "prd", "--checked", "--by", "smoke")
        write_review(root, "review.md")
        controller(root, "confirm", "review", "--by", "smoke")
        controller(root, "mark", "review")
        controller(root, "close", "review", "--checked", "--by", "smoke")
        controller(root, "validate")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_project_config_mapping():
    root = tempfile.mkdtemp(prefix="pm-flow-config-")
    try:
        config_path = os.path.join(root, "project_config.json")
        write_json(config_path, {
            "artifacts": {
                "context_confirmation": "product/context-confirmation.md",
                "requirement_analysis": "product/requirement-analysis.md",
                "scenario_catalog": "product/scenario-catalog.md",
                "use_cases": "product/use-cases.md",
                "end_to_end_flow": "product/end-to-end-flow.md",
                "metrics_definition": "product/metrics-definition.md",
                "artifact_plan": "product/artifact-plan.md",
                "prd": "requirements/prd.md",
                "review": "docs/review.md"
            }
        })
        controller(root, "attach", "micro", "--project", "Smoke", "--requirement", "Mapped flow",
                   "--config", config_path, "--force")
        bind_no_knowledge_base(root)
        write_context_confirmation(root, "product/context-confirmation.md")
        controller(root, "context", "confirm", "--confirm", "--by", "smoke")
        write_analysis_bundle(root, "product/requirement-analysis.md",
                              "product/scenario-catalog.md",
                              "product/use-cases.md",
                              "product/end-to-end-flow.md",
                              "product/metrics-definition.md",
                              "product/artifact-plan.md")
        controller(root, "analyze", "--confirm", "--by", "smoke")
        write_prd(root, "requirements/prd.md")
        controller(root, "confirm", "prd", "--by", "smoke")
        controller(root, "decide", "prd", "--text", "Mapped smoke decision", "--by", "smoke")
        controller(root, "mark", "prd")
        controller(root, "close", "prd", "--checked", "--by", "smoke")
        write_review(root, "docs/review.md")
        controller(root, "confirm", "review", "--by", "smoke")
        controller(root, "mark", "review")
        controller(root, "close", "review", "--checked", "--by", "smoke")
        controller(root, "validate")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_project_design_system_override():
    root = tempfile.mkdtemp(prefix="pm-flow-design-system-")
    marker = "PROJECT_DESIGN_SYSTEM_MARKER"
    try:
        design_system = os.path.join(root, "design-system")
        os.makedirs(design_system, exist_ok=True)
        with open(os.path.join(design_system, "tokens.css"), "w", encoding="utf-8") as f:
            f.write("/* %s */\n" % marker)
            f.write(":root { --color-primary: #123456; --font-family: sans-serif; }\n")
        with open(os.path.join(design_system, "README.md"), "w", encoding="utf-8") as f:
            f.write("# Project Design System\n")

        controller(root, "init", "iteration", "--project", "Smoke", "--requirement",
                   "Project design-system override", "--force")
        bind_no_knowledge_base(root)
        controller(root, "scaffold", "--name", "Smoke")
        assert_design_system_snapshot(root, marker=marker)
        run([sys.executable, os.path.join(root, "prototypes", "assets", "validate_prototype.py")], cwd=root)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    assert_skill_assets()
    test_new_platform_flow()
    test_default_flow()
    test_workspace_rebind()
    test_knowledge_rebind()
    test_knowledge_bind_boundary_change_requires_rebind()
    test_context_root()
    test_iteration_lite_flow()
    test_project_config_mapping()
    test_project_design_system_override()
    print("pm-flow all smoke tests passed")


if __name__ == "__main__":
    main()
