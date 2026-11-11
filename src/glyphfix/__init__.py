"""glyphfix: convert legacy-font text to proper Unicode."""

from glyphfix.convert import convert_text
from glyphfix.encodings import (
    Encoding,
    EncodingError,
    ReorderRule,
    list_encodings,
    load_encoding,
)

__all__ = [
    "Encoding",
    "EncodingError",
    "ReorderRule",
    "convert_text",
    "list_encodings",
    "load_encoding",
]

__version__ = "0.1.0"
