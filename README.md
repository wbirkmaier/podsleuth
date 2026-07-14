# PodSleuth

PodSleuth inspects how Kubernetes workloads in EKS could obtain AWS permissions through service accounts, IRSA, pod identity associations, and node-role fallback.

## What it inspects

- Kubernetes service accounts and workload references
- IAM roles, trust relationships, and policy documents
- Shared service account usage
- Wildcards, cross-account trust, and orphaned associations

## What it does not do

- It does not mutate Kubernetes or AWS resources.
- It does not claim access is usable without matching trust and policy evidence.
- It does not require live AWS calls for offline analysis.

## Offline and live use

- Offline: import sanitized Kubernetes and IAM fixtures, then run `podsleuth scan` and `podsleuth explain` against them.
- Live: planned adapters will read EKS and IAM metadata with least-privilege permissions.

## Safety

- Read-only by default
- Deterministic JSON output
- No hidden network calls
- Evidence gaps are surfaced as uncertainty

## Development status

The repository scaffold and CLI entrypoint are in place. Domain analysis commands are being added incrementally.
