# Adding a new encoding

Every legacy encoding that glyphfix can convert is a single YAML file in the
top-level `encodings/` directory. You do not need to touch any Python code to
add one. This guide walks through the file format and the testing workflow.

## 1. Create the encoding file

Copy an existing file, for example `encodings/bijoy.yaml`, to
`encodings/<id>.yaml`. The `<id>` is a short lowercase name such as
`krutidev` or `preeti`; it is what users pass to `--encoding`.

### Top-level fields

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Short lowercase identifier. Must match the file name. |
| `name` | yes | Human-readable name, shown by `glyphfix encodings list`. |
| `script` | yes | Script the encoding targets, for example `Bengali`. |
| `language` | no | BCP 47 language code, for example `bn`. |
| `fonts` | no | List of font names that use this encoding. |
| `status` | no | Free-form progress note, for example `in-progress`. |
| `mappings` | yes | Legacy character(s) to Unicode, see below. |
| `reorder` | no | Reordering rules, see below. |

### Mappings

`mappings` is a dictionary from legacy characters to Unicode text:

```yaml
mappings:
  "K": "ক"
  "Av": "আ"
  "¨": "্য"
```

Rules of thumb:

- **Keys can be more than one character.** The converter always applies the
  longest matching key first, so `"Av"` wins over `"A"` followed by `"v"`.
- **Values can be more than one code point**, for example a consonant plus a
  virama for a conjunct part (`"¨": "্য"`).
- **Quote both keys and values.** Characters such as `` ` ``, `&`, `|`, `~`
  and digits have special meaning in YAML when unquoted.
- Characters without a mapping pass through unchanged, so you do not need to
  map spaces or common punctuation unless the encoding redefines them
  (for example `"|": "।"` in Bijoy).

### Reorder rules

Legacy fonts store some signs in *visual* order while Unicode requires
*logical* order. Declare these signs and the converter moves them for you:

```yaml
reorder:
  - type: pre-base-vowel-sign
    signs: ["ি", "ে", "ৈ"]
```

`pre-base-vowel-sign` is currently the only rule type. It handles signs that
are typed **before** the consonant they attach to: after mapping, each listed
sign is moved after the following consonant cluster (a letter optionally
extended by virama + letter pairs). For example `ি` + `ক` becomes `ক` + `ি`,
and `ে` + `প্র` becomes `প্র` + `ে`.

After reordering, the output is normalised to NFC. This composes two-part
vowel signs automatically: you can map the right half of a two-part vowel
(for example Bijoy `"Š": "ৗ"`) and `ে` + `ৗ` will compose to `ৌ`.

If your encoding needs a rule type that does not exist yet (for example reph
handling), open an issue describing the behavior with examples.

## 2. Add golden test pairs

Create `tests/encodings/<id>.yaml`:

```yaml
encoding: <id>

cases:
  - name: simple-sentence
    legacy: "Avwg evsjv ewj"
    unicode: "আমি বাংলা বলি"
```

Guidelines:

- Use **real text** from real documents (redact anything private), not just
  isolated characters. Short common words and sentences are ideal.
- Cover every tricky behavior: pre-base vowel signs, two-part vowels,
  conjunct parts, digits and punctuation.
- Add at least one case per mapping section, so wrong entries cannot hide.
- Give each case a short descriptive `name`; it appears in the pytest output.

## 3. Run the tests

```bash
pip install -e ".[dev]"
pytest
```

Every case in your file runs automatically; a failure prints the expected and
actual Unicode so you can spot the wrong mapping.

You can also try it interactively:

```bash
echo "Avwg evsjv ewj" | glyphfix text --encoding <id>
```

## 4. Open a pull request

- Keep the pull request focused on one encoding.
- In the description, note which fonts and sample documents you tested with,
  and which characters or conjuncts are still missing.
- Do not copy mapping tables from other converters unless their license is
  MIT, Apache-2.0 or BSD. Derive the mapping from the keyboard layout, font
  documentation or real documents, and record what you consulted in
  [docs/sources.md](sources.md).

Native speakers are the best reviewers. If you can read the script, please
review encoding pull requests even if you do not write code.
