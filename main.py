#!/usr/bin/env python3
"""One Word for the Boss -- Make.fun entry.

Writes exactly one word describing the boss to /output/entry.txt.
The word is the whole entry: no phrase, no caption, no explanation.
"""

import os
import sys

# The chosen word: the boss who presents your idea in the meeting
# as if it were always his own. Nine letters, one word, no caption
# needed -- every employee recognises him instantly.
WORD = "Ideathief"

OUTPUT_PATH = "/output/entry.txt"


def validate_word(word):
    """Check the entry word against the competition gate.

    The gate requires UTF-8 text of 1 to 30 characters, not only
    whitespace, and the brief requires exactly one word: no spaces,
    no sentence, no explanation. Letters only, so nothing else can
    sneak in (no hyphen, no punctuation, no digits).
    """
    if not isinstance(word, str):
        raise TypeError("word must be a string")
    if not word:
        raise ValueError("word must not be empty")
    if len(word) > 30:
        raise ValueError(f"word is {len(word)} chars, over the 30-char limit")
    if word != word.strip():
        raise ValueError("word must not have leading or trailing whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be exactly one word (no spaces)")
    if not word.isalpha():
        raise ValueError("word must contain letters only")
    return True


def word_count(text):
    """Count the words in a text: split on whitespace, drop empties."""
    return len(text.split())


def verify_output(path, expected):
    """Read the file back and confirm it is byte-identical to the word.

    The entry is judged exactly as submitted, so what lands on disk
    must be the word and nothing else -- one word, no trailing
    newline, no extra whitespace.
    """
    with open(path, "r", encoding="utf-8") as f:
        actual = f.read()
    if actual != expected:
        raise ValueError(
            f"read-back mismatch: file holds {actual!r}, expected {expected!r}"
        )
    if word_count(actual) != 1:
        raise ValueError(f"file must hold exactly 1 word, found {word_count(actual)}")
    if not 1 <= len(actual) <= 30:
        raise ValueError(f"file length {len(actual)} outside 1-30 chars")
    return True


def main():
    validate_word(WORD)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(WORD)
    verify_output(OUTPUT_PATH, WORD)
    print(f"Wrote {WORD!r} to {OUTPUT_PATH} (verified: 1 word, {len(WORD)} chars)")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
