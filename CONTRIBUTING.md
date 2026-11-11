# Contributing to glyphfix

Thank you for helping make legacy-font text readable again. Contributions of
all kinds are welcome: encoding files, test pairs, bug reports, code and
documentation.

## Ground rules

- **English everywhere**: code, comments, docstrings, documentation, error
  messages and commit messages are written in English. The only exception is
  sample text in the target script, which the converter needs as test data.
- **Permissive dependencies only**: runtime and test dependencies must be
  MIT, Apache-2.0 or BSD licensed. Do not copy code or data tables from
  projects under other licenses, and do not consult GPL-licensed sources at
  all when working on mappings; see [docs/sources.md](docs/sources.md) for
  how references are recorded.
- **Small, focused pull requests**: one topic per pull request. Describe what
  works, how you tested it, and what is still missing.
- **Tests required**: every behavior change comes with tests. Encoding
  changes come with golden test pairs in `tests/encodings/<id>.yaml`.

## Development setup

```bash
git clone https://github.com/mosaddek93/glyphfix.git
cd glyphfix
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Python 3.9 or newer is required. The CI workflow runs `pytest` on every pull
request across the supported Python versions.

## Adding or improving an encoding

This is the most valuable contribution you can make, and it needs no deep
programming knowledge. See [docs/adding-an-encoding.md](docs/adding-an-encoding.md)
for the full guide. In short:

1. Copy an existing file in `encodings/` and fill in your mappings.
2. Add real before/after pairs in `tests/encodings/<id>.yaml`.
3. Run `pytest` until all pairs convert correctly.
4. Open a pull request. Mention which fonts and documents you tested with.

If you can read the script, you can review encoding pull requests; native
speakers are the best reviewers.

## Reporting bugs

Open a GitHub issue with:

- the legacy input text (redact anything private),
- the output you got,
- the output you expected,
- the encoding id and, if relevant, the source font name.

## Code style

- Follow the existing code layout under `src/glyphfix/`.
- Keep functions small and covered by unit tests in `tests/`.
- Comment sparingly, explaining intent rather than restating the code.

## Code of conduct

All contributors are expected to follow the
[Code of Conduct](CODE_OF_CONDUCT.md).
