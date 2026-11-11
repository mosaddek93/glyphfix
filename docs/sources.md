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

Every entry in `encodings/bijoy.yaml` agrees with the MIT-licensed
references. The entries recorded here as missing in earlier revisions
(alternate ``~`` and ``‰`` kar keys, and the contextual glyphs ``¸``, ``ï``,
``û``, ``ü``) are now mapped, each with a golden test. The conjunct glyph
entries added for milestone 2 (``³``, ``Ü``, ``ó``, ``›``, ``¤``, ``¯``,
``‹``, ``ú``, ``^``, ``¥``, and the reph ``©``) were cross-checked entry by
entry against bijoy2unicode and against poriborton's inverse table, and are
validated by golden tests built from real Bengali words. At the time of this
cross-check the bijoy_helper repository was no longer reachable on GitHub, so
the new entries could not be re-verified against it.

One segmentation difference, with identical output: bijoy2unicode maps the
half forms with a trailing virama (``¤`` is ম্) and the phala forms with a
leading one (``ú`` is ্প), while poriborton's inverse table emits pairs such
as ``¤c`` (half form + full consonant) for the same cluster. glyphfix follows
the bijoy2unicode segmentation and collapses the doubled virama that appears
when a half form meets a phala form, so both the ``¤ú`` and ``¤c`` spellings
of ম্প convert to the same Unicode.

Input conventions for the ``&`` and ``|`` keys: in a Bijoy font the bare
``&`` renders as the hasanta and the bare ``|`` as the danda, so glyphfix
maps bare ``&`` to the virama and bare ``|`` to the danda, as poriborton's
inverse table does. The escaped forms ``\&`` and ``\|`` produce a literal
ampersand and pipe in the output. bijoy2unicode uses the opposite convention
(bare ``&`` and ``|`` stay literal, and the escaped forms produce virama +
zero-width non-joiner and the danda); this is a difference in input
conventions, not in character identity.

## How to add entries

When you contribute an encoding, add a section like the one above: list every
reference you used with its name, URL and license, state what you took from
it, and make sure anything copied verbatim comes from an MIT, Apache-2.0 or
BSD licensed source. Do not consult GPL-licensed sources at all. Put Bijoy
and other legacy-text examples in fenced code blocks or double-backtick code
spans, because legacy text can contain Markdown-significant characters such
as the backtick.
