#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pm-flow controller.

This script keeps a product requirement workflow in a durable state file.
It enforces context confirmation, requirement analysis, required artifacts,
semantic checks, and stage transitions.
"""

import argparse
import glob
import json
import os
import shutil
import sys
from datetime import datetime, timezone

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRACT = os.path.join(SKILL_DIR, "contract_config.json")
SCHEMA = os.path.join(SKILL_DIR, "shared", "state_schema.json")

STAGES_ALL = ["research", "boundary", "prototype", "prd", "review"]

# Requirement type -> stage path (skipped stages excluded)
PATH_BY_TYPE = {
    "new-platform": ["research", "boundary", "prototype", "prd", "review"],
    "iteration": ["boundary", "prototype", "prd", "review"],
    "iteration-lite": ["boundary", "prd", "review"],
    "micro": ["prd", "review"],
}

STATUS_FLOW = ["skipped", "todo", "confirmed", "done", "closed"]

REQUIREMENT_ANALYSIS_KEY = "requirement_analysis"
REQUIREMENT_ANALYSIS_DEFAULT_ARTIFACT = "requirement_analysis.md"
SCENARIO_CATALOG_KEY = "scenario_catalog"
SCENARIO_CATALOG_DEFAULT_ARTIFACT = "scenario-catalog.md"
USE_CASES_KEY = "use_cases"
USE_CASES_DEFAULT_ARTIFACT = "use-cases.md"
END_TO_END_FLOW_KEY = "end_to_end_flow"
END_TO_END_FLOW_DEFAULT_ARTIFACT = "end-to-end-flow.md"
METRICS_DEFINITION_KEY = "metrics_definition"
METRICS_DEFINITION_DEFAULT_ARTIFACT = "metrics-definition.md"
ARTIFACT_PLAN_KEY = "artifact_plan"
ARTIFACT_PLAN_DEFAULT_ARTIFACT = "artifact-plan.md"
CONTEXT_CONFIRMATION_KEY = "context_confirmation"
CONTEXT_CONFIRMATION_DEFAULT_ARTIFACT = "context_confirmation.md"
REQUIREMENT_ANALYSIS_REQUIRED_HEADINGS = [
    "## 1. Original Request",
    "## 2. Problem And Goal",
    "## 3. Scope And Non-Scope",
    "## 4. Confirmed Facts, Assumptions, And Open Questions",
    "## 5. Requirement Analysis Level",
    "## 6. Assumptions And Risks",
    "## 7. Success Criteria And Acceptance Lens",
    "## 8. Artifact Routing",
    "## 9. Deferred Or Non-Applicable Decisions",
    "## 10. Source Error Check",
]
REQUIREMENT_ANALYSIS_PLACEHOLDERS = (
    "To be completed", "TBD", "TODO", "Not filled"
)
CONTEXT_CONFIRMATION_REQUIRED_HEADINGS = [
    "## 1. Context Mode",
    "## 2. Knowledge-Base Entry Points",
    "## 3. Applicable Sources",
    "## 4. Non-Applicable Sources",
    "## 5. Rule Strength And Conflicts",
    "## 6. Citation Conclusion",
]


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def die(msg):
    print("✗ " + msg, file=sys.stderr)
    sys.exit(1)


def load_contract():
    if not os.path.isfile(CONTRACT):
        die("contract_config.json not found: %s" % CONTRACT)
    with open(CONTRACT, encoding="utf-8") as f:
        return json.load(f)


def global_preflight(contract):
    return contract.get("global_preflight", {})


def state_path(root):
    return os.path.join(root, ".pm-flow", "state.json")


def pmflow_dir(root):
    return os.path.join(root, ".pm-flow")


def project_config_path(root):
    return os.path.join(pmflow_dir(root), "project_config.json")


def load_json_file(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def resolve_project_path(root, path):
    if not path:
        return path
    if os.path.isabs(path):
        return path
    return os.path.join(root, path)


def load_state(root):
    p = state_path(root)
    if not os.path.isfile(p):
        die("state.json not found (%s). Run init first." % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f), p


def save_state(root, state):
    p = state_path(root)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")


def load_project_config(root):
    p = project_config_path(root)
    if not os.path.isfile(p):
        return {}
    return load_json_file(p)


def save_project_config(root, config):
    write_json_file(project_config_path(root), config)


# ---------------------------------------------------------------- workspace + knowledge-base binding
WORKSPACE_DEFAULT_WORKDIR = ".pm-flow/work"
KNOWLEDGE_BASE_DEFAULT_MODE = "unknown"


def canonical_root(root):
    return os.path.realpath(os.path.abspath(root))


def normalize_plugin_workdir(workdir):
    workdir = workdir or WORKSPACE_DEFAULT_WORKDIR
    if os.path.isabs(workdir):
        die("workspace.plugin_workdir must be relative to the workspace root: %s" % workdir)
    normalized = os.path.normpath(workdir)
    if normalized in (".", "") or normalized.startswith(".."):
        die("workspace.plugin_workdir must stay inside the workspace root: %s" % workdir)
    return normalized


def workspace_binding_payload(root, config):
    workspace = config.get("workspace") if isinstance(config.get("workspace"), dict) else {}
    return {
        "root": workspace.get("root"),
        "realpath": workspace.get("realpath"),
        "confirmed_at": workspace.get("confirmed_at"),
        "confirmed_by": workspace.get("confirmed_by"),
        "plugin_workdir": normalize_plugin_workdir(workspace.get("plugin_workdir")),
        "preserve_existing_structure": workspace.get("preserve_existing_structure", True),
        "stop_on_mismatch": workspace.get("stop_on_mismatch", True),
        "current_root": os.path.abspath(root),
        "current_realpath": canonical_root(root),
    }


def workspace_mismatch_reason(root, config):
    workspace = config.get("workspace") if isinstance(config.get("workspace"), dict) else None
    if not workspace:
        return "Workspace root is not confirmed. Ask the human for the workspace location, then run workspace bind --confirm."
    payload = workspace_binding_payload(root, config)
    expected = payload.get("realpath") or payload.get("root")
    if payload.get("stop_on_mismatch", True) and expected and expected != payload["current_realpath"]:
        return (
            "Workspace root changed. Bound root: %s; current root: %s. "
            "Stop and clarify the workspace structure, or run workspace rebind --confirm after human approval."
            % (expected, payload["current_realpath"])
        )
    return None


def ensure_workspace_workdir(root, config):
    workspace = workspace_binding_payload(root, config)
    workdir = workspace["plugin_workdir"]
    os.makedirs(resolve_project_path(root, workdir), exist_ok=True)


def bind_workspace_config(root, config, by="user", allow_change=False):
    existing = config.get("workspace") if isinstance(config.get("workspace"), dict) else None
    reason = workspace_mismatch_reason(root, config) if existing else None
    if reason and not allow_change:
        die(reason)
    workdir = normalize_plugin_workdir((existing or {}).get("plugin_workdir"))
    config["workspace"] = {
        "root": os.path.abspath(root),
        "realpath": canonical_root(root),
        "confirmed_at": now_iso(),
        "confirmed_by": by or "user",
        "plugin_workdir": workdir,
        "preserve_existing_structure": True,
        "stop_on_mismatch": True,
    }
    ensure_workspace_workdir(root, config)
    return config


def assert_workspace_current(root):
    config = load_project_config(root)
    reason = workspace_mismatch_reason(root, config)
    if reason:
        die(reason)


def default_knowledge_base():
    return {
        "status": "unconfirmed",
        "mode": KNOWLEDGE_BASE_DEFAULT_MODE,
        "root": None,
        "realpath": None,
        "manifest": None,
        "sources": [],
        "confirmed_at": None,
        "confirmed_by": None,
        "no_knowledge_base_reason": None,
        "stop_on_mismatch": True,
    }


def normalize_knowledge_base(config):
    out = default_knowledge_base()
    kb = config.get("knowledge_base") if isinstance(config.get("knowledge_base"), dict) else None
    if kb:
        out.update(kb)
    out["sources"] = as_list(out.get("sources"))
    if out.get("mode") not in ("unknown", "none", "root", "files"):
        out["mode"] = KNOWLEDGE_BASE_DEFAULT_MODE
    if out.get("status") != "confirmed":
        out["status"] = "unconfirmed"
    return out


def resolve_knowledge_root(root, knowledge_root):
    if not knowledge_root:
        return None
    if os.path.isabs(knowledge_root):
        return os.path.realpath(os.path.abspath(knowledge_root))
    return os.path.realpath(os.path.abspath(os.path.join(root, knowledge_root)))


def resolve_knowledge_path(project_root, kb, path):
    if not path:
        return path
    if os.path.isabs(path):
        return os.path.realpath(os.path.abspath(path))
    if kb.get("mode") == "root" and kb.get("root"):
        return os.path.realpath(os.path.abspath(os.path.join(kb["root"], path)))
    return os.path.realpath(os.path.abspath(os.path.join(project_root, path)))


def guess_knowledge_manifest_abs(knowledge_root):
    for name in ("CONTEXT_MANIFEST.md", "INDEX.md"):
        candidate = os.path.join(knowledge_root, name)
        if os.path.isfile(candidate):
            return os.path.realpath(candidate)
    return os.path.realpath(os.path.join(knowledge_root, "CONTEXT_MANIFEST.md"))


def make_unconfirmed_knowledge_base(config):
    if isinstance(config.get("knowledge_base"), dict):
        return config
    config["knowledge_base"] = default_knowledge_base()
    return config


def make_knowledge_base_none(reason, by):
    if not reason or not reason.strip():
        die("knowledge bind --none requires --reason so the agent records why no external knowledge base is used.")
    kb = default_knowledge_base()
    kb.update({
        "status": "confirmed",
        "mode": "none",
        "confirmed_at": now_iso(),
        "confirmed_by": by or "user",
        "no_knowledge_base_reason": reason.strip(),
    })
    return kb


def make_knowledge_base_root(project_root, knowledge_root, manifest=None, sources=None, by="user"):
    root_abs = resolve_knowledge_root(project_root, knowledge_root)
    if not root_abs or not os.path.isdir(root_abs):
        die("Knowledge-base root does not exist or is not a directory: %s. Ask the human to confirm the knowledge-base path." % knowledge_root)
    manifest_abs = resolve_knowledge_path(project_root, {"mode": "root", "root": root_abs}, manifest) if manifest else guess_knowledge_manifest_abs(root_abs)
    if not os.path.isfile(manifest_abs):
        die("Knowledge-base manifest is missing: %s. Ask the human to confirm the knowledge-base path or provide --manifest." % manifest_abs)
    source_paths = []
    for src in as_list(sources):
        resolved = resolve_knowledge_path(project_root, {"mode": "root", "root": root_abs}, src)
        if not os.path.exists(resolved):
            die("Knowledge-base source does not exist: %s. Ask the human to confirm the knowledge-base path or source list." % resolved)
        source_paths.append(resolved)
    kb = default_knowledge_base()
    kb.update({
        "status": "confirmed",
        "mode": "root",
        "root": root_abs,
        "realpath": os.path.realpath(root_abs),
        "manifest": manifest_abs,
        "sources": list(dict.fromkeys([manifest_abs] + source_paths)),
        "confirmed_at": now_iso(),
        "confirmed_by": by or "user",
        "no_knowledge_base_reason": None,
        "stop_on_mismatch": True,
    })
    return kb


def make_knowledge_base_files(project_root, sources, by="user"):
    source_paths = []
    for src in as_list(sources):
        resolved = resolve_project_path(project_root, src)
        if not os.path.exists(resolved):
            die("Knowledge-base source file does not exist: %s. Ask the human to confirm the knowledge-base source list." % resolved)
        source_paths.append(os.path.realpath(os.path.abspath(resolved)))
    if not source_paths:
        die("knowledge bind --source requires at least one source file, or use --none with --reason.")
    kb = default_knowledge_base()
    kb.update({
        "status": "confirmed",
        "mode": "files",
        "sources": list(dict.fromkeys(source_paths)),
        "confirmed_at": now_iso(),
        "confirmed_by": by or "user",
        "stop_on_mismatch": True,
    })
    return kb


def knowledge_mismatch_reason(root, config):
    kb = normalize_knowledge_base(config)
    if kb.get("status") != "confirmed":
        return (
            "Knowledge-base path is not confirmed. Ask the human for the knowledge-base path, "
            "or confirm that no external knowledge base is used with knowledge bind --none --reason <reason> --confirm."
        )
    mode = kb.get("mode")
    if mode == "none":
        if not kb.get("no_knowledge_base_reason"):
            return "Knowledge base is marked as none without a reason. Stop and ask the human to confirm the context boundary."
        return None
    if mode == "root":
        root_path = kb.get("root")
        if not root_path:
            return "Knowledge-base mode is root, but root is missing. Stop and ask the human to confirm the knowledge-base path."
        current = resolve_knowledge_root(root, root_path)
        if not current or not os.path.isdir(current):
            return "Knowledge-base root is missing: %s. Stop and ask the human to confirm the knowledge-base path." % root_path
        expected = kb.get("realpath")
        if kb.get("stop_on_mismatch", True) and expected and expected != os.path.realpath(current):
            return (
                "Knowledge-base root changed. Bound root: %s; current root: %s. "
                "Stop and ask the human to confirm the knowledge-base path, or run knowledge rebind --confirm."
                % (expected, os.path.realpath(current))
            )
        manifest = kb.get("manifest")
        if not manifest:
            return "Knowledge-base manifest is missing from the binding. Stop and ask the human to confirm the entry point."
        if not os.path.isfile(resolve_knowledge_path(root, kb, manifest)):
            return "Knowledge-base manifest does not exist: %s. Stop and ask the human to confirm the knowledge-base path." % manifest
        for src in kb.get("sources", []):
            if src and not os.path.exists(resolve_knowledge_path(root, kb, src)):
                return "Knowledge-base source does not exist: %s. Stop and ask the human to confirm the source list." % src
        return None
    if mode == "files":
        if not kb.get("sources"):
            return "Knowledge-base mode is files, but sources are missing. Stop and ask the human to confirm the source list."
        for src in kb.get("sources", []):
            if src and not os.path.exists(resolve_knowledge_path(root, kb, src)):
                return "Knowledge-base source does not exist: %s. Stop and ask the human to confirm the source list." % src
        return None
    return "Knowledge-base mode is invalid or unconfirmed. Stop and ask the human to confirm the knowledge-base boundary."


def assert_knowledge_base_current(root):
    config = load_project_config(root)
    reason = knowledge_mismatch_reason(root, config)
    if reason:
        die(reason)


def context_from_knowledge_binding(ctx, kb):
    out = normalize_context(ctx)
    if kb.get("status") != "confirmed":
        return out
    if kb.get("mode") == "none":
        out["mode"] = "none"
        out["root"] = None
        out["manifest"] = None
        out["sources"] = []
    elif kb.get("mode") == "root":
        out["mode"] = "root"
        out["root"] = kb.get("root")
        out["manifest"] = kb.get("manifest")
        out["sources"] = list(dict.fromkeys([p for p in [kb.get("root"), kb.get("manifest")] + kb.get("sources", []) if p]))
    elif kb.get("mode") == "files":
        out["mode"] = "files"
        out["root"] = None
        out["manifest"] = None
        out["sources"] = list(dict.fromkeys(kb.get("sources", [])))
    return normalize_context(out)


def sync_state_context_from_knowledge(root, config):
    if not os.path.isfile(state_path(root)):
        return
    state, _ = load_state(root)
    state["context"] = context_from_knowledge_binding(
        state.get("context", {}),
        normalize_knowledge_base(config),
    )
    save_state(root, state)


def canonical_path_set(paths):
    return set(os.path.realpath(os.path.abspath(p)) for p in as_list(paths) if p)


def same_knowledge_base_binding(existing, requested):
    if existing.get("status") != requested.get("status"):
        return False
    if existing.get("mode") != requested.get("mode"):
        return False
    mode = existing.get("mode")
    if mode == "none":
        return existing.get("no_knowledge_base_reason") == requested.get("no_knowledge_base_reason")
    if mode == "root":
        return (
            existing.get("realpath") == requested.get("realpath")
            and canonical_path_set([existing.get("manifest")]) == canonical_path_set([requested.get("manifest")])
            and canonical_path_set(existing.get("sources", [])) == canonical_path_set(requested.get("sources", []))
        )
    if mode == "files":
        return canonical_path_set(existing.get("sources", [])) == canonical_path_set(requested.get("sources", []))
    return False


def bind_knowledge_base_config(root, config, args, allow_change=False):
    existing = normalize_knowledge_base(config)
    if getattr(args, "no_knowledge_base", False) and (
        getattr(args, "knowledge_root", None) or getattr(args, "manifest", None) or as_list(getattr(args, "source", None))
    ):
        die("knowledge bind --none cannot be combined with --knowledge-root, --manifest, or --source.")
    if getattr(args, "no_knowledge_base", False):
        requested = make_knowledge_base_none(getattr(args, "reason", None), getattr(args, "by", None))
    elif getattr(args, "knowledge_root", None):
        sources = as_list(getattr(args, "source", None))
        requested = make_knowledge_base_root(
            root,
            args.knowledge_root,
            manifest=getattr(args, "manifest", None),
            sources=sources,
            by=getattr(args, "by", None),
        )
    else:
        sources = as_list(getattr(args, "source", None))
        requested = make_knowledge_base_files(root, sources, by=getattr(args, "by", None))
    if existing.get("status") == "confirmed" and not allow_change:
        if not same_knowledge_base_binding(existing, requested):
            die("Knowledge base is already confirmed and the requested boundary differs. Use knowledge rebind --confirm after human approval to change root, manifest, sources, or no-knowledge-base reason.")
    config["knowledge_base"] = requested
    sync_state_context_from_knowledge(root, config)
    return config


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def default_requirement_analysis_state():
    return {
        "status": "todo",
        "artifact": REQUIREMENT_ANALYSIS_DEFAULT_ARTIFACT,
        "created_at": None,
        "confirmed_at": None,
        "confirmed_by": None,
    }


def default_context_confirmation_state():
    return {
        "status": "todo",
        "artifact": CONTEXT_CONFIRMATION_DEFAULT_ARTIFACT,
        "created_at": None,
        "confirmed_at": None,
        "confirmed_by": None,
    }


def requirement_analysis_state(state, root=None, contract=None):
    out = default_requirement_analysis_state()
    if isinstance(state.get(REQUIREMENT_ANALYSIS_KEY), dict):
        out.update(state.get(REQUIREMENT_ANALYSIS_KEY))
    if root:
        artifacts = effective_requirement_analysis_artifacts(root, contract)
        if artifacts and not out.get("artifact"):
            out["artifact"] = artifacts[0]
    if not out.get("artifact"):
        out["artifact"] = REQUIREMENT_ANALYSIS_DEFAULT_ARTIFACT
    return out


def context_confirmation_state(state, root=None):
    ctx = normalize_context(state.get("context", {}))
    out = default_context_confirmation_state()
    if isinstance(ctx.get("confirmation"), dict):
        out.update(ctx.get("confirmation"))
    if root:
        artifacts = effective_context_confirmation_artifacts(root)
        if artifacts and not out.get("artifact"):
            out["artifact"] = artifacts[0]
    if not out.get("artifact"):
        out["artifact"] = CONTEXT_CONFIRMATION_DEFAULT_ARTIFACT
    return out


def effective_required_artifacts(root, state, stage, contract=None):
    config = load_project_config(root)
    global_required = effective_requirement_analysis_artifacts(root, contract, config)
    mapped = config.get("artifacts", {}).get(stage)
    if mapped:
        stage_required = as_list(mapped)
    else:
        contract = contract or load_contract()
        stage_required = contract["stages"].get(stage, {}).get("required_artifacts", [])
    return list(dict.fromkeys(global_required + stage_required))


def effective_requirement_analysis_artifacts(root, contract=None, project_config=None):
    config = project_config if project_config is not None else load_project_config(root)
    contract = contract or load_contract()
    artifacts = global_preflight(contract).get(
        "required_artifacts", [REQUIREMENT_ANALYSIS_DEFAULT_ARTIFACT]
    )
    mapped_requirement = config.get("artifacts", {}).get(REQUIREMENT_ANALYSIS_KEY)
    mapped_scenario = config.get("artifacts", {}).get(SCENARIO_CATALOG_KEY)
    mapped_use_cases = config.get("artifacts", {}).get(USE_CASES_KEY)
    mapped_end_to_end_flow = config.get("artifacts", {}).get(END_TO_END_FLOW_KEY)
    mapped_metrics = config.get("artifacts", {}).get(METRICS_DEFINITION_KEY)
    mapped_artifact_plan = config.get("artifacts", {}).get(ARTIFACT_PLAN_KEY)
    mapped_context = config.get("artifacts", {}).get(CONTEXT_CONFIRMATION_KEY)
    out = []
    for artifact in artifacts:
        if artifact == REQUIREMENT_ANALYSIS_DEFAULT_ARTIFACT and mapped_requirement:
            out.extend(as_list(mapped_requirement))
        elif artifact == SCENARIO_CATALOG_DEFAULT_ARTIFACT and mapped_scenario:
            out.extend(as_list(mapped_scenario))
        elif artifact == USE_CASES_DEFAULT_ARTIFACT and mapped_use_cases:
            out.extend(as_list(mapped_use_cases))
        elif artifact == END_TO_END_FLOW_DEFAULT_ARTIFACT and mapped_end_to_end_flow:
            out.extend(as_list(mapped_end_to_end_flow))
        elif artifact == METRICS_DEFINITION_DEFAULT_ARTIFACT and mapped_metrics:
            out.extend(as_list(mapped_metrics))
        elif artifact == ARTIFACT_PLAN_DEFAULT_ARTIFACT and mapped_artifact_plan:
            out.extend(as_list(mapped_artifact_plan))
        elif artifact == CONTEXT_CONFIRMATION_DEFAULT_ARTIFACT and mapped_context:
            out.extend(as_list(mapped_context))
        else:
            out.append(artifact)
    return list(dict.fromkeys(out))


def effective_context_confirmation_artifacts(root, project_config=None):
    config = project_config if project_config is not None else load_project_config(root)
    mapped = config.get("artifacts", {}).get(CONTEXT_CONFIRMATION_KEY)
    if mapped:
        return as_list(mapped)
    return [CONTEXT_CONFIRMATION_DEFAULT_ARTIFACT]


def effective_named_artifacts(root, key, default_artifact, project_config=None):
    config = project_config if project_config is not None else load_project_config(root)
    mapped = config.get("artifacts", {}).get(key)
    if mapped:
        return as_list(mapped)
    return [default_artifact]


def artifact_exists(root, pattern):
    # Any glob metacharacter triggers wildcard matching (e.g. *.html, prototypes/*.html)
    if any(ch in pattern for ch in "*?["):
        return len(glob.glob(os.path.join(root, pattern), recursive=True)) > 0
    return os.path.isfile(os.path.join(root, pattern))


def default_context():
    return {
        "mode": "none",
        "root": None,
        "manifest": None,
        "sources": [],
        "assumptions": [],
        "unresolved_questions": [],
        "conflicts": [],
        "stage_refs": {},
        "confirmation": default_context_confirmation_state(),
    }


def normalize_context(ctx):
    out = default_context()
    if isinstance(ctx, dict):
        out.update(ctx)
    out["sources"] = as_list(out.get("sources"))
    out["assumptions"] = out.get("assumptions") or []
    out["unresolved_questions"] = out.get("unresolved_questions") or []
    out["conflicts"] = out.get("conflicts") or []
    out["stage_refs"] = out.get("stage_refs") or {}
    confirmation = default_context_confirmation_state()
    if isinstance(out.get("confirmation"), dict):
        confirmation.update(out.get("confirmation"))
    out["confirmation"] = confirmation
    if out.get("mode") not in ("none", "inline", "files", "root", "auto"):
        out["mode"] = "none"
    return out


def guess_manifest(root, context_root):
    abs_root = resolve_project_path(root, context_root)
    for name in ("CONTEXT_MANIFEST.md", "INDEX.md"):
        candidate = os.path.join(abs_root, name)
        if os.path.isfile(candidate):
            return os.path.join(context_root, name) if not os.path.isabs(context_root) else candidate
    return os.path.join(context_root, "CONTEXT_MANIFEST.md") if not os.path.isabs(context_root) else os.path.join(abs_root, "CONTEXT_MANIFEST.md")


def build_context(root, args, project_config):
    ctx = normalize_context(project_config.get("context", {}))
    context_roots = as_list(getattr(args, "context_root", None))
    context_files = as_list(getattr(args, "context_file", None))
    intake = getattr(args, "intake", None)

    if context_roots:
        ctx["mode"] = "root"
        ctx["root"] = context_roots[0]
        ctx["sources"] = list(dict.fromkeys(ctx.get("sources", []) + context_roots))
        if not ctx.get("manifest"):
            ctx["manifest"] = guess_manifest(root, context_roots[0])
    if context_files:
        if ctx["mode"] == "none":
            ctx["mode"] = "files"
        ctx["sources"] = list(dict.fromkeys(ctx.get("sources", []) + context_files))
    if intake:
        if ctx["mode"] == "none":
            ctx["mode"] = "files"
        ctx["sources"] = list(dict.fromkeys(ctx.get("sources", []) + [intake]))
    return normalize_context(ctx)


def open_conflicts(state, stage=None):
    conflicts = []
    for c in state.get("context", {}).get("conflicts", []):
        if c.get("status", "open") == "resolved":
            continue
        if stage is None or c.get("stage") in (None, stage):
            conflicts.append(c)
    return conflicts


def ensure_stage_context_ref(state, stage):
    ctx = normalize_context(state.get("context", {}))
    refs = ctx.setdefault("stage_refs", {})
    ref = refs.setdefault(stage, {})
    ref.setdefault("sources", [])
    ref.setdefault("applicable_rules", [])
    ref.setdefault("assumptions", [])
    ref.setdefault("conflicts", [])
    if ctx.get("mode") == "none":
        ref.setdefault("no_context_reason", "No external context was provided; proceed using the current requirement input and stage artifacts.")
    elif not ref.get("sources"):
        ref["sources"] = ctx.get("sources", [])
    state["context"] = ctx


def render_requirement_analysis_template(state, by):
    context = normalize_context(state.get("context", {}))
    lines = [
        "# Requirement Analysis",
        "",
        "- Project: %s" % state.get("project", ""),
        "- Requirement: %s" % state.get("requirement", ""),
        "- Analyst: %s" % (by or "agent"),
        "- Date: %s" % now_iso(),
        "- Input source: %s" % (state.get("intake") or "To be completed"),
        "- Context citation conclusion: To be completed. Reference context_confirmation.md.",
        "",
        "## 1. Original Request",
        "",
        "- Original wording: %s" % state.get("requirement", ""),
        "- Source: %s" % (" / ".join(context.get("sources", [])) if context.get("sources") else "To be completed"),
        "- Related materials: To be completed",
        "",
        "## 2. Problem And Goal",
        "",
        "- Problem to solve: To be completed",
        "- Affected users or roles: To be completed",
        "- Current pain: To be completed",
        "- Impact if not solved: To be completed",
        "- Expected result: To be completed",
        "",
        "## 3. Scope And Non-Scope",
        "",
        "- Scope: To be completed",
        "- Non-scope: To be completed",
        "- Client surfaces: To be completed",
        "- Roles: To be completed",
        "- Dependencies: To be completed",
        "",
        "## 4. Confirmed Facts, Assumptions, And Open Questions",
        "",
        "| Type | Content | Source | Handling |",
        "|---|---|---|---|",
        "| Confirmed fact | To be completed | To be completed | To be completed |",
        "| Assumption | To be completed | To be completed | To be completed |",
        "| Open question | To be completed | To be completed | To be completed |",
        "",
        "## 5. Requirement Analysis Level",
        "",
        "- Level: To be completed (A0 / A1 / A2 / A3)",
        "- Rationale: To be completed",
        "- PRD level recommendation: To be completed (L1 / L2 / L3 / not needed)",
        "",
        "## 6. Assumptions And Risks",
        "",
        "| Assumption or risk | Type | Impact | Confidence | Validation | Blocking |",
        "|---|---|---|---|---|---|",
        "| To be completed | To be completed | To be completed | To be completed | To be completed | To be completed |",
        "",
        "## 7. Success Criteria And Acceptance Lens",
        "",
        "- Business success criteria: To be completed",
        "- User success criteria: To be completed",
        "- Primary metric: To be completed",
        "- Input metrics: To be completed",
        "- Guardrail metrics: To be completed",
        "- Observable acceptance lens: To be completed",
        "- Failure or exception lens: To be completed",
        "",
        "## 8. Artifact Routing",
        "",
        "| Artifact | Needed | Reason | Output path |",
        "|---|---|---|---|",
        "| Metrics definition | To be completed | To be completed | To be completed |",
        "| Scenario catalog | To be completed | To be completed | To be completed |",
        "| Use cases | To be completed | To be completed | To be completed |",
        "| End-to-end flow | To be completed | To be completed | To be completed |",
        "| PRD | To be completed | To be completed | To be completed |",
        "| Field dictionary | To be completed | To be completed | To be completed |",
        "| HTML prototype | To be completed | To be completed | To be completed |",
        "| Prototype review artifact | To be completed | To be completed | To be completed |",
        "| Mermaid diagram | To be completed | To be completed | To be completed |",
        "| Test scenarios | To be completed | To be completed | To be completed |",
        "| Delivery check | To be completed | To be completed | To be completed |",
        "",
        "## 9. Source Error Check",
        "",
        "- Source errors found: To be completed",
        "- Highest severity: To be completed (none / P3 / P2 / P1 / P0)",
        "- Error location: To be completed",
        "- Correction conclusion: To be completed",
        "- Blocks downstream output: To be completed",
    ]
    return "\n".join(lines) + "\n"


def render_context_confirmation_template(state, by):
    context = normalize_context(state.get("context", {}))
    lines = [
        "# Context Intake Confirmation",
        "",
        "- Project: %s" % state.get("project", ""),
        "- Requirement: %s" % state.get("requirement", ""),
        "- Confirmed by: %s" % (by or "agent"),
        "- Generated at: %s" % now_iso(),
        "",
        "## 1. Context Mode",
        "- Context mode: %s" % context.get("mode", "none"),
        "- External knowledge base used: To be completed (yes / no)",
        "- Reason if not used: To be completed",
        "",
        "## 2. Knowledge-Base Entry Points",
        "- Context root: %s" % (context.get("root") or "None"),
        "- Manifest or index: %s" % (context.get("manifest") or "None"),
        "- Intake: %s" % (state.get("intake") or "None"),
        "- Other sources: %s" % (" / ".join(context.get("sources", [])) if context.get("sources") else "None"),
        "",
        "## 3. Applicable Sources",
        "- Required sources: To be completed",
        "- Stage-specific sources: To be completed",
        "- Applicable rules: To be completed (MUST / SHOULD / MAY / FORBIDDEN)",
        "- Referenced design guidelines, component library, fonts, or frontend framework: To be completed",
        "",
        "## 4. Non-Applicable Sources",
        "- Excluded sources: To be completed",
        "- Reason: To be completed",
        "- Archived or outdated materials: To be completed",
        "",
        "## 5. Rule Strength And Conflicts",
        "- MUST rules: To be completed",
        "- FORBIDDEN rules: To be completed",
        "- Conflicts: To be completed",
        "- Resolution: To be completed",
        "",
        "## 6. Citation Conclusion",
        "- Is the context usable: To be completed",
        "- Preconditions for continuing: To be completed",
        "- Sources that must be cited later: To be completed",
        "- Sources that must not be cited later: To be completed",
    ]
    return "\n".join(lines) + "\n"


def requirement_analysis_template_path(template_name):
    for skill_name in ("pm-requirement-analysis", "pm-metrics-definition"):
        sibling = os.path.join(
            os.path.dirname(SKILL_DIR),
            skill_name,
            "assets",
            "templates",
            template_name,
        )
        if os.path.isfile(sibling):
            return sibling
    return None


def write_analysis_side_artifact(root, artifact, template_name, fallback_content, force=False):
    target = resolve_project_path(root, artifact)
    if os.path.exists(target) and not force:
        print("○ side artifact already exists: %s" % target)
        return
    os.makedirs(os.path.dirname(target) or root, exist_ok=True)
    source = requirement_analysis_template_path(template_name)
    if source:
        shutil.copy2(source, target)
    else:
        with open(target, "w", encoding="utf-8") as f:
            f.write(fallback_content)
    print("✓ artifact written: %s" % target)


def check_requirement_analysis_ready(path):
    if not os.path.isfile(path):
        return False, "requirement analysis file not found: %s" % path
    with open(path, encoding="utf-8") as f:
        content = f.read()
    stripped = content.strip()
    if len(stripped) < 600:
        return False, "requirement analysis is too short; appears incomplete."
    missing = [h for h in REQUIREMENT_ANALYSIS_REQUIRED_HEADINGS if h not in content]
    if missing:
        return False, "requirement analysis missing required sections: %s" % ", ".join(missing)
    for token in REQUIREMENT_ANALYSIS_PLACEHOLDERS:
        if token in content:
            return False, "requirement analysis still contains unfilled placeholder: %s" % token
    return True, ""


def check_context_confirmation_ready(path):
    if not os.path.isfile(path):
        return False, "context intake confirmation file not found: %s" % path
    with open(path, encoding="utf-8") as f:
        content = f.read()
    stripped = content.strip()
    if len(stripped) < 500:
        return False, "context intake confirmation is too short; appears incomplete."
    missing = [h for h in CONTEXT_CONFIRMATION_REQUIRED_HEADINGS if h not in content]
    if missing:
        return False, "context intake confirmation missing required sections: %s" % ", ".join(missing)
    for token in REQUIREMENT_ANALYSIS_PLACEHOLDERS:
        if token in content:
            return False, "context intake confirmation still contains unfilled placeholder: %s" % token
    return True, ""


def ensure_context_confirmation_ready(root, state, action):
    artifacts = effective_context_confirmation_artifacts(root)
    missing = [r for r in artifacts if not artifact_exists(root, r)]
    if missing:
        die("context intake confirmation incomplete; cannot run %s. Produce first: %s" % (action, ", ".join(missing)))
    confirmation = context_confirmation_state(state, root)
    if confirmation.get("status") != "confirmed" or not confirmation.get("confirmed_at"):
        die("context intake confirmation not yet confirmed; cannot run %s. Complete %s then run `context confirm --confirm`."
            % (action, confirmation.get("artifact")))


def ensure_requirement_analysis_ready(root, state, contract, action):
    artifacts = effective_requirement_analysis_artifacts(root, contract)
    missing = [r for r in artifacts if not artifact_exists(root, r)]
    if missing:
        die("requirement analysis artifact incomplete; cannot run %s. Produce first: %s" % (action, ", ".join(missing)))
    ra = requirement_analysis_state(state, root, contract)
    if ra.get("status") != "confirmed" or not ra.get("confirmed_at"):
        die("requirement analysis artifact not yet confirmed; cannot run %s. Complete %s then run `analyze --confirm`."
            % (action, ra.get("artifact")))
    ensure_context_confirmation_ready(root, state, action)


# ---------------------------------------------------------------- init
def ensure_knowledge_base_for_init(root, project_config, args):
    if isinstance(project_config.get("knowledge_base"), dict) and project_config["knowledge_base"].get("status") == "confirmed":
        return project_config
    context_roots = as_list(getattr(args, "context_root", None))
    context_files = as_list(getattr(args, "context_file", None))
    intake = getattr(args, "intake", None)
    sources = context_files[:]
    if intake:
        sources.append(intake)
    source_paths = [resolve_project_path(root, src) for src in sources]
    if context_roots:
        manifest_path = resolve_project_path(root, guess_manifest(root, context_roots[0]))
        project_config["knowledge_base"] = make_knowledge_base_root(
            root,
            context_roots[0],
            manifest=manifest_path,
            sources=source_paths,
            by="user",
        )
    elif sources:
        project_config["knowledge_base"] = make_knowledge_base_files(root, source_paths, by="user")
    else:
        project_config = make_unconfirmed_knowledge_base(project_config)
    return project_config


def cmd_init(args):
    rtype = args.type
    if rtype not in PATH_BY_TYPE:
        die("Unknown requirement type: %s (expected new-platform | iteration | iteration-lite | micro)" % rtype)
    root = args.root
    p = state_path(root)
    if os.path.isfile(p) and not args.force:
        die("state.json already exists (%s). Use --force to overwrite and restart." % p)

    project_config = load_project_config(root)
    if getattr(args, "config", None):
        config_path = os.path.abspath(args.config)
        if not os.path.isfile(config_path):
            die("project config not found: %s" % args.config)
        project_config = load_json_file(config_path)
    project_config = bind_workspace_config(root, project_config, "user", allow_change=args.force)
    project_config = ensure_knowledge_base_for_init(root, project_config, args)
    save_project_config(root, project_config)

    path = PATH_BY_TYPE[rtype]
    stages = {}
    for s in STAGES_ALL:
        stages[s] = {
            "status": "todo" if s in path else "skipped",
            "confirmed_by": None, "confirmed_at": None,
            "done_at": None, "closed_at": None, "closed_by": None,
            "semantic_checked_at": None, "semantic_checked_by": None,
            "artifact": None, "notes": "",
        }
    state = {
        "schema_version": "1.0",
        "project": args.project or "(Untitled project)",
        "requirement": args.requirement or "(Untitled requirement)",
        "requirement_type": rtype,
        "created_at": now_iso(),
        "intake": getattr(args, "intake", None),
        "project_config": ".pm-flow/project_config.json" if project_config else None,
        "context": build_context(root, args, project_config),
        "requirement_analysis": default_requirement_analysis_state(),
        "current_stage": path[0],
        "path": path,
        "stages": stages,
        "decisions": [],
        "artifacts": {},
    }
    analysis_artifacts = effective_requirement_analysis_artifacts(root, load_contract(), project_config)
    if analysis_artifacts:
        state["requirement_analysis"]["artifact"] = analysis_artifacts[0]
    context_artifacts = effective_context_confirmation_artifacts(root, project_config)
    if context_artifacts:
        state["context"]["confirmation"]["artifact"] = context_artifacts[0]
    save_state(root, state)
    print("✓ initialized state.json (%s)" % p)
    print("  requirement type: %s" % rtype)
    print("  path: %s" % " → ".join(path))
    print("  current stage: %s" % path[0])
    if project_config:
        print("  project config mounted: %s" % project_config_path(root))
    if state["context"]["mode"] != "none":
        print("  context mode: %s" % state["context"]["mode"])


# ---------------------------------------------------------------- status
def status_payload(root, state):
    contract = load_contract()
    current = state["current_stage"]
    current_status = state["stages"].get(current, {}).get("status")
    analysis = requirement_analysis_state(state, root, contract)
    context_confirmation = context_confirmation_state(state, root)
    if all(state["stages"][s]["status"] == "closed" for s in state["path"]):
        next_action = "complete"
    elif context_confirmation.get("status") != "confirmed":
        next_action = "complete_context_confirmation"
    elif analysis.get("status") != "confirmed":
        next_action = "complete_requirement_analysis"
    elif current_status == "todo":
        next_action = "create_artifact_then_confirm"
    elif current_status == "confirmed":
        next_action = "mark"
    elif current_status == "done":
        next_action = "close_checked"
    else:
        next_action = "inspect_state"
    context = normalize_context(state.get("context", {}))
    return {
        "project": state["project"],
        "requirement": state["requirement"],
        "requirement_type": state["requirement_type"],
        "current_stage": current,
        "current_status": current_status,
        "next_required_action": next_action,
        "required_artifacts": effective_required_artifacts(root, state, current, contract),
        "context_mode": context["mode"],
        "context_sources": context.get("sources", []),
        "context_manifest": context.get("manifest"),
        "open_conflicts": open_conflicts(state),
        "project_config": state.get("project_config"),
        "requirement_analysis": {
            "status": analysis.get("status"),
            "artifact": analysis.get("artifact"),
            "exists": artifact_exists(root, analysis.get("artifact")),
            "confirmed_at": analysis.get("confirmed_at"),
            "confirmed_by": analysis.get("confirmed_by"),
        },
        "context_confirmation": {
            "status": context_confirmation.get("status"),
            "artifact": context_confirmation.get("artifact"),
            "exists": artifact_exists(root, context_confirmation.get("artifact")),
            "confirmed_at": context_confirmation.get("confirmed_at"),
            "confirmed_by": context_confirmation.get("confirmed_by"),
        },
    }


def cmd_status(args):
    state, _ = load_state(args.root)
    if args.json:
        print(json.dumps(status_payload(args.root, state), ensure_ascii=False, indent=2))
        return
    print("=== pm-flow status board ===")
    print("Project：%s" % state["project"])
    print("Requirement: %s (type: %s)" % (state["requirement"], state["requirement_type"]))
    print("Current stage: %s" % state["current_stage"])
    print("Next action: %s" % status_payload(args.root, state)["next_required_action"])
    analysis = status_payload(args.root, state)["requirement_analysis"]
    print("Requirement analysis artifact: %s (%s, exists=%s)" %
          (analysis["status"], analysis["artifact"], analysis["exists"]))
    context_confirmation = status_payload(args.root, state)["context_confirmation"]
    print("Knowledge base confirmation: %s (%s, exists=%s)" %
          (context_confirmation["status"], context_confirmation["artifact"],
           context_confirmation["exists"]))
    print("Context: %s" % normalize_context(state.get("context", {}))["mode"])
    if state.get("project_config"):
        print("Project config: %s" % state["project_config"])
    print("--- stages ---")
    for s in STAGES_ALL:
        st = state["stages"].get(s, {})
        mark = "●" if s == state["current_stage"] else " "
        print(" %s %-10s %-9s %s" % (mark, s, st.get("status", "?"), st.get("notes", "")))
    n_closed = sum(1 for s in state["path"] if state["stages"][s]["status"] == "closed")
    print("Progress: %d/%d stages closed" % (n_closed, len(state["path"])))


# ---------------------------------------------------------------- analyze
def cmd_analyze(args):
    state, _ = load_state(args.root)
    contract = load_contract()
    artifact = args.artifact or effective_named_artifacts(
        args.root, REQUIREMENT_ANALYSIS_KEY, REQUIREMENT_ANALYSIS_DEFAULT_ARTIFACT
    )[0]
    target = resolve_project_path(args.root, artifact)

    if os.path.exists(target) and not args.force:
        print("○ requirement analysis file already exists: %s" % target)
    else:
        os.makedirs(os.path.dirname(target) or args.root, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(render_requirement_analysis_template(state, args.by))
        print("✓ generated requirement analysis template: %s" % target)

    for side_artifact in effective_named_artifacts(
        args.root, SCENARIO_CATALOG_KEY, SCENARIO_CATALOG_DEFAULT_ARTIFACT
    ):
        write_analysis_side_artifact(
            args.root,
            side_artifact,
            "scenario-catalog.md",
            "# Scenario Catalog\n\nUse pm-requirement-analysis to complete this file.\n",
            args.force,
        )
    for side_artifact in effective_named_artifacts(
        args.root, USE_CASES_KEY, USE_CASES_DEFAULT_ARTIFACT
    ):
        write_analysis_side_artifact(
            args.root,
            side_artifact,
            "use-cases.md",
            "# Use Cases\n\nUse pm-requirement-analysis to complete this file.\n",
            args.force,
        )
    for side_artifact in effective_named_artifacts(
        args.root, END_TO_END_FLOW_KEY, END_TO_END_FLOW_DEFAULT_ARTIFACT
    ):
        write_analysis_side_artifact(
            args.root,
            side_artifact,
            "end-to-end-flow.md",
            "# End-To-End Flow\n\nUse pm-requirement-analysis to complete this file.\n",
            args.force,
        )
    for side_artifact in effective_named_artifacts(
        args.root, METRICS_DEFINITION_KEY, METRICS_DEFINITION_DEFAULT_ARTIFACT
    ):
        write_analysis_side_artifact(
            args.root,
            side_artifact,
            "metrics-definition.md",
            "# Metrics Definition\n\nUse pm-metrics-definition to complete this file.\n",
            args.force,
        )
    for side_artifact in effective_named_artifacts(
        args.root, ARTIFACT_PLAN_KEY, ARTIFACT_PLAN_DEFAULT_ARTIFACT
    ):
        write_analysis_side_artifact(
            args.root,
            side_artifact,
            "artifact-plan.md",
            "# Artifact Plan\n\nUse pm-requirement-analysis to complete this file.\n",
            args.force,
        )

    analysis = requirement_analysis_state(state, args.root, contract)
    analysis["artifact"] = artifact
    if not analysis.get("created_at"):
        analysis["created_at"] = now_iso()

    if args.confirm:
        ensure_context_confirmation_ready(args.root, state, "analyze --confirm")
        missing = [
            r for r in effective_requirement_analysis_artifacts(args.root, contract)
            if not artifact_exists(args.root, r)
        ]
        if missing:
            die("cannot confirm requirement analysis; missing artifact: %s" % ", ".join(missing))
        ok, reason = check_requirement_analysis_ready(target)
        if not ok:
            die("cannot confirm requirement analysis: %s" % reason)
        analysis["status"] = "confirmed"
        analysis["confirmed_at"] = now_iso()
        analysis["confirmed_by"] = args.by or "user"
        state["artifacts"][REQUIREMENT_ANALYSIS_KEY] = artifact
        print("✓ requirement analysis artifact confirmed (%s)" % analysis["confirmed_by"])
    elif analysis.get("status") == "todo":
        analysis["status"] = "draft"
        print("  complete the content, then run: analyze --confirm --by <name>")

    state[REQUIREMENT_ANALYSIS_KEY] = analysis
    save_state(args.root, state)


# ---------------------------------------------------------------- confirm
def cmd_confirm(args):
    state, p = load_state(args.root)
    s = args.stage
    if s not in state["path"]:
        die("stage %s is not in this requirement path (path: %s)" % (s, " → ".join(state["path"])))
    ensure_requirement_analysis_ready(args.root, state, load_contract(), "confirm %s" % s)
    st = state["stages"][s]
    if st["status"] == "confirmed":
        print("○ %s is already confirmed; no need to repeat." % s)
        return
    if st["status"] != "todo":
        die("%s is in state %s; cannot confirm (only todo -> confirmed)." % (s, st["status"]))
    st["status"] = "confirmed"
    st["confirmed_by"] = args.by or "user"
    st["confirmed_at"] = now_iso()
    state["current_stage"] = s
    save_state(args.root, state)
    print("✓ %s → confirmed (by %s)" % (s, st["confirmed_by"]))


# ---------------------------------------------------------------- mark
def ensure_stage_content_ready(root, contract, stage, action):
    if stage not in ("prd", "review"):
        return
    if SKILL_DIR not in sys.path:
        sys.path.insert(0, SKILL_DIR)
    import validate  # noqa: E402
    errors = validate.validate_stage_content(root, contract, load_project_config(root), stage)
    if errors:
        die("%s content check failed: %s" % (action, "; ".join(errors)))


def cmd_mark(args):
    state, p = load_state(args.root)
    s = args.stage
    if s not in state["path"]:
        die("stage %s is not in this requirement path." % s)
    contract = load_contract()
    ensure_requirement_analysis_ready(args.root, state, contract, "mark %s" % s)
    st = state["stages"][s]
    if st["status"] != "confirmed":
        die("%s is in state %s; run confirm first." % (s, st["status"]))

    # previous stages must already be closed
    idx = state["path"].index(s)
    for pre in state["path"][:idx]:
        if state["stages"][pre]["status"] != "closed":
            die("prerequisite stage %s is not closed; cannot mark %s." % (pre, s))

    if args.artifact:
        st["artifact"] = args.artifact
        state["artifacts"][s] = args.artifact

    # required artifact existence check (from contract_config)
    req = effective_required_artifacts(args.root, state, s, contract)
    missing = [r for r in req if not artifact_exists(args.root, r)]
    if missing:
        print("✗ mark failed: the following required artifacts were not found (relative to project root %s):" % args.root)
        for m in missing:
            print("   - %s" % m)
        print("  produce these files first, or verify the paths. state unchanged.")
        sys.exit(1)

    ensure_stage_content_ready(args.root, contract, s, "mark %s" % s)

    st["status"] = "done"
    st["done_at"] = now_iso()
    save_state(args.root, state)
    print("✓ %s → done (artifacts complete, pending close)" % s)


# ---------------------------------------------------------------- close
def cmd_close(args):
    state, p = load_state(args.root)
    s = args.stage
    if s not in state["path"]:
        die("stage %s is not in this requirement path." % s)
    contract = load_contract()
    ensure_requirement_analysis_ready(args.root, state, contract, "close %s" % s)
    st = state["stages"][s]
    if st["status"] != "done":
        die("%s is in state %s; run mark first." % (s, st["status"]))

    c = contract["stages"].get(s, {})
    req = effective_required_artifacts(args.root, state, s, contract)
    sem = c.get("semantic_checks", [])
    missing = [r for r in req if not artifact_exists(args.root, r)]

    print("=== close gate check: %s ===" % s)
    for r in req:
        ok = artifact_exists(args.root, r)
        print("  [%s] required artifact %s" % ("✓" if ok else "✗", r))
    if missing:
        die("required artifacts missing; close aborted. Complete first: %s" % ", ".join(missing))

    ensure_stage_content_ready(args.root, contract, s, "close %s" % s)

    print("  --- semantic check list (review manually / by AI) ---")
    for chk in sem:
        print("  [ ] %s" % chk)
    if sem and not args.checked:
        die("semantic checks not yet explicitly confirmed; close aborted. Review each item then rerun: close %s --checked" % s)
    conflicts = open_conflicts(state, s)
    if conflicts:
        die("unresolved context conflicts exist; close aborted: %d conflict(s)" % len(conflicts))

    ensure_stage_context_ref(state, s)
    st["status"] = "closed"
    st["closed_at"] = now_iso()
    st["closed_by"] = args.by or "user"
    st["semantic_checked_at"] = now_iso()
    st["semantic_checked_by"] = args.by or "user"
    # advance current_stage to next unclosed
    for nxt in state["path"]:
        if state["stages"][nxt]["status"] != "closed":
            state["current_stage"] = nxt
            break
    save_state(args.root, state)
    print("✓ %s → closed (semantic check confirmed by %s, stage locked)" % (s, st["closed_by"]))


# ---------------------------------------------------------------- next
def cmd_next(args):
    state, _ = load_state(args.root)
    for nxt in state["path"]:
        if state["stages"][nxt]["status"] != "closed":
            state["current_stage"] = nxt
            save_state(args.root, state)
            print("-> next stage: %s (status: %s)" % (nxt, state["stages"][nxt]["status"]))
            return
    print("★ flow done: all path stages closed.")


# ---------------------------------------------------------------- decide
def cmd_decide(args):
    state, p = load_state(args.root)
    s = args.stage
    if s not in state["stages"]:
        die("unknown stage: %s" % s)
    state["decisions"].append({
        "at": now_iso(),
        "stage": s,
        "decision": args.text,
        "who": args.by or "user",
    })
    save_state(args.root, state)
    print("✓ decision recorded (%s): %s" % (s, args.text))


# ---------------------------------------------------------------- review
def cmd_review(args):
    state, p = load_state(args.root)
    s = args.stage
    if s not in state["path"]:
        die("stage %s is not in this requirement path." % s)
    contract = load_contract()
    c = contract["stages"].get(s, {})
    sem = c.get("semantic_checks", [])
    req = effective_required_artifacts(args.root, state, s, contract)

    out_dir = os.path.join(args.root, "reviews")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "%s-audit.md" % s)
    lines = []
    lines.append("# independent review checklist · %s" % s)
    lines.append("")
    lines.append("- Project：%s" % state["project"])
    lines.append("- Requirement: %s (type: %s)" % (state["requirement"], state["requirement_type"]))
    lines.append("- Generated: %s" % now_iso())
    lines.append("- Reviewer: independent sub-agent / reviewer not involved in producing this stage")
    lines.append("")
    lines.append("## Required artifacts (existence auto-verified)")
    for r in req:
        ok = artifact_exists(args.root, r)
        lines.append("- [%s] `%s`" % ("x" if ok else " ", r))
    lines.append("")
    lines.append("## Semantic checks (verify each; mark ✅ when passed)")
    for chk in sem:
        lines.append("- [ ] %s" % chk)
    lines.append("")
    lines.append("## Review conclusion")
    lines.append("- Findings:")
    lines.append("- Disposition: close loop / log open question")
    lines.append("")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("✓ generated review checklist: %s" % out)
    print("  hand to an independent sub-agent / non-producing reviewer to verify item by item; write conclusions back into this file.")


# ---------------------------------------------------------------- validate (P4)
def cmd_validate(args):
    if SKILL_DIR not in sys.path:
        sys.path.insert(0, SKILL_DIR)
    import validate  # noqa: E402  (text，text)
    skill_dir = getattr(args, "skill", None) or SKILL_DIR
    errors, warnings, ok = validate.run_validation(args.root, skill_dir)
    print("=== pm-flow P4 · SSOT validation ===")
    print("Project root: %s" % args.root)
    print("Skill dir: %s" % SKILL_DIR)
    for w in warnings:
        print("  ⚠ warning: %s" % w)
    for e in errors:
        print("  ✗ error: %s" % e)
    if ok:
        print("✓ validation passed (no errors, %d warning(s))" % len(warnings))
        sys.exit(0)
    else:
        print("✗ validation failed: %d error(s), %d warning(s)" % (len(errors), len(warnings)))
        sys.exit(1)


# ---------------------------------------------------------------- context
def validate_context(root, state):
    errors = []
    warnings = []
    ctx = normalize_context(state.get("context", {}))
    mode = ctx.get("mode")

    if mode == "none":
        return errors, warnings

    def exists(path):
        return os.path.exists(resolve_project_path(root, path))

    if mode == "root":
        if not ctx.get("root"):
            errors.append("context.mode=root but context.root is missing")
        elif not os.path.isdir(resolve_project_path(root, ctx["root"])):
            errors.append("context.root does not exist or is not a directory: %s" % ctx["root"])
        manifest = ctx.get("manifest")
        if not manifest:
            errors.append("context.mode=root but manifest is missing")
        elif not os.path.isfile(resolve_project_path(root, manifest)):
            errors.append("context manifest does not exist: %s" % manifest)

    if mode in ("files", "inline", "auto", "root"):
        for src in ctx.get("sources", []):
            if src and not exists(src):
                warnings.append("context source not found: %s" % src)

    open_items = open_conflicts(state)
    if open_items:
        errors.append("unresolved context conflicts exist: %d" % len(open_items))

    return errors, warnings


def cmd_context_status(args):
    state, _ = load_state(args.root)
    ctx = normalize_context(state.get("context", {}))
    if args.json:
        print(json.dumps(ctx, ensure_ascii=False, indent=2))
        return
    print("=== pm-flow context ===")
    print("context: %s" % ctx["mode"])
    print("root：%s" % (ctx.get("root") or "-"))
    print("manifest：%s" % (ctx.get("manifest") or "-"))
    print("sources：%d" % len(ctx.get("sources", [])))
    print("assumptions：%d" % len(ctx.get("assumptions", [])))
    print("unresolved_questions：%d" % len(ctx.get("unresolved_questions", [])))
    print("open_conflicts：%d" % len(open_conflicts(state)))
    confirmation = context_confirmation_state(state, args.root)
    print("confirmation：%s（%s）" %
          (confirmation.get("status"), confirmation.get("artifact")))


def cmd_context_validate(args):
    state, _ = load_state(args.root)
    errors, warnings = validate_context(args.root, state)
    print("=== pm-flow context validation ===")
    for w in warnings:
        print("  ⚠ warning: %s" % w)
    for e in errors:
        print("  ✗ error: %s" % e)
    if errors:
        print("✗ context validation failed: %d error(s), %d warning(s)" % (len(errors), len(warnings)))
        sys.exit(1)
    print("✓ context validation passed (no errors, %d warning(s))" % len(warnings))


def cmd_context_confirm(args):
    state, _ = load_state(args.root)
    artifact = args.artifact or context_confirmation_state(state, args.root).get("artifact")
    target = resolve_project_path(args.root, artifact)

    if os.path.exists(target) and not args.force:
        print("○ context intake confirmation file already exists: %s" % target)
    else:
        os.makedirs(os.path.dirname(target) or args.root, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(render_context_confirmation_template(state, args.by))
        print("✓ generated context intake confirmation template: %s" % target)

    ctx = normalize_context(state.get("context", {}))
    confirmation = context_confirmation_state(state, args.root)
    confirmation["artifact"] = artifact
    if not confirmation.get("created_at"):
        confirmation["created_at"] = now_iso()

    if args.confirm:
        errors, warnings = validate_context(args.root, state)
        if errors:
            die("cannot confirm context intake confirmation: context validation failed: %s" % "；".join(errors))
        ok, reason = check_context_confirmation_ready(target)
        if not ok:
            die("cannot confirm context intake confirmation: %s" % reason)
        confirmation["status"] = "confirmed"
        confirmation["confirmed_at"] = now_iso()
        confirmation["confirmed_by"] = args.by or "user"
        state["artifacts"][CONTEXT_CONFIRMATION_KEY] = artifact
        print("✓ context intake confirmation confirmed (%s)" % confirmation["confirmed_by"])
        for w in warnings:
            print("  ⚠ warning: %s" % w)
    elif confirmation.get("status") == "todo":
        confirmation["status"] = "draft"
        print("  complete the content, then run: context confirm --confirm --by <name>")

    ctx["confirmation"] = confirmation
    state["context"] = ctx
    save_state(args.root, state)


# ---------------------------------------------------------------- scaffold
def find_prototype_scaffold():
    """Find prototype scaffold assets.

    pm-flow owns the workflow command; pm-html-prototype owns the heavy assets.
    Keep a local fallback for older installs that have not been split yet.
    """
    env_path = os.environ.get("PM_HTML_PROTOTYPE_SCAFFOLD") or os.environ.get("PM_PROTOTYPE_REVIEW_SCAFFOLD")
    sibling = os.path.join(os.path.dirname(SKILL_DIR), "pm-html-prototype", "assets", "scaffold")
    legacy_sibling = os.path.join(os.path.dirname(SKILL_DIR), "pm-prototype-review", "assets", "scaffold")
    legacy = os.path.join(SKILL_DIR, "scaffold")
    candidates = [p for p in (env_path, sibling, legacy_sibling, legacy) if p]
    for path in candidates:
        if os.path.isdir(path):
            return path
    die("prototype scaffold asset directory not found; install the sibling skill pm-html-prototype, or set PM_HTML_PROTOTYPE_SCAFFOLD")


def cmd_scaffold(args):
    """Lay an out-of-the-box prototype skeleton under <root>/prototypes/:
    - assets/design-system/  kit design-system snapshot (tokens.css + components.html + pda/)
    - assets/  prototype-chrome.css (layout only), review css+js, device-frame, fonts, validate_prototype.py
    - shared/  menu-config.js + app-shell.js (web admin menu engine, multi-role switcher)
    - index.html          Web admin empty skeleton (merges the user-provided "menu skeleton")
    - prototype-doc.html  review empty template (data-link pairing + connectors)
    - pda.html           mobile / PDA empty skeleton (device frames tiled)

    The prototype consumes the kit design-system as the single token source; it no
    longer bundles its own token set. design-system/ is copied in as a snapshot so
    each prototype stays self-contained and offline-openable.
    """
    root = os.path.abspath(args.root)
    skill_scaffold = find_prototype_scaffold()

    name = (args.name or "Product Prototype").strip() or "Product Prototype"
    logo = name[0] if name else "P"

    proto_dir = os.path.join(root, "prototypes")
    assets_dir = os.path.join(proto_dir, "assets")
    shared_dir = os.path.join(proto_dir, "shared")
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(shared_dir, exist_ok=True)

    # 1) text assets/ text shared/ text
    copied, skipped = [], []
    for src_dir, dst_dir in ((os.path.join(skill_scaffold, "assets"), assets_dir),
                             (os.path.join(skill_scaffold, "shared"), shared_dir)):
        if not os.path.isdir(src_dir):
            continue
        for current, _, files in os.walk(src_dir):
            rel_dir = os.path.relpath(current, src_dir)
            target_dir = dst_dir if rel_dir == "." else os.path.join(dst_dir, rel_dir)
            os.makedirs(target_dir, exist_ok=True)
            for fn in sorted(files):
                sp = os.path.join(current, fn)
                dp = os.path.join(target_dir, fn)
                if os.path.exists(dp) and not args.force:
                    skipped.append(os.path.relpath(dp, proto_dir))
                    continue
                shutil.copy2(sp, dp)
                copied.append(os.path.relpath(dp, proto_dir))

    # 2) render templates/ (inject {{PROJECT_NAME}} / {{PROJECT_LOGO}})
    tpl_dir = os.path.join(skill_scaffold, "templates")
    if os.path.isdir(tpl_dir):
        for fn in sorted(os.listdir(tpl_dir)):
            sp = os.path.join(tpl_dir, fn)
            if not os.path.isfile(sp) or not fn.endswith(".html"):
                continue
            dp = os.path.join(proto_dir, fn)
            if os.path.exists(dp) and not args.force:
                skipped.append(fn)
                continue
            with open(sp, encoding="utf-8") as fh:
                tpl = fh.read()
            out = tpl.replace("{{PROJECT_NAME}}", name).replace("{{PROJECT_LOGO}}", logo)
            with open(dp, "w", encoding="utf-8") as fh:
                fh.write(out)
            copied.append(fn)

    # 3) snapshot the kit design-system into the prototype (single token source)
    ds_src = os.path.join(skill_scaffold, "..", "..", "..", "..", "design-system")
    ds_dst = os.path.join(assets_dir, "design-system")
    if os.path.isdir(ds_src):
        os.makedirs(ds_dst, exist_ok=True)
        for cur, _, files in os.walk(ds_src):
            rel = os.path.relpath(cur, ds_src)
            tgt = ds_dst if rel == "." else os.path.join(ds_dst, rel)
            os.makedirs(tgt, exist_ok=True)
            for fn in sorted(files):
                sp = os.path.join(cur, fn)
                dp = os.path.join(tgt, fn)
                if os.path.exists(dp) and not args.force:
                    continue
                shutil.copy2(sp, dp)
                copied.append(os.path.join("assets", "design-system", fn) if rel == "."
                              else os.path.join("assets", "design-system", rel, fn))
    else:
        print("  ! design-system source not found at %s; prototype will miss tokens" % ds_src)

    print("✓ prototype skeleton laid out at: %s" % proto_dir)
    if copied:
        print("  generated/updated:")
        for c in copied:
            print("    + %s" % c)
    if skipped:
        print("  skipped (already exists; --force to overwrite):")
        for s in skipped:
            print("    · %s" % s)
    print("")
    print("Asset source: %s" % skill_scaffold)
    print("")
    print("Next steps:")
    print("  1. edit prototypes/shared/menu-config.js to add/remove menus/roles")
    print("  2. add business pages under prototypes/, referencing assets/prototype-chrome.css (tokens come from assets/design-system/tokens.css)")
    print("  3. run python3 prototypes/assets/validate_prototype.py for self-check")


# ---------------------------------------------------------------- workspace
def cmd_workspace_status(args):
    config = load_project_config(args.root)
    payload = workspace_binding_payload(args.root, config)
    mismatch = workspace_mismatch_reason(args.root, config)
    payload["mismatch"] = mismatch
    payload["bound"] = config.get("workspace") is not None
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print("=== pm-flow workspace ===")
    print("bound: %s" % ("yes" if payload["bound"] else "no"))
    print("bound_root: %s" % (payload.get("realpath") or "-"))
    print("current_root: %s" % payload["current_realpath"])
    print("plugin_workdir: %s" % payload["plugin_workdir"])
    print("preserve_existing_structure: %s" % payload["preserve_existing_structure"])
    print("stop_on_mismatch: %s" % payload["stop_on_mismatch"])
    if mismatch:
        print("mismatch: %s" % mismatch)


def cmd_workspace_bind(args):
    if not args.confirm:
        die("workspace bind requires human approval. Re-run with --confirm --by <name>.")
    config = load_project_config(args.root)
    config = bind_workspace_config(args.root, config, args.by or "user", allow_change=args.change)
    save_project_config(args.root, config)
    print("✓ workspace bound: %s" % config["workspace"]["realpath"])
    print("  workdir: %s" % config["workspace"]["plugin_workdir"])


def cmd_workspace_rebind(args):
    if not args.confirm:
        die("workspace rebind requires human approval. Re-run with --confirm --by <name> after clarifying the workspace structure.")
    config = load_project_config(args.root)
    config = bind_workspace_config(args.root, config, args.by or "user", allow_change=True)
    save_project_config(args.root, config)
    print("✓ workspace rebound: %s" % config["workspace"]["realpath"])
    print("  workdir: %s" % config["workspace"]["plugin_workdir"])


# ---------------------------------------------------------------- knowledge base
def knowledge_status_payload(root, config):
    kb = normalize_knowledge_base(config)
    return {
        "status": kb.get("status"),
        "mode": kb.get("mode"),
        "root": kb.get("root"),
        "realpath": kb.get("realpath"),
        "manifest": kb.get("manifest"),
        "sources": kb.get("sources", []),
        "confirmed_at": kb.get("confirmed_at"),
        "confirmed_by": kb.get("confirmed_by"),
        "no_knowledge_base_reason": kb.get("no_knowledge_base_reason"),
        "stop_on_mismatch": kb.get("stop_on_mismatch", True),
        "mismatch": knowledge_mismatch_reason(root, config),
    }


def cmd_knowledge_status(args):
    config = load_project_config(args.root)
    payload = knowledge_status_payload(args.root, config)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print("=== pm-flow knowledge base ===")
    print("status: %s" % payload["status"])
    print("mode: %s" % payload["mode"])
    print("root: %s" % (payload.get("root") or "-"))
    print("manifest: %s" % (payload.get("manifest") or "-"))
    print("sources: %d" % len(payload.get("sources", [])))
    print("confirmed_by: %s" % (payload.get("confirmed_by") or "-"))
    print("stop_on_mismatch: %s" % payload["stop_on_mismatch"])
    if payload.get("no_knowledge_base_reason"):
        print("reason: %s" % payload["no_knowledge_base_reason"])
    if payload.get("mismatch"):
        print("mismatch: %s" % payload["mismatch"])


def cmd_knowledge_bind(args):
    if not args.confirm:
        die("knowledge bind requires human approval. Re-run with --confirm --by <name>.")
    config = load_project_config(args.root)
    config = bind_knowledge_base_config(args.root, config, args, allow_change=args.change)
    save_project_config(args.root, config)
    payload = knowledge_status_payload(args.root, config)
    print("✓ knowledge base bound: %s/%s" % (payload["status"], payload["mode"]))
    if payload.get("root"):
        print("  root: %s" % payload["root"])
    if payload.get("manifest"):
        print("  manifest: %s" % payload["manifest"])
    if payload.get("no_knowledge_base_reason"):
        print("  reason: %s" % payload["no_knowledge_base_reason"])


def cmd_knowledge_rebind(args):
    if not args.confirm:
        die("knowledge rebind requires human approval. Re-run with --confirm --by <name> after clarifying the knowledge-base path.")
    config = load_project_config(args.root)
    config = bind_knowledge_base_config(args.root, config, args, allow_change=True)
    save_project_config(args.root, config)
    payload = knowledge_status_payload(args.root, config)
    print("✓ knowledge base rebound: %s/%s" % (payload["status"], payload["mode"]))
    if payload.get("root"):
        print("  root: %s" % payload["root"])
    if payload.get("manifest"):
        print("  manifest: %s" % payload["manifest"])
    if payload.get("no_knowledge_base_reason"):
        print("  reason: %s" % payload["no_knowledge_base_reason"])


# ---------------------------------------------------------------- CLI
def build_parser():
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--root", default=os.getcwd(), help="project root (default: current directory)")
    ap = argparse.ArgumentParser(prog="controller.py", parents=[parent], description="pm-flow stage state machine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", parents=[parent], help="initialize state.json")
    p_init.add_argument("type", choices=list(PATH_BY_TYPE.keys()))
    p_init.add_argument("--project", default="")
    p_init.add_argument("--requirement", default="")
    p_init.add_argument("--intake", default=None, help="requirement intake file path")
    p_init.add_argument("--context-root", action="append", default=None, help="context directory (repeatable)")
    p_init.add_argument("--context-file", action="append", default=None, help="context file (repeatable)")
    p_init.add_argument("--config", default=None, help="existing project path-mapping config JSON")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_attach = sub.add_parser("attach", parents=[parent], help="attach pm-flow to an existing project")
    p_attach.add_argument("type", choices=list(PATH_BY_TYPE.keys()))
    p_attach.add_argument("--project", default="")
    p_attach.add_argument("--requirement", default="")
    p_attach.add_argument("--intake", default=None, help="Requirement input file path")
    p_attach.add_argument("--context-root", action="append", default=None, help="contexttext，text")
    p_attach.add_argument("--context-file", action="append", default=None, help="contexttext，text")
    p_attach.add_argument("--config", default=None, help="Existing project path-mapping config JSON")
    p_attach.add_argument("--force", action="store_true")
    p_attach.set_defaults(func=cmd_init)

    p_status = sub.add_parser("status", parents=[parent], help="print status board")
    p_status.add_argument("--json", action="store_true", help="output machine-readable JSON")
    p_status.set_defaults(func=cmd_status)

    p_a = sub.add_parser("analyze", parents=[parent], help="generate/confirm the mandatory requirement-analysis precheck")
    p_a.add_argument("--artifact", default=None, help="requirement analysis file path (default requirement_analysis.md or project config mapping)")
    p_a.add_argument("--confirm", action="store_true", help="confirm requirement analysis is complete; only then may stages advance")
    p_a.add_argument("--force", action="store_true", help="overwrite existing requirement analysis file")
    p_a.add_argument("--by", default="user", help="analysis confirmer")
    p_a.set_defaults(func=cmd_analyze)

    p_c = sub.add_parser("confirm", parents=[parent], help="confirm stage output (todo->confirmed)")
    p_c.add_argument("stage", choices=STAGES_ALL)
    p_c.add_argument("--by", default="user")
    p_c.set_defaults(func=cmd_confirm)

    p_m = sub.add_parser("mark", parents=[parent], help="verify prerequisites + artifacts, persist done (confirmed->done)")
    p_m.add_argument("stage", choices=STAGES_ALL)
    p_m.add_argument("--artifact", default=None)
    p_m.set_defaults(func=cmd_mark)

    p_cl = sub.add_parser("close", parents=[parent], help="final gate; lock stage (done->closed)")
    p_cl.add_argument("stage", choices=STAGES_ALL)
    p_cl.add_argument("--checked", action="store_true", help="confirm the semantic checklist passed item by item")
    p_cl.add_argument("--by", default="user", help="semantic-check confirmer")
    p_cl.set_defaults(func=cmd_close)

    sub.add_parser("next", parents=[parent], help="advance to next unclosed stage").set_defaults(func=cmd_next)

    p_d = sub.add_parser("decide", parents=[parent], help="record a key decision")
    p_d.add_argument("stage", choices=STAGES_ALL)
    p_d.add_argument("--text", required=True)
    p_d.add_argument("--by", default="user")
    p_d.set_defaults(func=cmd_decide)

    p_r = sub.add_parser("review", parents=[parent], help="generate independent review checklist")
    p_r.add_argument("stage", choices=STAGES_ALL)
    p_r.set_defaults(func=cmd_review)

    p_v = sub.add_parser("validate", parents=[parent], help="P4 SSOT validation (state/contract/disk consistency; CI gate)")
    p_v.add_argument("--skill", default=SKILL_DIR, help="skill directory (default: controller's directory)")
    p_v.set_defaults(func=cmd_validate)

    p_ws = sub.add_parser("workspace", parents=[parent], help="confirm or inspect the project workspace binding")
    ws_sub = p_ws.add_subparsers(dest="workspace_cmd", required=True)
    p_ws_status = ws_sub.add_parser("status", parents=[parent], help="show workspace binding")
    p_ws_status.add_argument("--json", action="store_true", help="output JSON")
    p_ws_status.set_defaults(func=cmd_workspace_status)
    p_ws_bind = ws_sub.add_parser("bind", parents=[parent], help="confirm the workspace root without changing existing project structure")
    p_ws_bind.add_argument("--confirm", action="store_true", help="human-approved workspace confirmation")
    p_ws_bind.add_argument("--change", action="store_true", help="allow changing an existing workspace binding")
    p_ws_bind.add_argument("--by", default="user", help="human approver")
    p_ws_bind.set_defaults(func=cmd_workspace_bind)
    p_ws_rebind = ws_sub.add_parser("rebind", parents=[parent], help="change workspace root after human approval")
    p_ws_rebind.add_argument("--confirm", action="store_true", help="human-approved workspace change")
    p_ws_rebind.add_argument("--by", default="user", help="human approver")
    p_ws_rebind.set_defaults(func=cmd_workspace_rebind)

    p_kb = sub.add_parser("knowledge", parents=[parent], help="confirm or inspect the project knowledge-base binding")
    kb_sub = p_kb.add_subparsers(dest="knowledge_cmd", required=True)
    p_kb_status = kb_sub.add_parser("status", parents=[parent], help="show knowledge-base binding")
    p_kb_status.add_argument("--json", action="store_true", help="output JSON")
    p_kb_status.set_defaults(func=cmd_knowledge_status)
    p_kb_bind = kb_sub.add_parser("bind", parents=[parent], help="confirm the knowledge-base path or no-knowledge-base decision")
    kb_bind_mode = p_kb_bind.add_mutually_exclusive_group()
    kb_bind_mode.add_argument("--knowledge-root", default=None, help="human-confirmed knowledge-base root")
    kb_bind_mode.add_argument("--none", dest="no_knowledge_base", action="store_true",
                              help="human confirmed no external knowledge base is used")
    p_kb_bind.add_argument("--manifest", default=None, help="knowledge-base manifest or index file")
    p_kb_bind.add_argument("--source", action="append", default=None, help="additional confirmed source file")
    p_kb_bind.add_argument("--reason", default=None, help="required when --none is used")
    p_kb_bind.add_argument("--confirm", action="store_true", help="human-approved knowledge-base confirmation")
    p_kb_bind.add_argument("--change", action="store_true", help="allow changing an existing knowledge-base binding")
    p_kb_bind.add_argument("--by", default="user", help="human approver")
    p_kb_bind.set_defaults(func=cmd_knowledge_bind)
    p_kb_rebind = kb_sub.add_parser("rebind", parents=[parent], help="change knowledge-base binding after human approval")
    kb_rebind_mode = p_kb_rebind.add_mutually_exclusive_group()
    kb_rebind_mode.add_argument("--knowledge-root", default=None, help="new human-confirmed knowledge-base root")
    kb_rebind_mode.add_argument("--none", dest="no_knowledge_base", action="store_true",
                                help="human confirmed no external knowledge base is used")
    p_kb_rebind.add_argument("--manifest", default=None, help="knowledge-base manifest or index file")
    p_kb_rebind.add_argument("--source", action="append", default=None, help="additional confirmed source file")
    p_kb_rebind.add_argument("--reason", default=None, help="required when --none is used")
    p_kb_rebind.add_argument("--confirm", action="store_true", help="human-approved knowledge-base change")
    p_kb_rebind.add_argument("--by", default="user", help="human approver")
    p_kb_rebind.set_defaults(func=cmd_knowledge_rebind)

    p_ctx = sub.add_parser("context", parents=[parent], help="view or validate context intake")
    ctx_sub = p_ctx.add_subparsers(dest="context_cmd", required=True)
    p_ctx_status = ctx_sub.add_parser("status", parents=[parent], help="view context status")
    p_ctx_status.add_argument("--json", action="store_true", help="output machine-readable JSON")
    p_ctx_status.set_defaults(func=cmd_context_status)
    ctx_sub.add_parser("validate", parents=[parent], help="validate context intake").set_defaults(func=cmd_context_validate)
    p_ctx_confirm = ctx_sub.add_parser("confirm", parents=[parent], help="generate/confirm context intake confirmation")
    p_ctx_confirm.add_argument("--artifact", default=None, help="context intake confirmation file path (default context_confirmation.md or project config mapping)")
    p_ctx_confirm.add_argument("--confirm", action="store_true", help="confirm the context intake is complete")
    p_ctx_confirm.add_argument("--force", action="store_true", help="overwrite existing context intake confirmation file")
    p_ctx_confirm.add_argument("--by", default="user", help="confirmer")
    p_ctx_confirm.set_defaults(func=cmd_context_confirm)

    p_s = sub.add_parser("scaffold", parents=[parent],
                         help="lay prototype skeleton (web admin / review / mobile) into <root>/prototypes/")
    p_s.add_argument("--name", default="Product Prototype", help="project name; injected into title and brand logo")
    p_s.add_argument("--force", action="store_true", help="overwrite existing files")
    p_s.set_defaults(func=cmd_scaffold)
    return ap


def main():
    args = build_parser().parse_args()
    if args.cmd not in ("init", "attach", "workspace", "knowledge"):
        assert_workspace_current(args.root)
        assert_knowledge_base_current(args.root)
    args.func(args)


if __name__ == "__main__":
    main()
