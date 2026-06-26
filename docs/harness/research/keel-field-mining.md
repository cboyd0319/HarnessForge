# Keel Field Mining

Reviewed: 2026-06-26 UTC.

Scope: local sibling repository `keel`, branch `main`, commit
`db0c542 prepare v0.0.1 release (#5)`. This note records ideas for
HarnessForge. It is repo-local research evidence, not a generated target
harness contract.

Verification during review:

- `go test ./...` passed in `keel`.
- File inventory showed 134 non-git files, 71 files under `cmd`, `internal`,
  and `keel`, and 133 Go test functions.

## Product Reading

Keel and HarnessForge overlap, but they optimize different layers.
HarnessForge generates, assesses, and updates repo harness surfaces across
many project shapes. Keel installs a phase-execution runtime for one project,
with manifest phases, gates, rollback snapshots, event ledgers, and reports.

The useful transfer is not to make HarnessForge a phase runner by default. The
useful transfer is to improve HarnessForge's read-only analysis, optional
planning modes, generated guidance quality, lifecycle evidence, and stale
surface detection.

## High-Value Ideas To Consider

| Idea | Keel Evidence | HarnessForge Fit |
| --- | --- | --- |
| Deterministic work planning from deliverables | `internal/planner/plan_phases.go` validates deliverable IDs, builds a dependency DAG, computes topological layers, scores risk, isolates sensitive deliverable types, and packs remaining work under ceilings. | Strong candidate for deeper `enhance` planning and optional blueprint or plan output. Keep advisory and review-required; do not make default generation a phase runtime. |
| Explicit scope files per work unit | `keel/commands/keel-run.md` and `keel/rules/allowed-paths.md` require allowed paths, blocked paths, exit criteria, and stop-on-scope-expansion behavior. | Strengthen HarnessForge report and enhance findings for project-owned task plans: detect missing allowed paths, blocked paths, out-of-scope notes, and scope-expansion rules. |
| Gate records distinguish passed from failed work | `internal/gate/gate.go` writes passed or failed gate JSON, audit logs, build ledgers, and run logs from one close operation. | Feed feature-state gates and evidence classification. HarnessForge can recommend or validate pass/fail evidence shape without owning a target repo's execution lifecycle. |
| Current state derived from machine files | `internal/currentphase/current_phase.go` derives next phase from `BUILD_MANIFEST.yaml` plus `.agent/phase_gates/`, and treats failed gates as blockers. | Useful pattern for HarnessForge's feature-state scope reporting: derive status from evidence and touched surfaces instead of trusting prose state alone. |
| Append-only event ledgers with reducers | `internal/session/event.go`, `reduce.go`, and `report.go` model sessions as JSONL events, then derive state, token totals, tool counts, debug loops, and phase metrics. | Good model for process observability and token economics records. Prefer target-contained imported evidence, not always-on generated hooks. |
| Snapshot and rollback evidence | `internal/snapshot/snapshot.go` captures pre and post file manifests with hashes; `internal/rollback/rollback.go` reads rollback DAGs and produces a dry-run plan before confirmed rollback. | Useful for optional high-risk change evidence and migration blueprints. Avoid default file stashing or rollback execution in HarnessForge generated harnesses. |
| Stale plan and retired-path checks | `keel/rules/stale-plan.md` tells agents to stop when phase files conflict with PRD, TDD, manifest, or rules. `internal/verify/verify.go` scans for stale names such as retired execution-plan paths. | Strong fit for deeper instruction-quality scoring and generated fallback hardening. Add stale-reference checks where HarnessForge already owns generated template and enhance analysis. |
| Draft-then-approve feature workspaces | `keel/commands/new-feature.md`, `approve-feature.md`, and `internal/merge/merge_feature.go` separate feature authoring from project manifest execution. | Useful as a pattern for HarnessForge blueprints: candidate workspaces stay separate until explicitly approved. Do not add a default feature workflow tree. |
| Preflight context capture | `keel/scripts/preflight_context.py` records tool availability, source-document presence, repo state, and recommended next action without installing dependencies. | Fits `quickstart`, `session`, and `report`: show missing inputs and tool evidence compactly. Avoid writing target preflight files by default. |
| Template self-tests | `internal/generator/verify_generator_test.go` asserts required template files and banned strings in embedded templates. | Already partly covered by HarnessForge generated snapshot tests; add focused stale-token and retired-path cases when real misses appear. |

