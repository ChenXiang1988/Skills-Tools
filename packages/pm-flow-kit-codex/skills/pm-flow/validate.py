#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pm-flow SSOT validator.

Checks consistency between state.json, contract_config.json, and on-disk artifacts.
Also checks prototype review HTML files when the prototype stage is done or closed.
Exit code: 0 for no errors, 1 for errors.
"""

import argparse
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

STAGES_ALL = ["research", "boundary", "prototype", "prd", "review"]
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
WORKSPACE_DEFAULT_WORKDIR = ".pm-flow/work"
CONFIG_ARTIFACT_KEYS = STAGES_ALL + [
    REQUIREMENT_ANALYSIS_KEY,
    SCENARIO_CATALOG_KEY,
    USE_CASES_KEY,
    END_TO_END_FLOW_KEY,
    METRICS_DEFINITION_KEY,
    ARTIFACT_PLAN_KEY,
    CONTEXT_CONFIRMATION_KEY,
]

# reviewtext（text CDN），text http(s) text
EXT_ALLOW = ("fonts.googleapis.com", "fonts.gstatic.com")
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


def _class_set(attrs):
    classes = attrs.get("class", "")
    return set(classes.split())


class ReviewDocParser(HTMLParser):
    """Extract review-doc links from real HTML attributes, not sample text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.context_stack = []
        self.ui_keys = set()
        self.doc_keys = set()
        self.urls = []

    def _handle_start(self, tag, attrs, push):
        attrs = dict(attrs)
        classes = _class_set(attrs)
        parent = self.context_stack[-1] if self.context_stack else None

        if "pane-ui" in classes:
            context = "ui"
        elif "pane-doc" in classes:
            context = "doc"
        else:
            context = parent
        for attr in ("src", "href"):
            url = attrs.get(attr)
            if url and url.startswith(("http://", "https://")):
                self.urls.append(url)

        key = attrs.get("data-link")
        if key:
            if context == "ui":
                self.ui_keys.add(key)
            elif context == "doc":
                self.doc_keys.add(key)

        if push and tag not in VOID_TAGS:
            self.context_stack.append(context)

    def handle_starttag(self, tag, attrs):
        self._handle_start(tag, attrs, push=True)

    def handle_startendtag(self, tag, attrs):
        self._handle_start(tag, attrs, push=False)

    def handle_endtag(self, tag):
        if self.context_stack:
            self.context_stack.pop()


def _parse_review_doc(html):
    parser = ReviewDocParser()
    parser.feed(html)
    return parser


def load_json(path):
    if not os.path.isfile(path):
        return None, "text: %s" % path
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f), None
    except Exception as e:  # noqa: BLE001
        return None, "JSON text: %s (%s)" % (path, e)


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def resolve_project_path(root, path):
    if not path:
        return path
    if os.path.isabs(path):
        return path
    return os.path.join(root, path)


def canonical_root(root):
    return os.path.realpath(os.path.abspath(root))


def load_project_config(root):
    p = os.path.join(root, ".pm-flow", "project_config.json")
    if not os.path.isfile(p):
        return {}, None
    return load_json(p)


def as_bool(value, default):
    if value is None:
        return default
    return bool(value)


def normalize_plugin_workdir(workdir):
    workdir = workdir or WORKSPACE_DEFAULT_WORKDIR
    if os.path.isabs(workdir):
        return workdir
    normalized = os.path.normpath(workdir)
    return normalized


def validate_workspace_binding(root, project_config, errors):
    workspace = project_config.get("workspace") if isinstance(project_config.get("workspace"), dict) else None
    if not workspace:
        errors.append("workspace root is not confirmed; run workspace bind --confirm before product work")
        return
    expected = workspace.get("realpath") or workspace.get("root")
    current = canonical_root(root)
    if as_bool(workspace.get("stop_on_mismatch"), True) and expected and expected != current:
        errors.append("workspace root changed: bound=%s current=%s" % (expected, current))
    workdir = normalize_plugin_workdir(workspace.get("plugin_workdir"))
    if os.path.isabs(workdir):
        errors.append("workspace.plugin_workdir must be relative to workspace root: %s" % workdir)
    elif workdir in (".", "") or workdir.startswith(".."):
        errors.append("workspace.plugin_workdir must stay inside workspace root: %s" % workdir)
    elif not os.path.isdir(resolve_project_path(root, workdir)):
        errors.append("workspace plugin workdir missing: %s" % workdir)
    if not as_bool(workspace.get("preserve_existing_structure"), True):
        errors.append("workspace.preserve_existing_structure must remain true")


