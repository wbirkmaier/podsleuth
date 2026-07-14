# PodSleuth

PodSleuth inspects how Kubernetes workloads in EKS could obtain AWS permissions through service accounts, IRSA, pod identity associations, and node-role fallback.

## What it inspects today

- Kubernetes service accounts, workloads, and pod identity associations from fixture snapshots
- IAM roles, trust relationships, and policy documents from fixture snapshots
- Shared service account usage
- Wildcards, cross-account trust, explicit deny signals, missing role references, binding ambiguity, orphaned associations, and node-role fallback risk

## What it does not do

- It does not mutate Kubernetes or AWS resources.
- It does not claim access is usable without matching trust and policy evidence.
- It does not require live AWS calls for offline analysis.

## Offline and live use

- Offline: run `podsleuth scan --fixtures tests/fixtures/identity-snapshot`.
- Live: planned adapters will read EKS and IAM metadata with least-privilege permissions.

## Safety

- Read-only by default
- Deterministic JSON output
- No hidden network calls
- Evidence gaps are surfaced as uncertainty

## Example

```bash
uv run podsleuth scan --fixtures tests/fixtures/identity-snapshot
uv run podsleuth explain payments/api --fixtures tests/fixtures/identity-snapshot
uv run podsleuth diff tests/fixtures/diff/before.json tests/fixtures/diff/after.json
uv run podsleuth render tests/fixtures/diff/after.json --format mermaid
```

The current scan output is JSON and includes typed inventory plus findings with attached evidence IDs. The explain command renders a concise text path for one workload and calls out uncertainty when trust or policy evidence is incomplete. The diff command compares two JSON snapshots and reports added and removed findings plus workload identity changes. The render command emits a Mermaid graph for review and pull request discussion.

Role summaries include trust mode and whether explicit deny statements were found in attached or inline policies.

## Development status

`scan`, `explain`, `diff`, and Mermaid rendering work offline from fixtures.
