# Sources and references

This project does not copy code or data tables from projects unless their
license is MIT, Apache-2.0 or BSD. In addition, GPL-licensed sources must not
be consulted at all when working on mappings, so that no question of
derivation can arise. References are used only to understand an encoding; the
mapping files and the converter are written from scratch and validated by the
golden tests in `tests/encodings/`.

## Bijoy (`encodings/bijoy.yaml`)

The Bijoy mapping was derived by hand from well-known Bengali words and
real-world Bijoy-encoded text, and it is validated word by word by the golden
tests in `tests/encodings/bijoy.yaml`. Examples (note that Bijoy text can
contain the backtick character, which encodes the letter দ):

| Bijoy input | Unicode |
|---|---|
| ``evsjv‡`k`` | বাংলাদেশ |
| ``cÖ_g`` | প্রথম |
| ``ˆZwi`` | তৈরি |

The character identities of the Bijoy keyboard layout are factual properties
of the encoding itself.

### References

No code or data tables were copied from any of these references.

| Reference | URL | License | Use |
|---|---|---|---|
| Bijoy Bangla Typing Nirdeshika (bijoyekushe.net.bd PDF) | http://bijoyekushe.net.bd/img/Bijoy%20Bangla%20Typing%20Nirdeshika.pdf | Proprietary (Ananda Computers) | Real-world sample of Bijoy-encoded text, used to understand how common words are encoded. |
| bijoy2unicode (PyPI) | https://github.com/mad-fox/bijoy2unicode | MIT | Cross-check of the character mapping, entry by entry. |
| poriborton (crates.io) | https://github.com/OpenBangla/poriborton | MIT | Cross-check via its Unicode-to-Bijoy table (inverse direction), including contextual glyph variants. |
| bijoy_helper (pub.dev) | https://github.com/MuhammadFahidSarker/bijoy_helper | MIT | Cross-check of the character mapping, entry by entry. |
| lekhani-core, `converter/bijoy.rs` | https://docs.rs/lekhani-core/latest/src/lekhani_core/converter/bijoy.rs.html | GPL-3.0-or-later | Consulted once as a cross-check before the no-GPL policy above was introduced. No code or data was copied from it, and it must not be consulted again. |
| indianfontconverters.com Bijoy converter | https://indianfontconverters.com/bengali/bijoy-to-unicode/ | Proprietary web tool | Behavior reference for expected conversion output. |
| Unicode Standard, Bengali block (U+0980–U+09FF) | https://www.unicode.org/charts/PDF/U0980.pdf | Unicode License (permissive) | Code points, canonical compositions of two-part vowel signs, logical ordering rules. |

### Cross-check results

Every entry in `encodings/bijoy.yaml` agrees with all three MIT-licensed
references. The cross-check also surfaced entries those references have and
ours does not yet (missing entries, not conflicts):

| Bijoy input | Unicode | Where seen | Status in glyphfix |
|---|---|---|---|
| ``~`` | ূ (alternate uu-kar key) | bijoy2unicode, bijoy_helper, poriborton | Not mapped yet. |
| ``‰`` | ৈ (alternate pre-base oi-kar) | bijoy2unicode, bijoy_helper, poriborton | Not mapped yet. |
| contextual u-kar/uu-kar/ri-kar glyphs (e.g. ``¸``, ``ï``, ``û``, ``ü``) | ু / ূ / ৃ variants after specific consonants | poriborton | Not mapped yet; part of the known precomposed-glyph gap. |

One representational difference: glyphfix maps bare ``&`` to the virama and
``|`` to the danda, as poriborton's inverse table does; bijoy2unicode and
bijoy_helper only map the escaped forms ``\&`` and ``\|``. This is a
difference in input conventions, not in character identity.

## How to add entries

When you contribute an encoding, add a section like the one above: list every
reference you used with its name, URL and license, state what you took from
it, and make sure anything copied verbatim comes from an MIT, Apache-2.0 or
BSD licensed source. Do not consult GPL-licensed sources at all. Put Bijoy
and other legacy-text examples in fenced code blocks or double-backtick code
spans, because legacy text can contain Markdown-significant characters such
as the backtick.
