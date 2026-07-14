## Problem

PodSleuth could inspect one snapshot at a time, but operators also need to compare before and after captures during rollouts or IAM changes.

## Approach

- added a typed snapshot loader for persisted JSON captures
- implemented diff logic for added findings, removed findings, and workload identity changes
- exposed `podsleuth diff <before.json> <after.json>` with deterministic JSON output

## Important decisions

- kept the first diff scope narrow to findings and workload identity changes instead of inventing a generic recursive object diff
- treated newly appearing workloads as workload changes with empty `before_role_arns`
- reused the normalized snapshot schema so scan output can be piped directly into later diff runs

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run podsleuth diff tests/fixtures/diff/before.json tests/fixtures/diff/after.json`

## Known limitations

- diffing does not yet summarize policy document deltas inside a role
- semantic deny analysis is still pending

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Evidence and uncertainty are represented correctly

## Review findings

- no material findings after local self-review
