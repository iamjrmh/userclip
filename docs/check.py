"""Enforce userclip hard rule 1: no em dashes anywhere in the repository.

Scans every text file that is not excluded and fails with a non-zero exit code if
a forbidden character is found, printing every offending location.

The forbidden characters are referenced only by escape sequence so that this
checker never reports itself as a violation.

Usage:
    python scripts/check_no_em_dash.py [root]
"""

from __future__ import annotations

import sys
from pathlib import Path

# Built with chr() so that this file never contains the characters it forbids
# and therefore never reports itself as a violation.
FORBIDDEN = {
    chr(0x2014): "U+2014 EM DASH",
    chr(0x2015): "U+2015 HORIZONTAL BAR",
}

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "target",
    "dist",
    "build",
    "__pycache__",
    "gen",
    "models",
    "visual-qa",
    ".idea",
    ".vscode",
}

# Binary and asset extensions are skipped outright rather than decoded.
EXCLUDED_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".icns", ".bmp",
    ".mp4", ".mkv", ".mov", ".webm", ".mp3", ".wav", ".flac", ".ogg",
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
    ".onnx", ".gguf", ".bin", ".safetensors", ".pt", ".pth",
    ".zip", ".gz", ".tar", ".7z", ".xz",
    ".exe", ".dll", ".so", ".dylib", ".pdb", ".lib", ".msi",
    ".db", ".sqlite", ".sqlite3",
    ".pdf",
}

# prompt.md is the original product brief written by the author and is kept
# verbatim as the source of truth, so it is not subject to the output rule.
EXCLUDED_FILES = {"prompt.md"}


def is_excluded(path: Path, root: Path) -> bool:
    if path.name in EXCLUDED_FILES:
        return True
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return True
    return any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts)


def scan_file(path: Path) -> list[tuple[int, int, str, str]]:
    """Return (line_no, column, description, line_text) for each violation."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    if not any(char in text for char in FORBIDDEN):
        return []

    violations = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for char, description in FORBIDDEN.items():
            column = line.find(char)
            while column != -1:
                violations.append((line_no, column + 1, description, line.strip()))
                column = line.find(char, column + 1)
    return violations


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent.parent

    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    total = 0
    scanned = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or is_excluded(path, root):
            continue
        scanned += 1
        for line_no, column, description, line_text in scan_file(path):
            total += 1
            relative = path.relative_to(root)
            print(f"{relative}:{line_no}:{column}: {description}")
            safe = line_text.encode("ascii", "backslashreplace").decode("ascii")
            print(f"    {safe}")

    if total:
        print(f"\nFAIL: {total} forbidden dash character(s) found in {scanned} scanned files.")
        print("Hard rule 1: use commas, colons, parentheses, or hyphens instead.")
        return 1

    print(f"OK: no forbidden dash characters in {scanned} scanned files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
