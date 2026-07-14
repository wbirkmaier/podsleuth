## Problem

PodSleuth only had repository scaffolding and a version command. There was no domain model or usable identity analysis path.

## Approach

- added typed raw and normalized models for fixture-backed Kubernetes and IAM identity data
- implemented fixture ingestion with explicit validation errors
- added the first `podsleuth scan --fixtures ...` vertical slice with deterministic JSON output
- covered findings for shared service accounts, wildcard permissions, cross-account trust, orphaned associations, and node-role fallback risk

## Important decisions

- kept the first adapter fixture-only so the analysis path can be exercised offline
- preserved uncertainty by flagging missing bindings as node-role fallback risk rather than claiming effective AWS access
- used a golden JSON file for the integration test to keep output ordering stable

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run podsleuth scan --fixtures tests/fixtures/identity-snapshot`

## Known limitations

- live EKS and IAM adapters are not implemented yet
- `explain`, `diff`, and Mermaid rendering are still pending

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Evidence and uncertainty are represented correctly

## Review findings

- no material findings after local self-review
