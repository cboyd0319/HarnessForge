from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from . import __version__
from .models import WriteResult
from .paths import is_inside_root
from .redact import redact_local_paths

SCHEMA_VERSION = "harnessforge.blueprints.v1"
MANIFEST_SCHEMA_VERSION = "harnessforge.blueprintManifest.v1"
BLUEPRINT_ROOT = "docs/harness/blueprints"


@dataclass(frozen=True)
class Blueprint:
    id: str
    title: str
    summary: str
    domains: tuple[str, ...]
    fit_signals: tuple[str, ...]
    review_questions: tuple[str, ...]
    operating_model: tuple[str, ...]
    generated_review_items: tuple[str, ...]
    verification_gates: tuple[str, ...]
    promotion_gates: tuple[str, ...]

    @property
    def relative_path(self) -> str:
        return f"{BLUEPRINT_ROOT}/{self.id}.md"

    @property
    def generated_files(self) -> tuple[str, ...]:
        return (
            f"{BLUEPRINT_ROOT}/README.md",
            self.relative_path,
            f"{BLUEPRINT_ROOT}/manifest.json",
        )


BLUEPRINTS: tuple[Blueprint, ...] = (
    Blueprint(
        id="agentic-app",
        title="Agentic Application Blueprint",
        summary=(
            "Plan, build, verify, and release applications that include agent "
            "behavior, tool calls, autonomous actions, or model-mediated output."
        ),
        domains=("agent-runtime", "tooling", "evaluation", "release"),
        fit_signals=(
            "The product calls model APIs, local agents, hosted assistants, or tool routers.",
            "Agent outputs can change user-visible behavior, data, files, or workflows.",
            "Quality depends on prompts, policies, retrieval, tools, evals, and runtime safety.",
        ),
        review_questions=(
            "Which agent actions can change state, spend money, expose data, or contact users?",
            "What evidence proves the agent path works beyond static lint or unit tests?",
            "Where are prompt, tool, model, policy, and eval versions pinned or recorded?",
            "How does the project handle refusal, timeout, malformed output, and rollback?",
        ),
        operating_model=(
            "Map every agent capability to owner, input, output, authority, and failure mode.",
            "Separate local developer preferences from generated project instructions.",
            "Keep model, prompt, tool, and policy changes reviewable as product code.",
            "Require representative task runs before claiming agent effectiveness.",
        ),
        generated_review_items=(
            "Agent authority matrix with allowed tools, denied tools, and approval thresholds.",
            "Evaluation fixture list covering success, refusal, invalid output, and rollback paths.",
            "Runtime observability notes for request IDs, traces, redaction, and incident review.",
            "Release checklist entry for model, prompt, tool, and policy version changes.",
        ),
        verification_gates=(
            "Run structural checks for generated harness files and instruction routing.",
            "Run deterministic unit tests for tool schemas, output parsers, and guardrails.",
            "Run at least one representative agent task before release candidate promotion.",
            "Record skipped real-agent checks with owner, risk, and exact follow-up.",
        ),
        promotion_gates=(
            "No unreviewed tool authority expansion.",
            "No undocumented model or prompt change in release scope.",
            "No open high-risk eval regression or missing rollback path.",
        ),
    ),
    Blueprint(
        id="spec-driven",
        title="Spec-Driven Project Blueprint",
        summary=(
            "Turn product intent into executable specs, plans, task slices, and "
            "verification evidence before broad implementation."
        ),
        domains=("specification", "planning", "traceability", "verification"),
        fit_signals=(
            "The repo benefits from feature specs, acceptance criteria, and task plans.",
            "Multiple agents or humans need a stable contract before implementation.",
            "The project needs traceability from requirements to tests and release notes.",
        ),
        review_questions=(
            "Where do feature specs live, and what template defines done criteria?",
            "Which requirements are non-goals, constraints, security boundaries, or rollback needs?",
            "How are implementation tasks tied back to specs and acceptance checks?",
            "What evidence must exist before a task is marked complete?",
        ),
        operating_model=(
            "Create a small feature brief before implementation begins.",
            "Make acceptance criteria testable and link them to focused verification commands.",
            "Keep implementation plans separate from durable repo policy.",
            "Reject vague done states that only say code was written.",
        ),
        generated_review_items=(
            "Spec template with problem, non-goals, acceptance, data boundaries, and rollback.",
            "Plan template with ordered tasks, changed surfaces, verification, and open risks.",
            "Traceability note linking requirements to tests, docs, and release evidence.",
        ),
        verification_gates=(
            "Every active spec has at least one runnable or explicitly manual acceptance check.",
            "Implementation plans name files, commands, and rollback strategy when risk warrants it.",
            "Completed specs cite verification evidence rather than status-only claims.",
        ),
        promotion_gates=(
            "No release item lacks acceptance criteria.",
            "No spec-critical behavior merges without named verification evidence.",
            "No unresolved ownerless ambiguity in active implementation scope.",
        ),
    ),
    Blueprint(
        id="web-service",
        title="Web Service Blueprint",
        summary=(
            "Shape harness guidance for APIs, web apps, backend services, and "
            "frontend-backed product workflows."
        ),
        domains=("web", "api", "frontend", "operations"),
        fit_signals=(
            "The repo exposes HTTP routes, UI flows, API clients, or server-rendered pages.",
            "Correctness depends on accessibility, auth, state transitions, or deployments.",
            "Verification needs browser checks, API tests, or local service startup.",
        ),
        review_questions=(
            "Which commands start the app, run API checks, and run browser checks?",
            "What auth, role, data, and accessibility paths are required before release?",
            "Which routes or screens are critical enough to require visual or interaction evidence?",
        ),
        operating_model=(
            "Detect framework, package manager, app entrypoints, and test commands.",
            "Keep local dev startup, API checks, and UI checks visible in the verification matrix.",
            "Treat accessibility, auth, and data-loss behavior as release-blocking when relevant.",
        ),
        generated_review_items=(
            "Critical route inventory with owner, startup command, and verification method.",
            "Browser smoke checklist for layout, navigation, form validation, and error states.",
            "API contract checklist for auth, validation, pagination, and failure responses.",
        ),
        verification_gates=(
            "Run unit or integration checks for changed API surfaces.",
            "Run browser or screenshot verification for changed user-facing flows.",
            "Run accessibility checks for changed interactive UI where tooling is available.",
        ),
        promotion_gates=(
            "No critical route lacks a named verification command or manual check.",
            "No auth or data mutation change ships without negative-path coverage.",
            "No visible UI change ships without responsive inspection.",
        ),
    ),
    Blueprint(
        id="data-ml",
        title="Data And ML Blueprint",
        summary=(
            "Improve harness coverage for data pipelines, notebooks, analytics, "
            "models, benchmarks, and result artifacts."
        ),
        domains=("data", "ml", "benchmarking", "reproducibility"),
        fit_signals=(
            "The repo contains notebooks, datasets, training scripts, benchmarks, or reports.",
            "Outputs depend on data snapshots, model versions, random seeds, or hardware.",
            "Quality claims need reproducibility notes, metric definitions, and artifact handling.",
        ),
        review_questions=(
            "Which datasets, model artifacts, and result files are inputs versus generated outputs?",
            "Which metrics define success, and what variance or confidence bounds are acceptable?",
            "What data privacy, licensing, retention, and redaction boundaries apply?",
            "Which checks are deterministic enough for CI versus local/manual review?",
        ),
        operating_model=(
            "Separate source data contracts from generated result artifacts.",
            "Record metric definitions, seeds, sampling, and hardware assumptions.",
            "Avoid committing large or sensitive outputs unless the repo policy allows it.",
            "Prefer small deterministic fixtures for routine checks and larger runs for promotion.",
        ),
        generated_review_items=(
            "Data boundary map for source data, derived data, model artifacts, and result logs.",
            "Metric contract with target, tolerance, fixture, and promotion threshold.",
            "Artifact retention note for notebooks, benchmark outputs, and generated reports.",
        ),
        verification_gates=(
            "Run deterministic fixture tests for parsing, transforms, and metric calculations.",
            "Run benchmark or representative sample checks before claiming quality improvements.",
            "Record non-deterministic checks with seed, environment, and acceptable variance.",
        ),
        promotion_gates=(
            "No metric claim lacks data provenance.",
            "No sensitive dataset or artifact is added without explicit policy review.",
            "No benchmark regression is waived without owner and rationale.",
        ),
    ),
    Blueprint(
        id="security-sensitive",
        title="Security-Sensitive Project Blueprint",
        summary=(
            "Tighten harness expectations for repos that handle secrets, auth, "
            "payments, infrastructure, permissions, or sensitive user data."
        ),
        domains=("security", "privacy", "supply-chain", "operations"),
        fit_signals=(
            "The repo changes auth, identity, authorization, crypto, secrets, or infrastructure.",
            "The project processes sensitive user, customer, payment, health, or location data.",
            "Release risk includes privilege escalation, data loss, or external side effects.",
        ),
        review_questions=(
            "What assets, principals, trust boundaries, and attacker goals matter for this repo?",
            "Which commands scan dependencies, secrets, generated files, and infrastructure changes?",
            "Which operations require human approval, least privilege, or rollback evidence?",
            "How are security exceptions recorded, owned, and re-reviewed?",
        ),
        operating_model=(
            "Make threat model updates part of behavior changes that cross trust boundaries.",
            "Treat generated workflow permissions and tool authority as security-sensitive.",
            "Prefer fail-closed checks, least privilege, pinned dependencies, and explicit owners.",
            "Keep incident, rollback, and secret-rotation guidance current and tested.",
        ),
        generated_review_items=(
            "Threat model snapshot with assets, boundaries, mitigations, and known gaps.",
            "Sensitive-operation approval matrix for credentials, cloud, data, and deploys.",
            "Supply-chain checklist for pins, provenance, workflow permissions, and scanners.",
        ),
        verification_gates=(
            "Run dependency and secret checks when manifests, lockfiles, workflows, or configs change.",
            "Run focused negative-path tests for auth, authorization, validation, and rollback.",
            "Run policy or infrastructure plan checks before applying external-state changes.",
        ),
        promotion_gates=(
            "No new secret, token, or credential in committed files.",
            "No permission expansion without review evidence.",
            "No high-risk finding ships without explicit acceptance and owner.",
        ),
    ),
    Blueprint(
        id="workflow-automation",
        title="Workflow Automation Blueprint",
        summary=(
            "Design and verify CI, scheduled jobs, bots, self-heal flows, and "
            "repository automation without blurring local versus generated responsibilities."
        ),
        domains=("ci", "automation", "governance", "operations"),
        fit_signals=(
            "The repo includes GitHub Actions, scheduled jobs, bots, or generated pull requests.",
            "Automation can write files, open PRs, comment, publish, deploy, or call external services.",
            "Different environments need different permissions, triggers, and failure modes.",
        ),
        review_questions=(
            "Which workflows are repo-local policy, generated harness artifacts, or hosted Action behavior?",
            "What permissions, tokens, event triggers, and branch protections apply to each workflow?",
            "Which automation steps can mutate state, spend money, publish artifacts, or contact users?",
            "What evidence proves the automation is safe before enabling it by default?",
        ),
        operating_model=(
            "Keep local repo workflows separate from workflows generated for target repositories.",
            "Require explicit opt-in for scheduled, mutating, or network-heavy automation.",
            "Pin external actions and document why each permission is needed.",
            "Prefer manual dispatch until the workflow has representative evidence.",
        ),
        generated_review_items=(
            "Workflow ownership table separating local repo, generated repo, and hosted Action behavior.",
            "Permission matrix covering token scopes, event triggers, network calls, and write paths.",
            "Failure-mode checklist for retries, PR churn, rate limits, and partial writes.",
        ),
        verification_gates=(
            "Run pin checks for workflow and dependency changes.",
            "Run dry-run automation locally or in a sandbox before enabling mutating triggers.",
            "Record CI evidence for generated workflow templates and hosted Action behavior separately.",
        ),
        promotion_gates=(
            "No scheduled mutating workflow is enabled without explicit owner approval.",
            "No external action uses a floating tag in generated workflow templates.",
            "No generated workflow inherits local repo-only preferences or machine paths.",
        ),
    ),
)


