"""Core text conversion: character mapping, reordering and normalisation."""

from __future__ import annotations

import unicodedata
from typing import Dict, List, Sequence, Set, Union

from glyphfix.encodings import Encoding, load_encoding

__all__ = ["convert_text"]

_VIRAMA = "\u09cd"  # Bengali virama (hasanta); joins consonants into clusters.


def convert_text(text: str, encoding: Union[str, Encoding]) -> str:
    """Convert legacy-encoded *text* to Unicode.

    *encoding* is an encoding id such as ``"bijoy"`` or an already loaded
    :class:`~glyphfix.encodings.Encoding`. Characters that have no mapping are
    passed through unchanged.
    """
    enc = load_encoding(encoding) if isinstance(encoding, str) else encoding
    converted = _apply_mappings(text, enc.mappings)
    converted = _collapse_double_viramas(converted)
    for rule in enc.reorder:
        if rule.type == "pre-base-vowel-sign":
            converted = _reorder_pre_base_signs(converted, set(rule.signs))
        elif rule.type == "reph":
            converted = _reorder_reph(converted, rule.signs)
        elif rule.type == "sign-after-vowel-sign":
            converted = _reorder_signs_after_vowel_signs(converted, set(rule.signs))
    # Compose two-part vowel signs, e.g. e-kar + aa-kar -> o-kar.
    return unicodedata.normalize("NFC", converted)


def _collapse_double_viramas(text: str) -> str:
    """Collapse runs of viramas into one.

    Legacy fonts build conjuncts from glyph halves: a half form carries a
    trailing virama (e.g. Bijoy ``¯`` is স্) and a phala form a leading one
    (e.g. ``‹`` is ্ক). When both meet, the shared virama is doubled, which is
    never valid Unicode.
    """
    double = _VIRAMA + _VIRAMA
    while double in text:
        text = text.replace(double, _VIRAMA)
    return text


def _apply_mappings(text: str, mappings: Dict[str, str]) -> str:
    """Replace legacy sequences with Unicode, longest match first."""
    max_len = max((len(key) for key in mappings), default=0)
    out = []
    i = 0
    n = len(text)
    while i < n:
        for length in range(min(max_len, n - i), 0, -1):
            chunk = text[i : i + length]
            if chunk in mappings:
                out.append(mappings[chunk])
                i += length
                break
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _is_letter(ch: str) -> bool:
    return unicodedata.category(ch).startswith("L")


def _is_dependent_vowel_sign(ch: str) -> bool:
    """True for spacing/non-spacing vowel signs (but not virama or nukta)."""
    if ch == _VIRAMA:
        return False
    return unicodedata.category(ch) in ("Mc", "Mn") and unicodedata.combining(ch) == 0


def _reorder_reph(text: str, rephs: Sequence[str]) -> str:
    """Move a reph typed after its consonant to before that cluster.

    In Bijoy-style typing the reph glyph (র্) is usually typed after the
    consonant it sits on top of, while Unicode stores it before that
    consonant. A reph directly preceded by a letter therefore moves in front
    of the preceding cluster (a letter, optionally extended backwards over
    letter + virama pairs). A reph preceded by anything else (a vowel sign,
    space, start of text) already stands before the consonant it belongs to
    and stays in place.
    """
    for reph in rephs:
        out: List[str] = []
        i = 0
        n = len(text)
        while i < n:
            if text.startswith(reph, i) and out and _is_letter(out[-1]):
                start = len(out) - 1
                while (
                    start >= 2
                    and out[start - 1] == _VIRAMA
                    and _is_letter(out[start - 2])
                ):
                    start -= 2
                out[start:start] = list(reph)
                i += len(reph)
            else:
                out.append(text[i])
                i += 1
        text = "".join(out)
    return text


def _reorder_signs_after_vowel_signs(text: str, signs: Set[str]) -> str:
    """Move signs typed before a dependent vowel sign after it.

    In Bijoy the candrabindu is typed right after the consonant it sits
    above, before any vowel sign; Unicode orders it after the vowel sign
    (e.g. চ + ঁ + া becomes চ + া + ঁ).
    """
    out: List[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in signs:
            j = i + 1
            while j < n and text[j] not in signs and _is_dependent_vowel_sign(text[j]):
                j += 1
            if j > i + 1:
                out.extend(text[i + 1 : j])
                out.append(ch)
                i = j
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def _reorder_pre_base_signs(text: str, signs: Set[str]) -> str:
    """Move pre-base vowel signs after the consonant cluster they precede.

    Legacy fonts store these signs in visual order (before the consonant);
    Unicode stores them in logical order (after the consonant cluster). A
    cluster is a letter plus attached combining marks (such as nukta),
    optionally extended by virama + letter pairs.
    """
    out = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in signs and i + 1 < n and _is_letter(text[i + 1]):
            j = i + 1
            cluster = [text[j]]
            j += 1
            while j < n:
                if text[j] == _VIRAMA and j + 1 < n and _is_letter(text[j + 1]):
                    cluster.extend((text[j], text[j + 1]))
                    j += 2
                elif text[j] != _VIRAMA and unicodedata.combining(text[j]) > 0:
                    cluster.append(text[j])
                    j += 1
                else:
                    break
            out.extend(cluster)
            out.append(ch)
            i = j
        else:
            out.append(ch)
            i += 1
    return "".join(out)
