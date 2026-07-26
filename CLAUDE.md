# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Demand-side existence proof for [RFL](https://github.com/robotfoundationlayer/rfl): a real
foundation model emits valid, retargetable RFL Skill ISA. [README.md](./README.md) has the
claim, the pipeline diagram, the setup steps, and the published results.

## Architecture

One pipeline, two swappable ends: `Planner.plan(task, scene) -> skill_yaml`, then two
independent gates over that YAML string. Everything below hangs off that contract.

- `planner/contract.py`: the `Planner` Protocol + `TaskSpec` / `Scene` dataclasses + `load_task`.
- `planner/mock.py`: `MockPlanner`: deterministic, offline, returns a canned reference skill per task.
- `planner/claude.py`: `ClaudePlanner`: the real emitter (`claude-opus-4-8`). spec-only + few-shot modes.
- `planner/prompts/skill-isa-system.md`: the distilled Skill ISA system prompt (spec-only is blind).
- `harness/engine.py`: `ENGINE_18` (the reference engine's implemented primitives) + `primitives_used`.
- `harness/validate.py`: `schema_ok` (primary gate) + `retarget_outcome` (secondary, 4-way).
- `harness/report.py`: `Row` + `render_tables` — the two published markdown tables.
- `harness/schema/` and `harness/descriptors/`: vendored, commit-pinned (see each `SOURCE.md`).
- `tasks/`: task + scene inputs (novel; not the RFL examples). `reference_skills/`: the mock's skills.
- `run.py`: `--planner mock|claude --mode spec-only|few-shot --samples N`. Writes `results/`.

`run.py` draws `--samples` emissions per task, counts schema passes for `pass@k`, and then
retargets **the first schema-passing sample** against every descriptor in
`harness/descriptors/`. It overwrites `results/<planner>-<mode>.md`; the README's headline
table is maintained by hand from those files.

## Commands

Setup is in [README.md](./README.md#setup). On this machine, `unset CONDA_PREFIX` before
`maturin develop` (conda and the venv are both active).

- **Tests** (offline, no API key: the Claude tests use a fake client): `.venv/bin/python -m pytest -q`
- **One test file / one test**: `.venv/bin/python -m pytest tests/test_suite.py -q`,
  `.venv/bin/python -m pytest -q -k beyond_engine`
- **Mock proof** (offline): `python run.py --planner mock`
- **Claude proof**: `set -a; source .env; set +a; python run.py --planner claude --mode spec-only --samples 5`

## Conventions / invariants

1. **rfl is consumed, never edited.** The binding (`rfl.retarget`) and `skill-isa.schema.json`
   are dependencies. Do not modify the rfl repo from here.
2. **Two gates, deliberate order.** Schema-conformance against the full 50-primitive
   `skill-isa.schema.json` is the PRIMARY validity metric (independent of engine coverage).
   `rfl.retarget` is SECONDARY and 4-way: `retarget_ok` / `capability_rejected` /
   `beyond_engine` / `malformed`. The reference engine implements only 18 of the 50 primitives
   (`ENGINE_18`, transcribed from rfl `crates/rfl-core/src/skill_isa.rs`), so a valid emission
   the engine cannot lower is `beyond_engine` (a coverage gap, NOT a model error).
   **Order matters inside `retarget_outcome`**: the `beyond_engine` check runs *before* the
   `capability_absent` string match, because rfl reports an unimplemented primitive as
   `capability_absent` too. Only skills built purely from `ENGINE_18` can be truly
   `capability_rejected`. Regenerate `results/` after touching this classifier.
3. **The planner never sees the embodiment** (Principle 1). It gets task + scene only; the
   descriptor enters at retarget.
4. **The suite stays hermetic.** CI (`.github/workflows/ci.yml`) checks out rfl, builds the
   binding, and runs pytest with no API key. Never add a test that needs the network — mock
   the Anthropic client the way `tests/test_claude.py` does.
5. **Adding a task touches three places**: `tasks/<name>.yaml`, `reference_skills/<name>.yaml`,
   and a `_ROUTES` entry in `planner/mock.py` (keyed by an instruction substring). Miss the
   route and `MockPlanner` raises `KeyError`; `tests/test_suite.py` also assigns every task to
   GROUP_A (lowerable) or GROUP_B (`beyond_engine`).
6. **Vendored files are commit-pinned.** Refresh `harness/schema/` and `harness/descriptors/`
   by re-copying from a recorded rfl commit and bumping the `SOURCE.md` hash. `pincherx-100.yaml`
   is the exception: authored here from public Trossen specs, not copied.
7. **`docs/plans/` is LOCAL-ONLY** (gitignored). Never commit implementation plans.
8. **Never commit secrets.** `.env` (the API key) is gitignored; keep it that way.

## Verify before writing facts

Per the project owner's standing rule: SDK details (the Anthropic model id, Messages API
shape, `cache_control`) and product facts (hardware specs in descriptors) must be verified
in-session (the `claude-api` skill, official docs): never written from memory.
