from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from podsleuth.exceptions import PodSleuthError
from podsleuth.models import FixtureBundle, RawClusterFixture, RawIamFixture


def _load_json_file(path: Path) -> object:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as error:
        raise PodSleuthError(f"fixture file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise PodSleuthError(f"invalid JSON in fixture file: {path}") from error


def load_fixture_snapshot(fixtures_dir: Path) -> FixtureBundle:
    try:
        cluster = RawClusterFixture.model_validate(_load_json_file(fixtures_dir / "cluster.json"))
        iam = RawIamFixture.model_validate(_load_json_file(fixtures_dir / "iam.json"))
    except ValidationError as error:
        raise PodSleuthError(f"invalid fixture data: {error}") from error

    return FixtureBundle(cluster=cluster, iam=iam)