def default_knowledge_base():
    return {
        "status": "unconfirmed",
        "mode": "unknown",
        "root": None,
        "realpath": None,
        "manifest": None,
        "sources": [],
        "confirmed_at": None,
        "confirmed_by": None,
        "no_knowledge_base_reason": None,
        "stop_on_mismatch": True,
    }


def normalize_knowledge_base(project_config):
    out = default_knowledge_base()
    kb = project_config.get("knowledge_base") if isinstance(project_config.get("knowledge_base"), dict) else None
    if kb:
        out.update(kb)
    out["sources"] = as_list(out.get("sources"))
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


def validate_knowledge_base_binding(root, project_config, errors):
    kb = normalize_knowledge_base(project_config)
    if kb.get("status") != "confirmed":
        errors.append("knowledge base is not confirmed; ask the human for the knowledge-base path or bind --none with a reason")
        return
    mode = kb.get("mode")
    if mode == "none":
        if not kb.get("no_knowledge_base_reason"):
            errors.append("knowledge_base.mode=none requires no_knowledge_base_reason")
        return
    if mode == "root":
        root_path = kb.get("root")
        if not root_path:
            errors.append("knowledge_base.mode=root requires root")
            return
        current = resolve_knowledge_root(root, root_path)
        if not current or not os.path.isdir(current):
            errors.append("knowledge-base root missing: %s" % root_path)
            return
        expected = kb.get("realpath")
        if as_bool(kb.get("stop_on_mismatch"), True) and expected and expected != os.path.realpath(current):
            errors.append("knowledge-base root changed: bound=%s current=%s" % (expected, os.path.realpath(current)))
        manifest = kb.get("manifest")
        if not manifest:
            errors.append("knowledge_base.mode=root requires manifest")
        elif not os.path.isfile(resolve_knowledge_path(root, kb, manifest)):
            errors.append("knowledge-base manifest missing: %s" % manifest)
        for src in kb.get("sources", []):
            if src and not os.path.exists(resolve_knowledge_path(root, kb, src)):
                errors.append("knowledge-base source missing: %s" % src)
        return
    if mode == "files":
        if not kb.get("sources"):
            errors.append("knowledge_base.mode=files requires sources")
        for src in kb.get("sources", []):
            if src and not os.path.exists(resolve_knowledge_path(root, kb, src)):
                errors.append("knowledge-base source missing: %s" % src)
        return
    errors.append("knowledge_base.mode is invalid or unconfirmed: %s" % mode)


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
    return out


def open_conflicts(state, stage=None):
    conflicts = []
    for c in normalize_context(state.get("context", {})).get("conflicts", []):
        if c.get("status", "open") == "resolved":
            continue
        if stage is None or c.get("stage") in (None, stage):
            conflicts.append(c)
    return conflicts


def effective_required_artifacts(contract, project_config, stage):
    global_required = effective_requirement_analysis_artifacts(contract, project_config)
    mapped = project_config.get("artifacts", {}).get(stage)
    if mapped:
        stage_required = as_list(mapped)
    else:
        stage_required = contract.get("stages", {}).get(stage, {}).get("required_artifacts", [])
    return list(dict.fromkeys(global_required + stage_required))


def effective_requirement_analysis_artifacts(contract, project_config):
    artifacts = contract.get("global_preflight", {}).get(
        "required_artifacts", [REQUIREMENT_ANALYSIS_DEFAULT_ARTIFACT]
    )
    mapped_requirement = project_config.get("artifacts", {}).get(REQUIREMENT_ANALYSIS_KEY)
    mapped_scenario = project_config.get("artifacts", {}).get(SCENARIO_CATALOG_KEY)
    mapped_use_cases = project_config.get("artifacts", {}).get(USE_CASES_KEY)
    mapped_end_to_end_flow = project_config.get("artifacts", {}).get(END_TO_END_FLOW_KEY)
    mapped_metrics = project_config.get("artifacts", {}).get(METRICS_DEFINITION_KEY)
    mapped_artifact_plan = project_config.get("artifacts", {}).get(ARTIFACT_PLAN_KEY)
    mapped_context = project_config.get("artifacts", {}).get(CONTEXT_CONFIRMATION_KEY)
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


