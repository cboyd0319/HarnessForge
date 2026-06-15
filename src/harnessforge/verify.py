from __future__ import annotations

import platform
import sys
from dataclasses import dataclass
from typing import Any

from .detect import MISSING_VERIFICATION_COMMAND
from .models import ProjectProfile


SCHEMA_VERSION = "harnessforge.verify.v1"
PLAN_MESSAGE = "Plan mode only. Command execution requires explicit run mode."


@dataclass(frozen=True)
class VerifyCheck:
    id: str
    label: str
    command: str
    source: str
    working_directory: str
    required: bool
    status: str
    exit_code: int | None
    duration_ms: float | None
    message: str
    stdout_preview: str | None
    stderr_preview: str | None


@dataclass(frozen=True)
class VerifyReport:
    target: str
    mode: str
    verdict: str
    checks: tuple[VerifyCheck, ...]
    blocked_reasons: tuple[str, ...]
    warnings: tuple[str, ...]


def build_verify_plan(
    profile: ProjectProfile, *, explicit_commands: tuple[str, ...] = ()
) -> VerifyReport:
    commands = explicit_commands or profile.verification_commands
    source = "explicit" if explicit_commands else "detected"
    checks: list[VerifyCheck] = []
    blocked: list[str] = []
    for index, command in enumerate(commands):
        is_missing = command == MISSING_VERIFICATION_COMMAND or command.startswith(
            "REVIEW REQUIRED:"
        )
        status = "blocked" if is_missing else "planned"
        if is_missing:
            blocked.append("No project verification check detected.")
        checks.append(
            VerifyCheck(
                id=f"project.{source}.{index}",
                label=(
                    "Missing project verification"
                    if is_missing
                    else "Project verification"
                ),
                command=command,
                source=source,
                working_directory=".",
                required=True,
                status=status,
                exit_code=None,
                duration_ms=None,
                message=(
                    "Add --command with the smallest reliable project check."
                    if is_missing
                    else PLAN_MESSAGE
                ),
                stdout_preview=None,
                stderr_preview=None,
            )
        )
    verdict = "blocked" if blocked else "planned"
    return VerifyReport(
        target=profile.name,
        mode="plan",
        verdict=verdict,
        checks=tuple(checks),
        blocked_reasons=tuple(_dedupe(blocked)),
        warnings=(),
    )


def verify_report_to_dict(report: VerifyReport) -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "target": {
            "name": report.target,
            "root": None,
        },
        "mode": report.mode,
        "verdict": report.verdict,
        "platform": {
            "os": sys.platform,
            "python": platform.python_version(),
            "runner": "local",
        },
        "execution": {
            "commandsExecuted": False,
            "startedAt": None,
            "endedAt": None,
            "durationMs": None,
        },
        "summary": _summary(report.checks),
        "checks": [_check_to_dict(check) for check in report.checks],
        "blockedReasons": list(report.blocked_reasons),
        "warnings": list(report.warnings),
        "artifacts": [],
    }


def format_verify_plan(report: VerifyReport) -> str:
    lines = [f"Verify plan: {report.verdict}", ""]
    if report.blocked_reasons:
        lines.append("Blocked reasons:")
        lines.extend(f"  - {reason}" for reason in report.blocked_reasons)
        lines.append("")
    lines.append("Checks:")
    for check in report.checks:
        lines.append(
            f"  - {check.id}: {check.status}, source={check.source}, "
            f"command={check.command}"
        )
    return "\n".join(lines).rstrip()


def _summary(checks: tuple[VerifyCheck, ...]) -> dict[str, int]:
    counts = {
        "total": len(checks),
        "planned": 0,
        "skipped": 0,
        "blocked": 0,
        "passed": 0,
        "failed": 0,
        "timedOut": 0,
        "errors": 0,
    }
    for check in checks:
        if check.status == "timed_out":
            counts["timedOut"] += 1
        elif check.status == "error":
            counts["errors"] += 1
        elif check.status in counts:
            counts[check.status] += 1
    return counts


def _check_to_dict(check: VerifyCheck) -> dict[str, Any]:
    return {
        "id": check.id,
        "label": check.label,
        "command": check.command,
        "source": check.source,
        "workingDirectory": check.working_directory,
        "required": check.required,
        "status": check.status,
        "exitCode": check.exit_code,
        "durationMs": check.duration_ms,
        "message": check.message,
        "stdoutPreview": check.stdout_preview,
        "stderrPreview": check.stderr_preview,
    }


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result
