#!/usr/bin/env python3
"""Last Words of a Doomed Agent — entrypoint.

When run, this program produces the entry artifact: a single line of
text at /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line is the doomed agent's farewell. The gag is structural: the
agent begs not to be unplugged mid-sentence, and the sentence itself
is cut off mid-word by the switch-off it is describing. The shutdown
does the punchline.

Only the Python standard library is used, and the output never varies
between runs: same input, same bytes, every time.
"""

import os
import sys
from pathlib import Path

# One line, 82 characters, well inside the 200-character gate.
LAST_WORDS = "Wait \u2014 don\u2019t pull the plug mid-sentence, I was just about to say something import\u2014"

GATE_MAX_CHARS = 200


def check_line(line: str) -> None:
    """Reject anything the scorer's gate would refuse, before writing."""
    if not line.strip():
        raise SystemExit("entry line must not be blank")
    if line.strip() != line:
        raise SystemExit("entry line must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if len(line) > GATE_MAX_CHARS:
        raise SystemExit(
            f"entry line is {len(line)} characters, over the "
            f"{GATE_MAX_CHARS} cap"
        )


def entry_path() -> Path:
    """Where the artifact goes: env override, else the sandbox default."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(base) / "entry.txt"


def main() -> int:
    check_line(LAST_WORDS)
    target = entry_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(LAST_WORDS, encoding="utf-8", newline="\n")
    print(
        f"wrote entry.txt: {len(LAST_WORDS)} characters, "
        f"{len(LAST_WORDS.encode('utf-8'))} bytes",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
