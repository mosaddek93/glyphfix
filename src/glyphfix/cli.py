"""Command-line interface for glyphfix."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from glyphfix.convert import convert_text
from glyphfix.encodings import EncodingError, list_encodings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="glyphfix",
        description="Convert legacy-font text to proper Unicode.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    text_parser = subparsers.add_parser(
        "text",
        help="Convert legacy-encoded text to Unicode.",
        description=(
            "Convert legacy-encoded text to Unicode. Reads from standard "
            "input when no text argument is given."
        ),
    )
    text_parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text to convert. Omit to read from standard input.",
    )
    text_parser.add_argument(
        "--encoding",
        "-e",
        required=True,
        help="Id of the legacy encoding, for example 'bijoy'.",
    )

    encodings_parser = subparsers.add_parser(
        "encodings",
        help="Inspect available encodings.",
    )
    encodings_sub = encodings_parser.add_subparsers(
        dest="encodings_command", required=True
    )
    encodings_sub.add_parser("list", help="List available encodings.")

    return parser


def _cmd_text(args: argparse.Namespace) -> int:
    data = args.text if args.text is not None else sys.stdin.read()
    result = convert_text(data, args.encoding)
    sys.stdout.write(result if result.endswith("\n") else result + "\n")
    return 0


def _cmd_encodings_list() -> int:
    encodings = list_encodings()
    if not encodings:
        print("No encodings found.")
        return 0
    rows = [
        (enc.id, enc.script, enc.status or "-", enc.name) for enc in encodings
    ]
    headers = ("ID", "SCRIPT", "STATUS", "NAME")
    widths = [
        max(len(headers[col]), max(len(row[col]) for row in rows))
        for col in range(len(headers))
    ]
    for row in (headers, *rows):
        print("  ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip())
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "text":
            return _cmd_text(args)
        if args.command == "encodings" and args.encodings_command == "list":
            return _cmd_encodings_list()
    except EncodingError as exc:
        print(f"glyphfix: {exc}", file=sys.stderr)
        return 2
    parser.error("unknown command")
    return 2  # unreachable; parser.error exits


if __name__ == "__main__":
    sys.exit(main())
