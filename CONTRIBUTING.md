# Contributing

## Local workflow

1. Install `uv`.
2. Run `uv sync --all-extras --dev`.
3. Run `pre-commit install`.
4. Validate with:
   - `uv run ruff format --check .`
   - `uv run ruff check .`
   - `uv run mypy src`
   - `uv run pytest`
   - `uv run pytest --cov=src --cov-report=term-missing`
   - `uv build`

## Development notes

- Keep adapters small and explicit.
- Do not add write operations against Kubernetes or AWS APIs.
- Document evidence gaps when a conclusion is uncertain.