def effective_context_confirmation_artifacts(project_config):
    mapped = project_config.get("artifacts", {}).get(CONTEXT_CONFIRMATION_KEY)
    if mapped:
        return as_list(mapped)
    return [CONTEXT_CONFIRMATION_DEFAULT_ARTIFACT]


def artifact_exists(root, pattern):
    # text glob text（text *.html text prototypes/*.html）
    if any(ch in pattern for ch in "*?["):
        return len(glob.glob(os.path.join(root, pattern), recursive=True)) > 0
    return os.path.isfile(os.path.join(root, pattern))


def _stage_has_artifact(root, stage_state, required_artifacts):
    """done/closed text stage YesNotextartifact。"""
    art = stage_state.get("artifact")
    if art and artifact_exists(root, art):
        return True
    for r in required_artifacts:
        if artifact_exists(root, r):
            return True
    return False


def _missing_required_artifacts(root, required_artifacts):
    return [r for r in required_artifacts if not artifact_exists(root, r)]


def effective_stage_artifacts(contract, project_config, stage):
    mapped = project_config.get("artifacts", {}).get(stage)
    if mapped:
        return as_list(mapped)
    return contract.get("stages", {}).get(stage, {}).get("required_artifacts", [])


def matched_artifact_paths(root, patterns):
    files = []
    for pattern in patterns:
        if any(ch in pattern for ch in "*?["):
            files.extend(glob.glob(os.path.join(root, pattern), recursive=True))
            continue
        path = os.path.join(root, pattern)
        if os.path.isfile(path):
            files.append(path)
    return list(dict.fromkeys(files))


def _read_first_stage_artifact(root, contract, project_config, stage):
    files = matched_artifact_paths(root, effective_stage_artifacts(contract, project_config, stage))
    if not files:
        return None, "%s stage artifact is missing" % stage
    try:
        with open(files[0], encoding="utf-8") as f:
            return f.read(), None
    except Exception as e:  # noqa: BLE001
        return None, "%s stage artifact cannot be read: %s (%s)" % (stage, files[0], e)


def _line_value(content, label):
    pattern = r"(?im)^\s*-\s*%s:\s*(.+?)\s*$" % re.escape(label)
    match = re.search(pattern, content)
    return match.group(1).strip() if match else ""


def _has_file_or_non_applicability(content, names):
    lowered = content.lower()
    if "not applicable" in lowered or "non-applicability" in lowered:
        return True
    return any(name in lowered for name in names)


def _validate_prd_content(content):
    errors = []
    lowered = content.lower()
    if len(content.strip()) < 700:
        errors.append("prd.md is too short to be a completed PRD")
    forbidden_tokens = [
        "{Requirement Name}",
        "Paste the selected L1, L2, or L3 template body here",
        "PRD level: L1 / L2 / L3",
        "Decision 1:",
        "Decision 2:",
    ]
    for token in forbidden_tokens:
        if token in content:
            errors.append("prd.md still contains template placeholder: %s" % token)
    if not re.search(r"(?im)^\s*-\s*PRD level:\s*L[123]\b", content):
        errors.append("prd.md must include an explicit PRD level: L1, L2, or L3")
    if "scope" not in lowered or ("non-scope" not in lowered and "out of scope" not in lowered):
        errors.append("prd.md must include scope and non-scope/out-of-scope content")
    if "acceptance criteria" not in lowered and not all(term in lowered for term in ("given:", "when:", "then:")):
        errors.append("prd.md must include acceptance criteria")
    if not _has_file_or_non_applicability(
        content,
        ("metrics-definition.md", "scenario-catalog.md", "use-cases.md", "end-to-end-flow.md"),
    ):
        errors.append("prd.md must reference metrics/scenario/use-case/flow artifacts or record non-applicability")
    return errors


