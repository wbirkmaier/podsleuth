## Problem

The snapshot JSON is useful for automation, but review discussions often need a compact visual map of workload, service account, role, and finding relationships.

## Approach

- added Mermaid rendering for normalized identity snapshots
- modeled workload to service account to role edges, plus dashed evidence edges from findings
- exposed `podsleuth render <snapshot.json> --format mermaid`

## Important decisions

- kept the renderer snapshot-based so it works on persisted scan output instead of requiring a second live fetch path
- used dashed edges for findings to distinguish evidence from identity binding
- limited the first render format to Mermaid instead of introducing multiple half-finished output targets

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run podsleuth render tests/fixtures/diff/after.json --format mermaid`

## Known limitations

- the graph is a cluster-wide identity view, not a per-namespace filtered renderer yet
- repeated node declarations are tolerated by Mermaid and can be compacted later if needed

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Evidence and uncertainty are represented correctly

## Review findings

- no material findings after local self-review
