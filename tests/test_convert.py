"""Unit tests for the conversion pipeline."""

import pytest

from glyphfix import convert_text, load_encoding
from glyphfix.convert import (
    _apply_mappings,
    _reorder_pre_base_signs,
    _reorder_reph,
    _reorder_signs_after_vowel_signs,
)


def test_longest_match_wins():
    # "Av" is the independent vowel; it must not map as "A" + "v".
    assert convert_text("Av", "bijoy") == "আ"
    assert convert_text("A", "bijoy") == "অ"


def test_unmapped_characters_pass_through():
    assert convert_text("wK?", "bijoy") == "কি?"
    assert convert_text("( )", "bijoy") == "( )"


def test_accepts_encoding_instance():
    encoding = load_encoding("bijoy")
    assert convert_text("e", encoding) == "ব"


def test_two_part_vowel_composes_to_single_codepoint():
    result = convert_text("†fvU", "bijoy")
    assert "\u09cb" in result  # o-kar, not e-kar + aa-kar


def test_apply_mappings_longest_first():
    mappings = {"a": "1", "ab": "2"}
    assert _apply_mappings("ab a b", mappings) == "2 1 b"


def test_reorder_moves_sign_after_single_consonant():
    assert _reorder_pre_base_signs("\u09bf\u0995", {"\u09bf"}) == "\u0995\u09bf"


def test_reorder_moves_sign_after_virama_cluster():
    # e-kar before pa + virama + ra must land after the whole cluster.
    text = "\u09c7\u09aa\u09cd\u09b0\u09ae"
    expected = "\u09aa\u09cd\u09b0\u09c7\u09ae"
    assert _reorder_pre_base_signs(text, {"\u09c7"}) == expected


def test_reorder_moves_sign_after_nukta():
    # i-kar before dda + nukta (decomposed rra) must land after the nukta.
    text = "\u09bf\u09a1\u09bc"
    expected = "\u09a1\u09bc\u09bf"
    assert _reorder_pre_base_signs(text, {"\u09bf"}) == expected


def test_reorder_sign_without_following_base_stays_in_place():
    assert _reorder_pre_base_signs("\u09bf", {"\u09bf"}) == "\u09bf"
    assert _reorder_pre_base_signs("\u09bf ", {"\u09bf"}) == "\u09bf "


_REPH = "\u09b0\u09cd"  # ra + virama


def test_reph_after_consonant_moves_before_it():
    # ka + ma + reph -> ka + reph + ma
    assert _reorder_reph("\u0995\u09ae" + _REPH, [_REPH]) == "\u0995" + _REPH + "\u09ae"


def test_reph_after_consonant_moves_before_whole_cluster():
    # ta + virama + ma + reph -> reph + ta + virama + ma
    cluster = "\u09a4\u09cd\u09ae"
    assert _reorder_reph(cluster + _REPH, [_REPH]) == _REPH + cluster


def test_reph_after_vowel_sign_stays_in_place():
    # ma + aa-kar + reph + ca is already in logical order.
    text = "\u09ae\u09be" + _REPH + "\u099a"
    assert _reorder_reph(text, [_REPH]) == text


def test_candrabindu_moves_after_vowel_sign():
    # ca + candrabindu + aa-kar + da -> ca + aa-kar + candrabindu + da
    text = "\u099a\u0981\u09be\u09a6"
    expected = "\u099a\u09be\u0981\u09a6"
    assert _reorder_signs_after_vowel_signs(text, {"\u0981"}) == expected


def test_candrabindu_already_after_vowel_sign_stays():
    text = "\u099a\u09be\u0981\u09a6"
    assert _reorder_signs_after_vowel_signs(text, {"\u0981"}) == text


def test_half_form_plus_phala_shares_one_virama():
    # Bijoy half form "¯" (sa + virama) + phala "‹" (virama + ka): the doubled
    # virama must collapse so the result is a valid conjunct.
    assert convert_text("\u00af\u2039", "bijoy") == "\u09b8\u09cd\u0995"


def test_unknown_encoding_raises():
    with pytest.raises(Exception, match="unknown encoding"):
        convert_text("abc", "does-not-exist")