def list_blueprints() -> tuple[Blueprint, ...]:
    return BLUEPRINTS


def get_blueprint(blueprint_id: str) -> Blueprint:
    for blueprint in BLUEPRINTS:
        if blueprint.id == blueprint_id:
            return blueprint
    valid = ", ".join(blueprint.id for blueprint in BLUEPRINTS)
    raise ValueError(f"unknown blueprint '{blueprint_id}'. Valid blueprints: {valid}")


def blueprint_to_dict(blueprint: Blueprint) -> dict[str, object]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "id": blueprint.id,
        "title": blueprint.title,
        "summary": blueprint.summary,
        "domains": list(blueprint.domains),
        "fitSignals": list(blueprint.fit_signals),
        "reviewQuestions": list(blueprint.review_questions),
        "operatingModel": list(blueprint.operating_model),
        "generatedReviewItems": list(blueprint.generated_review_items),
        "verificationGates": list(blueprint.verification_gates),
        "promotionGates": list(blueprint.promotion_gates),
        "generatedFiles": list(blueprint.generated_files),
    }


def list_blueprints_to_dict() -> dict[str, object]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "blueprints": [
            {
                "id": blueprint.id,
                "title": blueprint.title,
                "summary": blueprint.summary,
                "domains": list(blueprint.domains),
                "generatedFiles": list(blueprint.generated_files),
            }
            for blueprint in BLUEPRINTS
        ],
    }


