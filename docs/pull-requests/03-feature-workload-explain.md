## Problem

`scan` exposed the full inventory, but there was still no focused explanation path for one workload.

## Approach

- added a typed workload explanation model and text renderer
- implemented `podsleuth explain <namespace>/<workload> --fixtures <dir>`
- surfaced bound roles, wildcard and cross-account flags, evidence IDs, and a trust note that avoids overstating usable access

## Important decisions

- kept `explain` text-first because operators usually need a concise review artifact for one workload
- used a distinct exit code when the requested workload is missing from the snapshot
- reused the existing fixture adapter and normalized snapshot instead of adding a second lookup path

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run podsleuth explain payments/api --fixtures tests/fixtures/identity-snapshot`

## Known limitations

- explain output is text only in this slice
- explicit deny analysis and snapshot diffs are still pending

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Evidence and uncertainty are represented correctly

## Review findings

- no material findings after local self-review
