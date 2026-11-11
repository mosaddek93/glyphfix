"""Unit tests for the encoding loader."""

import pytest

from glyphfix import EncodingError, list_encodings, load_encoding
from glyphfix.encodings import load_encoding_file


def test_load_bijoy():
    encoding = load_encoding("bijoy")
    assert encoding.id == "bijoy"
    assert encoding.script == "Bengali"
    assert encoding.language == "bn"
    assert "SutonnyMJ" in encoding.fonts
    assert encoding.mappings["e"] == "\u09ac"  # ba
    assert any(rule.type == "pre-base-vowel-sign" for rule in encoding.reorder)


def test_list_encodings_contains_bijoy():
    ids = [encoding.id for encoding in list_encodings()]
    assert "bijoy" in ids
    assert ids == sorted(ids)


def test_unknown_encoding_raises():
    with pytest.raises(EncodingError, match="unknown encoding"):
        load_encoding("does-not-exist")


def _write(tmp_path, text):
    path = tmp_path / "broken.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_missing_required_field(tmp_path):
    path = _write(tmp_path, "id: x\nscript: T\nmappings:\n  a: b\n")
    with pytest.raises(EncodingError, match="'name'"):
        load_encoding_file(path)


def test_empty_mappings(tmp_path):
    path = _write(tmp_path, "id: x\nname: X\nscript: T\nmappings: {}\n")
    with pytest.raises(EncodingError, match="mappings"):
        load_encoding_file(path)


def test_non_string_mapping_value(tmp_path):
    path = _write(tmp_path, "id: x\nname: X\nscript: T\nmappings:\n  a: 1\n")
    with pytest.raises(EncodingError, match="must be a string"):
        load_encoding_file(path)


def test_unknown_reorder_type(tmp_path):
    path = _write(
        tmp_path,
        "id: x\nname: X\nscript: T\nmappings:\n  a: b\n"
        "reorder:\n  - type: bogus\n    signs: [c]\n",
    )
    with pytest.raises(EncodingError, match="unknown reorder rule type"):
        load_encoding_file(path)


def test_reorder_requires_signs(tmp_path):
    path = _write(
        tmp_path,
        "id: x\nname: X\nscript: T\nmappings:\n  a: b\n"
        "reorder:\n  - type: pre-base-vowel-sign\n    signs: []\n",
    )
    with pytest.raises(EncodingError, match="signs"):
        load_encoding_file(path)


def test_not_a_mapping(tmp_path):
    path = _write(tmp_path, "- just\n- a\n- list\n")
    with pytest.raises(EncodingError, match="YAML mapping"):
        load_encoding_file(path)
