"""Golden tests: every encoding is validated against real before/after pairs."""

import pathlib

import pytest
import yaml

from glyphfix import convert_text

GOLDEN_DIR = pathlib.Path(__file__).parent / "encodings"


def _load_cases():
    params = []
    for path in sorted(GOLDEN_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        encoding_id = data["encoding"]
        for case in data["cases"]:
            params.append(
                pytest.param(
                    encoding_id,
                    case["legacy"],
                    case["unicode"],
                    id=f"{encoding_id}-{case['name']}",
                )
            )
    return params


@pytest.mark.parametrize(("encoding_id", "legacy", "expected"), _load_cases())
def test_golden(encoding_id, legacy, expected):
    assert convert_text(legacy, encoding_id) == expected
