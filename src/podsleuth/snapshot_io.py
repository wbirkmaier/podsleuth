from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from podsleuth.exceptions import PodSleuthError
from podsleuth.models import IdentitySnapshot


def load_snapshot(path: Path) -> IdentitySnapshot:
    try:
        return IdentitySnapshot.model_validate_json(path.read_text())
    except FileNotFoundError as error:
        raise PodSleuthError(f"snapshot file not found: {path}") from error
    except ValidationError as error:
        raise PodSleuthError(f"invalid snapshot JSON: {path}: {error}") from error
