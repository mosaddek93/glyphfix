"""Tests for the command-line interface."""

import io

from glyphfix.cli import main


def test_text_argument(capsys):
    assert main(["text", "Avwg evsjv ewj", "--encoding", "bijoy"]) == 0
    assert capsys.readouterr().out == "আমি বাংলা বলি\n"


def test_text_short_flag(capsys):
    assert main(["text", "†`k", "-e", "bijoy"]) == 0
    assert capsys.readouterr().out == "দেশ\n"


def test_text_reads_stdin(capsys, monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("evsjv‡`k\n"))
    assert main(["text", "--encoding", "bijoy"]) == 0
    assert capsys.readouterr().out == "বাংলাদেশ\n"


def test_unknown_encoding_fails_cleanly(capsys):
    assert main(["text", "abc", "--encoding", "does-not-exist"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "unknown encoding" in captured.err


def test_encodings_list(capsys):
    assert main(["encodings", "list"]) == 0
    out = capsys.readouterr().out
    assert "bijoy" in out
    assert "Bengali" in out
    assert "in-progress" in out
