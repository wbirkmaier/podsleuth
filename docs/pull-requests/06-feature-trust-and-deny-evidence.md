## Problem

PodSleuth identified broad allow and trust risks, but it still lacked explicit deny signals and a concise trust-mode summary for each role.

## Approach

- added `trust_mode` and `explicit_deny` to role summaries and workload explanations
- detected explicit deny statements in attached and inline policy documents
- surfaced the new evidence in shipped fixtures so persisted snapshots and follow-on diff/render flows stay schema-compatible

## Important decisions

- treated explicit deny as a low-severity finding because it constrains access rather than broadening it, but it still changes how operators should read an allow path
- kept trust mode coarse (`federated`, `service`, `aws-principal`, `unknown`) instead of overfitting the first pass to every IAM principal shape
- updated the persisted diff fixtures rather than adding backwards-compatibility parsing code for older snapshots

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run podsleuth explain payments/api --fixtures tests/fixtures/identity-snapshot`

## Known limitations

- trust mode is a summary, not a full trust policy explainer
- PodSleuth still does not attempt to prove that a requested action is definitely usable end to end

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Evidence and uncertainty are represented correctly

## Review findings

- no material findings after local self-review
