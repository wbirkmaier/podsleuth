# ADR 0001: Start With Fixture-First Ingestion

## Status

Accepted

## Context

Live EKS and IAM access is not always available in development or CI, but analysis logic still needs realistic coverage.

## Decision

Build the first analysis slices around sanitized fixture adapters and make live AWS support additive.

## Consequences

- Offline integration tests can stay deterministic.
- Live adapter behavior can be verified separately without blocking domain work.