def _validate_review_content(content):
    errors = []
    if len(content.strip()) < 500:
        errors.append("review.md is too short to be a completed review")
    forbidden_tokens = [
        "{Requirement Name}",
        "High / Medium / Low",
        "Ready / Rework required",
        "| 1 |  |",
        "- [ ] Independent review was performed.",
    ]
    for token in forbidden_tokens:
        if token in content:
            errors.append("review.md still contains template placeholder: %s" % token)
    reviewer = _line_value(content, "Reviewer")
    if not reviewer:
        errors.append("review.md must name the independent reviewer")
    missing_decisions = _line_value(content, "Missing decisions")
    if not missing_decisions:
        errors.append("review.md must complete the decision check")
    conclusion = _line_value(content, "Overall conclusion")
    if conclusion not in ("Ready", "Rework required"):
        errors.append("review.md must set overall conclusion to Ready or Rework required")
    if "[x] Independent review was performed." not in content:
        errors.append("review.md close checklist must confirm independent review")
    if not re.search(r"(?m)^\|\s*\d+\s*\|\s*[^|\s][^|]*\|\s*(High|Medium|Low)\s*\|\s*[^|]+\|\s*(Closed|Recorded as unresolved)\s*\|", content):
        errors.append("review.md must include at least one finding or explicit closed/no-finding row")
    return errors


def validate_stage_content(root, contract, project_config, stage):
    if stage not in ("prd", "review"):
        return []
    content, err = _read_first_stage_artifact(root, contract, project_config, stage)
    if err:
        return [err]
    if stage == "prd":
        return _validate_prd_content(content)
    return _validate_review_content(content)


def _stage_html_files(root, stage_state, required_artifacts):
    """text stage textMediumtext .html text（text）。"""
    files = []
    art = stage_state.get("artifact")
    if art and art.endswith(".html") and artifact_exists(root, art):
        files.append(os.path.join(root, art))
    for r in required_artifacts:
        if r.endswith(".html"):
            files.extend(glob.glob(os.path.join(root, r), recursive=True))
    return list(dict.fromkeys(files))


def _is_review_doc(html):
    return ("review-stage" in html) or ('id="conn-svg"' in html) \
        or ('conn-svg' in html and 'pane-ui' in html)


def _check_review_doc(path, html, errors, warnings):
    """textreviewtext html text。"""
    base = os.path.basename(path)
    parsed = _parse_review_doc(html)
    # text：text http(s) text（text CDN）
    for url in parsed.urls:
        if not any(a in url for a in EXT_ALLOW):
            errors.append("reviewtext %s referencetext: %s" % (base, url))
    if not _is_review_doc(html):
        return  # textreviewtext（textmobile/PC Ptext），text
    # reviewtext
    if 'id="conn-svg"' not in html and 'conn-svg' not in html:
        errors.append("reviewtext %s text #conn-svg（text SVG text）" % base)
    if 'connect-lines.js' not in html:
        errors.append("reviewtext %s text connect-lines.js" % base)
    # data-link text：text HTML text，text / code sample。
    if parsed.ui_keys or parsed.doc_keys:
        for k in sorted(parsed.ui_keys - parsed.doc_keys):
            errors.append("reviewtext %s：UI text data-link='%s' text" % (base, k))
        for k in sorted(parsed.doc_keys - parsed.ui_keys):
            errors.append("reviewtext %s：text data-link='%s' text UI text" % (base, k))
    else:
        warnings.append("reviewtext %s text pane-ui/pane-doc text，text data-link text" % base)


def _validate_prototype(root, stage_state, required_artifacts, errors, warnings):
    """prototype stage done/closed text，textreviewtext。"""
    for p in _stage_html_files(root, stage_state, required_artifacts):
        try:
            with open(p, encoding="utf-8") as f:
                html = f.read()
        except Exception as e:  # noqa: BLE001
            errors.append("reviewtext: %s (%s)" % (p, e))
            continue
        if not _is_review_doc(html):
            continue  # textreviewtext（textPtext），text 4b textvalidation
        _check_review_doc(p, html, errors, warnings)


def _validate_context(root, state, errors, warnings):
    ctx = normalize_context(state.get("context", {}))
    mode = ctx.get("mode")
    if mode not in ("none", "inline", "files", "root", "auto"):
        errors.append("context.mode text: %s" % mode)
        return
    if mode == "none":
        return

    def exists(path):
        return os.path.exists(resolve_project_path(root, path))

    if mode == "root":
        root_path = ctx.get("root")
        if not root_path:
            errors.append("context.mode=root text context.root")
        elif not os.path.isdir(resolve_project_path(root, root_path)):
            errors.append("context.root textYestext: %s" % root_path)
        manifest = ctx.get("manifest")
        if not manifest:
            errors.append("context.mode=root text manifest")
        elif not os.path.isfile(resolve_project_path(root, manifest)):
            errors.append("context manifest text: %s" % manifest)

    for src in ctx.get("sources", []):
        if src and not exists(src):
            warnings.append("context source text: %s" % src)

    conflicts = open_conflicts(state)
    if conflicts:
        errors.append("textcontexttext: %d text" % len(conflicts))


