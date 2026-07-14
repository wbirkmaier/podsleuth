# Threat Model

## Assets

- Kubernetes workload metadata
- IAM trust and policy documents
- Evidence snapshots written to local disk

## Main risks

- Credential leakage in logs or error messages
- Overstating access because of incomplete trust evidence
- Unsafe future adapter changes that attempt mutation
- Ingesting malformed fixture or API data without validation

## Mitigations

- Structured parsing with Pydantic models
- Read-only adapters by design
- Deterministic offline fixtures for regression tests
- Explicit uncertainty states in findings and explanations
