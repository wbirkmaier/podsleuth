# Architecture

PodSleuth keeps ingestion, normalization, and analysis separate so offline fixture runs and live adapters can share the same finding logic.

## Current layers

1. Adapters load Kubernetes and IAM data from fixtures or live APIs.
2. Normalizers convert external documents into typed internal models.
3. Analysis computes reachable identity paths, uncertainty, and findings.
4. Renderers emit JSON, Mermaid, and concise human explanations.

The first shipped path implements fixture adapters and JSON rendering.

## Early decisions

- Favor explicit models over generic resource containers.
- Keep evidence attached to normalized entities and findings.
- Model uncertainty directly rather than treating missing data as denial or success.
