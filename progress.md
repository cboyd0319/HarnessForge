# Progress

Last Updated: 2026-06-15 UTC

## Current Objective

Reduce HarnessForge harness maintenance cost and token burn without weakening
generated harness effectiveness, product-boundary enforcement, or verification.

## Current State

- HarnessForge is an alpha/pre-release Python 3.13+ CLI and composite GitHub
  Action for creating, assessing, and updating AI coding-agent harnesses.
- No external deployment or compatibility boundary exists yet. Prefer the clean
  current product contract over legacy shims unless maintainers declare a
  release boundary.
- Product boundaries are locked: repo-local HarnessForge docs and workflows,
  generated target-repo harness content, CLI/runtime behavior, GitHub Action
  behavior, optional workflow scaffolds, tests/fixtures, release/package
  surfaces, research ledger, security/privacy controls, and platform contracts
  must be considered separately.
- Target repos must not receive HarnessForge repo-local self-healing, local
  machine paths, sibling-checkout commands, personal tool mandates, or wording
  that makes HarnessForge canonical after initial generation.
- Generated target harnesses now use the organized `docs/harness/` layout,
  include a zero-install `.agents/skills/harness/SKILL.md`, and keep repository
  docs/state authoritative unless the owner opts into HarnessForge checks.
- Routine doc fan-out is controlled by
  `docs/harness/authoritative-facts.md` and report/audit checks.

## Latest Work

- Compacted generated harness templates for README, roadmap, source notes,
  security map, agent operating model, verification matrix, first-agent task,
  quality document, authoritative map, and root instructions.
- Preserved generated safety surfaces while reducing representative generated
  Markdown from 85,839 bytes and 1,730 lines to 69,009 bytes and 1,454 lines.
- Removed the HarnessForge product-local research source allowlist from
  generated targets, compacted generated/local manifests, and shortened the
  generated harness skill. Representative generated total output is now
  136,337 bytes and 2,911 lines, down from 160,684 bytes and 4,190 lines at the
  start of the second pass.
- Replaced the 913-line repo-local `remaining-ideas-research.md` history note
  with an 86-line current-state summary. Active `docs/harness` Markdown is now
  2,764 lines, down from 3,589 lines before this pass.
- Added regression tests that keep representative generated Markdown below
  70,000 bytes and 1,500 lines, total generated output below 140,000 bytes and
  3,000 lines, and generated audit at `100/100`.
- Replaced the root `progress.md` and `session-handoff.md` startup logs with
  compact current-state snapshots, dropping them from 2,557 combined lines to
  153 combined lines. Historical detail remains in git history and the compact
  evidence log.
- Narrowed local and generated startup routing so fresh sessions read compact
  state first and open heavier README, harness README, roadmap, and component
  inventory files only when the task touches those surfaces.

## Verification

Latest optimization verification:

- `PYTHONPATH=src:. python3 -m unittest tests.test_generate_audit`
- `PYTHONPATH=src:. python3 -m unittest discover -s tests`
- `PYTHONPATH=src:. python3 -m compileall -q src tests`
- `PYTHONPATH=src:. python3 -m harnessforge audit --target . --min-score 85`
- `python3 -m json.tool feature_list.json`
- `python3 -m json.tool docs/harness/manifest.json`
- `PYTHONPATH=src:. python3 -m harnessforge report --target . --since HEAD --json`
- `PYTHONPATH=src:. python3 -m harnessforge corpus --min-score 90 --json`
- stale flat-path scan
- `git diff --check`

Results: 246 unit tests passed, compile passed, self-audit stayed `100/100`,
generated-target smoke audit stayed `100/100`, duplicate durable fact blocks
were `0`, corpus passed across 13 fixtures with minimum score `100`, and diff
hygiene passed.

## Recommended Next Step

Continue accepted pre-release backlog before release prep:

- first-agent lifecycle evidence
- instruction-quality and signal-to-noise reporting
- compact repo map and SBOM-aware detection or adapter design
- Action summary polish
- `release-check`
- harness maturity levels
- expanded policy presets
- interactive quickstart/init UX

Do not push unless the user asks or a release/batch boundary is declared.
