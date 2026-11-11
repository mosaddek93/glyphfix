# glyphfix

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)
[![Tests](https://github.com/mosaddek93/glyphfix/actions/workflows/tests.yml/badge.svg)](https://github.com/mosaddek93/glyphfix/actions/workflows/tests.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Turn broken legacy-font text into proper Unicode. Open, community-driven, and built for the world's scripts.**

Millions of documents in South Asia and beyond (government notices, textbooks, newspapers, court records, archives) were typed with *legacy fonts* such as Bijoy, Kruti Dev or Preeti. These fonts store text as plain Latin characters and rely on a special font to draw the right shapes. Copy such text, or extract it from a PDF, and you get gibberish like `Avwg evsjv ewj` instead of `আমি বাংলা বলি`.

`glyphfix` converts legacy-font text to standard Unicode, so it becomes searchable, copyable, accessible to screen readers, and usable in modern software.

```text
$ echo "Avwg evsjv ewj" | glyphfix text --encoding bijoy
আমি বাংলা বলি
```

## Why this project exists

- Legacy-encoded text is invisible to search engines, translation tools, screen readers and AI systems.
- Existing converters are usually closed web forms for a single script, with no API, no tests and no way to add new fonts.
- Every script community solves this problem separately. `glyphfix` gives them one shared, open engine where **each encoding is a data file anyone can contribute**, with no deep programming knowledge required.

## Features

- **Data-driven encodings**: every legacy encoding lives in a human-readable YAML file under `encodings/`. Adding a new one does not require changing the core code.
- **Vowel-sign reordering**: handles signs typed in visual order (before the consonant) and moves them to logical Unicode order, including across conjunct clusters.
- **CLI and Python library**: use it in a terminal, a script or a data pipeline.
- **Fully offline**: no file is ever uploaded; everything runs locally.
- **Tested against real examples**: each encoding ships with before/after golden test pairs.

Planned (not implemented yet, see the [Roadmap](#roadmap)): PDF text extraction, per-page auto-detection of Unicode/legacy/scanned content, OCR fallback via Tesseract, and full conjunct/reph handling.

## Supported encodings

| Script | Encoding / font family | Status |
|---|---|---|
| Bengali | Bijoy / SutonnyMJ | In progress: base characters and vowel-sign reordering work; conjunct glyphs and reph are pending |
| Devanagari (Hindi) | Kruti Dev | Planned, help wanted |
| Devanagari (Nepali) | Preeti | Planned, help wanted |
| Tamil | Bamini | Planned, help wanted |
| Sinhala | FM Abhaya | Planned, help wanted |

Missing yours? See [Adding a new encoding](#adding-a-new-encoding). It is the most valuable contribution you can make.

## Installation

`glyphfix` is not published on PyPI yet. Install it from source:

```bash
git clone https://github.com/mosaddek93/glyphfix.git
cd glyphfix
pip install .
```

Once the planned OCR support lands, scanned-PDF conversion will additionally require [Tesseract](https://github.com/tesseract-ocr/tesseract) and the language data for your script.

## Quick start

### Command line

```bash
# Convert text
echo "Avwg evsjv ewj" | glyphfix text --encoding bijoy

# Or pass the text as an argument
glyphfix text "Avwg evsjv ewj" --encoding bijoy

# List available encodings
glyphfix encodings list
```

PDF commands (`glyphfix pdf`, `glyphfix detect`) are planned but not implemented yet.

### Python

```python
from glyphfix import convert_text

print(convert_text("Avwg evsjv ewj", encoding="bijoy"))
```

## How it works

```text
legacy text
    |
    v
 apply mapping file      (longest match first, e.g. "Av" -> আ)
    |
    v
 reorder signs           (visual order -> logical order, e.g. ি moves after ক)
    |
    v
 normalise to NFC        (composes two-part vowels, e.g. ে + া -> ো)
    |
    v
 clean Unicode text
```

The planned PDF pipeline (extraction with pdfminer.six, page classification, rendering with pypdfium2 and OCR with Tesseract) is described in the [Roadmap](#roadmap).

## Adding a new encoding

An encoding is one YAML file in `encodings/`. This is an illustrative excerpt:

```yaml
id: bijoy
name: Bijoy (SutonnyMJ and compatible fonts)
script: Bengali
language: bn
fonts: [SutonnyMJ]
status: in-progress

mappings:          # legacy character(s) -> Unicode
  e: "ব"
  g: "ম"
  j: "ল"
  v: "া"
  s: "ং"
  w: "ি"

reorder:           # visual order -> logical order
  - type: pre-base-vowel-sign
    signs: ["ি"]
```

To contribute one:

1. Copy an existing file in `encodings/` as a starting point.
2. Fill in the mappings and rules.
3. Add test pairs (legacy text and the expected Unicode) in `tests/encodings/<id>.yaml`.
4. Run `pytest` and open a pull request.

Native speakers are the best reviewers. If you can read the script, you can verify the results. Full guide: [docs/adding-an-encoding.md](docs/adding-an-encoding.md).

## Project layout

```text
glyphfix/
├── src/glyphfix/        # core library and CLI
├── encodings/           # one mapping file per legacy encoding
├── tests/               # unit tests and per-encoding golden tests
├── docs/                # guides, including how to add an encoding
├── pyproject.toml
├── LICENSE
└── CONTRIBUTING.md
```

## Development

```bash
git clone https://github.com/mosaddek93/glyphfix.git
cd glyphfix
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Roadmap

- [x] Bijoy to Unicode: base characters and vowel-sign reordering
- [ ] Bijoy conjunct glyphs, reph and candrabindu reordering
- [ ] PDF text extraction (pdfminer.six) with `glyphfix pdf` and `glyphfix detect`
- [ ] Auto-detection: classify each page as Unicode, legacy or scanned
- [ ] OCR fallback for scanned pages (pypdfium2 + Tesseract)
- [ ] Publish to PyPI
- [ ] Kruti Dev, Preeti, Bamini, FM Abhaya
- [ ] DOCX support
- [ ] Output as a searchable PDF (invisible Unicode text layer)
- [ ] Browser version that runs entirely on the user's device
- [ ] Documentation in more languages

## Community

- **Questions and ideas**: open a GitHub Discussion.
- **Bug reports**: open an issue and include the legacy input, the output you got and the output you expected. Please remove anything private from sample files before sharing.
- **Translations**: README and docs translations are welcome as `README.<lang>.md`.
- **Conduct**: be respectful and patient. All contributors are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Limitations

- Conversion quality depends on the encoding file. For Bijoy, precomposed conjunct glyphs, reph and candrabindu reordering are not handled yet; please report wrong output.
- Mixed legacy-script and English text cannot be told apart within one string, because legacy encodings reuse the Latin character range.
- PDF handling, auto-detection and OCR are not implemented yet.

## Disclaimer

`glyphfix` does not include or distribute any font files. Font names are trademarks of their respective owners and are used only to identify the encodings the tool can convert.

## Acknowledgements

The planned PDF and OCR features will build on [pdfminer.six](https://github.com/pdfminer/pdfminer.six), [pypdfium2](https://github.com/pypdfium2-team/pypdfium2), [pytesseract](https://github.com/madmaze/pytesseract) and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract). References consulted while writing the encoding data are listed in [docs/sources.md](docs/sources.md).

## License

[MIT](LICENSE)
