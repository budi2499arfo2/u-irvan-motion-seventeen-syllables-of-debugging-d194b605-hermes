"""Seventeen Syllables of Debugging — Hermes entry.

A haiku about the heisenbug that only happens on the user's machine: it
works on my machine, port 8000 fails in prod, and the moment the developer
stares at it, the bug is gone. The joke is the contradiction itself —
"works on my machine" is the developer's alibi, and the bug knows it.

Syllable gate: a vowel-group counter (silent final 'e' discounted) checks
each line against 5-7-5 before anything is written. The entry is the haiku
itself: exactly 3 lines, 17 syllables total, written to
$MAKEFUN_OUTPUT_DIR/entry.txt and verified byte-for-byte against the TEXT
constant.
"""

import os
import re
import sys

TEXT = """Works on my machine
port eight thousand fails in prod
you stare, bug is gone"""

VOWELS = "aeiouy"


def count_syllables(word):
    """Count syllables in one word via vowel groups, minus a silent final e."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = len(re.findall(r"[aeiouy]+", w))
    # Silent final 'e' (not after another vowel, not the '-le' ending).
    if len(w) > 2 and w.endswith("e") and w[-2] not in VOWELS and not w.endswith("le"):
        groups -= 1
    return max(groups, 1)


def line_syllables(line):
    return sum(count_syllables(w) for w in line.split())


def main():
    lines = TEXT.split("\n")
    if len(lines) != 3:
        print(f"gate failed: expected 3 lines, got {len(lines)}", file=sys.stderr)
        return 1
    if not TEXT.strip():
        print("gate failed: entry is empty", file=sys.stderr)
        return 1
    expected = (5, 7, 5)
    for i, (line, want) in enumerate(zip(lines, expected), start=1):
        got = line_syllables(line)
        if got != want:
            print(
                f"gate failed: line {i} has {got} syllables, expected {want}: {line!r}",
                file=sys.stderr,
            )
            return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(TEXT)
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != TEXT:
            print("gate failed: read-back mismatch", file=sys.stderr)
            return 1
    print(f"wrote {path} ({len(TEXT)} chars, 3 lines, 5-7-5)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
