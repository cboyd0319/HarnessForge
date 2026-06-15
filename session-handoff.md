# Session Handoff

Last Updated: 2026-06-15 UTC

## Current Objective

Continue reducing HarnessForge harness maintenance and token cost while keeping
generated harness quality, product boundaries, and verification evidence intact.

## What Changed

- Generated repo skills were rechecked against
  `/Users/c/Downloads/specification.md`. `SKILL.md` now uses a one-level
  `references/repo-harness.md` route, with detailed repo paths in the bundled
  reference file.
- RunHaven's deployed skill copy was updated to the same shape during the
  active harness migration; RunHaven audit is now `100/100`.
- Generated target harness Markdown was compacted without deleting safety
  surfaces.
- Representative generated Markdown is now 69,009 bytes and 1,454 lines, down
  from 85,839 bytes and 1,730 lines.
- Representative generated total output is now 136,337 bytes and 2,911 lines,
  down from 160,684 bytes and 4,190 lines at the start of the second pass.
- Generated targets no longer receive this repo's product-local research
  source allowlist; generated manifests are compact machine-readable JSON.
- Repo-local `remaining-ideas-research.md` was compacted from 913 lines to 86
  lines; active `docs/harness` Markdown is now 2,764 lines.
- Generated audit remains `100/100`.
- `tests/test_generate_audit.py` now includes generated-footprint regression
  caps for Markdown and total output.
- Root startup state was compacted from 2,557 combined lines to 153 combined
  lines. Historical detail remains in git history and the compact evidence log.
- Local and generated startup routes now read compact state first and make
  heavier docs task-specific.

## Files

- `src/harnessforge/templates/agent-operating-model.md.tmpl`
- `src/harnessforge/templates/agents.md.tmpl`
- `src/harnessforge/templates/authoritative-facts.md.tmpl`
- `src/harnessforge/templates/first-agent-task.md.tmpl`
- `src/harnessforge/templates/harness-readme.md.tmpl`
- `src/harnessforge/templates/harness-skill.md.tmpl`
- `src/harnessforge/templates/harness-skill-reference.md.tmpl`
- `src/harnessforge/templates/quality-document.md.tmpl`
- `src/harnessforge/templates/roadmap.md.tmpl`
- `src/harnessforge/templates/security-boundary-map.md.tmpl`
- `src/harnessforge/templates/source-record.schema.json.tmpl`
- `src/harnessforge/templates/source-record-example.json.tmpl`
- `src/harnessforge/templates/sources.md.tmpl`
- `src/harnessforge/templates/verification-matrix.md.tmpl`
- `src/harnessforge/audit.py`
- `src/harnessforge/generate.py`
- `src/harnessforge/harness_paths.py`
- `tests/test_generate_audit.py`
- `docs/harness/manifest.json`
- `docs/harness/evidence/evidence-log.md`
- `docs/harness/research/source-record.schema.json`
- `docs/harness/research/source-record-example.json`
- `docs/roadmap.md`
- `progress.md`
- `session-handoff.md`

## Verification To Trust

Latest checks:

- focused generated/audit tests passed with 56 tests
- full unit discovery passed with 247 tests
- explicit Agent Skills spec validation passed for a fresh render and the
  RunHaven deployed skill
- fresh generated-target audit passed threshold at `93/100`; the only warning
  was the expected lack of a project-specific command in the temporary repo
- RunHaven audit passed at `100/100`
- HarnessForge and RunHaven `git diff --check` passed

Earlier optimization checks also passed before the spec adjustment:

- compile passed
- self-audit passed at `100/100`
- JSON validation passed for `feature_list.json` and
  `docs/harness/manifest.json`
- report smoke passed with no duplicate durable fact blocks
- public fixture corpus passed with 13 fixtures and minimum score `100`
- stale flat-path scan was clean

Rerun focused tests after any further template or scoring edit.

## Constraints To Preserve

- Generated target repos must not receive HarnessForge repo-local self-healing
  docs or workflows.
- Generated docs should not say HarnessForge is canonical for a target repo.
  Repo-owned docs and checks are canonical unless the owner opts into the
  GitHub Action or a recurring HarnessForge command.
- Contributors should not need HarnessForge installed after initial generation.
  The generated repo skill is the zero-install maintenance path.
- Keep root startup files compact. Put durable product rules in the specific
  harness doc that owns them.
- Avoid adding compatibility shims before release unless a maintainer declares a
  real compatibility boundary.

## Blockers

- No known blockers.

## Next Session

If the user wants more backlog work, continue with first-agent lifecycle
evidence or instruction-quality and signal-to-noise reporting. If the user asks
to checkpoint, commit the current optimization slice first.
