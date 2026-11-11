"""Loading and validation of encoding definition files.

Every legacy encoding is a YAML file. In a source checkout the files live in
the top-level ``encodings/`` directory; in an installed wheel they are shipped
inside the package as ``glyphfix/encodings/``.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

__all__ = [
    "Encoding",
    "EncodingError",
    "ReorderRule",
    "list_encodings",
    "load_encoding",
    "load_encoding_file",
]

#: Reorder rule types understood by the converter.
REORDER_TYPES = frozenset({"pre-base-vowel-sign", "reph", "sign-after-vowel-sign"})


class EncodingError(ValueError):
    """Raised when an encoding is unknown or its definition file is invalid."""


@dataclass(frozen=True)
class ReorderRule:
    """A single reordering rule (visual order to logical order)."""

    type: str
    signs: Tuple[str, ...]


@dataclass(frozen=True)
class Encoding:
    """A parsed legacy-encoding definition."""

    id: str
    name: str
    script: str
    mappings: Dict[str, str]
    language: str = ""
    fonts: Tuple[str, ...] = ()
    status: str = ""
    reorder: Tuple[ReorderRule, ...] = ()


def _candidate_dirs() -> List[object]:
    """Directories that may contain encoding files, in priority order."""
    dirs: List[object] = []
    try:
        pkg_dir = resources.files("glyphfix") / "encodings"
        if pkg_dir.is_dir():
            dirs.append(pkg_dir)
    except (ModuleNotFoundError, TypeError):
        pass
    # Source checkout: src/glyphfix/encodings.py -> repository root.
    repo_dir = Path(__file__).resolve().parents[2] / "encodings"
    if repo_dir.is_dir():
        dirs.append(repo_dir)
    return dirs


def _require_str(data: dict, key: str, source: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise EncodingError(f"{source}: field '{key}' must be a non-empty string")
    return value


def _parse_reorder(raw: object, source: str) -> Tuple[ReorderRule, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise EncodingError(f"{source}: 'reorder' must be a list of rules")
    rules = []
    for entry in raw:
        if not isinstance(entry, dict):
            raise EncodingError(f"{source}: each reorder rule must be a mapping")
        rule_type = entry.get("type")
        if rule_type not in REORDER_TYPES:
            raise EncodingError(
                f"{source}: unknown reorder rule type {rule_type!r}; "
                f"supported types: {', '.join(sorted(REORDER_TYPES))}"
            )
        signs = entry.get("signs")
        if (
            not isinstance(signs, list)
            or not signs
            or not all(isinstance(s, str) and s for s in signs)
        ):
            raise EncodingError(
                f"{source}: reorder rule 'signs' must be a non-empty list of strings"
            )
        rules.append(ReorderRule(type=rule_type, signs=tuple(signs)))
    return tuple(rules)


def _parse_encoding(data: object, source: str) -> Encoding:
    if not isinstance(data, dict):
        raise EncodingError(f"{source}: encoding file must contain a YAML mapping")

    mappings = data.get("mappings")
    if not isinstance(mappings, dict) or not mappings:
        raise EncodingError(f"{source}: 'mappings' must be a non-empty mapping")
    for key, value in mappings.items():
        if not isinstance(key, str) or not key:
            raise EncodingError(f"{source}: mapping keys must be non-empty strings")
        if not isinstance(value, str):
            raise EncodingError(
                f"{source}: mapping value for {key!r} must be a string"
            )

    fonts = data.get("fonts") or []
    if not isinstance(fonts, list) or not all(isinstance(f, str) for f in fonts):
        raise EncodingError(f"{source}: 'fonts' must be a list of strings")

    return Encoding(
        id=_require_str(data, "id", source),
        name=_require_str(data, "name", source),
        script=_require_str(data, "script", source),
        mappings=dict(mappings),
        language=str(data.get("language") or ""),
        fonts=tuple(fonts),
        status=str(data.get("status") or ""),
        reorder=_parse_reorder(data.get("reorder"), source),
    )


def load_encoding_file(path) -> Encoding:
    """Load and validate a single encoding definition file."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise EncodingError(f"{path}: cannot read encoding file: {exc}") from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise EncodingError(f"{path}: invalid YAML: {exc}") from exc
    return _parse_encoding(data, str(path))


def load_encoding(encoding_id: str) -> Encoding:
    """Load the encoding with the given id, for example ``"bijoy"``."""
    for directory in _candidate_dirs():
        candidate = directory / f"{encoding_id}.yaml"
        if candidate.is_file():
            return load_encoding_file(candidate)
    available = ", ".join(sorted(e.id for e in list_encodings())) or "none"
    raise EncodingError(
        f"unknown encoding '{encoding_id}' (available encodings: {available})"
    )


def list_encodings() -> List[Encoding]:
    """Return all available encodings, sorted by id."""
    seen: Dict[str, Encoding] = {}
    for directory in _candidate_dirs():
        for entry in directory.iterdir():
            if not entry.name.endswith(".yaml") or not entry.is_file():
                continue
            encoding = load_encoding_file(entry)
            seen.setdefault(encoding.id, encoding)
    return sorted(seen.values(), key=lambda e: e.id)
