# Sources and references

This project does not copy code or data tables from projects unless their
license is MIT, Apache-2.0 or BSD. References under other licenses are used
only to understand an encoding; the mapping files and the converter are
written from scratch and validated by the golden tests in `tests/encodings/`.

## Bijoy (`encodings/bijoy.yaml`)

The Bijoy mapping was derived by hand from well-known Bengali words and
real-world Bijoy-encoded text (for example `evsjv‡`k` = বাংলাদেশ, `cÖ_g` =
প্রথম, `ˆZwi` = তৈরি) and is validated word by word by the golden tests in
`tests/encodings/bijoy.yaml`. The character identities of the Bijoy keyboard
layout are factual properties of the encoding itself.

References consulted to understand the encoding (no code or tables copied):

| Reference | URL | License | Use |
|---|---|---|---|
| Bijoy Bangla Typing Nirdeshika (bijoyekushe.net.bd PDF) | http://bijoyekushe.net.bd/img/Bijoy%20Bangla%20Typing%20Nirdeshika.pdf | Proprietary (Ananda Computers) | Real-world sample of Bijoy-encoded text, used to understand how common words are encoded. |
| lekhani-core, `converter/bijoy.rs` | https://docs.rs/lekhani-core/latest/src/lekhani_core/converter/bijoy.rs.html | GPL-3.0-or-later | Cross-check of independently derived character identities only. Not copied: GPL is not a permissive license. |
| indianfontconverters.com Bijoy converter | https://indianfontconverters.com/bengali/bijoy-to-unicode/ | Proprietary web tool | Behavior reference for expected conversion output. |
| Unicode Standard, Bengali block (U+0980–U+09FF) | https://www.unicode.org/charts/PDF/U0980.pdf | Unicode License (permissive) | Code points, canonical compositions of two-part vowel signs, logical ordering rules. |

## How to add entries

When you contribute an encoding, add a section like the one above: list every
reference you used with its name, URL and license, state what you took from
it, and make sure anything copied verbatim comes from an MIT, Apache-2.0 or
BSD licensed source.