## Cautionary Findings

These findings are useful because they show failure modes HarnessForge can
detect in target repos.

| Finding | Evidence | HarnessForge Lesson |
| --- | --- | --- |
| Generated/runtime surfaces can drift during renames | `keel/scripts/verify_phase0.py` still checks old `harness/` paths while active docs and Go verifier use `keel/` paths. `keel/scripts/preflight_context.py` also records `bash harness/hooks/preflight.sh` in run-log metadata. | Treat stale generated paths as first-class report and enhance findings. A passing package test is not enough if shipped helper scripts disagree with live docs. |
| Agent-facing rules can over-specify runtime behavior | Keel command prompts require exact one-phase execution, TDD-first loops, Drift checkpoints, and gate writes. | Keep HarnessForge generated defaults smaller. Rich execution protocols belong in opt-in policy presets, blueprints, or target-owned docs. |
| Rollback automation has a data-loss boundary | Keel rollback can delete created files and restore modified files from snapshots after confirmation. | HarnessForge should continue to require explicit confirmation for destructive or overwrite-capable paths and should prefer dry-run rollback plans as evidence. |
| Release automation can carry credential and cost risk | `.github/workflows/release.yml` updates a Homebrew tap using a repository secret and writes to another repo. | Keep generated workflows opt-in and local-script-backed. Surface credentialed vendor writes as high-risk review surfaces. |

## Candidate Product Work

1. Add a "work-unit plan quality" report section that checks detected task or
   phase files for allowed paths, blocked paths, exit criteria, verification
   commands, stale-source references, and explicit out-of-scope notes.
2. Extend `enhance` planning with an advisory deliverable-DAG mode for
   project-owned specs or TDD files. Output should be dry-run JSON first, with
   risk, dependency, and isolation rationale.
3. Add stale generated-surface findings for retired path names, mismatched
   harness directory names, and helper scripts that disagree with canonical
   docs.
4. Extend feature-state gates so "passing" requires evidence agreement:
   status text, changed surface, verification evidence, and any failure gate
   must align.
5. Add optional rollback-evidence recommendations for high-risk blueprint
   classes: migration, generated-code refresh, public API change, auth,
   security-sensitive work, and cross-cutting refactor.
6. Import target-contained event ledgers as report evidence when present:
   phase/session events, token buckets, tool failures, debug loops, and failed
   gates should improve observability without HarnessForge installing hooks.
7. Add a fixture shaped like a phase-gated repo with stale helper-script paths,
   passed and failed gates, a phase manifest, and rollback evidence. Use it to
   test report, enhance, readiness, and instruction-quality findings.

## Do Not Adopt By Default

- Do not turn default HarnessForge generation into a phase runner.
- Do not generate `.agent/` ledgers, rollback stashes, hook scripts, or
  command adapters unless a user explicitly asks for that style of harness.
- Do not require PRD/TDD files as universal target inputs.
- Do not install token, tool, or transcript hooks in normal generated repos.
- Do not copy Keel's exact directory layout, release workflow, or slash-command
  protocol into generated targets.

## Roadmap Fit

This mining pass supports existing accepted backlog rather than creating a new
release boundary:

- Better `enhance` planning.
- Feature-state gates and scope-surface reporting.
- Instruction lifecycle and signal-to-noise review.
- Generated harness fallback hardening from real target reviews.
- More real-repo golden fixtures and deeper instruction-quality scoring.
- Harness token economics evidence, through imported event-ledger and token
  metric records only.

## Next Review Step

Before implementation, choose one narrow slice: stale generated-surface
detection is the smallest high-confidence candidate because Keel demonstrates a
real rename-drift failure and HarnessForge already has report, enhance,
instruction-quality, and fixture surfaces that can carry the signal.

The implementation sequence is captured in
`keel-derived-enhancement-plan.md`.