def _validate_stage_context_ref(state, stage, errors):
    ctx = normalize_context(state.get("context", {}))
    refs = ctx.get("stage_refs", {})
    ref = refs.get(stage)
    if not ref:
        errors.append("stage '%s' text closed，text context.stage_refs text" % stage)
        return
    if not ref.get("sources") and not ref.get("no_context_reason"):
        errors.append("stage '%s' text closed，textcontextreferencetext no_context_reason" % stage)


def _validate_requirement_analysis(root, state, contract, project_config, errors):
    artifacts = effective_requirement_analysis_artifacts(contract, project_config)
    active = False
    for s in state.get("path", []):
        if state.get("stages", {}).get(s, {}).get("status") in ("confirmed", "done", "closed"):
            active = True
            break
    if not active:
        return

    missing = _missing_required_artifacts(root, artifacts)
    if missing:
        errors.append("Requirementtext，text: %s" % ", ".join(missing))
    analysis = state.get(REQUIREMENT_ANALYSIS_KEY, {})
    if not isinstance(analysis, dict):
        errors.append("state.json Medium requirement_analysis text")
        return
    if analysis.get("status") != "confirmed" or not analysis.get("confirmed_at"):
        errors.append("Requirementtextconfirm，text stage")


def _validate_context_confirmation(root, state, project_config, errors):
    active = False
    for s in state.get("path", []):
        if state.get("stages", {}).get(s, {}).get("status") in ("confirmed", "done", "closed"):
            active = True
            break
    analysis = state.get(REQUIREMENT_ANALYSIS_KEY, {})
    if isinstance(analysis, dict) and analysis.get("status") == "confirmed":
        active = True
    if not active:
        return

    artifacts = effective_context_confirmation_artifacts(project_config)
    missing = _missing_required_artifacts(root, artifacts)
    if missing:
        errors.append("knowledge basetextconfirmtext，text: %s" % ", ".join(missing))

    ctx = normalize_context(state.get("context", {}))
    confirmation = ctx.get("confirmation", {})
    if not isinstance(confirmation, dict):
        errors.append("state.json Medium context.confirmation text")
        return
    if confirmation.get("status") != "confirmed" or not confirmation.get("confirmed_at"):
        errors.append("knowledge basetextconfirmtextconfirm，textRequirementtext stage")


