"""Core text conversion: character mapping, reordering and normalisation."""

from __future__ import annotations

import unicodedata
from typing import Dict, Set, Union

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
    for rule in enc.reorder:
        if rule.type == "pre-base-vowel-sign":
            converted = _reorder_pre_base_signs(converted, set(rule.signs))
    # Compose two-part vowel signs, e.g. e-kar + aa-kar -> o-kar.
    return unicodedata.normalize("NFC", converted)


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
