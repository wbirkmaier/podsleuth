## Problem

PodSleuth still treated a bound role list as straightforward even when a service account referenced multiple identity paths or a role ARN that did not exist in the IAM snapshot.

## Approach

- added findings for multiple identity bindings on one service account
- added findings for role ARNs referenced by Kubernetes metadata but missing from the IAM snapshot
- surfaced missing role evidence in workload explanations so operators can see the ambiguity directly

## Important decisions

- attached the missing-role finding to the service account because the ambiguity originates in the Kubernetes identity wiring rather than a single role document
- kept effective role ARNs visible even when one role is unresolved, instead of silently dropping missing references
- expanded the shipped fixture to include both IRSA and pod identity on one service account so the behavior is regression-tested end to end

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run podsleuth scan --fixtures tests/fixtures/identity-snapshot`
- `uv run podsleuth explain payments/api --fixtures tests/fixtures/identity-snapshot`

## Known limitations

- PodSleuth still does not rank which of multiple bindings would actually win at runtime in every EKS mode
- live EKS Pod Identity discovery is still fixture-first rather than tested against AWS

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Evidence and uncertainty are represented correctly

## Review findings

- no material findings after local self-review