def run_validation(root, skill_dir):
    """text (errors, warnings, ok)。"""
    errors = []
    warnings = []

    state, err = load_json(os.path.join(root, ".pm-flow", "state.json"))
    if err:
        return [err], warnings, False
    contract, cerr = load_json(os.path.join(skill_dir, "contract_config.json"))
    if cerr:
        return [cerr], warnings, False
    project_config, pcerr = load_project_config(root)
    if pcerr:
        return [pcerr], warnings, False

    # 2. state text
    REQUIRED_KEYS = ("schema_version", "project", "requirement",
                      "requirement_type", "current_stage", "path",
                      "stages", "decisions", "artifacts")
    for k in REQUIRED_KEYS:
        if k not in state:
            errors.append("state.json textfield: %s" % k)

    path = state.get("path", [])
    stages = state.get("stages", {})
    contract_stages = contract.get("stages", {})
    if "context" not in state:
        warnings.append("state.json text context field，text mode=none text")
    validate_workspace_binding(root, project_config, errors)
    validate_knowledge_base_binding(root, project_config, errors)
    _validate_context(root, state, errors, warnings)

    _validate_context_confirmation(root, state, project_config, errors)
    _validate_requirement_analysis(root, state, contract, project_config, errors)

    for s in project_config.get("artifacts", {}):
        if s not in CONFIG_ARTIFACT_KEYS:
            errors.append("project_config.artifacts text stage: %s" % s)

    # 3. path text（text：path→contract text text stage）
    for s in path:
        if s not in STAGES_ALL:
            errors.append("state.path text stage: %s" % s)
        if s not in contract_stages:
            errors.append("state.path text stage '%s' text contract_config MediumNonetext" % s)
    # contract Mediumtext path text stage text（text）

    # 4. stages statustext
    for s in path:
        st = stages.get(s, {})
        st_status = st.get("status")
        if st_status not in STATUS_FLOW:
            errors.append("stage '%s' statustext: %s" % (s, st_status))
            continue
        required_artifacts = effective_required_artifacts(contract, project_config, s)
        idx = path.index(s)
        # 4a. text
        if st_status in ("done", "closed"):
            for pre in path[:idx]:
                pre_status = stages.get(pre, {}).get("status")
                if pre_status != "closed":
                    errors.append("stage '%s' status=%s，text '%s' status=%s（text closed）"
                                 % (s, st_status, pre, pre_status))
        # 4b. artifacttext
        if st_status in ("done", "closed"):
            missing_required = _missing_required_artifacts(root, required_artifacts)
            if missing_required:
                errors.append("stage '%s' status=%s，text: %s"
                             % (s, st_status, ", ".join(missing_required)))
            for content_error in validate_stage_content(root, contract, project_config, s):
                errors.append("stage '%s' status=%s content: %s" % (s, st_status, content_error))
        if st_status == "confirmed" and matched_artifact_paths(root, effective_stage_artifacts(contract, project_config, s)):
            for content_error in validate_stage_content(root, contract, project_config, s):
                errors.append("stage '%s' status=%s content: %s" % (s, st_status, content_error))
        # 4c. closed textconfirmtext
        if st_status == "closed" and contract_stages.get(s, {}).get("semantic_checks"):
            if not st.get("semantic_checked_at") or not st.get("semantic_checked_by"):
                errors.append("stage '%s' text closed，text semantic_checked_at/semantic_checked_by textconfirmtext" % s)
            _validate_stage_context_ref(state, s, errors)
        # 4d. prototype reviewtext（text done/closed textreviewtext）
        if s == "prototype" and st_status in ("done", "closed"):
            _validate_prototype(root, st, required_artifacts, errors, warnings)

    # 5. current_stage text
    cs = state.get("current_stage")
    if cs not in path:
        errors.append("current_stage '%s' text path Medium" % cs)
    else:
        cs_status = stages.get(cs, {}).get("status")
        all_closed = all(stages.get(s, {}).get("status") == "closed" for s in path)
        if cs_status == "closed" and not all_closed:
            warnings.append("current_stage '%s' text closed（flowtext，textconfirmYesNotext）" % cs)

    # 6. decisions referencetext stage text
    for d in state.get("decisions", []):
        ds = d.get("stage")
        if ds not in STAGES_ALL:
            errors.append("decisions referencetext stage: %s" % ds)

    # 7. artifacts text
    for s, p in state.get("artifacts", {}).items():
        if s == REQUIREMENT_ANALYSIS_KEY:
            continue
        if s == CONTEXT_CONFIRMATION_KEY:
            continue
        if s not in stages:
            errors.append("artifacts text stage: %s" % s)
        elif stages[s].get("artifact") != p:
            warnings.append("artifacts['%s']=%s text stages['%s'].artifact=%s text"
                            % (s, p, s, stages[s].get("artifact")))

    ok = len(errors) == 0
    return errors, warnings, ok


def main():
    ap = argparse.ArgumentParser(prog="validate.py", description="pm-flow P4 · SSOT validationtext")
    ap.add_argument("--root", default=os.getcwd(), help="Projecttext（text）")
    ap.add_argument("--skill", default=os.path.dirname(os.path.abspath(__file__)),
                    help="skill text（text）")
    args = ap.parse_args()

    print("=== pm-flow P4 · SSOT validation ===")
    print("Projecttext：%s" % args.root)
    print("skilltext：%s" % args.skill)
    errors, warnings, ok = run_validation(args.root, args.skill)
    for w in warnings:
        print("  ⚠ warning: %s" % w)
    for e in errors:
        print("  ✗ error: %s" % e)
    if ok:
        print("✓ validationtext（Noneerror，%d warning）" % len(warnings))
        sys.exit(0)
    else:
        print("✗ validationtext：%d texterror，%d warning" % (len(errors), len(warnings)))
        sys.exit(1)


if __name__ == "__main__":
    main()