def apply_blueprint(
    target: Path,
    blueprint_id: str,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> tuple[Blueprint, tuple[WriteResult, ...]]:
    root = target.resolve()
    blueprint = get_blueprint(blueprint_id)
    files = _render_files(blueprint)
    writes: list[WriteResult] = []
    for relative_path, content in files.items():
        writes.append(
            _write_blueprint_file(
                root,
                relative_path,
                content,
                dry_run=dry_run,
                force=force,
            )
        )

    manifest_content = _manifest_content(root, blueprint, files, tuple(writes))
    writes.append(
        _write_manifest(
            root,
            f"{BLUEPRINT_ROOT}/manifest.json",
            manifest_content,
            dry_run=dry_run,
            force=force,
        )
    )
    return blueprint, tuple(writes)


def _render_files(blueprint: Blueprint) -> dict[str, str]:
    return {
        f"{BLUEPRINT_ROOT}/README.md": _blueprints_readme(),
        blueprint.relative_path: _blueprint_markdown(blueprint),
    }


def _blueprints_readme() -> str:
    return """# Harness Blueprints

HarnessForge blueprints are optional project overlays. They do not replace the
base harness. Use them when a repository needs stronger guidance for a known
operating mode such as agentic applications, spec-driven delivery, sensitive
security work, or workflow automation.

## Rules

- Treat every blueprint artifact as generated but project-reviewed.
- Keep local developer preferences out of blueprint content.
- Preserve project edits unless `--force` is explicitly used after review.
- Record verification evidence before promoting a blueprint from draft to policy.

"""


def _blueprint_markdown(blueprint: Blueprint) -> str:
    lines = [
        f"# {blueprint.title}",
        "",
        "> Generated by HarnessForge blueprint mode. Review this file before treating it as project policy.",
        "",
        "## Purpose",
        "",
        blueprint.summary,
        "",
        "## Fit Signals",
        "",
    ]
    _append_bullets(lines, blueprint.fit_signals)
    lines.extend(
        [
            "",
            "## Review Required",
            "",
            "Answer these before promoting this blueprint to active repo policy.",
            "",
        ]
    )
    _append_numbered(lines, blueprint.review_questions)
    lines.extend(["", "## Operating Model", ""])
    _append_bullets(lines, blueprint.operating_model)
    lines.extend(["", "## Generated But Needs Project Review", ""])
    _append_bullets(lines, blueprint.generated_review_items)
    lines.extend(["", "## Verification Gates", ""])
    _append_bullets(lines, blueprint.verification_gates)
    lines.extend(["", "## Promotion Gates", ""])
    _append_bullets(lines, blueprint.promotion_gates)
    lines.extend(
        [
            "",
            "## Ownership Metadata",
            "",
            f"- Blueprint ID: `{blueprint.id}`",
            "- Ownership: generated blueprint, project-reviewed before policy use",
            "- Safe update rule: preserve local edits unless `--force` is explicit",
            "",
        ]
    )
    return redact_local_paths("\n".join(lines))


def _append_bullets(lines: list[str], values: tuple[str, ...]) -> None:
    for value in values:
        lines.append(f"- {value}")


def _append_numbered(lines: list[str], values: tuple[str, ...]) -> None:
    for index, value in enumerate(values, 1):
        lines.append(f"{index}. {value}")


def _write_blueprint_file(
    root: Path,
    relative_path: str,
    content: str,
    *,
    dry_run: bool,
    force: bool,
) -> WriteResult:
    destination = root / relative_path
    _validate_destination(root, destination)
    content = _ensure_trailing_newline(redact_local_paths(content))
    if destination.exists() and not force:
        if destination.read_text(encoding="utf-8") == content:
            return WriteResult(path=destination, status="unchanged")
        return WriteResult(path=destination, status="skipped", reason="exists")
    if dry_run:
        status = "would_update" if destination.exists() else "would_write"
        return WriteResult(path=destination, status=status)
    existed = destination.exists()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8", newline="\n")
    return WriteResult(
        path=destination,
        status="updated" if existed and force else "written",
    )


def _write_manifest(
    root: Path,
    relative_path: str,
    content: str,
    *,
    dry_run: bool,
    force: bool,
) -> WriteResult:
    destination = root / relative_path
    _validate_destination(root, destination)
    content = _ensure_trailing_newline(redact_local_paths(content))
    exists = destination.exists()
    if exists and not force and not _is_generated_manifest(destination):
        return WriteResult(path=destination, status="skipped", reason="exists")
    if exists and destination.read_text(encoding="utf-8") == content:
        return WriteResult(path=destination, status="unchanged")
    if dry_run:
        return WriteResult(
            path=destination,
            status="would_update" if exists else "would_write",
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8", newline="\n")
    return WriteResult(path=destination, status="updated" if exists else "written")


def _validate_destination(root: Path, destination: Path) -> None:
    if not is_inside_root(destination, root):
        raise ValueError(f"refusing to write outside target repository: {destination}")


def _is_generated_manifest(path: Path) -> bool:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        isinstance(payload, dict)
        and payload.get("schemaVersion") == MANIFEST_SCHEMA_VERSION
        and payload.get("generatedBy") == "harnessforge"
    )


def _manifest_content(
    root: Path,
    blueprint: Blueprint,
    files: dict[str, str],
    writes: tuple[WriteResult, ...],
) -> str:
    manifest_path = root / BLUEPRINT_ROOT / "manifest.json"
    manifest = _load_manifest(manifest_path)
    applied = manifest.setdefault("appliedBlueprints", {})
    assert isinstance(applied, dict)
    write_statuses = {
        _relative_to_root(write.path, root): write
        for write in writes
        if _relative_to_root(write.path, root) in files
    }
    generated_files: dict[str, object] = {}
    preserved_files: dict[str, object] = {}
    for relative_path, content in files.items():
        write = write_statuses.get(relative_path)
        if write and write.status == "skipped":
            preserved_files[relative_path] = {
                "ownership": "project-owned-preserved",
                "reason": write.reason or "exists",
            }
            continue
        generated_files[relative_path] = {
            "ownership": "generated-blueprint-project-reviewed",
            "contentSha256": _sha256_text(_ensure_trailing_newline(content)),
            "reviewRequired": relative_path == blueprint.relative_path,
        }
    applied[blueprint.id] = {
        "title": blueprint.title,
        "ownership": "generated-blueprint-project-reviewed",
        "reviewRequired": True,
        "generatedFiles": generated_files,
        "preservedFiles": preserved_files,
    }
    manifest["schemaVersion"] = MANIFEST_SCHEMA_VERSION
    manifest["generatedBy"] = "harnessforge"
    manifest["generatorVersion"] = __version__
    manifest["safeUpdateRule"] = "preserve existing project edits unless --force is explicit"
    return f"{json.dumps(manifest, indent=2, sort_keys=True)}\n"


def _load_manifest(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "schemaVersion": MANIFEST_SCHEMA_VERSION,
            "generatedBy": "harnessforge",
            "generatorVersion": __version__,
            "appliedBlueprints": {},
        }
    if not isinstance(payload, dict) or payload.get("generatedBy") != "harnessforge":
        return {
            "schemaVersion": MANIFEST_SCHEMA_VERSION,
            "generatedBy": "harnessforge",
            "generatorVersion": __version__,
            "appliedBlueprints": {},
        }
    applied = payload.get("appliedBlueprints")
    if not isinstance(applied, dict):
        payload["appliedBlueprints"] = {}
    return payload


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def _relative_to_root(path: Path, root: Path) -> str:
    return path.resolve(strict=False).relative_to(root.resolve(strict=False)).as_posix()


def _ensure_trailing_newline(text: str) -> str:
    return text if text.endswith("\n") else f"{text}\n"
