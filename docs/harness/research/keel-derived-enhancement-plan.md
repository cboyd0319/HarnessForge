# Keel-Derived Enhancement Plan

Status: draft implementation plan.
Created: 2026-06-26 UTC.
Source note: `keel-field-mining.md`.

## Problem

The Keel mining pass found concrete harness patterns that can improve
HarnessForge without changing the product boundary. The risk is importing too
much of Keel's phase-execution model into default generation. HarnessForge
should instead use the findings to improve read-only analysis, optional
planning, evidence import, generated fallback hardening, and fixture coverage.

Success means HarnessForge can detect and report the same class of problems
that Keel exposes, especially stale generated paths and weak work-unit scope,
while keeping target repos project-owned and zero-install by default.

## Scope And Non-Goals

In scope:

- Report and enhance findings for stale generated or retired path references.
- Advisory work-unit plan quality checks for task, phase, or plan files.
- Stronger feature-state evidence alignment and scope-surface reporting.
- Optional import of target-contained phase, gate, event, token, and rollback
  evidence into reports.
- Optional deliverable-DAG planning for specs or TDD-like files.
- A Keel-shaped fixture that proves the findings against real drift patterns.

Out of scope:

- Making default HarnessForge generation a phase runner.
- Generating `.agent/` ledgers, rollback stashes, hooks, slash commands, or
  command adapters by default.
- Requiring PRD, TDD, phase files, or build manifests in target repos.
- Installing token, tool, or transcript hooks in generated harnesses.
- Copying Keel's directory layout or release automation into target repos.

## Constraints And Risks

- Normal `init`, `quickstart`, `report`, `index`, `enhance`, and `sync` flows
  stay read-only unless an existing write-capable command is explicitly chosen.
- Findings must distinguish observed target files from inferred conventions.
- Keel-shaped checks must be generic enough to work for non-Keel task plans.
- Event-ledger and token import must redact local paths and avoid raw
  transcript or stdout capture.
- Windows 11 and macOS behavior must be preserved. Path checks should use
  existing path helpers and fixture tests rather than POSIX-only parsing.
- Structural findings are harness-health signals, not proof that an agent will
  perform better.

## Milestones

### 1. Stale Generated-Surface Detection

Goal: make the cheapest high-confidence finding visible in reports and
enhance output.

Files to inspect first:

- `src/harnessforge/evidence/instruction_quality.py`
- `src/harnessforge/generation/generate.py`
- `src/harnessforge/evidence/report.py`
- `src/harnessforge/project/readiness.py`
- `tests/test_cli.py`
- `tests/test_generate_audit.py`
- `tests/test_public_repo_corpus.py`

Implementation tasks:

1. Add a small detector for stale generated references:
   retired file names, old harness directory names, helper-script commands
   that disagree with canonical docs, unrendered template tokens, and
   contradictory generated ownership markers.
2. Feed the detector into `instructionQuality` and `enhanceExistingPlan`
   findings as advisory review work.
3. Surface a compact summary in `report --json` and text output without
   changing generated files.
4. Add a fixture with active docs using one harness path and helper scripts
   using a retired path.

Focused verification:

```bash
PYTHONPATH=src:. python3 -m unittest tests.test_cli -k 'enhance or report'
PYTHONPATH=src:. python3 -m unittest tests.test_generate_audit
PYTHONPATH=src:. python3 -m harnessforge report --target . --json >/tmp/harnessforge-report.json
```

Done when:

- A target with stale helper-script paths gets an advisory finding.
- A clean generated target does not get the finding.
- Report and enhance JSON fields name the source file, stale reference, likely
  canonical owner, and repair hint.

Rollback point:

- Revert the detector and report plumbing only; no generated target contract
  should have changed in this milestone.

### 2. Work-Unit Plan Quality And Feature-State Alignment

Goal: improve scope and lifecycle signals without taking over execution.

Files to inspect first:

- `src/harnessforge/evidence/feature_state.py`
- `src/harnessforge/evidence/report.py`
- `src/harnessforge/project/readiness.py`
- `src/harnessforge/project/indexer.py`
- `tests/test_feature_state.py`
- `tests/test_cli.py`
- `docs/harness/feedback/report-json-contract.md`

Implementation tasks:

1. Detect task, phase, implementation-plan, and feature-plan files from common
   names and existing index classifications.
2. Score work-unit quality for allowed paths, blocked paths or out-of-scope
   notes, exit criteria, verification commands, evidence requirements, and
   stop conditions.
3. Add report-only `workUnitPlanQuality` data with observed files, missing
   fields, and repair hints.
4. Extend feature-state reporting so `passing`, `validated`, and `shipped`
   warn when evidence is missing, stale, failed, or unrelated to touched
   surfaces.
5. Keep all findings advisory unless a future flag explicitly requires them.

Focused verification:

```bash
PYTHONPATH=src:. python3 -m unittest tests.test_feature_state
PYTHONPATH=src:. python3 -m unittest tests.test_cli -k 'featureState or report'
PYTHONPATH=src:. python3 -m unittest tests.test_verify_contract
```

Done when:

- A plan with tasks but no verification gets a clear finding.
- A feature marked passing without evidence gets a mismatch finding.
- JSON contract docs cover any new stable report fields.

Rollback point:

- Remove the new report field and tests before changing any Action summary or
  release-check gate.

### 3. Optional Evidence Import

Goal: read target-contained execution evidence when it exists, without
installing hooks or creating ledgers.

Files to inspect first:

- `src/harnessforge/evidence/observability.py`
- `src/harnessforge/evidence/token_economics.py`
- `src/harnessforge/evidence/report.py`
- `src/harnessforge/project/session.py`
- `tests/test_token_economics.py`
- `tests/test_cli.py`

Implementation tasks:

1. Detect common local evidence files: phase gates, failed gates, rollback
   DAGs, session JSONL ledgers, audit JSONL ledgers, and compact token records.
2. Parse only bounded, target-relative, target-contained evidence. Skip raw
   transcripts and large logs.
3. Add report summaries for passed gates, failed gates, rollback evidence,
   token buckets, tool failures, debug-loop counts, and unknown schema records.
4. Map imported token data into existing token-economics metric shapes where
   the required fields are present.
5. Document that imported ledgers are process evidence, not HarnessForge-owned
   execution state.

Focused verification:

```bash
PYTHONPATH=src:. python3 -m unittest tests.test_token_economics
PYTHONPATH=src:. python3 -m unittest tests.test_cli -k 'observability or report'
PYTHONPATH=src:. python3 -m harnessforge report --target . --json >/tmp/harnessforge-report.json
```

Done when:

- Existing target ledgers improve observability status or add advisory context.
- Missing or malformed ledgers do not fail report by default.
- Local absolute paths and raw log bodies are not emitted.

Rollback point:

- Keep the parser isolated so report import can be removed without affecting
  generated templates or normal readiness.

### 4. Optional Deliverable-DAG Planning

Goal: turn Keel's strongest planning idea into a HarnessForge-native advisory
mode.

Files to inspect first:

- `src/harnessforge/project/verify.py`
- `src/harnessforge/project/indexer.py`
- `src/harnessforge/generation/blueprints.py`
- `src/harnessforge/generation/generate.py`
- `src/harnessforge/cli.py`
- `tests/test_cli.py`
- `tests/test_public_repo_corpus.py`

Implementation tasks:

1. Define a minimal standard-library parser for fenced YAML-like or JSON
   deliverable blocks only if existing project files expose them. Do not add a
   dependency for generic YAML parsing.
2. Validate deliverable IDs, dependency references, touched paths, and
   verification commands.
3. Produce an advisory DAG and phase grouping with risk and isolation rationale
   in `enhance --json` or a new explicit planning subfield.
4. Keep output dry-run and review-required. Do not write phase files or
   manifests.
5. Add blueprint guidance for high-risk deliverables: schema, migration, auth,
   generated code, public API change, security-sensitive change, and
   cross-cutting refactor.

Focused verification:

```bash
PYTHONPATH=src:. python3 -m unittest tests.test_cli -k 'enhance or plan'
PYTHONPATH=src:. python3 -m unittest tests.test_public_repo_corpus
PYTHONPATH=src:. python3 -m harnessforge enhance --target . --json >/tmp/harnessforge-enhance.json
```

Done when:

- Valid deliverables produce deterministic grouping.
- Cycles and unknown dependencies produce actionable findings.
- Repeated runs produce stable JSON ordering.

Rollback point:

- Keep this behind an advisory output field so it can be removed or deferred
  without changing `init`, generated content, or report gates.

### 5. Keel-Shaped Fixture And Corpus Gates

Goal: preserve the field lesson as a regression fixture.

Files to inspect first:

- `src/harnessforge/generation/public_repo_corpus.py`
- `tests/test_public_repo_corpus.py`
- `tests/test_large_public_repo_analysis.py`
- `docs/harness/research/large-public-repo-corpus.json`

Implementation tasks:

1. Add a generated or static fixture shaped like a phase-gated repo:
   manifest, phase docs, passed gate, failed gate, rollback evidence,
   helper-script stale path, and event ledger sample.
2. Assert report, readiness, enhance, instruction-quality, feature-state, and
   observability expectations against the fixture.
3. Add corpus labels that make the fixture's purpose obvious:
   stale-generated-surface, phase-gated-state, rollback-evidence, and
   event-ledger-import.
4. Keep fixture content compact and free of copied Keel code beyond tiny
   shape-compatible examples.

Focused verification:

```bash
PYTHONPATH=src:. python3 -m unittest tests.test_public_repo_corpus
PYTHONPATH=src:. python3 -m unittest tests.test_large_public_repo_analysis
PYTHONPATH=src:. python3 -m harnessforge corpus --min-score 90
```

Done when:

- The fixture fails before the relevant detector exists and passes after the
  implementation.
- Corpus output explains the regression without relying on Keel-specific names.

Rollback point:

- Remove the fixture and expected checks together if it becomes noisy or too
  Keel-specific.

## Verification

Minimum docs-plan verification for this file:

```bash
python3 scripts/refresh_research.py --root . --check
git diff --check
PYTHONPATH=src:. python3 -m harnessforge audit --target . --min-score 100
```

Milestone implementation verification should add the focused commands listed
above. Before claiming a milestone done, run either `./init.sh` or record why a
smaller verification set is sufficient.

## Progress

- Draft plan created from Keel mining findings.
- No product behavior implemented yet.
- No generated target defaults changed.

## Surprises And Discoveries

- Keel's Go tests pass, but its shipped helper-script surface still contains
  old `harness/` references. This makes stale generated-surface detection the
  first and highest-confidence HarnessForge slice.

## Decision Log

- Start with stale generated-surface detection because it is evidence-backed,
  small, and aligned with existing report and enhance surfaces.
- Keep deliverable-DAG planning optional and advisory because HarnessForge does
  not own target repo execution.
- Import target-contained ledgers only as evidence. HarnessForge should not
  generate or install always-on execution hooks by default.

## Outcomes And Retrospective

Pending implementation.
