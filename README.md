# PodSleuth

PodSleuth inspects how Kubernetes workloads in EKS could obtain AWS permissions through service accounts, IRSA, pod identity associations, and node-role fallback.

## What it inspects today

- Kubernetes service accounts, workloads, and pod identity associations from fixture snapshots
- IAM roles, trust relationships, and policy documents from fixture snapshots
- Shared service account usage
- Wildcards, cross-account trust, orphaned associations, and node-role fallback risk

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
```

The current scan output is JSON and includes typed inventory plus findings with attached evidence IDs. The explain command renders a concise text path for one workload and calls out uncertainty when trust or policy evidence is incomplete.

## Development status

`scan` and `explain` work offline from fixtures. `diff` and Mermaid rendering are planned next.
