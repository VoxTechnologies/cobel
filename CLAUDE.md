# CLAUDE.md

Demand-side existence proof for [RFL](https://github.com/robotfoundationlayer/rfl): a real
foundation model emits valid, retargetable RFL Skill ISA. See [README.md](./README.md) for the
result and the pipeline diagram.

## Architecture

- `planner/contract.py`: the `Planner.plan(task, scene) -> skill_yaml` contract + `load_task`.
- `planner/mock.py`: `MockPlanner`: deterministic, offline, returns a canned reference skill per task.
- `planner/claude.py`: `ClaudePlanner`: the real emitter (`claude-opus-4-8`). spec-only + few-shot modes.
- `planner/prompts/skill-isa-system.md`: the distilled Skill ISA system prompt (spec-only is blind).
- `harness/engine.py`: `ENGINE_18` (the reference engine's implemented primitives) + `primitives_used`.
- `harness/validate.py`: `schema_ok` (primary gate) + `retarget_outcome` (secondary, 4-way).
- `harness/schema/` and `harness/descriptors/`: vendored, commit-pinned (see each `SOURCE.md`).
- `tasks/`: task + scene inputs (novel; not the RFL examples). `reference_skills/`: the mock's skills.
- `run.py`: `--planner mock|claude --mode spec-only|few-shot --samples N`. Writes `results/`.

## Setup

`uv` venv + the published RFL binding (cobel and rfl are sibling repos under the same parent):

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
unset CONDA_PREFIX                                   # this machine has conda + venv both active
maturin develop -m ../rfl/bindings/python/Cargo.toml # or: pip install ../rfl/bindings/python
python -c "import rfl; print(rfl.retarget)"          # smoke test
```

## Commands

- **Tests** (offline, no API key: the Claude tests use a fake client): `.venv/bin/python -m pytest -q`
- **Mock proof** (offline): `python run.py --planner mock`
- **Claude proof** (needs `ANTHROPIC_API_KEY`): `set -a; source .env; set +a; python run.py --planner claude --mode spec-only --samples 5`

## Conventions / invariants

1. **rfl is consumed, never edited.** The binding (`rfl.retarget`) and `skill-isa.schema.json`
   are dependencies. Do not modify the rfl repo from here.
2. **Two gates, deliberate order.** Schema-conformance against the full 50-primitive
   `skill-isa.schema.json` is the PRIMARY validity metric (independent of engine coverage).
   `rfl.retarget` is SECONDARY and 4-way: `retarget_ok` / `capability_rejected` /
   `beyond_engine` / `malformed`. The reference engine implements only 18 of the 50 primitives
   (`ENGINE_18`, transcribed from rfl `crates/rfl-core/src/skill_isa.rs`), so a valid emission
   the engine cannot lower is `beyond_engine` (a coverage gap, NOT a model error).
3. **The planner never sees the embodiment** (Principle 1). It gets task + scene only; the
   descriptor enters at retarget.
4. **Vendored files are commit-pinned.** Refresh `harness/schema/` and `harness/descriptors/`
   by re-copying from a recorded rfl commit and bumping the `SOURCE.md` hash.
5. **`docs/plans/` is LOCAL-ONLY** (gitignored). Never commit implementation plans.
6. **Never commit secrets.** `.env` (the API key) is gitignored; keep it that way.

## Verify before writing facts

Per the project owner's standing rule: SDK details (the Anthropic model id, Messages API
shape, `cache_control`) and product facts (hardware specs in descriptors) must be verified
in-session (the `claude-api` skill, official docs): never written from memory.
