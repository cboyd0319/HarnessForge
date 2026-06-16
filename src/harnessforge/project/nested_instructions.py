from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any

from ..core.models import ProjectProfile

SCHEMA_VERSION = "harnessforge.nestedInstructionPlan.v1"
DEFAULT_CANDIDATE_LIMIT = 20


def build_nested_instruction_plan(
    profile: ProjectProfile,
    *,
    candidate_limit: int = DEFAULT_CANDIDATE_LIMIT,
) -> dict[str, Any]:
    existing = sorted(
        file
        for file in profile.files
        if PurePosixPath(file).name == "AGENTS.md" and file != "AGENTS.md"
    )
    components = [
        component
        for component in (_component_record(value) for value in profile.components)
        if component["path"] not in {"", "."}
    ]
    signals = _nested_instruction_signals(profile, components, existing)
    candidates = []
    if signals:
        for component in components:
            path = component["path"]
            if _has_nested_agent(existing, path):
                continue
            candidates.append(
                {
                    "path": path,
                    "instructionPath": f"{path}/AGENTS.md",
                    "reason": _candidate_reason(component),
                    "recommendedAction": "review_required",
                }
            )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "review_required" if candidates else "no_action",
        "writeByDefault": False,
        "rootAgentsPresent": "AGENTS.md" in profile.files,
        "monorepoSignals": signals,
        "existingNestedAgents": existing[:candidate_limit],
        "existingNestedAgentCount": len(existing),
        "candidateComponents": candidates[:candidate_limit],
        "candidateCount": len(candidates),
        "candidateLimit": candidate_limit,
        "candidateListTruncated": len(candidates) > candidate_limit,
        "guidance": (
            "Use root AGENTS.md as a short repo-wide router. Add nested "
            "AGENTS.md only for meaningful components whose stack, commands, "
            "ownership, constraints, or verification differ."
        ),
    }


def _component_record(component: str) -> dict[str, Any]:
    path, markers = _parse_component(component)
    return {"path": path, "markers": markers}


def _parse_component(component: str) -> tuple[str, list[str]]:
    if component.endswith(")") and " (" in component:
        path, marker_text = component[:-1].split(" (", 1)
        markers = [marker.strip() for marker in marker_text.split(",")]
        return path, [marker for marker in markers if marker]
    return component, []


def _nested_instruction_signals(
    profile: ProjectProfile,
    components: list[dict[str, Any]],
    existing: list[str],
) -> list[str]:
    signals = list(profile.workspace_markers)
    if len(components) >= 4:
        signals.append("4+ detected component boundaries")
    if profile.component_scan_truncated:
        signals.append("component inventory truncated")
    if existing:
        signals.append("existing nested AGENTS.md")
    return list(dict.fromkeys(signals))


def _has_nested_agent(existing: list[str], component: str) -> bool:
    prefix = component.rstrip("/") + "/"
    return any(path.startswith(prefix) for path in existing)


def _candidate_reason(component: dict[str, Any]) -> str:
    markers = component["markers"]
    if markers:
        return "component has boundary markers: " + ", ".join(markers[:4])
    return "component has its own detected boundary signal"
