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

- Added first-agent lifecycle evidence for generated harnesses. New targets get
  `docs/harness/evidence/first-agent-review.json`, and `harnessforge report`
  plus readiness can classify the first deep harness review as pending,
  completed, retired, blocked, invalid, or stale.
- Added Agent Skills `.md` source references for the generated repo skill:
  spec, best practices, description optimization, evaluation, and scripts.
- Reverified the generated/deployed repo skill against the Agent Skills
  specification. The generated `SKILL.md` now keeps
  file references one level deep by routing detailed repo paths through
  `.agents/skills/harness/references/repo-harness.md`.
- Added generated manifest metadata and regression coverage for the bundled
  skill reference. Applied the same deployed-skill shape to RunHaven during the
  active harness migration and fixed its remaining harness Markdown link.
- Compacted generated harness templates for README, roadmap, source notes,
  security map, agent operating model, verification matrix, first-agent task,
  quality document, authoritative map, and root instructions.
- Preserved generated safety surfaces while reducing representative generated
  Markdown from 85,839 bytes and 1,730 lines to 69,927 bytes after adding
  first-agent lifecycle evidence.
- Removed the HarnessForge product-local research source allowlist from
  generated targets, compacted generated/local manifests, and shortened the
  generated harness skill. Representative generated total output is now
  139,404 bytes after adding first-agent lifecycle evidence, down from 160,684
  bytes and 4,190 lines at the start of the second pass.
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

Latest lifecycle/spec-alignment verification:

- `PYTHONPATH=src:. python3 -m unittest discover -s tests`
- `PYTHONPATH=src:. python3 -m unittest tests.test_cli tests.test_generate_audit`
- explicit Agent Skills spec validator for fresh render and RunHaven deployed
  skill
- fresh generated-target `harnessforge audit --min-score 85`
- HarnessForge `harnessforge audit --target . --min-score 85`
- RunHaven `harnessforge audit --min-score 85`
- RunHaven manifest JSON validation
- JSON validation for `feature_list.json` and `docs/harness/manifest.json`
- HarnessForge and RunHaven `git diff --check`

Results: 250 unit tests passed, focused first-agent lifecycle and generated
tests passed with 137 tests, fresh generated skill spec validation passed,
RunHaven deployed skill spec validation passed, fresh generated-target audit
was `100/100`, HarnessForge self-audit was `100/100`, RunHaven audit was
`100/100`, and diff hygiene passed.

Earlier optimization verification also included:

- `PYTHONPATH=src:. python3 -m compileall -q src tests`
- `PYTHONPATH=src:. python3 -m harnessforge audit --target . --min-score 85`
- `python3 -m json.tool feature_list.json`
- `python3 -m json.tool docs/harness/manifest.json`
- `PYTHONPATH=src:. python3 -m harnessforge report --target . --since HEAD --json`
- `PYTHONPATH=src:. python3 -m harnessforge corpus --min-score 90 --json`
- stale flat-path scan
- `git diff --check`

## Recommended Next Step

Continue accepted pre-release backlog before release prep:

- instruction-quality and signal-to-noise reporting
- compact repo map and SBOM-aware detection or adapter design
- Action summary polish
- `release-check`
- harness maturity levels
- expanded policy presets
- interactive quickstart/init UX

Do not push unless the user asks or a release/batch boundary is declared.
